# Built in Python functions
import csv
import logging
import math

# External Python libraries (installed via pip install)
from collections import Counter
from haversine import haversine
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from scipy.spatial import Voronoi

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def convertColumnsToCSV(text_file=None, flipBankDirection=False):
	# Convert txt file to a comma seperated version of the file to use in pandas

	centerline_width.errrorHandlingConvertColumnsToCSV(text_file=text_file, flipBankDirection=flipBankDirection)

	left_rows = []
	right_rows = []
	with open(text_file) as input_file:
		lines = input_file.readlines()
		for i, line in enumerate(lines):
			line = line.strip().split(" ")
			line = [x for x in line if x != '']
			if i == 0:
				header_fields = line
			else:
				left_rows.append(line[:2])
				right_rows.append(line[2:])

	# reverse the direction for the right bank
	if flipBankDirection:
		right_rows = right_rows[::-1]

	total_rows = []
	for i, row in enumerate(left_rows):
		total_rows.append(row + right_rows[i])

	write_file_name = text_file.split(".")[0] + ".csv"
	with open(write_file_name, "w") as f:
		write = csv.writer(f)
		write.writerow(header_fields)
		write.writerows(total_rows)

def leftRightCoordinates(dataframe):
	right_bank_coordinates = [] # without nan
	left_bank_coordinates = [] # wtihout nan
	for index, row in dataframe.iterrows():
		if not math.isnan(row.rlat) and not math.isnan(row.rlon):
			right_bank_coordinates.append([row.rlon, row.rlat])
		if not math.isnan(row.llat) and not math.isnan(row.llon):
			left_bank_coordinates.append([row.llon, row.llat])
	return left_bank_coordinates, right_bank_coordinates

def generatePolygon(left_bank_lst, right_bank_lst):
	# Return a shapely polygon based on the position of the river bank points
	circular_list_of_banks = left_bank_lst + right_bank_lst[::-1] + [left_bank_lst[0]]

	bank_points_swapped = []
	for i, bank_point in enumerate(circular_list_of_banks):
		bank_points_swapped.append([bank_point[0], bank_point[1]]) # Swap the x and y to graph with longitude on the y-axis

	river_polygon = Polygon(bank_points_swapped)
	top_river = LineString([Point(left_bank_lst[::-1][0][0],left_bank_lst[::-1][0][1]), Point(right_bank_lst[::-1][0][0], right_bank_lst[::-1][0][1])])
	bottom_river = LineString([Point(right_bank_lst[0][0], right_bank_lst[0][1]), Point(left_bank_lst[0][0], left_bank_lst[0][1])])

	if not river_polygon.is_valid:
		logger.critical("[FAILED]  Invalid Polygon needs to be corrected")
	else:
		logger.info("[SUCCESS] Valid polygon generated")

	return river_polygon, top_river, bottom_river

def generateVoronoi(left_bank_lst, right_bank_lst):
	# Generate a Voronoi shape based on the left/right bank points
	all_banks_points = left_bank_lst + right_bank_lst
	all_banks_points = np.array(all_banks_points)

	river_voronoi = Voronoi(all_banks_points)
	logger.info("[SUCCESS] Voronoi diagram generated")
	return river_voronoi

def pointsFromVoronoi(river_voronoi, river_polygon):
	# Returns a dictionary list of all the voronoi points: {start point : [list of end points]}
	points_dict = {}
	all_connections_start_to_end = []
	logger.info("[PROCESSING] Attempting to determine a valid centerline from Voronoi points, may take a few minutes...") # longest step, O(n^n)
	for ridge_vertex_point in river_voronoi.ridge_vertices:
		if ridge_vertex_point[0] >= 0 and ridge_vertex_point[1] >= 0: # Only include non-infinity vertex edges
			v0 = river_voronoi.vertices[ridge_vertex_point[0]]
			v1 = river_voronoi.vertices[ridge_vertex_point[1]]
			# Check if start and end points are within the polygon, otherwise remove the connection pair
			if river_polygon.contains(Point([v0[0], v0[1]])) and river_polygon.contains(Point([v1[0], v1[1]])):
				start_point = tuple([v0[0], v0[1]])
				end_point = tuple([v1[0], v1[1]])
				start_to_end = [start_point, end_point]
				if start_to_end not in all_connections_start_to_end: 
					all_connections_start_to_end.append(start_to_end)

	# Dictionary with connections that have at least one connection
	connections_counter_start_to_end = Counter(x for xs in all_connections_start_to_end for x in set(xs)) # counter the amount of connections for each point
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

def interpolateBetweenPoints(river_object, left_bank_coordinates, right_bank_coordinates):
	# Interpolated between points at an even distance along the river banks to attempt to even out Voronoi diagrams
	deg_to_m = 111.139 * 1000 # degrees to kilometers to meters
	distance_delta = int(deg_to_m / 700) # every 700 meters

	def interpolateList(lst):
		# Add points to existing list to increase resolution
		#haversine_distance_between = haversine((lat1, lon1), (lat2, lon2), unit=units)
		bank_expanded = []
		for i in range(len(lst)):
			if i+1 < len(lst):
				lon1, lat1 = lst[i][0], lst[i][1]
				lon2, lat2 = lst[i+1][0], lst[i+1][1]

				x_lon_distance = haversine((0, lon1), (0, lon2), unit="m")
				y_lat_distance = haversine((lat1, 0), (lat2, 0), unit="m")
				x_expand = np.linspace(lon1, lon2, distance_delta)
				y_expand = np.linspace(lat1, lat2, distance_delta)

				for j in range(len(x_expand)):
					bank_expanded.append([x_expand[j],y_expand[j]])
					bank_expanded.append(lst[i+1])
			else: 
				bank_expanded.append(lst[i])
		return bank_expanded

	right_interpolated_coordinates = interpolateList(right_bank_coordinates)
	left_interpolated_coordinates = interpolateList(left_bank_coordinates)
	interpolated_voronoi = centerline_width.generateVoronoi(left_interpolated_coordinates, right_interpolated_coordinates)

	return right_interpolated_coordinates, left_interpolated_coordinates, interpolated_voronoi
