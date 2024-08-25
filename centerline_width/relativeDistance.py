#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      relativeDistance.py contains calculations to convert latitude and longtiude                #
#      (decimal degree) coordinates to a relative distance from the first point on                #
#      the left bank                                                                              #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - _relative_single_coordinate: backend function           #
#                                              converts a single point to a relative              #
#                                              distance from first                                #
#                                              point on the left bank                             #
#                                                                                                 #
#                                       - _relative_bank_coordinates: backend convert             #
#                                              latitude and longitude coordinates as a            #
#                                              relative distance                                  #
#                                                                                                 #
#                                                                                                 #
#                                       - _relative_centerline_coordinates: backend               #
#                                              convert centerline coordinates to relative         #
#                                              distance from the first point on the               #
#                                              left bank                                          #
#                                                                                                 #
#                                       - _relative_ridge_coordinates: backend convert            #
#                                              Voronoi ridges coordinates to a relative           #
#                                              distance                                           #
#                                                                                                 #
#                                       - _relative_width_coordinates: backend convert            #
#                                              width dictionary to a relative distance            #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
import math

# Related Third Party Imports
import numpy as np
import pyproj
import geopy.distance


def _relative_single_coordinate(first_point=None,
                                lat_lon_coord=None,
                                ellipsoid: str = "WGS84") -> tuple:
    # Convert a single point to relative position
    if lat_lon_coord is None:
        return None

    geodesic = pyproj.Geod(ellps=ellipsoid)
    forward_bearing, _, distance_between_meters = geodesic.inv(
        first_point[0], first_point[1], lat_lon_coord[0], lat_lon_coord[1])
    x = distance_between_meters * math.cos(np.deg2rad(forward_bearing))
    y = distance_between_meters * math.sin(np.deg2rad(forward_bearing))
    return (x, y)


def _relative_bank_coordinates(left_lon_lat_coordinates=None,
                               right_lon_lat_coordinates=None,
                               ellipsoid: str = "WGS84"):
    # Convert bank latitude/longtiude coordinates to relative coordinates
    if left_lon_lat_coordinates is None or right_lon_lat_coordinates is None:
        return None, None
    if len(left_lon_lat_coordinates) == 0 or len(
            right_lon_lat_coordinates) == 0:
        return None, None

    first_point = left_lon_lat_coordinates[
        0]  # first point is the first point on the left bank

    left_relative_coordinates = []
    for left_point in left_lon_lat_coordinates:
        if left_point == first_point:
            coord_pair = (0.0, 0.0)
        else:
            coord_pair = _relative_single_coordinate(first_point, left_point,
                                                     ellipsoid)
        left_relative_coordinates.append(coord_pair)

    right_relative_coordinates = []
    for right_point in right_lon_lat_coordinates:
        coord_pair = _relative_single_coordinate(first_point, right_point,
                                                 ellipsoid)
        right_relative_coordinates.append(coord_pair)

    return left_relative_coordinates, right_relative_coordinates


def _relative_centerline_coordinates(first_point=None,
                                     centerline_coordinates=None,
                                     ellipsoid: str = "WGS84"):
    # Convert centerline coordinates to relative distance from the first point on the left bank
    centerline_relative_coordinates = []

    if centerline_coordinates is None:
        return None

    for centerline_coords in centerline_coordinates:
        coord_pair = _relative_single_coordinate(first_point,
                                                 centerline_coords, ellipsoid)
        centerline_relative_coordinates.append(coord_pair)

    return centerline_relative_coordinates


def _relative_ridge_coordinates(first_point=None,
                                x_ridge=None,
                                y_ridge=None,
                                ellipsoid: str = "WGS84"):
    # Convert Voronoi ridges from Decimal Degree to Relative Distance

    x_relative_ridges = []
    y_relative_ridges = []
    for i in range(len(x_ridge)):
        # Coordinates are saved as a pair (x1, x2) and (y1, y2)
        coord_pair = _relative_single_coordinate(
            first_point, (x_ridge[i][0], y_ridge[i][0]), ellipsoid)
        x1 = coord_pair[0]
        y1 = coord_pair[1]
        coord_pair = _relative_single_coordinate(
            first_point, (x_ridge[i][1], y_ridge[i][1]), ellipsoid)
        x2 = coord_pair[0]
        y2 = coord_pair[1]
        x_relative_ridges.append((x1, x2))
        y_relative_ridges.append((y1, y2))

    return x_relative_ridges, y_relative_ridges


def _relative_width_coordinates(first_point=None,
                                width_dictionary: dict = None,
                                ellipsoid: str = "WGS84") -> dict:
    # Convert width dictionary from Decimal Degree to Relative Distance

    relative_width_dictionary = {}
    for k, v in width_dictionary.items():
        # Setup relative distance for key
        coord_pair_k = _relative_single_coordinate(first_point, k, ellipsoid)
        # Setup relative distance for value
        if type(v) == tuple:
            # converting a coordinate -> coordinate dictionary
            coord_pair_v = _relative_single_coordinate(first_point, v,
                                                       ellipsoid)
            relative_width_dictionary[coord_pair_k] = coord_pair_v
        else:
            # converting a coordinate -> int dictionary
            relative_width_dictionary[coord_pair_k] = v

    return relative_width_dictionary
