# Find the center point and width between lat/long points along river bank
# Modified from R - CMGO code functionality
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

def convertColumnsToCSV(text_file):
	# Convert txt file to a comma seperated version of the file to use in pandas
	rows = []
	with open(text_file) as input_file:
		lines = input_file.readlines()
		for i, line in enumerate(lines):
			line = line.strip().split(" ")
			line = [x for x in line if x != '']
			if i == 0:
				header_fields = line
			else:
				rows.append(line)

	write_file_name = text_file.split(".")[0] + ".csv"
	with open(write_file_name, "w") as f:
		write = csv.writer(f)
		write.writerow(header_fields)
		write.writerows(rows)

########################################################################

def plotRiver(river_df, latitude_extrapolation, longitude_extrapolation, nearest_neighbors_dict, save_plot_name):
	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("River Coordinates")
	plt.scatter(x=river_df['llat'], y=river_df['llon'], s=3, c="black")
	plt.plot(river_df['llat'], river_df['llon'], c="dodgerblue", label="Left Bank")
	plt.scatter(x=river_df['rlat'], y=river_df['rlon'], s=3, c="black")
	plt.plot(river_df['rlat'], river_df['rlon'], c="orange", label="Right Bank")
	plt.plot(latitude_extrapolation, longitude_extrapolation)
	plt.plot(nearest_neighbors_dict.keys(), nearest_neighbors_dict.values(), c="red")
	plt.xlabel("Latitude")
	plt.ylabel("Longitude")
	plt.legend()
	plt.show()
	fig.savefig(save_plot_name)

########################################################################
if __name__ == "__main__":
	convertColumnsToCSV("data/river_coords.txt")
	df = pd.read_csv("data/river_coords.csv")

	# Lines between points on graph
	latitude_points = []
	longitude_points = []
	for index, row in df.iterrows():
		latitude_points.append([row.llat, row.rlat])
		longitude_points.append([row.llon, row.rlon])

	nearest_neighbors = {}
	for index, row in df.iterrows():
		pass

	# Plot river banks
	plotRiver(df, latitude_points, longitude_points, nearest_neighbors, "data/river_coords.png")
