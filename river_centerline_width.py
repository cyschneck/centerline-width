# Find the center point and width between latitude/longitude points along right/left river bank
import math
import csv
from collections import Counter
import logging

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Point, Polygon, LineString

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

########################################################################
def convertColumnsToCSV(text_file=None, flipBankDirection=False):
	# Convert txt file to a comma seperated version of the file to use in pandas
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
	for index, row in df.iterrows():
		if not math.isnan(row.rlat) and not math.isnan(row.rlon):
			right_bank_coordinates.append([row.rlon, row.rlat])
		if not math.isnan(row.llat) and not math.isnan(row.llon):
			left_bank_coordinates.append([row.llon, row.llat])
	return left_bank_coordinates, right_bank_coordinates

########################################################################
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
		logger.critical("Invalid Polygon needs to be corrected")

	return river_polygon, top_river, bottom_river

def generateVoronoi(left_bank_lst, right_bank_lst):
	# Generate a Voronoi shape based on the left/right bank points
	all_banks_points = left_bank_lst + right_bank_lst
	all_banks_points = np.array(all_banks_points)

	river_voronoi = Voronoi(all_banks_points)
	return river_voronoi

def pointsFromVoronoi(river_voronoi, river_polygon):
	# Returns a dictionary list of all the voronoi points: {start point : [list of end points]}
	points_dict = {}
	all_connections_start_to_end = []
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

def centerlinePath(river_voronoi, river_polygon, top_polygon_line, bottom_polygon_line):
	# Return the starting node, ending node, and centerline path
	start_end_points_dict = pointsFromVoronoi(river_voronoi, river_polygon)
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
		return None
	#nx.draw(graph_connections, with_labels=True, font_size=10)
	return shortest_path
########################################################################
def centerlineLatitudeLongitude(river_df=None):
	# Returns the latitude and longitude for the centerline
	left_bank_coordinates, right_bank_coordinates = leftRightCoordinates(river_df)

	river_bank_polygon, top_river_line, bottom_river_line = generatePolygon(left_bank_coordinates, right_bank_coordinates)
	river_bank_voronoi = generateVoronoi(left_bank_coordinates, right_bank_coordinates)

	starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict = centerlinePath(river_bank_voronoi, river_bank_polygon, top_river_line, bottom_river_line)
	shortest_path_coordinates = networkXGraphShortestPath(start_end_points_dict, starting_node, ending_node)

	return shortest_path_coordinates

def plotRiver(river_df=None, display_all_paths=False, save_plot_name=None):
	# display_all_paths: display all possible paths (not just centerline) (useful for debugging)
	# Plot river
	left_bank_coordinates, right_bank_coordinates = leftRightCoordinates(river_df)
	river_bank_polygon, top_river_line, bottom_river_line = generatePolygon(left_bank_coordinates, right_bank_coordinates)
	river_bank_voronoi = generateVoronoi(left_bank_coordinates, right_bank_coordinates)

	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(10,10))
	ax = fig.add_subplot(111)
	
	# Isolate center line:
	# Plot the ridge edges of the Voronoi polygons that lie within the river banks
	# Find the start and ending node to find the centerline
	starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict = centerlinePath(river_bank_voronoi,
																									river_bank_polygon, 
																									top_river_line, 
																									bottom_river_line)

	# Plot River as a Polygon
	plt.plot(*river_bank_polygon.exterior.xy, c="gainsboro")
	plt.plot(*top_river_line.xy, c="forestgreen")
	plt.plot(*bottom_river_line.xy, c="lightcoral")

	#voronoi_plot_2d(river_bank_voronoi, show_points=True, point_size=1, ax=ax)

	# Dynamically assign the starting and ending
	plt.scatter(starting_node[0], starting_node[1], c="green", label="Starting Node")
	plt.scatter(ending_node[0], ending_node[1], c="red", label="Ending Node")

	# Plot all possible paths with text for positions
	if display_all_paths or not river_bank_polygon.is_valid: # display paths if polygon is not valid (debugging purposes)
		for i in range(len(x_ridge_point)):
			plt.plot(x_ridge_point[i], y_ridge_point[i], 'cyan', linewidth=1)
			# Plot (X, Y) positions as text
			#ax.text(x=x_ridge_point[i][0], y=y_ridge_point[i][0], s="{0}, {1}".format(x_ridge_point[i][0], y_ridge_point[i][0]))
			#ax.text(x=x_ridge_point[i][1], y=y_ridge_point[i][1], s="{0}, {1}".format(x_ridge_point[i][1], y_ridge_point[i][1]))

	# Plot colored river bank (including extrapolations) between known points
	scatter_plot_size = 4
	x = []
	y = []
	for i in right_bank_coordinates: 
		x.append(i[0])
		y.append(i[1])
	plt.scatter(x, y, c="dodgerblue", s=scatter_plot_size, label="Right Bank")
	x = []
	y = []
	for i in left_bank_coordinates: 
		x.append(i[0])
		y.append(i[1])
	plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank")

	# Find centerline from NetworkX
	shortest_path_points = networkXGraphShortestPath(start_end_points_dict, starting_node, ending_node)
	valid_path_through = False
	if shortest_path_points:
		valid_path_through = True
		plt.plot(*zip(*shortest_path_points), c="black", label="Centerline")

	plt.title("River Coordinates: Valid Centerline = {0}, Valid Polygon = {1}".format(valid_path_through, river_bank_polygon.is_valid))
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	fig.savefig(save_plot_name)

def riverWidthFromCenterline(river_df=None, centerline_coordinates=None, save_to_csv=None):
	# Return river width: right to center, left to center, total width
	width_dict = {}

	left_bank_coordinates, right_bank_coordinates = leftRightCoordinates(river_df)
	river_bank_polygon, top_river_line, bottom_river_line = generatePolygon(left_bank_coordinates, right_bank_coordinates)

	if save_to_csv:
		headers = ["Right-Center Width", "Left-Center Width", "Total Width"]
		#total_rows = []
		#total_rows.append(row + right_rows[i])

		#write_file_name = text_file.split(".")[0] + ".csv"
		#with open(write_file_name, "w") as f:
		#	write = csv.writer(f)
		#	write.writerow(header_fields)
		#	write.writerows(total_rows)

	return width_dict

########################################################################
if __name__ == "__main__":
	convertColumnsToCSV(text_file="data/river_coords.txt", flipBankDirection=True)
	df = pd.read_csv("data/river_coords.csv")
	# Valid Examples
	#df = df.head(15) # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#df = df.head(100) # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	df = df.head(550) # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	# Invalid Examples
	#df = df.head(250) # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
	#df = df.head(40) # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#df = df.head(700) # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#df = df.head(1000) # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

	# Return the latitude/longtiude coordinates for the centerline
	#centerline_longitude_latitude_coordinates = centerlineLatitudeLongitude(river_df=df)

	# Plot river banks
	plotRiver(river_df=df, save_plot_name="data/river_coords.png", display_all_paths=False)

	# Return the width of the river for each centerline vertex (distance from right, left, total)
	#river_width_dict = riverWidthFromCenterline(river_df=df, centerline_coordinates=centerline_longitude_latitude_coordinates, save_to_csv="data/river_width.csv")
