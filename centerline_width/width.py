#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      width.py is responsible for determining the width between banks based on latitude and      #
#      and longitude. Width is calculated from the coordinates of the centerline to where         #
#      the width line intersects the banks                                                        #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - riverWidthFromCenterlineCoordinates: backend for        #
#                                              plotCenterlineWidth, returns the coordinates       #
#                                              for the width intersection points                  #
#                                                                                                 #
#                                       - width: returns width dictionary and width at            #
#                                                centerline where {[centerline latitude,          #
#                                                centerline longitude] : widthValue }             #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Built-in Python functions
import logging
import csv
import math

# External Python libraries
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import split
import geopy.distance
from pyproj import Geod

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def riverWidthFromCenterlineCoordinates(
        river_object: centerline_width.CenterlineWidth = None,
        centerline_coordinates: list = None,
        transect_span_distance: int = 3,
        transect_slope: str = "Average",
        remove_intersections: bool = False,
        coordinate_unit: str = "Decimal Degrees",
        save_to_csv: str = None) -> [dict, dict, dict]:
    # Return the left/right coordinates of width centerlines
    # Returns three dictionaries: right_width_coordinates, left_width_coordinates, num_intersection_coordinates
    # Used in the backend to plot coordinates in plot_centerline_width()

    # Group the centerline coordinates into groups of length n
    centerline_slope = {}
    # group points inclusive of previous point: [A, B, C, D] = [A, B], [B, C], [C, D]
    groups_of_n_points = []
    for i in range(0, len(centerline_coordinates), transect_span_distance):
        if i == 0:
            groups_of_n_points.append(
                centerline_coordinates[0:transect_span_distance])
        else:
            groups_of_n_points.append(
                centerline_coordinates[i - 1:i + transect_span_distance])

    geodesic = Geod(ellps=river_object.ellipsoid)

    # Average all slopes for every n points to chart (slope of A->B + B->C)
    if transect_slope == "Average":
        for group_points in groups_of_n_points:
            slope_sum = 0
            total_slopes = 0
            for i in range(len(group_points)):
                if i + 1 < len(group_points):
                    lon_start = group_points[i][0]
                    lat_start = group_points[i][1]
                    lon_end = group_points[i + 1][0]
                    lat_end = group_points[i + 1][1]
                    forward_bearing, reverse_bearing, distance_between_meters = geodesic.inv(
                        lon_start, lat_start, lon_end, lat_end)
                    x_diff = math.sin(
                        np.deg2rad(forward_bearing)) * distance_between_meters
                    y_diff = math.cos(
                        np.deg2rad(forward_bearing)) * distance_between_meters
                    dy = group_points[i + 1][1] - group_points[i][1]
                    dx = group_points[i + 1][0] - group_points[i][0]
                    if dx != 0:
                        slope_sum += (y_diff / x_diff)
                        total_slopes += 1
                        #print(f"angle is 90 = {math.floor(np.rad2deg(math.atan((1/(y_diff / x_diff) - (y_diff / x_diff)) / (1.00000001 + y_diff / x_diff * -1/(y_diff / x_diff)))))}")
            if slope_sum != 0:
                slope_avg = slope_sum / total_slopes
                normal_of_slope = -1 / slope_avg
                #print(f"angle is 90 = {math.ceil(np.rad2deg(math.atan((slope_avg - normal_of_slope) / (1.00000001 + (slope_avg * normal_of_slope)))))}")
                middle_of_list = (
                    len(group_points) + 1
                ) // 2  # set centerline point to be the middle point being averaged
                centerline_slope[
                    group_points[middle_of_list]] = normal_of_slope

    # Direct slope across n points (slope of A->C)
    if transect_slope == "Direct":
        for group_points in groups_of_n_points:
            if len(group_points) > 1:
                lon_start = group_points[0][0]
                lat_start = group_points[0][1]
                lon_end = group_points[-1][0]
                lat_end = group_points[-1][1]
                forward_bearing, reverse_bearing, distance_between_meters = geodesic.inv(
                    lon_start, lat_start, lon_end, lat_end)
                x_diff = math.sin(
                    np.deg2rad(forward_bearing)) * distance_between_meters
                y_diff = math.cos(
                    np.deg2rad(forward_bearing)) * distance_between_meters
                slope = 0
                if x_diff != 0:
                    slope = (y_diff / x_diff)
                if slope != 0:
                    normal_of_slope = -1 / slope
                    #print(f"angle = {math.ceil(np.rad2deg(math.atan((slope - normal_of_slope) / (1.00000001 + (slope * normal_of_slope)))))}")
                    middle_of_list = (
                        len(group_points) + 1
                    ) // 2  # set centerline point to be the middle point being averaged
                    centerline_slope[group_points[0]] = normal_of_slope

    def intersectsTopOrBottomOfBank(point1, point2):
        # returns True/False if the points lie on the 'false' top/bottom of the river
        points_intersect_false_edges = False

        # avoiding floating point precession errors when determining if point lies within the line
        # if point is within a small distance of a line it is considered to intersect
        if river_object.top_bank.distance(
                point1) < 1e-8 or river_object.bottom_bank.distance(
                    point1) < 1e-8:
            points_intersect_false_edges = True
        if river_object.top_bank.distance(
                point2) < 1e-8 or river_object.bottom_bank.distance(
                    point2) < 1e-8:
            points_intersect_false_edges = True
        return points_intersect_false_edges

    # Generate a list of lines from the centerline point with its normal
    logger.info(
        "[PROCESSING] Calculating and positioning width lines, may take a few minutes..."
    )

    right_width_coordinates = {}
    left_width_coordinates = {}
    num_intersection_coordinates = {}

    min_x, min_y, max_x, max_y = river_object.bank_polygon.bounds
    for centerline_point, slope in centerline_slope.items():
        # draw a max line that extends the entire distance of the available space, will be trimmed below to just within polygon
        left_y = slope * (min_x - centerline_point[0]) + centerline_point[1]
        right_y = slope * (max_x - centerline_point[0]) + centerline_point[1]

        # Save the points where they intersect the polygon
        sloped_line = LineString([(min_x, left_y), (max_x, right_y)
                                  ])  # sloped line from the centerpoint
        line_intersection_points = river_object.bank_polygon.exterior.intersection(
            sloped_line)  # points where the line intersects the polygon

        # if the line only intersects in two places (does not intersect polygon any additional times)
        if str(
                line_intersection_points
        ) != "LINESTRING Z EMPTY":  # if linestring has intersect (not empty)
            if len(line_intersection_points.geoms) == 2:
                # only save width lines that do not touch the artificial top/bottom
                if not intersectsTopOrBottomOfBank(
                        line_intersection_points.geoms[0],
                        line_intersection_points.geoms[1]):
                    left_width_coordinates[centerline_point] = (
                        line_intersection_points.geoms[0].x,
                        line_intersection_points.geoms[0].y)
                    right_width_coordinates[centerline_point] = (
                        line_intersection_points.geoms[1].x,
                        line_intersection_points.geoms[1].y)
            else:
                # line intersects to polygon at multiple points
                if river_object.bank_polygon.contains(
                        Point(centerline_point)
                ):  # width line made by centering centerline point, skip this width line if the centerline is outside of the polygon due to smoothing
                    all_linestring = split(
                        sloped_line, river_object.bank_polygon
                    )  # split linestring where it intersects the polygon
                    left_point = None
                    right_point = None
                    for i, possible_linestring in enumerate(
                            all_linestring.geoms
                    ):  # iterate through all linestrings
                        if possible_linestring.distance(
                                Point(centerline_point)
                        ) < 1e-8:  # select linestring that contains the centerline point
                            left_point = Point(possible_linestring.coords[0])
                            right_point = Point(possible_linestring.coords[1])

                    # linestring contains the centerline, save coordinates
                    if left_point is not None and right_point is not None:
                        # only save width lines that do not touch the artificial top/bottom
                        if not intersectsTopOrBottomOfBank(
                                left_point, right_point):
                            left_width_coordinates[centerline_point] = (
                                left_point.x, left_point.y)
                            right_width_coordinates[centerline_point] = (
                                right_point.x, right_point.y)

    # Determine lines that intersect with other lines in multiple places to flag/remove
    all_linestrings = []
    linestring_with_centerlines = {
    }  # linestring with associated centerline: {linestring : centerline coordinate}
    linestring_with_linestrings_that_intersect = {
    }  # dictionary of all the linestrings that a linestring intersects with
    # Generate a list of linestrings
    for centerline_coord in right_width_coordinates.keys():
        linestring_generated = LineString([
            Point(left_width_coordinates[centerline_coord][0],
                  left_width_coordinates[centerline_coord][1]),
            Point(right_width_coordinates[centerline_coord][0],
                  right_width_coordinates[centerline_coord][1])
        ])
        linestring_with_centerlines[linestring_generated] = centerline_coord
        all_linestrings.append(linestring_generated)
    # count the number of intersections for each linestring, +1 for each time one line string intersects another
    for linestring_to_check in all_linestrings:
        num_intersection_coordinates[linestring_with_centerlines[
            linestring_to_check]] = 0  # default set all intersects to zero
        for linestring_to_check_against in all_linestrings:
            if linestring_to_check != linestring_to_check_against:
                if linestring_to_check.intersects(
                        linestring_to_check_against
                ):  # check if two lines intersect
                    intersection_points_linestrings = linestring_to_check.intersection(
                        linestring_to_check_against
                    )  # return point positions where intersection occurs
                    if str(
                            intersection_points_linestrings
                    ) != "LINESTRING Z EMPTY":  # if linestring has intersect (not empty), increment count
                        num_intersection_coordinates[
                            linestring_with_centerlines[
                                linestring_to_check]] += 1
                        if linestring_to_check not in linestring_with_linestrings_that_intersect.keys(
                        ):
                            linestring_with_linestrings_that_intersect[
                                linestring_to_check] = []
                        linestring_with_linestrings_that_intersect[
                            linestring_to_check].append(
                                linestring_to_check_against)

    # Remove Intersection Lines
    centerline_coordinates_to_be_removed = []
    if remove_intersections:
        logger.info("[PROCESSING] Recursively removing intersection lines...")
        # iterate from the most intersections to the least intersections
        for linestring_most_interactions in sorted(
                linestring_with_linestrings_that_intersect,
                key=lambda k: len(linestring_with_linestrings_that_intersect[k]
                                  ),
                reverse=True):

            # when number of intersections > 1, remove lines with the most interactions to the smallest
            if num_intersection_coordinates[linestring_with_centerlines[
                    linestring_most_interactions]] > 1:
                lst_linestrings_hit_by_linestring = linestring_with_linestrings_that_intersect[
                    linestring_most_interactions]

                # iterate through each and remove linestring from the associated lists of places it intersects
                for linestring_hit in lst_linestrings_hit_by_linestring:
                    # remove linestring with most intersections from all linestrings that it hits
                    linestring_with_linestrings_that_intersect[
                        linestring_hit].remove(linestring_most_interactions)
                    # decrease intersections by 1 after removing linestring, from both the linestring and the places it intersects
                    num_intersection_coordinates[linestring_with_centerlines[
                        linestring_most_interactions]] -= 1
                    num_intersection_coordinates[
                        linestring_with_centerlines[linestring_hit]] -= 1

                # remove linestring that intersects the most linestrings
                centerline_of_removed_line = linestring_with_centerlines[
                    linestring_most_interactions]
                if centerline_of_removed_line not in centerline_coordinates_to_be_removed:
                    centerline_coordinates_to_be_removed.append(
                        centerline_of_removed_line)

            # if two linestring both have one intersection (with just each other), remove the longer width line
            if num_intersection_coordinates[linestring_with_centerlines[
                    linestring_most_interactions]] == 1:
                linestring_1 = linestring_most_interactions
                linestring_2 = linestring_with_linestrings_that_intersect[
                    linestring_most_interactions][0]
                # remove linestring that is longer
                if linestring_1.length >= linestring_2.length:
                    centerline_of_removed_line = linestring_with_centerlines[
                        linestring_1]
                else:
                    centerline_of_removed_line = linestring_with_centerlines[
                        linestring_2]
                if centerline_of_removed_line not in centerline_coordinates_to_be_removed:
                    centerline_coordinates_to_be_removed.append(
                        centerline_of_removed_line)
                # decrease intersecetions by 1 after removing linestring, from both the linestring and the places it intersects
                num_intersection_coordinates[
                    linestring_with_centerlines[linestring_1]] -= 1
                num_intersection_coordinates[
                    linestring_with_centerlines[linestring_2]] -= 1

        # Delete all width lines that have been flagged for removal
        for centerline_coord in centerline_coordinates_to_be_removed:
            del right_width_coordinates[centerline_coord]
            del left_width_coordinates[centerline_coord]
        logger.info("[SUCCESS] Intersection lines removed")

    # if using Relative Distance, convert points from Decimal Degrees to Relative Distance
    if coordinate_unit == "Relative Distance":
        right_width_coordinates = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0], right_width_coordinates,
            river_object.ellipsoid)
        left_width_coordinates = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0], left_width_coordinates,
            river_object.ellipsoid)
        num_intersection_coordinates = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0],
            num_intersection_coordinates, river_object.ellipsoid)

    return right_width_coordinates, left_width_coordinates, num_intersection_coordinates


def width(river_object: centerline_width.CenterlineWidth = None,
          transect_span_distance: int = 3,
          transect_slope: str = "Average",
          apply_smoothing: bool = True,
          remove_intersections: bool = False,
          coordinate_unit: str = "Decimal Degrees",
          coordinate_reference: str = "Centerline",
          save_to_csv: str = None) -> dict:
    # Return river width: centerline and width at centerline
    # Width is measured to the bank, relative to the center point (normal of the centerline)
    # { [centerline latitude, centerline longitude] : widthValue }

    centerline_width.errorHandlingWidth(
        river_object=river_object,
        transect_span_distance=transect_span_distance,
        transect_slope=transect_slope,
        apply_smoothing=apply_smoothing,
        remove_intersections=remove_intersections,
        coordinate_unit=coordinate_unit,
        coordinate_reference=coordinate_reference,
        save_to_csv=save_to_csv)

    transect_slope = transect_slope.title()
    coordinate_unit = coordinate_unit.title()
    coordinate_reference = coordinate_reference.title()
    right_left_coords = {
    }  # used to track left/right bank coordinates when coordinate_reference=="Banks"

    if river_object.centerline_voronoi is None:
        logger.critical(
            "\nCRITICAL ERROR, unable to find width without a valid centerline"
        )
        return None

    # Run all as "Decimal Degrees" to be able to calculate width below
    if apply_smoothing:
        # if using smoothing, replace left/right coordinates with the smoothed variation
        right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(
            river_object=river_object,
            centerline_coordinates=river_object.centerlineSmoothed,
            transect_span_distance=transect_span_distance,
            remove_intersections=remove_intersections,
            coordinate_unit="Decimal Degrees")
    else:
        right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(
            river_object=river_object,
            centerline_coordinates=river_object.centerline_evenly_spaced,
            transect_span_distance=transect_span_distance,
            remove_intersections=remove_intersections,
            coordinate_unit="Decimal Degrees")

    width_dict = {}

    geodesic = Geod(ellps=river_object.ellipsoid)

    for centerline_coord, _ in right_width_coordinates.items():
        # store the distance between the lat/lon position of the right/left bank
        lon1, lat1 = right_width_coordinates[centerline_coord]
        lon2, lat2 = left_width_coordinates[centerline_coord]
        if coordinate_reference == "Banks":
            # store the coordinates of the right/left bank
            right_left_coords[centerline_coord] = (
                right_width_coordinates[centerline_coord],
                left_width_coordinates[centerline_coord])
        _, _, distance_between_right_and_left_m = geodesic.inv(
            lon1, lat1, lon2, lat2)
        width_dict[centerline_coord] = distance_between_right_and_left_m / 1000

    # Convert to Relative Distance after accounting for the width dictionary
    if coordinate_unit == "Relative Distance":
        right_width_coordinates = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0], right_width_coordinates,
            river_object.ellipsoid)
        left_width_coordinates = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0], left_width_coordinates,
            river_object.ellipsoid)
        if coordinate_reference == "Banks":
            # store the coordinates of the right/left bank
            for centerline_relative_coord, _ in right_width_coordinates.items(
            ):
                right_left_coords[centerline_relative_coord] = (
                    right_width_coordinates[centerline_relative_coord],
                    left_width_coordinates[centerline_relative_coord])
        width_dict = centerline_width.relativeWidthCoordinates(
            river_object.left_bank_coordinates[0], width_dict,
            river_object.ellipsoid)

    # If width reference set to "Banks", convert from referencing the centerline to reference left/right banks
    if coordinate_reference == "Banks":
        width_dict = {right_left_coords[k]: v for k, v in width_dict.items()}

    # Set headers and convert to Relative Distance if needed for output
    if coordinate_reference == "Centerline":
        if coordinate_unit == "Decimal Degrees":
            latitude_header, longitude_header = "Centerline Latitude (Deg)", "Centerline Longitude (Deg)"
        if coordinate_unit == "Relative Distance":
            latitude_header, longitude_header = "Relative Distance Y (from Latitude) (m)", "Relative Distance X (from Longitude) (m)"
    if coordinate_reference == "Banks":
        if coordinate_unit == "Decimal Degrees":
            right_latitude_header, right_longitude_header = "Right Latitude (Deg)", "Right Longitude (Deg)"
            left_latitude_header, left_longitude_header = "Left Latitude (Deg)", "Left Longitude (Deg)"
        if coordinate_unit == "Relative Distance":
            right_latitude_header, right_longitude_header = "Right Relative Distance Y (from Latitude) (m)", "Right Relative Distance X (from Longitude) (m)"
            left_latitude_header, left_longitude_header = "Left Relative Distance Y (from Latitude) (m)", "Left Relative Distance X (from Longitude) (m)"

    # Save width dictionary to a csv file (Latitude, Longtiude, Width)
    if save_to_csv:
        with open(save_to_csv, "w") as csv_file_output:
            writer = csv.writer(csv_file_output)
            if coordinate_reference == "Centerline":
                writer.writerow(
                    [latitude_header, longitude_header, "Width (km)"])
                for coordinate_key, width_value in width_dict.items():
                    writer.writerow(
                        [coordinate_key[1], coordinate_key[0], width_value])
            if coordinate_reference == "Banks":
                writer.writerow([
                    right_latitude_header, right_longitude_header,
                    left_latitude_header, left_longitude_header, "Width (km)"
                ])
                for coordinate_key, width_value in width_dict.items():
                    writer.writerow([
                        coordinate_key[0][1], coordinate_key[0][0],
                        coordinate_key[1][1], coordinate_key[1][0], width_value
                    ])

    return width_dict
