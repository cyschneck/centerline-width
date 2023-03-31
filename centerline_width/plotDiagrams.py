import math
import logging

import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import voronoi_plot_2d

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def plotCenterline(csv_data=None,
					display_all_possible_paths=False, 
					plot_title=None, 
					save_plot_name=None, 
					displayVoronoi=False,
					optional_cutoff=None):
	# Plot Centerline of River

	centerline_width.errorHandlingPlotCenterline(csv_data=csv_data,
												display_all_possible_paths=display_all_possible_paths,
												plot_title=plot_title,
												save_plot_name=save_plot_name,
												displayVoronoi=displayVoronoi,
												optional_cutoff=optional_cutoff)

	# Plot river
	df = pd.read_csv(csv_data)
	if optional_cutoff: # only include the first x amount of the data
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

	# Plot all possible paths with text for positions
	if display_all_possible_paths or not river_bank_polygon.is_valid: # display paths if polygon is not valid (debugging purposes)
		for i in range(len(x_ridge_point)):
			plt.plot(x_ridge_point[i], y_ridge_point[i], 'cyan', linewidth=1)
			# Plot (X, Y) positions as text
			#ax.text(x=x_ridge_point[i][0], y=y_ridge_point[i][0], s="{0}, {1}".format(x_ridge_point[i][0], y_ridge_point[i][0]))
			#ax.text(x=x_ridge_point[i][1], y=y_ridge_point[i][1], s="{0}, {1}".format(x_ridge_point[i][1], y_ridge_point[i][1]))

	# Plot colored river bank
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
		x = []
		y = []
		for k, v in shortest_path_points:
			x.append(k)
			y.append(v)
		#plt.scatter(x, y, c="slategray", label="Centerline Coordinates", s=5)
		plt.plot(*zip(*shortest_path_points), c="black", label="Centerline")

	# Dynamically assign the starting and ending
	if starting_node is not None: # error handling for when data is too small to generate centerline coordiantes
		plt.scatter(starting_node[0], starting_node[1], c="green", label="Starting Node", s=45)
		plt.scatter(ending_node[0], ending_node[1], c="red", label="Ending Node", s=45)

	# Plot Title, Legends, and Axis Labels
	if not plot_title:
		plt.title("River Coordinates: Valid Centerline = {0}, Valid Polygon = {1}".format(valid_path_through, river_bank_polygon.is_valid))
	else:
		plt.title(plot_title)
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	if save_plot_name: fig.savefig(save_plot_name)

def plotCenterlineWidth(csv_data=None,
						plot_title=None, 
						save_plot_name=None, 
						displayTrueCenterline=True,
						n_interprolate_centerpoints=None,
						transect_span_distance=3,
						gaussian_filter_sigma=None,
						optional_cutoff=None):
	# Plot Width Lines based on Centerline

	centerline_width.errorHandlingPlotCenterlineWidth(csv_data=csv_data,
													plot_title=plot_title, 
													save_plot_name=save_plot_name, 
													displayTrueCenterline=displayTrueCenterline,
													n_interprolate_centerpoints=n_interprolate_centerpoints,
													transect_span_distance=transect_span_distance,
													gaussian_filter_sigma=gaussian_filter_sigma,
													optional_cutoff=optional_cutoff)

	# Plot river
	df = pd.read_csv(csv_data)
	if optional_cutoff: # only include the first x amount of the data
		df = df.head(optional_cutoff)

	if n_interprolate_centerpoints is None:
		# if plotting width, but n_interprolate_centerpoints is undefined, set to the size of the dataframe
		n_interprolate_centerpoints = len(df)

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

	# Plot colored river bank
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
		if displayTrueCenterline:
			x = []
			y = []
			for k, v in shortest_path_points:
				x.append(k)
				y.append(v)
			#plt.scatter(x, y, c="slategray", label="Centerline Coordinates", s=5)
			plt.plot(*zip(*shortest_path_points), c="black", label="Centerline")

	# Determine the Width of River
	number_of_evenly_spaced_points = ""
	if not shortest_path_points:
		logger.info("Unable to generate width lines without a valid centerline")
	if shortest_path_points:
		number_of_evenly_spaced_points = "\nCenterline made of {0} Fixed Points, width lines generated every {1} points".format(n_interprolate_centerpoints, transect_span_distance)
		if starting_node is not None: # error handling for when data is too small to generate centerline coordiantes
			# recreate the centerline with evenly spaced points
			evenly_spaced_centerline_coordinates = centerline_width.evenlySpacedCenterline(centerline_coordinates=shortest_path_points,
																						number_of_fixed_points=n_interprolate_centerpoints)
			if gaussian_filter_sigma is not None:
				smoothed_centerline_coordinates = centerline_width.gaussianSmoothedCoordinates(centerline_coordinates=evenly_spaced_centerline_coordinates,
																								gaussian_sigma=gaussian_filter_sigma)
				# if using gaussian_filter, replace left/right coordinates with the smoothed variation
				right_width_coordinates, left_width_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(csv_data=csv_data, 
																												bank_polygon=river_bank_polygon,
																												centerline_coordinates=smoothed_centerline_coordinates,
																												transect_span_distance=transect_span_distance,
																												optional_cutoff=optional_cutoff)
				x = []
				y = []
				for k, v in smoothed_centerline_coordinates:
					x.append(k)
					y.append(v)
				plt.scatter(x, y, c="blue", label="Smoothed Centerline Coordinates, sigma={0}".format(gaussian_filter_sigma), s=20)
				plt.plot(*zip(*smoothed_centerline_coordinates), "--", c="lightblue", label="Smoothed Centerline, sigma={0}".format(gaussian_filter_sigma))
			else:
				right_width_coordinates, left_width_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(csv_data=csv_, 
																														bank_polygon=river_bank_polygon,
																														centerline_coordinates=evenly_spaced_centerline_coordinates,
																														transect_span_distance=transect_span_distance,
																														optional_cutoff=optional_cutoff)

			x = []
			y = []
			for k, v in evenly_spaced_centerline_coordinates:
				x.append(k)
				y.append(v)
			plt.scatter(x, y, c="plum", label="Evenly Spaced Centerline Coordinates", s=20)
			plt.plot(*zip(*evenly_spaced_centerline_coordinates), "--", c="thistle", label="Evenly Spaced Centerline")

			x = []
			y = []
			for k, v in right_width_coordinates.items():
				x.append(k[0])
				y.append(k[1])
			plt.scatter(x, y, c="purple", label="Every X Number", s=5)

			for center_coord, edge_coord in right_width_coordinates.items():
				x_points = (right_width_coordinates[center_coord][0], left_width_coordinates[center_coord][0])
				y_points = (right_width_coordinates[center_coord][1], left_width_coordinates[center_coord][1])
				plt.plot(x_points, y_points, 'mediumorchid', linewidth=1)
			"""
			x = []
			y = []
			for center_coord, edge_coord in right_width_coordinates.items():
				x.append(right_width_coordinates[center_coord][0])
				y.append(right_width_coordinates[center_coord][1])
			plt.scatter(x, y, c="red")
			x = []
			y = []
			for center_coord, edge_coord in right_width_coordinates.items():
				x.append(left_width_coordinates[center_coord][0])
				y.append(left_width_coordinates[center_coord][1])
			plt.scatter(x, y, c="blue")
			"""

	# Dynamically assign the starting and ending
	if starting_node is not None: # error handling for when data is too small to generate centerline coordiantes
		plt.scatter(starting_node[0], starting_node[1], c="green", label="Starting Node", s=45)
		plt.scatter(ending_node[0], ending_node[1], c="red", label="Ending Node", s=45)

	# Plot Title, Legends, and Axis Labels
	if not plot_title:
		plt.title("River Coordinates: Valid Centerline = {0}, Valid Polygon = {1}{2}".format(valid_path_through, river_bank_polygon.is_valid, number_of_evenly_spaced_points))
	else:
		plt.title(plot_title)
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	if save_plot_name: fig.savefig(save_plot_name)
