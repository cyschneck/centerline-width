# River features, unrelated to width/centerline: area, length, sinuosity

# External Python libraries
from pyproj import Geod
from shapely.geometry import Point, LineString


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
        centerline_evenlySpaced_coordinates: list = None,
        ellipsoid: str = "WGS84",
        incremental_points: int = 10) -> dict:
    # Return the sinuosity of the river in increments
    if centerline_evenlySpaced_coordinates is None:
        return {}

    # Ignore the first and last point in the coordinates
    centerline_coordinates = centerline_evenlySpaced_coordinates[1:-1]

    # Separate centerline in groups of incremental_points long
    centerline_groups = list(
        zip(*[iter(centerline_coordinates)] * incremental_points))

    # Calculate incremental sinuosity
    incremental_sinuosity = {}
    for centerline_coords in centerline_groups:
        incremental_sinuosity[(
            centerline_coords[0], centerline_coords[-1])] = calculateSinuosity(
                centerline_evenlySpaced_coordinates=centerline_coords,
                ellipsoid=ellipsoid)

    return incremental_sinuosity
