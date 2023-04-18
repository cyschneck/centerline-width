import math
import logging

import numpy as np
import pandas as pd
import networkx as nx
from shapely.geometry import Point, Polygon, LineString

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def centerlinePath(river_voronoi, river_polygon, top_polygon_line, bottom_polygon_line):
	# Return the starting node, ending node, and centerline path
	start_end_points_dict = centerline_width.pointsFromVoronoi(river_voronoi, river_polygon)
	x_ridge_point = []
	y_ridge_point = []
	starting_node = None
	ending_node = None
	for start_point, end_point_list in start_end_points_dict.items():
		if len(end_point_list) > 0: # TESTING TESTING: Show only the end points that have multiple connections
			# Find the starting and ending node based on distance from the top and bottom of the polygon
			if starting_node is None: starting_node = start_point
			else:
				if Point(start_point).distance(top_polygon_line) <= Point(starting_node).distance(top_polygon_line):
					starting_node = start_point
			for end_point in end_point_list:
				if Point(end_point).distance(top_polygon_line) <= Point(starting_node).distance(top_polygon_line):
					starting_node = end_point
				if ending_node is None: ending_node = end_point
				else:
					if Point(start_point).distance(bottom_polygon_line) <= Point(ending_node).distance(bottom_polygon_line):
						ending_node = start_point
					if Point(end_point).distance(bottom_polygon_line) <= Point(ending_node).distance(bottom_polygon_line):
						ending_node = end_point
				x_ridge_point.append([start_point[0], end_point[0]])
				y_ridge_point.append([start_point[1], end_point[1]])

	if starting_node is None:
		logger.critical("\nCRITICAL ERROR, Voronoi diagram generated too small to find centerline (no starting node found), unable to plot centerline. Set displayVoronoi=True to view. Can typically be fixed by adding more data to expand range.")

	return starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict

def networkXGraphShortestPath(all_points_dict, starting_node, ending_node):
	def distanceBetween(start, end):
		lat1 = start[0]
		lat2 = end[0]
		lon1 = start[1]
		lon2 = end[1]
		p = math.pi/180
		a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2
		return math.asin(math.sqrt(a))

	if starting_node is not None:
		graph_connections = nx.Graph()
		node_as_keys_pos_values = {}
		for start_point, end_point_list in all_points_dict.items():
			node_as_keys_pos_values[start_point] = (start_point[0], start_point[1])
			graph_connections.add_node(start_point, pos=(start_point[0], start_point[1]))
			for end_point in end_point_list:
				graph_connections.add_node(end_point, pos=(end_point[0], end_point[1]))
				node_as_keys_pos_values[end_point] = (end_point[0], end_point[1])
				graph_connections.add_edge(start_point, end_point, weight=distanceBetween(start_point,end_point))
		try:
			shortest_path = nx.shortest_path(graph_connections, source=starting_node, target=ending_node)
			logger.info("[SUCCESS] Valid centerline path found")
		except nx.NetworkXNoPath: # no direct path found
			logger.info("[FAILED]  No direct path found from starting node to ending node")
			return None
		#nx.draw(graph_connections, with_labels=True, font_size=10)
		return shortest_path
	else:
		return None

def centerlineLatitudeLongitude(csv_data=None, optional_cutoff=None):
	# Returns the latitude and longitude for the centerline

	centerline_width.errorHandlingCenterlineLatitudeLongitude(csv_data=csv_data, optional_cutoff=optional_cutoff)

	df = pd.read_csv(csv_data)
	if optional_cutoff:
		df = df.head(optional_cutoff)
	left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)

	river_bank_polygon, top_river_line, bottom_river_line = centerline_width.generatePolygon(left_bank_coordinates, right_bank_coordinates)
	river_bank_voronoi = centerline_width.generateVoronoi(left_bank_coordinates, right_bank_coordinates)

	starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict = centerline_width.centerlinePath(river_bank_voronoi, river_bank_polygon, top_river_line, bottom_river_line)
	shortest_path_coordinates = centerline_width.networkXGraphShortestPath(start_end_points_dict, starting_node, ending_node)

	return shortest_path_coordinates

def evenlySpacedCenterline(centerline_coordinates=None, number_of_fixed_points=10):
	# Interpolate to evenly space points along the centerline coordinates (effectively smoothing with fewer points)
	centerline_line = LineString(centerline_coordinates)

	# Splitting into a fixed number of points
	distances_evenly_spaced = np.linspace(0, centerline_line.length, number_of_fixed_points)
	points_evenly_spaced = [centerline_line.interpolate(distance) for distance in distances_evenly_spaced]

	# Convert Shapley Points to a List of Tuples (coordinates)
	interpolated_centerline_coordinates = []
	for point in points_evenly_spaced:
		interpolated_centerline_coordinates.append((point.x, point.y))

	return interpolated_centerline_coordinates

def smoothedCoordinates(centerline_coordinates=None, interprolate_num=None):
	# return a list coordinates after applying b-spline (smoothing)
	x_coordinates = []
	y_coordinates = []

	# splitting centerline coordinaets into an x and y component
	for centerline_point in centerline_coordinates:
		x_coordinates.append(centerline_point[0])
		y_coordinates.append(centerline_point[1])

	# applying a path smoothing spline
	smoothed_coordinates = []
	from scipy import interpolate
	tck, *rest = interpolate.splprep([x_coordinates, y_coordinates], s=0.000001) # spline prep, tck = knots - coefficeinets - degree
	u = np.linspace(0, 1, interprolate_num) # number of steps between each point (to determine smoothness)
	x_smoothed, y_smoothed =  interpolate.splev(u, tck) # interpolated list of points

	x_smoothed, y_smoothed = x_smoothed.tolist(), y_smoothed.tolist() # convert array to list
	smoothed_coordinates = list(zip(x_smoothed, y_smoothed))
	#print(centerline_coordinates)
	#print(smoothed_coordinates)
	return smoothed_coordinates

def riverWidthFromCenterlineCoordinates(csv_data=None,
										centerline_coordinates=None,
										transect_span_distance=3,
										bank_polygon=None,
										remove_intersections=False,
										save_to_csv=None,
										optional_cutoff=None):
	# Return the left/right coordinates of width centerlines
	right_width_coordinates = {}
	left_width_coordinates = {}
	num_intersection_coordinates = {}
	x = []
	y = []

	df = pd.read_csv(csv_data)
	if optional_cutoff:
		df = df.head(optional_cutoff)
	left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)
	if bank_polygon is None:
		bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(left_bank_coordinates, right_bank_coordinates)
	else:
		left_bank_lst, right_bank_lst = centerline_width.leftRightCoordinates(df)
		top_bank = LineString([Point(left_bank_lst[::-1][0][0],left_bank_lst[::-1][0][1]), Point(right_bank_lst[::-1][0][0], right_bank_lst[::-1][0][1])])
		bottom_bank = LineString([Point(right_bank_lst[0][0], right_bank_lst[0][1]), Point(left_bank_lst[0][0], left_bank_lst[0][1])])

	# Average slopes for every n points to chart
	centerline_slope = {}
	groups_of_n_points = [centerline_coordinates[i:i+transect_span_distance] for i in range(0, len(centerline_coordinates), transect_span_distance)]
	for group_points in groups_of_n_points:
		#print(group_points)
		slope_sum = 0
		total_slopes = 0
		for i in range(len(group_points)):
			if i+1 < len(group_points):
				dy = group_points[i+1][1] - group_points[i][1]
				dx = group_points[i+1][0] - group_points[i][0]
				if dx != 0:
					slope_sum += (dy / dx)
					total_slopes += 1
		if slope_sum != 0:
			slope_avg = slope_sum / total_slopes
			normal_of_slope = -1 / slope_avg
			middle_of_list = len(group_points) // 2
			#print("slope_avg = {0}".format(slope_avg))
			#print("normal_of_slope = {0}\n".format(normal_of_slope))
			#print(group_points[middle_of_list])
			#print(normal_of_slope)
			centerline_slope[group_points[middle_of_list]] = normal_of_slope

	def intersectsTopOrBottomOfBank(point1, point2):
		# returns True/False if the points lie on the 'false' top/bottom of the river
		points_intersect_false_edges = False
		# avoding floating point precession errors when determining if point lies within the line
		# if point is within a small distance of a line it is considered to intersect
		if top_bank.distance(point1) < 1e-8 or bottom_bank.distance(point1) < 1e-8:
			points_intersect_false_edges = True
		if top_bank.distance(point2) < 1e-8 or bottom_bank.distance(point2) < 1e-8:
			points_intersect_false_edges = True
		return points_intersect_false_edges

	# Generate a list of lines from the centerline point with its normal
	min_x, min_y, max_x, max_y = bank_polygon.bounds
	for centerline_point, slope in centerline_slope.items():
		left_y = slope * (min_x - centerline_point[0]) + centerline_point[1]
		right_y = slope * (max_x - centerline_point[0]) + centerline_point[1]

		# Save the points where they intersect the polygon
		sloped_line = LineString([(min_x, left_y), (max_x, right_y)]) # sloped line from the centerpoint
		line_intersection_points = bank_polygon.exterior.intersection(sloped_line) # points where the line intersects the polygon
		if len(line_intersection_points.geoms) == 2:
			 # only save width lines that do not touch the artifical top/bottom
			if not intersectsTopOrBottomOfBank(line_intersection_points.geoms[0], line_intersection_points.geoms[1]):
				left_width_coordinates[centerline_point] = (line_intersection_points.geoms[0].x, line_intersection_points.geoms[0].y)
				right_width_coordinates[centerline_point] = (line_intersection_points.geoms[1].x, line_intersection_points.geoms[1].y)
		else:
			# line intersects to polygon at multiple points, find the closest two points to chart
			distances_between_centerline_and_point = []
			for i in range(len(line_intersection_points.geoms)):
				point_intersection = Point(line_intersection_points.geoms[i].x, line_intersection_points.geoms[i].y)
				distance_between = Point(centerline_point).distance(point_intersection)
				distances_between_centerline_and_point.append(distance_between)
			# collect the two closest points
			index_of_sorted_list = sorted(range(len(distances_between_centerline_and_point)),key=distances_between_centerline_and_point.__getitem__)
			smallest_point = line_intersection_points.geoms[index_of_sorted_list[0]]
			second_smallest_point = line_intersection_points.geoms[index_of_sorted_list[1]]
			if not intersectsTopOrBottomOfBank(smallest_point, second_smallest_point): # only save width lines that do not touch the artifical top/bottom
				left_width_coordinates[centerline_point] = (smallest_point.x, smallest_point.y)
				right_width_coordinates[centerline_point] = (second_smallest_point.x, second_smallest_point.y)
				# Verify that closest pair of points that form the line lie within the polygon
				print("TODO: bug fix: check if a linestring lies outside a polygon")
	
	# Determine lines that have multiple intersections to flag/remove
	all_linestrings = []
	linestring_with_centerlines = {} # TODOODODO: replace when can figure out how to decompose LineString into two points
	linestring_with_linestrings_that_intersect = {} # dictionary of all the linestrings that a linestring intersects with
	# Generate a list of linestrings
	for centerline_coord in right_width_coordinates.keys():
		linestring_generated = LineString([Point(left_width_coordinates[centerline_coord][0], left_width_coordinates[centerline_coord][1]),
											Point(right_width_coordinates[centerline_coord][0], right_width_coordinates[centerline_coord][1])])
		linestring_with_centerlines[linestring_generated] = centerline_coord
		all_linestrings.append(linestring_generated)
	# count the number of intersections for each linestring, +1 for each time one line string intersects another
	for linestring_to_check in all_linestrings:
		num_intersection_coordinates[linestring_with_centerlines[linestring_to_check]] = 0 # default set all intersects to zero
		for linestring_to_check_against in all_linestrings:
			if linestring_to_check != linestring_to_check_against:
				if linestring_to_check.intersects(linestring_to_check_against): # check if two lines intersect
					intersection_points_linestrings = linestring_to_check.intersection(linestring_to_check_against) # return point positions where intersection occurs
					if str(intersection_points_linestrings) != "LINESTRING Z EMPTY": # if linestring has intersect, increment count
						num_intersection_coordinates[linestring_with_centerlines[linestring_to_check]] += 1
						if linestring_to_check not in linestring_with_linestrings_that_intersect.keys():
							linestring_with_linestrings_that_intersect[linestring_to_check] = []
						linestring_with_linestrings_that_intersect[linestring_to_check].append(linestring_to_check_against)

	# Remove Intersection lines
	if remove_intersections:
		# iterate from the most intersections to the least intersections
		for linestring_most_interactions in sorted(linestring_with_linestrings_that_intersect, key=lambda k: len(linestring_with_linestrings_that_intersect[k]), reverse=True):
			#print(dict((k, v) for k, v in num_intersection_coordinates.items() if v > 0))

			# when number of intersections > 1, remove lines with the most interactions, to the smallest
			if num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] > 1: 
				lst_linestrings_hit_by_linestring = linestring_with_linestrings_that_intersect[linestring_most_interactions]
				# iterate through each and remove linestring from the associated lists of places it intersects
				for linestring_hit in lst_linestrings_hit_by_linestring: 
					linestring_with_linestrings_that_intersect[linestring_hit].remove(linestring_most_interactions)
					num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] -= 1
					num_intersection_coordinates[linestring_with_centerlines[linestring_hit]] -= 1
				centerline_of_removed_line = linestring_with_centerlines[linestring_most_interactions]
				del right_width_coordinates[centerline_of_removed_line] # remove coordinates that result in the interactions
				del left_width_coordinates[centerline_of_removed_line] # remove coordinates coordinates that result in the interactions

			# when number of intersections == 1, remove the longer width line
			'''
			if num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] == 1: 
				pass
				break
				if len(linestring_with_linestrings_that_intersect[linestring_most_interactions]):
					pass
				print("\nline start = {0}".format(linestring_most_interactions))
				print(len(linestring_with_linestrings_that_intersect[linestring_most_interactions]))
				print(num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]])
				for i in linestring_with_linestrings_that_intersect[linestring_most_interactions]:
					print(i)
				print("\n")
			'''

	print(dict((k, v) for k, v in num_intersection_coordinates.items() if v > 0))
	return right_width_coordinates, left_width_coordinates, num_intersection_coordinates

def riverWidthFromCenterline(csv_data=None, centerline_coordinates=None, bank_polygon=None, save_to_csv=None, optional_cutoff=None):
	# Return river width: right to center, left to center, total width
	# Width is measured to the bank, relative to the center point (normal of the centerline)
	# { [centerline latitude, centerline longitude] : { rightCenter : distance, leftCenter : distance, totalWidth: distance } }

	centerline_width.errorHandlingRiverWidthFromCenterline(csv_data=csv_data,
															centerline_coordinates=centerline_coordinates,
															bank_polygon=bank_polygon,
															save_to_csv=save_to_csv,
															optional_cutoff=optional_cutoff)

	width_dict = {}

	'''
	for centerline_lat_long in centerline_coordinates:
		distance = 0 # TODO: find distance between each coordinate normal to the polygon
		internal_dict = {}
		internal_dict["rightCenter"] = distance
		internal_dict["leftCenter"] = distance
		internal_dict["totalWidth"] = distance
		width_dict[centerline_lat_long] = internal_dict

	if save_to_csv:
		header_fields = ["Right-Center Width", "Left-Center Width", "Total Width"]
		#total_rows = []
		#for coordinates in centerline_coordinates:
		#	total_rows.append(coordinates)
		#with open(save_to_csv, "w") as f:
		#	write = csv.writer(f)
		#	write.writerow(header_fields)
		#	write.writerows(total_rows)

	print("riverWidthFromCenterline = {0}".format(width_dict))
	'''
	return width_dict

def centerlineLength(centerline_coordinates=None):
	# Return the length/distance for all the centerline coordaintes

	centerline_width.errorHandlingCenterlineLength(centerline_coordinates=centerline_coordinates)

	total_length = 0
	previous_pair = None
	for xy_pair in centerline_coordinates:
		if previous_pair is None:
			previous_pair = xy_pair
		else:
			x1, x2 = previous_pair[0], xy_pair[0]
			y1, y2 = previous_pair[1], xy_pair[1]
			distance_to_add = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
			total_length += distance_to_add
	return total_length
