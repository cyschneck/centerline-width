# Find the center point and width between lat/long points along river bank
import math
import csv
from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as mat_poly
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Point, Polygon

########################################################################

def convertColumnsToCSV(text_file):
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
	right_rows = right_rows[::-1]

	total_rows = []
	for i, row in enumerate(left_rows):
		total_rows.append(row + right_rows[i])

	write_file_name = text_file.split(".")[0] + ".csv"
	with open(write_file_name, "w") as f:
		write = csv.writer(f)
		write.writerow(header_fields)
		write.writerows(total_rows)

########################################################################

def expand_list(lst, expand_n):
	# Add points between existing points to increase closest neighbors
	expand_n += 2 # Add two points, to account for the start/end point
	bank_expanded = []
	for i in range(len(lst)):
		if i+1 < len(lst):
			x_expand = np.linspace(lst[i][0], lst[i+1][0], expand_n)
			y_expand = np.linspace(lst[i][1], lst[i+1][1], expand_n)
			for j in range(len(x_expand)):
				bank_expanded.append([x_expand[j],y_expand[j]])
			bank_expanded.append(lst[i+1])
		else: 
			bank_expanded.append(lst[i])
	return bank_expanded

def generatePolygon(left_bank_lst, right_bank_lst):
	# Return a shapely polygon based on the position of the river bank points
	circular_list_of_banks = left_bank_lst + right_bank_lst[::-1] + [left_bank_lst[0]]

	bank_points_swapped = []
	for i, bank_point in enumerate(circular_list_of_banks):
		bank_points_swapped.append([bank_point[1], bank_point[0]]) # Swap the x and y to graph with longitude on the y-axis

	river_polygon = Polygon(bank_points_swapped)

	if not river_polygon.is_valid:
		print("Invalid Polygon needs to be corrected")
		#exit()

	return river_polygon

def generateVoronoi(left_bank_lst, right_bank_lst):
	# Generate a Voronoi shape based on the left/right bank points
	all_banks_points = left_bank_lst + right_bank_lst
	all_banks_points = np.array(all_banks_points)

	river_voronoi = Voronoi(all_banks_points)
	#vor_vertices = vor.vertices # Voronoi vertices
	#vor_regions = vor.regions  # Voronoi regions: each sub-list contains coordiantes for the regions
	return river_voronoi

def voronoiVerticesWithinPolygon(bank_polygon, bank_voronoi):
	# Return two lists of points that are contained within the polygon
	x_points_within = []
	y_points_within = []
	#TODO: improve run time by removing values that are exceptionally large/small
	for vertex_point in bank_voronoi.vertices:
		if bank_polygon.contains(Point([vertex_point[1], vertex_point[0]])):
			x_points_within.append(vertex_point[1])
			y_points_within.append(vertex_point[0])
	return x_points_within, y_points_within

def networkXGraph(all_points_dict, starting_node, ending_node):
	def distanceBetween(start, end):
		lat1 = start[1]
		lat2 = end[1]
		lon1 = start[0]
		lon2 = end[0]
		p = math.pi/180
		a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2
		return math.asin(math.sqrt(a))

	g = nx.Graph()
	node_as_keys_pos_values = {}
	for start_point, end_point_list in all_points_dict.items():
		node_as_keys_pos_values[start_point] = (start_point[0], start_point[1])
		g.add_node(start_point, pos=(start_point[0], start_point[1]))
		#print(start_point)
		for end_point in end_point_list:
			#print(end_point)
			g.add_node(end_point, pos=(end_point[0], end_point[1]))
			node_as_keys_pos_values[end_point] = (end_point[0], end_point[1])
			g.add_edge(start_point, end_point, weight=distanceBetween(start_point,end_point))
		#print("\n")
	try:
		shortest_path = nx.shortest_path(g, source=starting_node, target=ending_node)
	except nx.NetworkXNoPath:
		return None
	return shortest_path


########################################################################

def plotRiver(river_df, print_all_paths,
			latitude_extrapolation, longitude_extrapolation,
			right_bank_expanded, left_bank_expanded,
			river_bank_polygon, river_bank_voronoi,
			save_plot_name):

	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(10,10))
	ax = fig.add_subplot(111)

	# Plot Voronoi Polygons
	vertices_x, vertices_y = voronoiVerticesWithinPolygon(river_bank_polygon, river_bank_voronoi)
	plt.scatter(vertices_x, vertices_y, c="red", s=2, label="Voronoi Vertices (Within River)") # TODO: replace with final ridge points that are within the polygon and along the centerline
	#voronoi_plot_2d(river_bank_voronoi, show_points=True, point_size=1, ax=ax)

	# Isolate center line:
	# Plot the ridge edges of the Voronoi polygons that lie within the river banks
	points_dict = {}
	all_connections_start_to_end = []
	for ridge_vertex_point in river_bank_voronoi.ridge_vertices:
		if ridge_vertex_point[0] >= 0 and ridge_vertex_point[1] >= 0:
			v0 = river_bank_voronoi.vertices[ridge_vertex_point[0]]
			v1 = river_bank_voronoi.vertices[ridge_vertex_point[1]]
			# Check if start and end points are within the polygon, otherwise remove the connection pair
			if river_bank_polygon.contains(Point([v0[1], v0[0]])) and river_bank_polygon.contains(Point([v1[1], v1[0]])):
				start_point = tuple([v0[1], v0[0]])
				end_point = tuple([v1[1], v1[0]])
				start_to_end = [start_point, end_point]
				if start_to_end not in all_connections_start_to_end: 
					all_connections_start_to_end.append(start_to_end)

	connections_counter_start_to_end = Counter(x for xs in all_connections_start_to_end for x in set(xs))
	# Plot the connections
	for connection in all_connections_start_to_end:
		start_point = connection[0]
		end_point = connection[1]
		# Only plot points with at least two connections
		if connections_counter_start_to_end[start_point] > 1:
			if connections_counter_start_to_end[end_point] > 1: 
				#print("Start : {0} - {1}".format(start_point[0], connections_counter_start_to_end[start_point]))
				#print("End   : {0} - {1}".format(end_point[0], connections_counter_start_to_end[end_point]))
				if start_point not in points_dict.keys():
					points_dict[start_point] = []
				points_dict[start_point].append(end_point)
				
	x_ridge_point = []
	y_ridge_point = []
	starting_node = None
	ending_node = None
	for start_point, end_point_list in points_dict.items():
		if starting_node is None: starting_node = start_point
		else:
			if start_point[1] > starting_node[1]:
				starting_node = start_point
		#print(start_point)
		#print(end_point_list)
		for end_point in end_point_list:
			if len(end_point_list) > 0:
				if ending_node is None: ending_node = end_point
				else:
					if end_point[1] < ending_node[1]:
						ending_node = end_point
					if start_point[1] < ending_node[1]:
						ending_node = start_point
				x_ridge_point.append([start_point[0], end_point[0]])
				y_ridge_point.append([start_point[1], end_point[1]])

	# Dynamically assign the starting and ending
	plt.scatter(starting_node[0], starting_node[1], c="green", label="Starting Node")
	plt.scatter(ending_node[0], ending_node[1], c="purple", label="Ending Node")

	# Plot River as a Polygon
	plt.plot(*river_bank_polygon.exterior.xy, c="silver")
	#ax.add_patch(mat_poly(right_bank_expanded+left_bank_expanded, closed=True, facecolor='red'))

	if print_all_paths or not river_bank_polygon.is_valid:
		for i in range(len(x_ridge_point)):
			plt.plot(x_ridge_point[i], y_ridge_point[i], 'cyan', linewidth=1)
			# Plot (X, Y) positions as text
			#ax.text(x=x_ridge_point[i][0], y=y_ridge_point[i][0], s="{0}, {1}".format(x_ridge_point[i][0], y_ridge_point[i][0]))
			#ax.text(x=x_ridge_point[i][1], y=y_ridge_point[i][1], s="{0}, {1}".format(x_ridge_point[i][1], y_ridge_point[i][1]))


	# Plot colored river bank (including extrapolations) between known points
	scatter_plot_size = 3
	x = []
	y = []
	for i in right_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="dodgerblue", s=scatter_plot_size, label="Right Bank")
	x = []
	y = []
	for i in left_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank")

	shortest_path_points = networkXGraph(points_dict, starting_node, ending_node)
	valid_path_through = False
	if shortest_path_points:
		valid_path_through = True
		plt.plot(*zip(*shortest_path_points), c="black", label="Shortest Path (Centerline)")

	plt.title("River Coordinates: Valid Path = {0}, Valid Polygon = {1}".format(valid_path_through, river_bank_polygon.is_valid))
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.tight_layout()
	plt.show()
	fig.savefig(save_plot_name)

########################################################################
if __name__ == "__main__":
	convertColumnsToCSV("data/river_coords.txt")
	df = pd.read_csv("data/river_coords.csv")
	#df = df.head(10) # valid path, valid polygon, correct centerline
	#df = df.head(40) # valid path, valid polgyon, correct centerline
	#df = df.head(100) # valid path, valid polygon, but incorrect centerline
	df = df.head(550) # valid path, valid polygon, but incorrect centerline
	#df = df.head(250) # valid path, invalid polygon, so incorrect centerline
	#df = df.head(700) # invalid path, valid polgyon, so incorrect centerline

	# Lines between points on graph
	latitude_points = []
	longitude_points = []
	right_bank_pairs = [] # without nan
	left_bank_pairs = [] # wtihout nan
	for index, row in df.iterrows():
		latitude_points.append([row.llat, row.rlat])
		longitude_points.append([row.llon, row.rlon])
		if not math.isnan(row.rlat) and not math.isnan(row.rlon):
			right_bank_pairs.append([row.rlat, row.rlon])
		if not math.isnan(row.llat) and not math.isnan(row.llon):
			left_bank_pairs.append([row.llat, row.llon])

	# Add points between existing bank points
	additional_points_between_each_pair = 0 # User defined: 0 only uses the original points
	right_bank_expanded = expand_list(right_bank_pairs, additional_points_between_each_pair)
	left_bank_expanded =  expand_list(left_bank_pairs, additional_points_between_each_pair)

	# Set up a polygon based on the left and right bank
	polygon_river = generatePolygon(left_bank_expanded, right_bank_expanded)

	# Set up Vornoi based on the left and right bank
	voronoi_river = generateVoronoi(left_bank_expanded, right_bank_expanded)

	# Plot river banks
	print_all_paths = True # print all possible paths (not just centerline) in cyan
	plotRiver(df, print_all_paths, latitude_points, longitude_points,
			right_bank_expanded, left_bank_expanded,
			polygon_river, voronoi_river,
			 "data/river_coords.png")
