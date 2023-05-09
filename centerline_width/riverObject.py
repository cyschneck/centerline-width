# River object class used for all functions and centerline functions
import pandas as pd

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

class riverCenterline:
	def __init__(self, csv_data, optional_cutoff=None):
		self.river_name = csv_data
		df = pd.read_csv(csv_data)
		if optional_cutoff:
			df = df.head(optional_cutoff)
		self.df = df

		# Left and Right Coordinates from the given csv data and data cutoff
		left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(df)
		self.left_bank_coordinates = left_bank_coordinates
		self.right_bank_coordinates = right_bank_coordinates

		# River polygon, position of the top/bottom polygon
		river_bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(left_bank_coordinates, right_bank_coordinates)
		self.bank_polygon = river_bank_polygon
		self.top_bank = top_bank
		self.bottom_bank = bottom_bank

		# Voronoi
		river_bank_voronoi = centerline_width.generateVoronoi(left_bank_coordinates, right_bank_coordinates)
		self.river_bank_voronoi = river_bank_voronoi

		# All possible paths: starting/ending node, all possible paths (ridges), paths dictionary
		starting_node, ending_node, x_ridge_point, y_ridge_point, start_end_points_dict = centerline_width.centerlinePath(river_bank_voronoi, river_bank_polygon, top_bank, bottom_bank)
		self.starting_node = starting_node # starting position for centerline
		self.ending_node = ending_node # ending position for centerline

		# Centerline coordinates
		shortest_path_coordinates = centerline_width.networkXGraphShortestPath(start_end_points_dict, starting_node, ending_node)
		self.centerline_latitude_longtiude = shortest_path_coordinates

		# Centerline length
		self.centerline_length = centerline_width.centerlineLength(centerline_coordinates=shortest_path_coordinates)

	def riverWidthFromCenterline(self,
								n_interprolate_centerpoints=None,
								transect_span_distance=3,
								apply_smoothing=True,
								remove_intersections=False,
								save_to_csv=None):
		return centerline_width.riverWidthFromCenterline(river_object=self,
														n_interprolate_centerpoints=n_interprolate_centerpoints,
														transect_span_distance=transect_span_distance,
														apply_smoothing=apply_smoothing,
														remove_intersections=remove_intersections,
														save_to_csv=save_to_csv)

	def plotCenterline(self, display_all_possible_paths=False, plot_title=None, save_plot_name=None, display_voronoi=False):
		centerline_width.plotCenterline(river_object=self,
										display_all_possible_paths=display_all_possible_paths, 
										plot_title=plot_title, 
										save_plot_name=save_plot_name, 
										display_voronoi=display_voronoi)

	def plotCenterlineWidth(self,
							plot_title=None, 
							save_plot_name=None, 
							display_true_centerline=True,
							n_interprolate_centerpoints=None,
							transect_span_distance=3,
							apply_smoothing=False,
							flag_intersections=True,
							remove_intersections=False):
		centerline_width.plotCenterlineWidth(river_object=self,
											plot_title=plot_title, 
											save_plot_name=save_plot_name, 
											display_true_centerline=display_true_centerline,
											n_interprolate_centerpoints=n_interprolate_centerpoints,
											transect_span_distance=transect_span_distance,
											apply_smoothing=apply_smoothing,
											flag_intersections=flag_intersections,
											remove_intersections=remove_intersections)
