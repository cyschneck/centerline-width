# External Python libraries
import pyproj


def calculateRiverArea(bank_polygon=None, ellipsoid="WGS84"):
    # Return the area contained within the river polygon (km^2)
    if bank_polygon is None:
        return 0
    geodesic = pyproj.Geod(ellps=ellipsoid)
    river_area, river_perimeter = geodesic.geometry_area_perimeter(
        bank_polygon)
    return abs(river_area) / 1000  # km


def centerlineLength(centerline_coordinates=None, ellipsoid="WGS84"):
    # Return the length/distance for all the centerline coordinates in km
    total_length = 0
    previous_pair = None
    if centerline_coordinates is None:
        return 0

    geodesic = pyproj.Geod(ellps=ellipsoid)

    for xy_pair in centerline_coordinates:
        if previous_pair is None:
            previous_pair = xy_pair
        else:
            lon1, lon2 = previous_pair[0], xy_pair[0]
            lat1, lat2 = previous_pair[1], xy_pair[1]
            _, _, distance_between_meters = geodesic.inv(
                lon1, lat1, lon2, lat2)
            total_length += distance_between_meters
        # Set previous_pair to xy_pair for the next iteration.
        previous_pair = xy_pair
    return total_length / 1000  # km
