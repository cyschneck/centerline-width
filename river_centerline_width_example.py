# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
	#print("original data: leftbank/rightbank.kml")
	#centerline_width.extractPointsToTextFile(left_kml="data/leftbank.kml",
	#										right_kml="data/rightbank.kml",
	#										text_output_name="data/river_coords.txt")
	#print("new data with gap: N8_R1/N8_R2.kml")
	#centerline_width.extractPointsToTextFile(left_kml="data/N8_R1.kml",
	#										right_kml="data/N8_R2.kml",
	#										text_output_name="data/N47_R_output.txt")
	#centerline_width.convertColumnsToCSV(text_file="data/N47_R_output.txt", flipBankDirection=True)
	centerline_width.extractPointsToTextFile(left_kml="data/NA7_FP1.kml",
											right_kml="data/NA7_FP2.kml",
											text_output_name="data/NA7_output.txt")
	centerline_width.convertColumnsToCSV(text_file="data/NA7_output.txt", flipBankDirection=False)

	# Valid Examples
	cutoff = None
	#cutoff = 10
	cutoff = 15 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 30
	#cutoff = 100 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 550 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	# Invalid Examples
	#cutoff = 5 # invalid centerline, invalid path, valid polygon, invalid starting node, invalid ending nodes
	#cutoff = 250 # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
	#cutoff = 40 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 700 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 1000 # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

	river = centerline_width.riverCenterline(csv_data="data/NA7_output.csv", optional_cutoff=cutoff, interpolate_data=False)
	print(river.interpolated_voronoi)
	print(river.right_bank_interpolated_coordinates)
	print(river.left_bank_interpolated_coordinates)
	#print(river)
	#print(river.__dict__)
	print("Length = {0} km".format(river.centerline_length))
	#print(river.centerline_latitude_longtiude)

	# Plot river bank centerline
	river.plotCenterline(save_plot_name=None, 
						display_all_possible_paths=True, 
						display_voronoi=False,
						interpolate_data=True)
	transect = 3
	exit()

	# Plot river bank width line
	river.plotCenterlineWidth(save_plot_name=None, 
							display_true_centerline=False,
							n_interprolate_centerpoints=None,
							transect_span_distance=transect,
							apply_smoothing=True,
							flag_intersections=True,
							remove_intersections=True)

	# Return width line for each centerline coordinates
	river_width_dict = river.riverWidthFromCenterline(n_interprolate_centerpoints=None,
													transect_span_distance=transect,
													apply_smoothing=True,
													remove_intersections=True,
													units="m",
													save_to_csv=None)

	print("\nriver width dict = {0}\n".format(river_width_dict))
