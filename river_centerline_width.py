# Find the center point and width between lat/long points along river bank
# Modified from R - CMGO code functionality
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

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

def plotRiver(river_df, 
			latitude_extrapolation, longitude_extrapolation, 
			right_bank_nearest_neighbor_x, right_bank_nearest_neighbor_y,
			left_bank_nearest_neighbor_x, left_bank_nearest_neighbor_y,
			right_bank_expanded, left_bank_expanded,
			save_plot_name):
	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(12,12), dpi=100)

	
	x = []
	y = []
	for i in right_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="orange", s=1, label="Right Bank Extrapolation")
	x = []
	y = []
	for i in left_bank_expanded: 
		x.append(i[1])
		y.append(i[0])
	plt.scatter(x, y, c="dodgerblue", s=1, label="Left Bank Extrapolation")

	plt.scatter(x=river_df['llon'], y=river_df['llat'], s=0.5, c="black")
	plt.scatter(x=river_df['rlon'], y=river_df['rlat'], s=0.5, c="black")


	plt.plot(right_bank_nearest_neighbor_x, right_bank_nearest_neighbor_y, c="red", linewidth=0.5, label="Right -> Left Bank Nearest Neighbor")
	plt.plot(left_bank_nearest_neighbor_x, left_bank_nearest_neighbor_y, c="green", linewidth=0.5, label="Left -> Right Bank Nearest Neighbor")

	plt.title("River Coordinates")
	plt.xlabel("Longitude")
	plt.ylabel("Latitude")
	plt.legend()
	plt.show()
	fig.savefig(save_plot_name)

########################################################################
if __name__ == "__main__":
	#convertColumnsToCSV("data/river_coords.txt")
	df = pd.read_csv("data/river_coords.csv")
	#df = df.head(310)
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

	# Add points between existing points to increase closest neighbors
	def expand_list(lst, expand_n):
		bank_expanded = []
		for i in range(len(lst)):
			bank_expanded.append(lst[i])
			if i+1 < len(lst):
				x_expand = np.linspace(lst[i][0], lst[i+1][0], expand_n)
				y_expand = np.linspace(lst[i][1], lst[i+1][1], expand_n)
				for j in range(len(x_expand)):
					bank_expanded.append([x_expand[j],y_expand[j]])
				bank_expanded.append(lst[i+1])
		return bank_expanded

	additional_points_between_each_pair = 10
	right_bank_expanded = expand_list(right_bank_pairs, additional_points_between_each_pair)
	left_bank_expanded =  expand_list(left_bank_pairs, additional_points_between_each_pair)

	# Search for closest value in list of lists (KNN)
	from scipy import spatial
	# Closest neighbors to the right bank
	plot_every_n = 100
	right_bank_nearest_neighbor_x = []
	right_bank_nearest_neighbor_y = [] # closest left pair
	tree = spatial.KDTree(np.array(left_bank_expanded))
	for right_pair in right_bank_pairs[::plot_every_n]:
		distances, index = tree.query(right_pair)
		closest_left_pair = list(tree.data[index])
		right_bank_nearest_neighbor_x.append(right_pair[1])
		right_bank_nearest_neighbor_x.append(closest_left_pair[1])
		right_bank_nearest_neighbor_y.append(right_pair[0])
		right_bank_nearest_neighbor_y.append(closest_left_pair[0])

	#Closest neighbors to the left bank
	left_bank_nearest_neighbor_x = []
	left_bank_nearest_neighbor_y = [] # closest right pair
	tree = spatial.KDTree(np.array(right_bank_expanded))
	for left_pair in left_bank_pairs[::plot_every_n]:
		distances, index = tree.query(left_pair)
		closest_right_pair = list(tree.data[index])
		left_bank_nearest_neighbor_x.append(left_pair[1])
		left_bank_nearest_neighbor_x.append(closest_right_pair[1])
		left_bank_nearest_neighbor_y.append(left_pair[0])
		left_bank_nearest_neighbor_y.append(closest_right_pair[0])

	# Plot river banks
	plotRiver(df, latitude_points, longitude_points,
			right_bank_nearest_neighbor_x, right_bank_nearest_neighbor_y,
			left_bank_nearest_neighbor_x, left_bank_nearest_neighbor_y,
			right_bank_expanded, left_bank_expanded,
			 "data/river_coords.png")
