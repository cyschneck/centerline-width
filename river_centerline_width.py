# Find the center point and width between lat/long points along river bank
import math
import csv

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
		exit()

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

########################################################################

def plotRiver(river_df, 
			latitude_extrapolation, longitude_extrapolation,
			right_bank_expanded, left_bank_expanded,
			river_bank_polygon, river_bank_voronoi,
			save_plot_name):

	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(15,15))
	ax = fig.add_subplot(111)

	#plt.scatter(x=river_df['llon'], y=river_df['llat'], s=0.5, c="darkgrey")
	#plt.scatter(x=river_df['rlon'], y=river_df['rlat'], s=0.5, c="darkgrey")

	# Plot Voronoi Polygons
	
	vertices_x, vertices_y = voronoiVerticesWithinPolygon(river_bank_polygon, river_bank_voronoi)
	plt.scatter(vertices_x, vertices_y, c="red", s=1, label="Voronoi Vertices (Within River)")
	#voronoi_plot_2d(river_bank_voronoi, show_points=True, point_size=1, ax=ax) #TODO

	# Isolate center line:
	# Plot the ridge edges of the Voronoi polygons that lie within the river banks
	for vpair in river_bank_voronoi.ridge_vertices:
		if vpair[0] >= 0 and vpair[1] >= 0:
			v0 = river_bank_voronoi.vertices[vpair[0]]
			v1 = river_bank_voronoi.vertices[vpair[1]]
			if river_bank_polygon.contains(Point([v0[1], v0[0]])) and river_bank_polygon.contains(Point([v1[1], v1[0]])):
				plt.plot([v0[1], v1[1]], [v0[0], v1[0]], 'black', linewidth=1)

	# Plot River as a Polygon
	plt.plot(*river_bank_polygon.exterior.xy, c="silver")
	#ax.add_patch(mat_poly(right_bank_expanded+left_bank_expanded, closed=True, facecolor='red'))

	# Plot colored extrapolations between known points
	scatter_plot_size = 3
	x = []
	y = []
	for i in right_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="dodgerblue", s=scatter_plot_size, label="Right Bank Extrapolation")
	x = []
	y = []
	for i in left_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank Extrapolation")

	plt.title("River Coordinates: Area = {0}".format(river_bank_polygon.area*111139))
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend()
	plt.show()
	fig.savefig(save_plot_name)

########################################################################
if __name__ == "__main__":
	#convertColumnsToCSV("data/river_coords.txt")
	df = pd.read_csv("data/river_coords.csv")
	df = df.head(500)
	#df = df.loc[100:510]

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
	#print(voronoi_river.vertices)
	#print(voronoi_river.ridge_points)
	#print(voronoi_river.ridge_dict)

	# Plot river banks
	plotRiver(df, latitude_points, longitude_points,
			right_bank_expanded, left_bank_expanded,
			polygon_river, voronoi_river,
			 "data/river_coords.png")
