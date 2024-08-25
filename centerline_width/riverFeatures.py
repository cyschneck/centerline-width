#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      riverFeatures.py contains calculations for determining river features which are            #
#      unrelated to width and centerline. This currently includes area, length, and               #
#      sinuosity                                                                                  #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - _calculate_river_area: backend function to              #
#                                              calculate area within the river                    #
#                                              polygon/coordinates                                #
#                                                                                                 #
#                                       - _centerline_length: backend function to                 #
#                                                calculate the length of a line                   #
#                                                                                                 #
#                                       - _calculate_sinuosity: backend to calculate              #
#                                                 the total sinuosity                             #
#                                                                                                 #
#                                       - incremental_sinuosity: returns the incremental          #
#                                                 sinuosity along the length of the river         #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
import csv

# Related Third Party Imports
from pyproj import Geod
from shapely.geometry import Point, LineString

# Internal Local Imports
import centerline_width


def _calculate_river_area(bank_polygon=None,
                          ellipsoid: str = "WGS84") -> float:
    # Return the area contained within the river polygon (km^2)
    if bank_polygon is None:
        return 0
    geodesic = Geod(ellps=ellipsoid)
    river_area, river_perimeter = geodesic.geometry_area_perimeter(
        bank_polygon)
    return abs(river_area) / 1000  # km


def _centerline_length(centerline_coordinates: list = None,
                       ellipsoid: str = "WGS84") -> float:
    # Return the length/distance for all the centerline coordinates (km)
    if centerline_coordinates is None:
        return 0

    geodesic = Geod(ellps=ellipsoid)
    geo_coordinates = LineString(map(Point, centerline_coordinates))
    centerline_length_km = geodesic.geometry_length(
        geo_coordinates) / 1000  # km

    return centerline_length_km


def _calculate_sinuosity(centerline_evenlySpaced_coordinates: list = None,
                         ellipsoid: str = "WGS84") -> float:
    # Return the sinuosity of the river in total
    if centerline_evenlySpaced_coordinates is None:
        return 0

    # sinuosity is the difference of length of first/last point to centerline
    sinuosity = 0
    sinuosity = _centerline_length(
        centerline_evenlySpaced_coordinates) / _centerline_length([
            centerline_evenlySpaced_coordinates[0],
            centerline_evenlySpaced_coordinates[-1]
        ], ellipsoid)

    return sinuosity


def incremental_sinuosity(
        river_object: centerline_width.CenterlineWidth = None,
        incremental_points: int = 100,
        save_to_csv: str = None) -> dict:
    # Return the sinuosity of the river in increments
    # (Centerline Coordinate Start, Centerline Coordinate End Longtiude, Sinuosity)

    centerline_width._error_handling_incremental_sinuosity(
        river_object=river_object,
        incremental_points=incremental_points,
        save_to_csv=save_to_csv)

    if river_object.centerline_evenly_spaced is None:
        return {}

    # Ignore the first and last point in the coordinates
    centerline_coordinates = river_object.centerline_evenly_spaced[1:-1]

    # Separate centerline in groups of incremental_points long
    centerline_groups = list(
        zip(*[iter(centerline_coordinates)] * incremental_points))

    # Calculate incremental sinuosity
    incremental_sinuosity_dict = {}
    for centerline_coords in centerline_groups:
        incremental_sinuosity_dict[(
            centerline_coords[0],
            centerline_coords[-1])] = _calculate_sinuosity(
                centerline_evenlySpaced_coordinates=centerline_coords,
                ellipsoid=river_object.ellipsoid)

    # Save width dictionary to a csv file
    if save_to_csv:
        with open(save_to_csv, "w") as csv_file_output:
            writer = csv.writer(csv_file_output)
            writer.writerow([
                "Centerline Latitude Start (Deg)",
                "Centerline Longitude Start (Deg)",
                "Centerline Latitude End (Deg)",
                "Centerline Longitude End (Deg)", "Sinuosity"
            ])
            for coordinate_key, sinuosity_value in incremental_sinuosity_dict.items(
            ):
                writer.writerow([
                    coordinate_key[0][1], coordinate_key[0][0],
                    coordinate_key[1][1], coordinate_key[1][0], sinuosity_value
                ])

    return incremental_sinuosity_dict
