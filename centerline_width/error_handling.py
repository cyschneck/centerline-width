########################################################################
# ERROR CATCHES AND LOGGING FOR CLARITY WHEN USING CENTERLINE-WIDTH
########################################################################

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
