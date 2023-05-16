########################################################################
# ERROR CATCHES AND LOGGING FOR CLARITY WHEN USING CENTERLINE-WIDTH
########################################################################

# Built in Python functions
import logging

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .CRITICAL
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

## Error Handling: preprocessing.py
def errrorHandlingConvertColumnsToCSV(text_file=None,
									flipBankDirection=None):
	# Error handling for convertColumnsToCSV()
	if text_file is None:
		logger.critical("\nCRITICAL ERROR, [text_file]: Requires text file")
		exit()
	else:
		if type(text_file) != str:
			logger.critical("\nCRITICAL ERROR, [text_file]: Must be a str, current type = '{0}'".format(type(text_file)))
			exit()
		else:
			if not text_file.lower().endswith(".txt"):
				logger.critical("\nCRITICAL ERROR, [text_file]: Extension must be a .txt file, current extension = '{0}'".format(text_file.split(".")[1]))
				exit()

	if type(flipBankDirection) != bool:
		logger.critical("\nCRITICAL ERROR, [flipBankDirection]: Must be a bool, current type = '{0}'".format(type(flipBankDirection)))
		exit()

## Error Handling: plotDiagrams.py
def errorHandlingPlotCenterline(river_object=None,
								display_all_possible_paths=None,
								plot_title=None,
								save_plot_name=None,
								display_voronoi=None):
	# Error handling for plotCenterline()
	if river_object is None:
		logger.critical("\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)")
		exit()
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			logger.critical("\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))
			exit()

	if type(display_all_possible_paths) != bool:
		logger.critical("\nCRITICAL ERROR, [display_all_possible_paths]: Must be a bool, current type = '{0}'".format(type(display_all_possible_paths)))
		exit()

	if plot_title is not None and type(plot_title) != str:
		logger.critical("\nCRITICAL ERROR, [plot_title]: Must be a str, current type = '{0}'".format(type(plot_title)))
		exit()

	if save_plot_name is not None and type(save_plot_name) != str:
		logger.critical("\nCRITICAL ERROR, [save_plot_name]: Must be a str, current type = '{0}'".format(type(save_plot_name)))
		exit()

	if type(display_voronoi) != bool:
		logger.critical("\nCRITICAL ERROR, [display_voronoi]: Must be a bool, current type = '{0}'".format(type(display_voronoi)))
		exit()

def errorHandlingPlotCenterlineWidth(river_object=None,
									plot_title=None,
									save_plot_name=None,
									display_true_centerline=None,
									n_interprolate_centerpoints=None,
									transect_span_distance=None,
									apply_smoothing=None,
									flag_intersections=None,
									remove_intersections=None):
	# Error handling for plotCenterlineWidth()
	if river_object is None:
		logger.critical("\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)")
		exit()
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			logger.critical("\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))
			exit()

	if plot_title is not None and type(plot_title) != str:
		logger.critical("\nCRITICAL ERROR, [plot_title]: Must be a str, current type = '{0}'".format(type(plot_title)))
		exit()

	if save_plot_name is not None and type(save_plot_name) != str:
		logger.critical("\nCRITICAL ERROR, [save_plot_name]: Must be a str, current type = '{0}'".format(type(save_plot_name)))
		exit()

	if type(display_true_centerline) != bool:
		logger.critical("\nCRITICAL ERROR, [display_true_centerline]: Must be a bool, current type = '{0}'".format(type(display_true_centerline)))
		exit()

	if n_interprolate_centerpoints is not None:
		if type(n_interprolate_centerpoints) != int:
			logger.critical("\nCRITICAL ERROR, [n_interprolate_centerpoints]: Must be a int, current type = '{0}'".format(type(n_interprolate_centerpoints)))
			exit()
		else:
			if n_interprolate_centerpoints < 2:
				logger.critical("\nCRITICAL ERROR, [n_interprolate_centerpoints]: Must be a greater than 1, currently = '{0}'".format(n_interprolate_centerpoints))
				exit()

	if type(transect_span_distance) != int:
		logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be a int, current type = '{0}'".format(type(transect_span_distance)))
		exit()
	else:
		if transect_span_distance < 3:
			logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be a greater than 2 to find the slope between at least two points, currently = '{0}'".format(transect_span_distance))
			exit()

	if apply_smoothing is not None:
		if type(apply_smoothing) != bool:
			logger.critical("\nCRITICAL ERROR, [apply_smoothing]: Must be a bool, current type = '{0}'".format(type(apply_smoothing)))
			exit()
	
	if type(flag_intersections) != bool:
		logger.critical("\nCRITICAL ERROR, [flag_intersections]: Must be a bool, current type = '{0}'".format(type(flag_intersections)))
		exit()

	if type(remove_intersections) != bool:
		logger.critical("\nCRITICAL ERROR, [remove_intersections]: Must be a bool, current type = '{0}'".format(type(remove_intersections)))
		exit()

## Error Handling: centerline.py
def errorHandlingRiverWidthFromCenterlineCoordinates(river_object=None,
													centerline_coordinates=None,
													transect_span_distance=3,
													remove_intersections=False,
													save_to_csv=None):
	# Error Handling for riverWidthFromCenterlineCoordinates()
	if river_object is None:
		logger.critical("\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)")
		exit()
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			logger.critical("\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))
			exit()

	if transect_span_distance is not None:
		if type(transect_span_distance) != int:
			logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be a int, current type = '{0}'".format(type(transect_span_distance)))
			exit()
		else:
			if transect_span_distance < 3:
				logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be greater than 2, currently = '{0}'".format(transect_span_distance))
				exit()

	if type(remove_intersections) != bool:
		logger.critical("\nCRITICAL ERROR, [remove_intersections]: Must be a bool, current type = '{0}'".format(type(remove_intersections)))
		exit()

	if save_to_csv is not None:
		if type(save_to_csv) != str:
			logger.critical("\nCRITICAL ERROR, [save_to_csv]: Must be a str, current type = '{0}'".format(type(save_to_csv)))
			exit()

def errorHandlingRiverWidthFromCenterline(river_object=None,
										n_interprolate_centerpoints=None,
										transect_span_distance=None,
										apply_smoothing=None,
										remove_intersections=None,
										save_to_csv=None,
										optional_cutoff=None):
	# Error Handling for riverWidthFromCenterline()

	if river_object is None:
		logger.critical("\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)")
		exit()
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			logger.critical("\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))
			exit()

	if n_interprolate_centerpoints is not None:
		if type(n_interprolate_centerpoints) != int:
			logger.critical("\nCRITICAL ERROR, [n_interprolate_centerpoints]: Must be a int, current type = '{0}'".format(type(n_interprolate_centerpoints)))
			exit()

	if transect_span_distance is not None:
		if type(transect_span_distance) != int:
			logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be a int, current type = '{0}'".format(type(transect_span_distance)))
			exit()
		else:
			if transect_span_distance < 3:
				logger.critical("\nCRITICAL ERROR, [transect_span_distance]: Must be greater than 2, currently = '{0}'".format(transect_span_distance))
				exit()

	if type(apply_smoothing) != bool:
		logger.critical("\nCRITICAL ERROR, [apply_smoothing]: Must be a bool, current type = '{0}'".format(type(apply_smoothing)))
		exit()

	if type(remove_intersections) != bool:
		logger.critical("\nCRITICAL ERROR, [remove_intersections]: Must be a bool, current type = '{0}'".format(type(remove_intersections)))
		exit()

	if save_to_csv is not None:
		if type(save_to_csv) != str:
			logger.critical("\nCRITICAL ERROR, [save_to_csv]: Must be a str, current type = '{0}'".format(type(save_to_csv)))
			exit()

# Error Handling: getCoordinatesKML.py
def errorHandlingExtractPointsToTextFile(left_kml=None, right_kml=None, text_output_name=None):
	# Error Handling for extractPoints()
	if left_kml is None:
		logger.critical("\nCRITICAL ERROR, [left_kml]: Requires left_kml file")
		exit()
	else:
		if type(left_kml) != str:
			logger.critical("\nCRITICAL ERROR, [left_kml]: Must be a str, current type = '{0}'".format(type(left_kml)))
			exit()
		if not left_kml.lower().endswith(".kml"):
			logger.critical("\nCRITICAL ERROR, [left_kml]: Extension must be a .kml file, current extension = '{0}'".format(left_kml.split(".")[1]))
			exit()

	if right_kml is None:
		logger.critical("\nCRITICAL ERROR, [right_kml]: Requires right_kml file")
		exit()
	else:
		if type(right_kml) != str:
			logger.critical("\nCRITICAL ERROR, [right_kml]: Must be a str, current type = '{0}'".format(type(right_kml)))
			exit()
		if not right_kml.lower().endswith(".kml"):
			logger.critical("\nCRITICAL ERROR, [right_kml]: Extension must be a .kml file, current extension = '{0}'".format(right_kml.split(".")[1]))
			exit()

	if text_output_name is None:
		logger.critical("\nCRITICAL ERROR, [text_output_name]: Requires output file name file")
		exit()
	else:
		if type(text_output_name) != str:
			logger.critical("\nCRITICAL ERROR, [text_output_name]: Must be a str, current type = '{0}'".format(type(text_output_name)))
			exit()

## Error Handling: riverCenterlineClass.py
def errorHandlingRiverCenterlineClass(csv_data=None, optional_cutoff=None):
	# Error Handling for riverCenterlineClass()
	if csv_data is None:
		logger.critical("\nCRITICAL ERROR, [csv_data]: Requires csv_data name")
		exit()
	else:
		if type(csv_data) != str:
			logger.critical("\nCRITICAL ERROR, [csv_data]: Must be a str, current type = '{0}'".format(type(csv_data)))
			exit()

	if optional_cutoff is not None:
		if type(optional_cutoff) != int:
			logger.critical("\nCRITICAL ERROR, [optional_cutoff]: Must be a int, current type = '{0}'".format(type(optional_cutoff)))
			exit()
