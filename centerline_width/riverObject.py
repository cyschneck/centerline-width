import pandas as pd

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

class river:
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
