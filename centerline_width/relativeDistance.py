# Built in Python functions
import math

# External Python libraries (installed via pip install)
import numpy as np
import pyproj
import geopy.distance

def relativeSingleCoordinate(first_point, lat_lon_coord, ellipsoid):
	# Convert a single point to relative position
	if lat_lon_coord is None:
		return None

	geodesic = pyproj.Geod(ellps=ellipsoid)
	forward_bearing, _, distance_between_meters = geodesic.inv(first_point[0],
																first_point[1],
																lat_lon_coord[0],
																lat_lon_coord[1])
	x = distance_between_meters*math.cos(np.deg2rad(forward_bearing))
	y = distance_between_meters*math.sin(np.deg2rad(forward_bearing))
	return (x, y)

def relativeBankCoordinates(left_lon_lat_coordinates, right_lon_lat_coordinates, ellipsoid):
	# Convert bank latitude/longtiude coordinates to relative coordinates
	first_point = left_lon_lat_coordinates[0] # first point is the first point on the left bank

	if left_lon_lat_coordinates is None or right_lon_lat_coordinates is None:
		return None, None

	left_relative_coordinates = []
	for left_point in left_lon_lat_coordinates[1:]: # skip the bottom left most value
		coord_pair = relativeSingleCoordinate(first_point, left_point, ellipsoid)
		left_relative_coordinates.append(coord_pair)

	right_relative_coordinates = []
	for right_point in right_lon_lat_coordinates:
		coord_pair = relativeSingleCoordinate(first_point, right_point, ellipsoid)
		right_relative_coordinates.append(coord_pair)

	return left_relative_coordinates, right_relative_coordinates

def relativeCenterlineCoordinates(first_point, centerline_coordinates, ellipsoid):
	# Convert centerline coordinates to relative distance from the first point on the left bank
	centerline_relative_coordinates = []

	if centerline_coordinates is None:
		return None

	for centerline_coords in centerline_coordinates:
		coord_pair = relativeSingleCoordinate(first_point, centerline_coords, ellipsoid)
		centerline_relative_coordinates.append(coord_pair)

	return centerline_relative_coordinates

def relativeRidgeCoordinates(first_point, x_ridge, y_ridge, ellipsoid):
	# Convert Voronoi ridges from Decimal Degree to Relative Distance
	geodesic = pyproj.Geod(ellps=ellipsoid)

	x_relative_ridges = []
	y_relative_ridges = []
	for i in range(len(x_ridge)):
		# Coordinates are saved as a pair (x1, x2) and (y1, y2)
		coord_pair = relativeSingleCoordinate(first_point, (x_ridge[i][0],y_ridge[i][0]), ellipsoid)
		x1 = coord_pair[0]
		y1 = coord_pair[1]
		coord_pair = relativeSingleCoordinate(first_point, (x_ridge[i][1],y_ridge[i][1]), ellipsoid)
		x2 = coord_pair[0]
		y2 = coord_pair[1]
		x_relative_ridges.append((x1, x2))
		y_relative_ridges.append((y1, y2))

	return x_relative_ridges, y_relative_ridges

def relativeWidthCoordinates(first_point, width_dictionary, ellipsoid):
	# Convert width dictionary from Decimal Degree to Relative Distance
	geodesic = pyproj.Geod(ellps=ellipsoid)

	relative_width_dictionary = {}
	for k, v in width_dictionary.items():
		# Setup relative distance for key
		coord_pair_k = relativeSingleCoordinate(first_point, k, ellipsoid)
		# Setup relative distance for value
		if type(v) == tuple:
			# converting a coordinate -> coordinate dictionary
			coord_pair_v = relativeSingleCoordinate(first_point, v, ellipsoid)
			relative_width_dictionary[coord_pair_k] = coord_pair_v
		else:
			# converting a coordinate -> int dictionary
			relative_width_dictionary[coord_pair_k] = v

	return relative_width_dictionary
