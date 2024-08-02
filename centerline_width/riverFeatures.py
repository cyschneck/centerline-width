#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      riverFeatures.py contains calculations for determining river features which are            #
#      unrelated to width and centerline. This currently includes area, length, and               #
#      sinuosity                                                                                  #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - calculateRiverArea: returns the area contains           #
#                                              within the river polygon/coordinates               #
#                                                                                                 #
#                                       - riverWidthFromCenterline: returns the length of         #
#                                                centerline                                       #
#                                                                                                 #
#                                       - calculateSinuosity: returns the total sinuosity         #
#                                                                                                 #
#                                       - calculateIncrementalSinuosity: returns the              #
#                                                incremental sinuosity along the length of        #
#                                                the river                                        #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Built-in Python functions
import csv

# External Python libraries
from pyproj import Geod
from shapely.geometry import Point, LineString

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width


def calculateRiverArea(bank_polygon=None, ellipsoid: str = "WGS84") -> float:
    # Return the area contained within the river polygon (km^2)
    if bank_polygon is None:
        return 0
    geodesic = Geod(ellps=ellipsoid)
    river_area, river_perimeter = geodesic.geometry_area_perimeter(
        bank_polygon)
    return abs(river_area) / 1000  # km


def centerlineLength(centerline_coordinates: list = None,
                     ellipsoid: str = "WGS84") -> float:
    # Return the length/distance for all the centerline coordinates in km
    if centerline_coordinates is None:
        return 0

    geodesic = Geod(ellps=ellipsoid)
    geo_coordinates = LineString(map(Point, centerline_coordinates))
    centerline_length_km = geodesic.geometry_length(
        geo_coordinates) / 1000  # km

    return centerline_length_km


def calculateSinuosity(centerline_evenlySpaced_coordinates: list = None,
                       ellipsoid: str = "WGS84") -> float:
    # Return the sinuosity of the river in total
    if centerline_evenlySpaced_coordinates is None:
        return 0

    # sinuosity is the difference of length of first/last point to centerline
    sinuosity = 0
    sinuosity = centerlineLength([
        centerline_evenlySpaced_coordinates[0],
        centerline_evenlySpaced_coordinates[-1]
    ], ellipsoid) / centerlineLength(centerline_evenlySpaced_coordinates)

    return sinuosity


def calculateIncrementalSinuosity(
        river_object: centerline_width.riverCenterline = None,
        incremental_points: int = 100,
        save_to_csv: str = None) -> dict:
    # Return the sinuosity of the river in increments
    # (Centerline Coordinate Start, Centerline Coordinate End Longtiude, Sinuosity)

    centerline_width.errorHandlingCalculateIncrementalSinuosity(
        river_object=river_object,
        incremental_points=incremental_points,
        save_to_csv=save_to_csv)

    if river_object.centerlineEvenlySpaced is None:
        return {}

    # Ignore the first and last point in the coordinates
    centerline_coordinates = river_object.centerlineEvenlySpaced[1:-1]

    # Separate centerline in groups of incremental_points long
    centerline_groups = list(
        zip(*[iter(centerline_coordinates)] * incremental_points))

    # Calculate incremental sinuosity
    incremental_sinuosity = {}
    for centerline_coords in centerline_groups:
        incremental_sinuosity[(
            centerline_coords[0], centerline_coords[-1])] = calculateSinuosity(
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
            for coordinate_key, sinuosity_value in incremental_sinuosity.items(
            ):
                writer.writerow([
                    coordinate_key[0][1], coordinate_key[0][0],
                    coordinate_key[1][1], coordinate_key[1][0], sinuosity_value
                ])

    return incremental_sinuosity
