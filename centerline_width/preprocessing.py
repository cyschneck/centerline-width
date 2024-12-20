#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      preprocessing.py calculates and processes river data input data                            #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - _left_right_coordinates: input left and right           #
#                                              coordinates from the input values                  #
#                                                                                                 #
#                                       - _generate_polygon: generate river polygon               #
#                                              based on input values                              #
#                                              distance                                           #
#                                                                                                 #
#                                       - _generate_voronoi: generate Voronoi diagram             #
#                                              based on the left/right bank points                #
#                                                                                                 #
#                                       - _interpolate_between_points: interpolates               #
#                                              additional points at an even distance              #
#                                              along river banks                                  #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
from collections import Counter
import csv
import logging
import math
import os

# Related Third Party Imports
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from scipy.spatial import Voronoi

# Internal Local Imports
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def _left_right_coordinates(dataframe=None):
    # returns the left and right coordinates from the input values
    right_bank_coordinates = []
    left_bank_coordinates = []

    for index, row in dataframe.iterrows():
        # iterate through input dataframe and save non-nan values
        if not math.isnan(row.rlat) and not math.isnan(row.rlon):
            right_bank_coordinates.append([row.rlon, row.rlat])
        if not math.isnan(row.llat) and not math.isnan(row.llon):
            left_bank_coordinates.append([row.llon, row.llat])

    return left_bank_coordinates, right_bank_coordinates


def _generate_polygon(
        left_bank_lst: list = None,
        right_bank_lst: list = None,
        coord_type: str = None,
        recursion_check: bool = False) -> [Polygon, LineString, LineString]:
    # Return a shapely polygon based on the position of the river bank points
    if len(right_bank_lst) == 0:
        raise ValueError("CRITICAL ERROR, right bank data is empty (or NaN)")
    if len(left_bank_lst) == 0:
        raise ValueError("\nCRITICAL ERROR, left bank data is empty (or NaN)")
    circular_list_of_banks = left_bank_lst + right_bank_lst[::-1] + [
        left_bank_lst[0]
    ]

    river_polygon = Polygon(circular_list_of_banks)
    top_river = LineString([
        Point(left_bank_lst[::-1][0][0], left_bank_lst[::-1][0][1]),
        Point(right_bank_lst[::-1][0][0], right_bank_lst[::-1][0][1])
    ])
    bottom_river = LineString([
        Point(right_bank_lst[0][0], right_bank_lst[0][1]),
        Point(left_bank_lst[0][0], left_bank_lst[0][1])
    ])

    if not river_polygon.is_valid and not recursion_check:
        logger.critical(
            f"[FAILED]  Invalid Polygon may need to be corrected - {coord_type}"
        )
        # only run once with recursion_check set (just to check if reverse banks fixes issue)
        polygon_check, _, _ = _generate_polygon(
            left_bank_lst=left_bank_lst,
            right_bank_lst=right_bank_lst[::-1],
            coord_type=coord_type,
            recursion_check=True)
        if polygon_check.is_valid:
            logger.critical(
                "\nWARNING: Invalid Polygon Due to Flipped Banks, fix recommendation: rerun convertColumnsToCSV() and set flip_direction=True (or reset to default 'False' if currently set to flip_direction=True)\n"
            )
    if river_polygon.is_valid and not recursion_check:
        logger.info(f"[SUCCESS] Valid polygon generated - {coord_type}")

    return river_polygon, top_river, bottom_river


def _generate_voronoi(left_bank_lst: list = None,
                      right_bank_lst: list = None,
                      coord_type: str = None) -> Voronoi:
    # Generate a Voronoi diagram based on the left/right bank points
    all_banks_points = left_bank_lst + right_bank_lst
    all_banks_points = np.array(all_banks_points)

    river_voronoi = Voronoi(all_banks_points)
    logger.info(f"[SUCCESS] Voronoi diagram generated - {coord_type}")
    return river_voronoi


def _points_from_voronoi(river_voronoi: Voronoi = None,
                         river_polygon: Polygon = None) -> dict:
    # Returns a dictionary list of all the voronoi points: {start point : [list of end points]}
    points_dict = {}
    all_connections_start_to_end = []
    logger.info(
        "[PROCESSING] Attempting to determine a valid centerline from Voronoi points, may take a few minutes..."
    )  # longest step, O(n^n)
    for ridge_vertex_point in river_voronoi.ridge_vertices:
        if ridge_vertex_point[0] >= 0 and ridge_vertex_point[
                1] >= 0:  # Only include non-infinity vertex edges
            v0 = river_voronoi.vertices[ridge_vertex_point[0]]
            v1 = river_voronoi.vertices[ridge_vertex_point[1]]
            # Check if start and end points are within the polygon, otherwise remove the connection pair
            if river_polygon.contains(Point([v0[0], v0[1]
                                             ])) and river_polygon.contains(
                                                 Point([v1[0], v1[1]])):
                start_point = tuple([v0[0], v0[1]])
                end_point = tuple([v1[0], v1[1]])
                start_to_end = [start_point, end_point]
                if start_to_end not in all_connections_start_to_end:
                    all_connections_start_to_end.append(start_to_end)

    # Dictionary with connections that have at least one connection
    connections_counter_start_to_end = Counter(
        x for xs in all_connections_start_to_end
        for x in set(xs))  # counter the amount of connections for each point
    for connection in all_connections_start_to_end:
        start_point = connection[0]
        end_point = connection[1]
        # Only plot points with at least two connections (removes any edges that are not connected to additional points)
        if connections_counter_start_to_end[start_point] > 1:
            if connections_counter_start_to_end[end_point] > 1:
                if start_point not in points_dict.keys():
                    points_dict[start_point] = []
                points_dict[start_point].append(end_point)

    return points_dict


def _interpolate_between_points(left_bank_coordinates: list = None,
                                right_bank_coordinates: list = None,
                                interpolate_n: int = 5) -> [list, list]:
    # Interpolated between points at an even distance along the river banks to attempt to even out Voronoi diagrams
    interpolate_n += 2  # adds two exta points, to ensure that interpolating is adding the points between the existing points

    def interpolateList(lst):
        # Add points to existing list to increase resolution
        #haversine_distance_between = haversine((lat1, lon1), (lat2, lon2), unit=units)
        bank_expanded = []
        for i in range(len(lst)):
            if i + 1 < len(lst):
                lon1, lat1 = lst[i][0], lst[i][1]
                lon2, lat2 = lst[i + 1][0], lst[i + 1][1]

                x_expand = np.linspace(lon1, lon2, interpolate_n)
                y_expand = np.linspace(lat1, lat2, interpolate_n)

                for j in range(len(x_expand)):
                    bank_expanded.append([x_expand[j], y_expand[j]])
                bank_expanded.append(
                    lst[i + 1]
                )  # add end position (np.linspace excludes ending position)
            else:
                bank_expanded.append(lst[i])
        return bank_expanded

    right_interpolated_coordinates = interpolateList(right_bank_coordinates)
    left_interpolated_coordinates = interpolateList(left_bank_coordinates)

    return right_interpolated_coordinates, left_interpolated_coordinates
