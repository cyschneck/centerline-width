# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
	#print("original data: leftbank/rightbank.kml")
	#centerline_width.extractPointsToTextFile(left_kml="data/leftbank.kml",
	#										right_kml="data/rightbank.kml",
	#										text_output_name="data/river_coords.txt")
	#print("new data with gap: N8_R1/N8_R2.kml")
	centerline_width.extractPointsToTextFile(left_kml="data/left.kml",
											right_kml="data/right.kml",
											text_output_name="data/N_output.txt")
	centerline_width.convertColumnsToCSV(text_file="data/N_output.txt", flipBankDirection=False)

	# Valid Examples
	cutoff = None
	#cutoff = 10
	#cutoff = 15 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 30
	#cutoff = 100 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	#cutoff = 550 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
	# Invalid Examples
	#cutoff = 5 # invalid centerline, invalid path, valid polygon, invalid starting node, invalid ending nodes
	#cutoff = 250 # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
	#cutoff = 40 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 700 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
	#cutoff = 1000 # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

	river = centerline_width.riverCenterline(csv_data="data/N_output.csv",
											optional_cutoff=cutoff,
											interpolate_data=True,
											interpolate_n=10,
											interpolate_n_centerpoints=62)
	#print(river)
	#print(river.__dict__.keys())
	print("Centerline Length = {0} km".format(river.centerlineLength))
	print("Right Bank Length = {0} km".format(river.rightBankLength))
	print("Left Bank Length = {0} km".format(river.leftBankLength))
	print("centerlineVoronoi = {0}".format(len(river.centerlineVoronoi)))
	print("centerlineEvenlySpaced = {0}".format(len(river.centerlineEvenlySpaced)))
	print("centerlineSmoothed = {0}".format(len(river.centerlineSmoothed)))
	

	# Plot river bank centerline
	#river.plotCenterline(save_plot_name=None, 
	#					display_all_possible_paths=False, 
	#					display_voronoi=False)

	transect = 3

	# Plot river bank width line
	river.plotCenterlineWidth(save_plot_name=None, 
							plot_title=None,
							display_true_centerline=True,
							transect_span_distance=transect,
							apply_smoothing=True,
							flag_intersections=False,
							remove_intersections=True)

	# Return width line for each centerline coordinates
	river_width_dict = river.riverWidthFromCenterline(transect_span_distance=transect,
													apply_smoothing=True,
													remove_intersections=True,
													units="m",
													save_to_csv=None)

	print("\nriver width dict = {0}\n".format(river_width_dict))
