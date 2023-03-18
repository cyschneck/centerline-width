import math
import logging

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
	except nx.NetworkXNoPath: # no direct path found
		logger.info("No direct path found from starting node to ending node")
		return None
	#nx.draw(graph_connections, with_labels=True, font_size=10)
	return shortest_path

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

def riverWidthFromCenterline(csv_data=None, centerline_coordinates=None, save_to_csv=None, optional_cutoff=None):
	# Return river width: right to center, left to center, total width
	# Width is measured to the bank, relative to the center point (normal of the centerline)
	# { [centerline latitude, centerline longitude] : { rightCenter : distance, leftCenter : distance, totalWidth: distance } }

	centerline_width.errorHandlingRiverWidthFromCenterline(csv_data=csv_data,
															centerline_coordinates=centerline_coordinates,
															save_to_csv=save_to_csv,
															optional_cutoff=optional_cutoff)

	width_dict = {}

	df = pd.read_csv(csv_data)
	if optional_cutoff:
		df = df.head(optional_cutoff)
	left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)
	river_bank_polygon, _, _ = centerline_width.generatePolygon(left_bank_coordinates, right_bank_coordinates)

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
	return width_dict

def riverWidthFromCenterlineCoordinates(csv_data=None, centerline_coordinates=None, save_to_csv=None, optional_cutoff=None):
	# Return the coordinates of the width positions relative to the centerline (latitude/longitude)
	pass
