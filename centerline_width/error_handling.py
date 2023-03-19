########################################################################
# ERROR CATCHES AND LOGGING FOR CLARITY WHEN USING CENTERLINE-WIDTH
########################################################################

import logging

import numpy as np

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .CRITICAL
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

## Error Handling: preprocessing.py
def errrorHandlingConvertColumnsToCSV(text_file=None,
									flipBankDirection=False):
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
		logger.critical("\nCRITICAL ERROR, [flipBankDirection]: Must be a bool, current type = '{0}'".format(flipBankDirection))
		exit()

## Error Handling: plotDiagrams.py
def errorHandlingPlotCenterline(csv_data=None,
								display_all_possible_paths=False,
								plot_title=None,
								save_plot_name=None,
								displayVoronoi=False,
								optional_cutoff=None):
	# Error handling for plotCenterline()
	if csv_data is None:
		logger.critical("\nCRITICAL ERROR, [csv_data]: Requires csv file")
		exit()
	else:
		if type(csv_data) != str:
			logger.critical("\nCRITICAL ERROR, [csv_data]: Must be a str, current type = '{0}'".format(type(csv_data)))
			exit()
		else:
			if not csv_data.lower().endswith(".csv"):
				logger.critical("\nCRITICAL ERROR, [csv_data]: Extension must be a .csv file, current extension = '{0}'".format(csv_data.split(".")[1]))
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

	if type(displayVoronoi) != bool:
		logger.critical("\nCRITICAL ERROR, [displayVoronoi]: Must be a bool, current type = '{0}'".format(type(displayVoronoi)))
		exit()

	if optional_cutoff is not None and type(optional_cutoff) != int:
		logger.critical("\nCRITICAL ERROR, [optional_cutoff]: Must be a int, current type = '{0}'".format(type(optional_cutoff)))
		exit()

## Error Handling: centerline.py
def errorHandlingCenterlineLatitudeLongitude(csv_data=None, optional_cutoff=None):
	# Error Handling for centerlineLatitudeLongitude()
	if csv_data is None:
		logger.critical("\nCRITICAL ERROR, [csv_data]: Requires csv file")
		exit()
	else:
		if type(csv_data) != str:
			logger.critical("\nCRITICAL ERROR, [csv_data]: Must be a str, current type = '{0}'".format(type(csv_data)))
			exit()
		else:
			if not csv_data.lower().endswith(".csv"):
				logger.critical("\nCRITICAL ERROR, [csv_data]: Extension must be a .csv file, current extension = '{0}'".format(csv_data.split(".")[1]))
				exit()

	if optional_cutoff is not None and type(optional_cutoff) != int:
		logger.critical("\nCRITICAL ERROR, [optional_cutoff]: Must be a int, current type = '{0}'".format(type(optional_cutoff)))
		exit()

def errorHandlingRiverWidthFromCenterline(csv_data=None,
										centerline_coordinates=None,
										save_to_csv=None,
										optional_cutoff=None):
	# Error Handling for riverWidthFromCenterline()
	if csv_data is None:
		logger.critical("\nCRITICAL ERROR, [csv_data]: Requires csv file")
		exit()
	else:
		if type(csv_data) != str:
			logger.critical("\nCRITICAL ERROR, [csv_data]: Must be a str, current type = '{0}'".format(type(csv_data)))
			exit()
		else:
			if not csv_data.lower().endswith(".csv"):
				logger.critical("\nCRITICAL ERROR, [csv_data]: Extension must be a .csv file, current extension = '{0}'".format(csv_data.split(".")[1]))
				exit()

	if type(centerline_coordinates) != list:
		logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: Must be a list of lists, current type = '{0}'".format(type(centerline_coordinates)))
		exit()

	if save_to_csv is not None and type(save_to_csv) != str:
		logger.critical("\nCRITICAL ERROR, [save_to_csv]: Must be a str, current type = '{0}'".format(type(save_to_csv)))
		exit()

	if optional_cutoff is not None and type(optional_cutoff) != int:
		logger.critical("\nCRITICAL ERROR, [optional_cutoff]: Must be a int, current type = '{0}'".format(type(optional_cutoff)))
		exit()

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

def errorHandlingCenterlineLength(centerline_coordinates=None):
	# Error Handling for centerlineLength()
	if centerline_coordinates is None:
		logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: Requires centerline_coordinates")
		exit()
	else:
		if type(centerline_coordinates) != list:
			logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: Must be a list, current type = '{0}'".format(type(centerline_coordinates)))
			exit()
		else:
			for centerline_pair in centerline_coordinates:
				if type(centerline_pair) != list and type(centerline_pair) != tuple:
					logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: All elements in centerline_coordinates must be a list of lists, current item '{0}' is type = '{1}'".format(centerline_pair, type(centerline_pair)))
					exit()
				if len(centerline_pair) != 2:
					logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: All elements in centerline_coordinates must be xy pair, length = 2, current length of '{0}' = '{1}'".format(centerline_pair, len(centerline_pair)))
					exit()
				if type(centerline_pair[0]) != int and type(centerline_pair[0]) != float and type(centerline_pair[0]) != np.float64:
					logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: All elements in centerline_coordinates be a int or float, current type = '{0}'".format(type(centerline_pair[0])))
					exit()
				if type(centerline_pair[1]) != int and type(centerline_pair[1]) != float and type(centerline_pair[1]) != np.float64:
					logger.critical("\nCRITICAL ERROR, [centerline_coordinates]: All elements in centerline_coordinates be a int or float, current type = '{0}'".format(type(centerline_pair[0])))
					exit()
