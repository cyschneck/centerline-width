# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
	#centerline_width.extractPointsToTextFile(left_kml="data/leftbank.kml",
	#										right_kml="data/rightbank.kml",
	#										text_output_name="data/river_coords.txt")
	centerline_width.extractPointsToTextFile(left_kml="data/59deg48_18dot87_N_69deg46_59dot57_E_lb.kml",
											right_kml="data/59deg48_18dot87_N_69deg46_59dot57_E_rb.kml",
											text_output_name="data/N_output.txt")
	centerline_width.convertColumnsToCSV(text_file="data/N_output.txt", flipBankDirection=True)

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

	river = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
											optional_cutoff=cutoff,
											interpolate_data=False,
											interpolate_n=10,
											interpolate_n_centerpoints=None,
											equal_distance=20,
											ellipsoid="WGS84")

	#print(river)
	#print(river.__dict__.keys())
	print("\nCenterline Length = {0} km".format(river.centerlineLength))
	print("Centerline Length = {0} m".format(river.centerlineLength*1000))
	print("Right Bank Length = {0} km".format(river.rightBankLength))
	print("Left Bank Length = {0} km".format(river.leftBankLength))
	#print("ellipsoid = {0}".format(river.ellipsoid))
	#print("centerlineVoronoi = {0}".format(river.centerlineVoronoi))
	#print("equalDistanceCenterline = {0}".format(river.centerlineEqualDistance))
	#print("centerlineEvenlySpaced = {0}".format(river.centerlineEvenlySpaced))
	#print("centerlineSmoothed = {0}".format(river.centerlineSmoothed))
	#print("centerlineVoronoi = {0}".format(len(river.centerlineVoronoi)))
	#print("equalDistanceCenterline = {0}".format(len(river.centerlineEqualDistance)))
	#print("centerlineEvenlySpaced = {0}".format(len(river.centerlineEvenlySpaced)))
	#print("centerlineSmoothed = {0}".format(len(river.centerlineSmoothed)))

	coord_type = "Decimal Degrees"
	#coord_type = "Relative Distance"
	center_type = "Smoothed"
	
	river.saveCenterlineCSV(save_to_csv="centerline_for_csv.csv", centerline_type=center_type, coordinate_type=coord_type)
	river.saveCenterlineMAT(save_to_mat="centerline_for_matlab.mat", centerline_type=center_type, coordinate_type=coord_type)
	#exit()
	#river.saveCenterlineCSV(save_to_csv="centerline_for_csv.csv", latitude_header="lat", longitude_header="long", centerline_type="Equal Distance")
	#river.saveCenterlineMAT(save_to_mat="centerline_for_matlab.mat", latitude_header="lat", longitude_header="long", centerline_type="Evenly Spaced")

	# Plot river bank centerline
	river.plotCenterline(save_plot_name=None,
						centerline_type=center_type,
						marker_type="scatter",
						centerline_color="black",
						display_all_possible_paths=True, 
						display_voronoi=False,
						plot_title=None,
						coordinate_type=coord_type)

	transect = 3

	# Plot river bank width line
	river.plotCenterlineWidth(save_plot_name=None, 
							plot_title=None,
							display_true_centerline=True,
							transect_span_distance=transect,
							apply_smoothing=True,
							flag_intersections=True,
							remove_intersections=True,
							coordinate_type=coord_type)
	exit()
	# Return width line for each centerline coordinates
	river_width_dict = river.riverWidthFromCenterline(transect_span_distance=transect,
													apply_smoothing=True,
													remove_intersections=True,
													save_to_csv=None,
													coordinate_type=coord_type)

	print("\nriver width dict = {0}\n".format(river_width_dict))
