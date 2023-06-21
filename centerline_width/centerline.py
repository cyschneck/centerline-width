# Built in Python functions
import math
import logging
import csv

# External Python libraries (installed via pip install)
from haversine import haversine
import numpy as np
import networkx as nx
from scipy import interpolate
from shapely.geometry import Point, LineString

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def generateNXGraph(all_points_dict):
	# Generate a NetworkX graph to find the largest graph
	def distanceBetween(start, end):
		lat1 = start[0]
		lat2 = end[0]
		lon1 = start[1]
		lon2 = end[1]
		p = math.pi/180
		a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2
		return math.asin(math.sqrt(a))

	all_connections_in_graph = nx.Graph()
	node_as_keys_pos_values = {}
	for start_point, end_point_list in all_points_dict.items():
		node_as_keys_pos_values[start_point] = (start_point[0], start_point[1])
		all_connections_in_graph.add_node(start_point, pos=(start_point[0], start_point[1]))
		for end_point in end_point_list:
			all_connections_in_graph.add_node(end_point, pos=(end_point[0], end_point[1]))
			node_as_keys_pos_values[end_point] = (end_point[0], end_point[1])
			all_connections_in_graph.add_edge(start_point, end_point, weight=distanceBetween(start_point,end_point))

	components_of_subgraphs = [all_connections_in_graph.subgraph(c).copy() for c in nx.connected_components(all_connections_in_graph)]
	nodes_of_largest_subgraph = []
	for idx, g in enumerate(components_of_subgraphs, start=1):
		if len(g.nodes()) > len(nodes_of_largest_subgraph):
			nodes_of_largest_subgraph = list(g.nodes())
		#print("Subgraph {0}: Nodes: {1}, Edges: {2}".format(idx, len(g.nodes()), len(g.edges())))

	return all_connections_in_graph, nodes_of_largest_subgraph

def networkXGraphShortestPath(nx_graph, starting_node, ending_node):
	# Find the shortest path if it exists
	if starting_node is not None:
		try:
			shortest_path = nx.shortest_path(nx_graph, source=starting_node, target=ending_node)
			logger.info("[SUCCESS] Valid centerline path found")
		except nx.NetworkXNoPath: # no direct path found
			logger.info("[FAILED]  No direct path found from starting node to ending node")
			return None
		#nx.draw(graph_connections, with_labels=True, font_size=10)
		return shortest_path
	else:
		return None

def centerlinePath(river_voronoi, river_polygon, top_polygon_line, bottom_polygon_line):
	# Return the starting node, ending node, all possible paths positions, and all paths starting/end position as a dictionary
	start_end_points_dict = centerline_width.pointsFromVoronoi(river_voronoi, river_polygon) # All possible path connections from Voronoi
	nx_graphs, largest_subgraph_nodes = generateNXGraph(start_end_points_dict)

	x_ridge_point = [] # X position on path
	y_ridge_point = [] # Y poistion on path
	starting_node = None # starting position at the top of the river
	ending_node = None # ending position at the bottom of the river
	for start_point, end_point_list in start_end_points_dict.items():
		if len(end_point_list) > 0: # TESTING TESTING: Show only the end points that have multiple connections (set to 0 during production)
			# Find the starting and ending node based on distance from the top and bottom of the polygon
			if starting_node is None: 
				starting_node = start_point
			else:
				# Only include if starting point node is on the largest subgraph (that represents the centerline)
				if start_point in largest_subgraph_nodes: 
					# if start_point is closer to the top of the polygon than the current starting_node
					if Point(start_point).distance(top_polygon_line) <= Point(starting_node).distance(top_polygon_line):
						starting_node = start_point
			for end_point in end_point_list:
				if ending_node is None: 
					ending_node = end_point
				# Only include if starting point node is on the largest subgraph (that represents the centerline)
				if start_point in largest_subgraph_nodes:
					# if the end_point is closer to the top of the polygon than the current starting_node
					if Point(end_point).distance(top_polygon_line) <= Point(starting_node).distance(top_polygon_line):
						starting_node = end_point
					else:
						# if start_point is closer to the bottom than current ending_node
						if Point(start_point).distance(bottom_polygon_line) <= Point(ending_node).distance(bottom_polygon_line):
							ending_node = start_point
						# if end_point is closer to the bottom than current ending_node
						if Point(end_point).distance(bottom_polygon_line) <= Point(ending_node).distance(bottom_polygon_line):
							ending_node = end_point
				# Save all starting and end positions for all possible paths
				x_ridge_point.append((start_point[0], end_point[0]))
				y_ridge_point.append((start_point[1], end_point[1]))

	if starting_node is None:
		logger.critical("\nCRITICAL ERROR, Polygon too short for the Voronoi diagram generated (no starting node found), unable to plot centerline. Set displayVoronoi=True to view vertices. Can typically be fixed by adding more data to expand range.")
		shortest_path_points = None
	else:
		shortest_path_points = networkXGraphShortestPath(nx_graphs, starting_node, ending_node)

	return starting_node, ending_node, x_ridge_point, y_ridge_point, shortest_path_points

def evenlySpacedCenterline(centerline_coordinates=None, number_of_fixed_points=None):
	# Interpolate to evenly space points along the centerline coordinates (effectively smoothing with fewer points)
	if centerline_coordinates is None:
		return None

	centerline_line = LineString(centerline_coordinates)

	# Splitting into a fixed number of points
	distances_evenly_spaced = np.linspace(0, centerline_line.length, number_of_fixed_points)
	points_evenly_spaced = [centerline_line.interpolate(distance) for distance in distances_evenly_spaced]

	# Convert Shapley Points to a List of Tuples (coordinates)
	interpolated_centerline_coordinates = []
	for point in points_evenly_spaced:
		interpolated_centerline_coordinates.append((point.x, point.y))

	return interpolated_centerline_coordinates

def smoothedCoordinates(river_object=None, centerline_coordinates=None, interprolate_num=None):
	# return a list coordinates after applying b-spline (smoothing)
	if centerline_coordinates is None:
		return None

	x_coordinates = []
	y_coordinates = []

	# splitting centerline coordinaets into an x and y component
	for centerline_point in centerline_coordinates:
		x_coordinates.append(centerline_point[0])
		y_coordinates.append(centerline_point[1])

	# applying a path smoothing spline
	smoothed_coordinates = []
	tck, *rest = interpolate.splprep([x_coordinates, y_coordinates], s=0.000001) # spline prep, tck = knots - coefficeinets - degree
	u = np.linspace(0, 1, interprolate_num) # number of steps between each point (to determine smoothness)
	x_smoothed, y_smoothed =  interpolate.splev(u, tck) # interpolated list of points

	x_smoothed, y_smoothed = x_smoothed.tolist(), y_smoothed.tolist() # convert array to list
	smoothed_coordinates = list(zip(x_smoothed, y_smoothed))

	# Check if smoothed centerline lies outside polygon
	points_outside_polygon = 0
	for centerline_point in smoothed_coordinates:
		if not river_object.bank_polygon.contains(Point(centerline_point)):
			points_outside_polygon += 1
	if points_outside_polygon > 2:
		logger.critical("\nWARNING: Partially invalid smoothed centerline due to sparse centerline data ({0} points lie outside the polygon), fix recommendation: rerun riverCenterline to create river object with interpolate_n_centerpoints set to {1}+\n".format(points_outside_polygon, round(len(centerline_coordinates)*2.5)))

	return smoothed_coordinates

def riverWidthFromCenterlineCoordinates(river_object=None,
										centerline_coordinates=None,
										transect_span_distance=3,
										remove_intersections=False,
										save_to_csv=None):
	# Return the left/right coordinates of width centerlines
	right_width_coordinates = {}
	left_width_coordinates = {}
	num_intersection_coordinates = {}
	x = []
	y = []

	# Average slopes for every n points to chart
	centerline_slope = {}
	groups_of_n_points = [centerline_coordinates[i:i+transect_span_distance] for i in range(0, len(centerline_coordinates), transect_span_distance)]
	for group_points in groups_of_n_points:
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
			middle_of_list = len(group_points) // 2 # set centerline point to be the middle point being averaged
			centerline_slope[group_points[middle_of_list]] = normal_of_slope

	def intersectsTopOrBottomOfBank(point1, point2):
		# returns True/False if the points lie on the 'false' top/bottom of the river
		points_intersect_false_edges = False
		# avoiding floating point precession errors when determining if point lies within the line
		# if point is within a small distance of a line it is considered to intersect
		if river_object.top_bank.distance(point1) < 1e-8 or river_object.bottom_bank.distance(point1) < 1e-8:
			points_intersect_false_edges = True
		if river_object.top_bank.distance(point2) < 1e-8 or river_object.bottom_bank.distance(point2) < 1e-8:
			points_intersect_false_edges = True
		return points_intersect_false_edges

	# Generate a list of lines from the centerline point with its normal
	min_x, min_y, max_x, max_y = river_object.bank_polygon.bounds
	for centerline_point, slope in centerline_slope.items():
		# draw a max line that extends the entire distance of the available space, will be trimmed below to just within polygon
		left_y = slope * (min_x - centerline_point[0]) + centerline_point[1]
		right_y = slope * (max_x - centerline_point[0]) + centerline_point[1]

		# Save the points where they intersect the polygon
		sloped_line = LineString([(min_x, left_y), (max_x, right_y)]) # sloped line from the centerpoint
		line_intersection_points = river_object.bank_polygon.exterior.intersection(sloped_line) # points where the line intersects the polygon
		# if the line only intersects in two places (does not intersect polygon any additional times)
		if len(line_intersection_points.geoms) == 2:
			 # only save width lines that do not touch the artifical top/bottom
			if not intersectsTopOrBottomOfBank(line_intersection_points.geoms[0], line_intersection_points.geoms[1]):
				left_width_coordinates[centerline_point] = (line_intersection_points.geoms[0].x, line_intersection_points.geoms[0].y)
				right_width_coordinates[centerline_point] = (line_intersection_points.geoms[1].x, line_intersection_points.geoms[1].y)
		else:
			# line intersects to polygon at multiple points, by default, find the closest two points to chart
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

				# Verify linestring contains the centerline (avoid making connections outside of polygon)
				linestring_generated = LineString([Point(smallest_point.x, smallest_point.y), Point(second_smallest_point.x, second_smallest_point.y)])
				if not linestring_generated.distance(Point(centerline_point)) < 1e-8: 
					# linestring does not contains the centerline
					# find a new second_smallest_point that falls on the centerline
					for i in index_of_sorted_list: # search for new point in order of distance (smallest -> greatest)
						second_smallest_point = line_intersection_points.geoms[index_of_sorted_list[i]]
						linestring_generated = LineString([Point(smallest_point.x, smallest_point.y), Point(second_smallest_point.x, second_smallest_point.y)])
						if smallest_point != second_smallest_point: # ignore current smallest_point (make a unique pair)
							if linestring_generated.distance(Point(centerline_point)) < 1e-8: # if point is within a small distance of a line it is considered to intersect
								break # once a linestring is found that lies within polygon, break out of search early

				# linestring contains the centerline, save coordinates
				left_width_coordinates[centerline_point] = (smallest_point.x, smallest_point.y)
				right_width_coordinates[centerline_point] = (second_smallest_point.x, second_smallest_point.y)

	# Determine lines that intersect with other lines in mulitple places to flag/remove
	all_linestrings = []
	linestring_with_centerlines = {} # linestring with associated centerline: {linestring : centerline coordinate}
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
					if str(intersection_points_linestrings) != "LINESTRING Z EMPTY": # if linestring has intersect (not empty), increment count
						num_intersection_coordinates[linestring_with_centerlines[linestring_to_check]] += 1
						if linestring_to_check not in linestring_with_linestrings_that_intersect.keys():
							linestring_with_linestrings_that_intersect[linestring_to_check] = []
						linestring_with_linestrings_that_intersect[linestring_to_check].append(linestring_to_check_against)

	# Remove Intersection Lines
	centerline_coordinates_to_be_removed = []
	if remove_intersections:
		logger.info("[PROCESSING] Recursively removing intersection lines...")
		# iterate from the most intersections to the least intersections
		for linestring_most_interactions in sorted(linestring_with_linestrings_that_intersect, key=lambda k: len(linestring_with_linestrings_that_intersect[k]), reverse=True):

			# when number of intersections > 1, remove lines with the most interactions to the smallest
			if num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] > 1: 
				lst_linestrings_hit_by_linestring = linestring_with_linestrings_that_intersect[linestring_most_interactions]

				# iterate through each and remove linestring from the associated lists of places it intersects
				for linestring_hit in lst_linestrings_hit_by_linestring: 
					# remove linestring with most intersections from all linestrings that it hits
					linestring_with_linestrings_that_intersect[linestring_hit].remove(linestring_most_interactions)
					# decrease intersections by 1 after removing linestring, from both the linestring and the places it intersects
					num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] -= 1
					num_intersection_coordinates[linestring_with_centerlines[linestring_hit]] -= 1

				# remove linestring that intersects the most linestrings
				centerline_of_removed_line = linestring_with_centerlines[linestring_most_interactions]
				if centerline_of_removed_line not in centerline_coordinates_to_be_removed: centerline_coordinates_to_be_removed.append(centerline_of_removed_line)

			# if two linestring both have one intersection (with just eachother), remove the longer width line
			if num_intersection_coordinates[linestring_with_centerlines[linestring_most_interactions]] == 1: 
				linestring_1 = linestring_most_interactions
				linestring_2 = linestring_with_linestrings_that_intersect[linestring_most_interactions][0]
				# remove linestring that is longer
				if linestring_1.length >= linestring_2.length:
					centerline_of_removed_line = linestring_with_centerlines[linestring_1]
				else:
					centerline_of_removed_line = linestring_with_centerlines[linestring_2]
				if centerline_of_removed_line not in centerline_coordinates_to_be_removed: centerline_coordinates_to_be_removed.append(centerline_of_removed_line)
				# decrease intersecetions by 1 after removing linestring, from both the linestring and the places it intersects
				num_intersection_coordinates[linestring_with_centerlines[linestring_1]] -= 1
				num_intersection_coordinates[linestring_with_centerlines[linestring_2]] -= 1

		# Delete all width lines that have been flagged for removal
		for centerline_coord in centerline_coordinates_to_be_removed:
			del right_width_coordinates[centerline_coord]
			del left_width_coordinates[centerline_coord]
		logger.info("[SUCCESS] Intersection lines removed")

	return right_width_coordinates, left_width_coordinates, num_intersection_coordinates

def riverWidthFromCenterline(river_object=None,
							transect_span_distance=3,
							apply_smoothing=True,
							remove_intersections=False,
							units="km",
							save_to_csv=None):
	# Return river width: centerline and width at centerline
	# Width is measured to the bank, relative to the center point (normal of the centerline)
	# { [centerline latitude, centerline longitude] : widthValue }

	centerline_width.errorHandlingRiverWidthFromCenterline(river_object=river_object,
															transect_span_distance=transect_span_distance,
															apply_smoothing=apply_smoothing,
															remove_intersections=remove_intersections,
															units=units,
															save_to_csv=save_to_csv)

	if river_object.centerlineVoronoi is None:
		logger.critical("\nCRITICAL ERROR, unable to find width without a valid centerline")
		return None

	# recreate the centerline with evenly spaced points
	defined_centerline_coordinates = centerline_width.evenlySpacedCenterline(centerline_coordinates=river_object.centerlineVoronoi,
																			number_of_fixed_points=river_object.interpolate_n_centerpoints)
	if apply_smoothing:
		defined_centerline_coordinates = centerline_width.smoothedCoordinates(river_object=river_object,
																				centerline_coordinates=river_object.centerlineVoronoi,
																				interprolate_num=river_object.interpolate_n_centerpoints)
	# if using smoothing, replace left/right coordinates with the smoothed variation
	right_width_coord, left_width_coord, _ = centerline_width.riverWidthFromCenterlineCoordinates(river_object=river_object, 
																								centerline_coordinates=defined_centerline_coordinates,
																								transect_span_distance=transect_span_distance,
																								remove_intersections=remove_intersections)

	width_dict = {}
	for centerline_coord, _ in right_width_coord.items():
		# store the haversine distance between the lat/lon position of the right/left bank
		lon1, lat1 = right_width_coord[centerline_coord]
		lon2, lat2 = left_width_coord[centerline_coord]
		haversine_distance_between_right_and_left = haversine((lat1, lon1), (lat2, lon2), unit=units)
		width_dict[centerline_coord] = haversine_distance_between_right_and_left

	# Save width dictionary to a csv file (Latitude, Longtiude, Width)
	if save_to_csv:
		with open(save_to_csv, "w") as csv_file_output:
			writer = csv.writer(csv_file_output)
			writer.writerow(["Centerline Latitude (Deg)", "Centerline Longitude (Deg)", "Width ({0})".format(units)])
			for coordinate_key, width_value in width_dict.items():
				writer.writerow([coordinate_key[1], coordinate_key[0], width_value])

	return width_dict

def centerlineLength(centerline_coordinates=None):
	# Return the length/distance for all the centerline coordaintes in km
	total_length = 0
	previous_pair = None
	if centerline_coordinates is None:
		return 0

	for xy_pair in centerline_coordinates:
		if previous_pair is None:
			previous_pair = xy_pair
		else:
			lon1, lon2 = previous_pair[0], xy_pair[0]
			lat1, lat2 = previous_pair[1], xy_pair[1]
			distance_to_add = haversine((lat1, lon1), (lat2, lon2), unit="km")
			total_length += distance_to_add
	return total_length

def saveCenterlineCSV(river_object=None, save_to_csv=None, centerline_type="Voronoi"):
	# Save Centerline Coordinates generated by Voronoi Diagram to CSV
	centerline_width.errorHandlingSaveCenterlineCSV(river_object=river_object, save_to_csv=save_to_csv, centerline_type=centerline_type)
	centerline_type = centerline_type.title()

	if centerline_type == "Voronoi": centerline_coordinates_by_type = river_object.centerlineVoronoi
	if centerline_type == "Evenly Spaced": centerline_coordinates_by_type = river_object.centerlineEvenlySpaced
	if centerline_type == "Smoothed": centerline_coordinates_by_type = river_object.centerlineSmoothed

	with open(save_to_csv, "w") as csv_file_output:
		writer = csv.writer(csv_file_output)
		writer.writerow(["{0} Centerline Latitude (Deg)".format(centerline_type), "{0} Centerline Longitude (Deg)".format(centerline_type)])
		if centerline_coordinates_by_type is not None:
			for latitude_longitude in centerline_coordinates_by_type:
				writer.writerow([latitude_longitude[1], latitude_longitude[0]])
		else:
			logger.warn("\nWARNING, no {0} centerline coordinates found, {1} file generated will be empty".format(centerline_type, save_to_csv))
