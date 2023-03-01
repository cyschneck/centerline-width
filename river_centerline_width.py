# Find the center point and width between lat/long points along river bank
# Modified from R - CMGO code functionality
import matplotlib.pyplot as plt
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

def plotRiver(river_df):
	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("River Coordinates (Latitude/Longitude)")
	plt.scatter(x=river_df['llat'], y=river_df['llon'], s=1, label="Left Bank")
	plt.scatter(x=river_df['rlat'], y=river_df['rlon'], s=1, label="Right Bank")
	plt.legend()
	plt.show()

if __name__ == "__main__":
	convertColumnsToCSV("data/river_coords.txt")
	df = pd.read_csv("data/river_coords.csv")
	plotRiver(df)
