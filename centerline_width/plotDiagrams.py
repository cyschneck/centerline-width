import math

import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import voronoi_plot_2d

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

def plotCenterline(csv_data=None, display_all_possible_paths=False, plot_title=None, save_plot_name=None, displayVoronoi=False, optional_cutoff=None):
	# display_all_paths: display all possible paths (not just centerline) (useful for debugging)
	# Plot river
	df = pd.read_csv(csv_data)
	if optional_cutoff:
		df = df.head(optional_cutoff)

	left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)
	river_bank_polygon, top_river_line, bottom_river_line = centerline_width.generatePolygon(left_bank_coordinates, right_bank_coordinates)
	river_bank_voronoi = centerline_width.generateVoronoi(left_bank_coordinates, right_bank_coordinates)

	# Plot river based on right/left bank coordinates
	fig = plt.figure(figsize=(10,10))
	ax = fig.add_subplot(111)
	
	# Isolate center line:
	# Plot the ridge edges of the Voronoi polygons that lie within the river banks
	# Find the start and ending node to find the centerline
	starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict = centerline_width.centerlinePath(river_bank_voronoi,
																													river_bank_polygon, 
																													top_river_line, 
																													bottom_river_line)

	# Plot River as a Polygon
	plt.plot(*river_bank_polygon.exterior.xy, c="gainsboro")
	plt.plot(*top_river_line.xy, c="forestgreen")
	plt.plot(*bottom_river_line.xy, c="lightcoral")

	# Display the Voronoi Diagram
	if displayVoronoi:
		voronoi_plot_2d(river_bank_voronoi, show_points=True, point_size=1, ax=ax)

	# Dynamically assign the starting and ending
	plt.scatter(starting_node[0], starting_node[1], c="green", label="Starting Node")
	plt.scatter(ending_node[0], ending_node[1], c="red", label="Ending Node")

	# Plot all possible paths with text for positions
	if display_all_possible_paths or not river_bank_polygon.is_valid: # display paths if polygon is not valid (debugging purposes)
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
	shortest_path_points = centerline_width.networkXGraphShortestPath(start_end_points_dict, starting_node, ending_node)
	valid_path_through = False
	if shortest_path_points:
		valid_path_through = True
		plt.plot(*zip(*shortest_path_points), c="black", label="Centerline")

	if not plot_title:
		plt.title("River Coordinates: Valid Centerline = {0}, Valid Polygon = {1}".format(valid_path_through, river_bank_polygon.is_valid))
	else:
		plt.title(plot_title)
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	if save_plot_name: fig.savefig(save_plot_name)
