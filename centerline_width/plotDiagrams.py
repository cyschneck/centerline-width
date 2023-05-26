# Built in Python functions
import math
import logging

# External Python libraries (installed via pip install)
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

def plotCenterlineBackend(river_object=None, display_true_centerline=True):
	# Shared components between plotCenterline and plotCenterlineWidth
	fig = plt.figure(figsize=(10,10))
	ax = fig.add_subplot(111)
	
	# Plot River as a Polygon
	plt.plot(*river_object.bank_polygon.exterior.xy, c="gainsboro")
	plt.plot(*river_object.top_bank.xy, c="forestgreen")
	plt.plot(*river_object.bottom_bank.xy, c="lightcoral")

	scatter_plot_size = 4
	x = []
	y = []
	for i in river_object.right_bank_coordinates: 
		x.append(i[0])
		y.append(i[1])
	plt.scatter(x, y, c="dodgerblue", s=scatter_plot_size, label="Right Bank")
	x = []
	y = []
	for i in river_object.left_bank_coordinates:
		x.append(i[0])
		y.append(i[1])
	plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank")

	# Plot centerline found from NetworkX
	valid_path_through = False
	if river_object.centerlineVoronoi: # shortest path through points
		valid_path_through = True
		x = []
		y = []
		for k, v in river_object.centerlineVoronoi:
			x.append(k)
			y.append(v)
		#plt.scatter(x, y, c="black", label="Centerline Coordinates", s=8)
		if display_true_centerline:
			plt.plot(*zip(*river_object.centerlineVoronoi), c="black", label="Centerline")

	# Dynamically assign the starting and ending
	if river_object.starting_node is not None: # error handling for when data is too small to generate centerline coordiantes
			plt.scatter(river_object.starting_node[0], river_object.starting_node[1], c="green", label="Starting Node", s=45)
			plt.scatter(river_object.ending_node[0], river_object.ending_node[1], c="red", label="Ending Node", s=45)

	return fig, ax, valid_path_through

def plotCenterline(river_object=None,
					display_all_possible_paths=False, 
					plot_title=None, 
					save_plot_name=None, 
					display_voronoi=False):
	# Plot Centerline of River
	centerline_width.errorHandlingPlotCenterline(river_object=river_object,
												display_all_possible_paths=display_all_possible_paths,
												plot_title=plot_title,
												save_plot_name=save_plot_name,
												display_voronoi=display_voronoi)

	fig, ax, valid_path_through = plotCenterlineBackend(river_object=river_object)

	# Display the Voronoi Diagram
	if display_voronoi:
		voronoi_plot_2d(river_object.bank_voronoi, show_points=True, point_size=1, ax=ax)

	# Plot all possible paths with text for positions
	if display_all_possible_paths:
		for i in range(len(river_object.x_voronoi_ridge_point)):
			plt.plot(river_object.x_voronoi_ridge_point[i], river_object.y_voronoi_ridge_point[i], 'cyan', linewidth=1)

	# Plot Title, Legends, and Axis Labels
	if not plot_title:
		plt.title("River Coordinates: Valid Centerline = {0}, Valid Polygon = {1}, Interpolated = {2}".format(valid_path_through, river_object.bank_polygon.is_valid, river_object.interpolate_data))
	else:
		plt.title(plot_title)
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	if save_plot_name: fig.savefig(save_plot_name)

def plotCenterlineWidth(river_object=None,
						plot_title=None, 
						save_plot_name=None, 
						display_true_centerline=True,
						transect_span_distance=3,
						apply_smoothing=False,
						flag_intersections=True,
						remove_intersections=False):
	# Plot Width Lines based on Centerline
	centerline_width.errorHandlingPlotCenterlineWidth(river_object=river_object,
													plot_title=plot_title, 
													save_plot_name=save_plot_name, 
													display_true_centerline=display_true_centerline,
													transect_span_distance=transect_span_distance,
													apply_smoothing=apply_smoothing,
													flag_intersections=flag_intersections,
													remove_intersections=remove_intersections)

	fig, ax, valid_path_through = plotCenterlineBackend(river_object=river_object, display_true_centerline=display_true_centerline)

	# Plot river

	# Determine the Width of River
	number_of_evenly_spaced_points = ""

	if river_object.centerlineVoronoi is not None:
		number_of_evenly_spaced_points = "\nCenterline made of {0} Fixed Points, width lines generated every {1} points".format(river_object.interpolate_n_centerpoints, transect_span_distance)
		if river_object.starting_node is not None: # error handling for when data is too small to generate centerline coordiantes
			if apply_smoothing:
				# if using smoothing, replace left/right coordinates with the smoothed variation
				right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(river_object=river_object,
																																					centerline_coordinates=river_object.centerlineSmoothed,
																																					transect_span_distance=transect_span_distance,
																																					remove_intersections=remove_intersections)
				x = []
				y = []
				for k, v in river_object.centerlineSmoothed:
					x.append(k)
					y.append(v)
				plt.scatter(x, y, c="blue", label="Smoothed Centerline Coordinates", s=5)
			else:
				# recreate the centerline with evenly spaced points
				right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(river_object=river_object, 
																														centerline_coordinates=river_object.centerlineEvenlySpaced,
																														transect_span_distance=transect_span_distance,
																														remove_intersections=remove_intersections)

			# Display the evenly spaced centerline
			#x = []
			#y = []
			#for k, v in river_object.centerlineEvenlySpaced:
			#	x.append(k)
			#	y.append(v)
			#plt.scatter(x, y, c="plum", label="Evenly Spaced Centerline Coordinates", s=8)
			#plt.plot(*zip(*evenly_spaced_centerline_coordinates), "--", c="thistle", label="Evenly Spaced Centerline")

			for center_coord, edge_coord in right_width_coordinates.items():
				x_points = (right_width_coordinates[center_coord][0], left_width_coordinates[center_coord][0])
				y_points = (right_width_coordinates[center_coord][1], left_width_coordinates[center_coord][1])
				if flag_intersections:
					if num_intersection_coordinates[center_coord] > 0:
						if remove_intersections:
							logger.error("\nERROR: Unable to completely resolve all intersections lines to be removed")
						plt.plot(x_points, y_points, 'red', linewidth=1)
					else:
						plt.plot(x_points, y_points, 'green', linewidth=1)
				else:
					plt.plot(x_points, y_points, 'green', linewidth=1)

	# Plot Title, Legends, and Axis Labels
	if not plot_title:
		plt.title("River Width Coordinates: Valid Centerline = {0}, Valid Polygon = {1}{2}, Interpolated = {3}".format(valid_path_through, river_object.bank_polygon.is_valid, number_of_evenly_spaced_points, river_object.interpolate_data))
	else:
		plt.title(plot_title)
	plt.xlabel("Longitude (°)")
	plt.ylabel("Latitude (°)")
	plt.legend(loc="upper right")
	plt.show()
	if save_plot_name: fig.savefig(save_plot_name)
