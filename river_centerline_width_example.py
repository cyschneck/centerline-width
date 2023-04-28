# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
	centerline_width.extractPointsToTextFile(left_kml="data/leftbank.kml",
											right_kml="data/rightbank.kml",
											text_output_name="data/river_coords.txt")
	centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt", flipBankDirection=True)

	# Valid Examples
	cutoff = None
	#cutoff = 10
	#cutoff = 15 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 30
	#cutoff = 100 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	cutoff = 550 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	# Invalid Examples
	#cutoff = 5 # invalid centerline, invalid path, valid polygon, invalid starting node, invalid ending nodes
	#cutoff = 250 # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
	#cutoff = 40 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 700 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 1000 # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

	# Plot river bank centerline
	#centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
	#								save_plot_name="data/river_coords_centerline.png", 
	#								display_all_possible_paths=False, 
	#								display_voronoi=False,
	#								optional_cutoff=cutoff)

	transect = 3

	# Plot river bank width line
	centerline_width.plotCenterlineWidth(csv_data="data/river_coords.csv", 
										save_plot_name="data/river_coords_width.png", 
										display_true_centerline=False,
										n_interprolate_centerpoints=None,
										transect_span_distance=transect,
										apply_smoothing=True,
										flag_intersections=True,
										remove_intersections=True,
										optional_cutoff=cutoff)
	exit()

	# Return width line for each centerline coordinates
	river_width_dict = centerline_width.riverWidthFromCenterline(csv_data="data/river_coords.csv",
																n_interprolate_centerpoints=None,
																transect_span_distance=transect,
																apply_smoothing=True,
																remove_intersections=True,
																save_to_csv="data/centerline_coords.csv",
																optional_cutoff=cutoff)
	print("\nriver width dict = {0}\n".format(river_width_dict))

	# Return the latitude/longtiude coordinates for the centerline
	centerline_long_lat_coordinates = centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv", 
																					optional_cutoff=cutoff)
	print("\ncenterline lat/long = {0}\n".format(centerline_long_lat_coordinates))

	# Centerline Total Length (in degrees)
	centerline_length = centerline_width.centerlineLength(centerline_coordinates=centerline_long_lat_coordinates)
	print("\nCenterline Length (degrees) = {0}".format(centerline_length))

