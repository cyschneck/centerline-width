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


#def calculateSinuosity():
#    # Return the sinuosity of the river, in total and in evenly spaced parts
#    pass
