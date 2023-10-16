########################################################################
# ERROR CATCHES AND LOGGING FOR CLARITY WHEN USING CENTERLINE-WIDTH
########################################################################

# Built in Python functions
import logging
from io import StringIO

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .CRITICAL
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

centerline_type_options = ["Voronoi", "Evenly Spaced", "Smoothed", "Equal Distance"]

## Error Handling: preprocessing.py
def errrorHandlingConvertColumnsToCSV(text_file=None,
									flipBankDirection=None):
	# Error handling for convertColumnsToCSV()
	if text_file is None:
		raise ValueError("[text_file]: Requires text file")
	else:
		if type(text_file) != str:
			raise ValueError("[text_file]: Must be a str, current type = '{0}'".format(type(text_file)))
		else:
			if not text_file.lower().endswith(".txt"):
				raise ValueError("[text_file]: Extension must be a .txt file, current extension = '{0}'".format(text_file.split(".")[1]))

	if type(flipBankDirection) != bool:
		raise ValueError("[flipBankDirection]: Must be a bool, current type = '{0}'".format(type(flipBankDirection)))

## Error Handling: plotDiagrams.py
def errorHandlingPlotCenterline(river_object=None,
								centerline_type=None,
								marker_type=None,
								centerline_color=None,
								display_all_possible_paths=None,
								plot_title=None,
								save_plot_name=None,
								display_voronoi=None,
								coordinate_unit=None):
	# Error handling for plotCenterline()
	if river_object is None:
		raise ValueError("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			raise ValueError("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))

	if type(centerline_type) != str:
		raise ValueError("[centerline_type]: Must be a str, current type = '{0}'".format(type(centerline_type)))
	else:
		if centerline_type.title() not in centerline_type_options:
			raise ValueError("[centerline_type]: Must be an available option in {0}, current option = '{1}'".format(centerline_type_options, centerline_type))

	if type(marker_type) != str:
		raise ValueError("[marker_type]: Must be a str, current type = '{0}'".format(type(marker_type)))
	else:
		marker_type_options = ["Line", "Scatter"]
		if marker_type.title() not in marker_type_options:
			raise ValueError("[marker_type]: Must be an available option in {0}, current option = '{1}'".format(marker_type_options, marker_type))

	if type(centerline_color) != str:
		raise ValueError("[centerline_color]: Must be a str, current type = '{0}'".format(type(centerline_color)))

	if type(display_all_possible_paths) != bool:
		raise ValueError("[display_all_possible_paths]: Must be a bool, current type = '{0}'".format(type(display_all_possible_paths)))

	if plot_title is not None and type(plot_title) != str:
		raise ValueError("[plot_title]: Must be a str, current type = '{0}'".format(type(plot_title)))

	if save_plot_name is not None and type(save_plot_name) != str:
		raise ValueError("[save_plot_name]: Must be a str, current type = '{0}'".format(type(save_plot_name)))

	if type(display_voronoi) != bool:
		raise ValueError("[display_voronoi]: Must be a bool, current type = '{0}'".format(type(display_voronoi)))

	if type(coordinate_unit) != str:
		raise ValueError("[coordinate_unit]: Must be a str, current type = '{0}'".format(type(coordinate_unit)))
	else:
		coordinate_unit_options = ["Decimal Degrees", "Relative Distance"]
		if coordinate_unit.title() not in coordinate_unit_options:
			raise ValueError("[coordinate_unit]: Must be an available option in {0}, current option = '{1}'".format(coordinate_unit_options, coordinate_unit))

def errorHandlingPlotCenterlineWidth(river_object=None,
									plot_title=None,
									save_plot_name=None,
									display_true_centerline=None,
									transect_span_distance=None,
									apply_smoothing=None,
									flag_intersections=None,
									remove_intersections=None,
									coordinate_unit=None):
	# Error handling for plotCenterlineWidth()
	if river_object is None:
		raise ValueError("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			raise ValueError("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))

	if plot_title is not None and type(plot_title) != str:
		raise ValueError("[plot_title]: Must be a str, current type = '{0}'".format(type(plot_title)))

	if save_plot_name is not None and type(save_plot_name) != str:
		raise ValueError("[save_plot_name]: Must be a str, current type = '{0}'".format(type(save_plot_name)))

	if type(display_true_centerline) != bool:
		raise ValueError("[display_true_centerline]: Must be a bool, current type = '{0}'".format(type(display_true_centerline)))

	if type(transect_span_distance) != int:
		raise ValueError("[transect_span_distance]: Must be a int, current type = '{0}'".format(type(transect_span_distance)))
	else:
		if transect_span_distance < 3:
			raise ValueError("[transect_span_distance]: Must be a greater than 2 to find the slope between at least two points, currently = '{0}'".format(transect_span_distance))

	if apply_smoothing is not None:
		if type(apply_smoothing) != bool:
			raise ValueError("[apply_smoothing]: Must be a bool, current type = '{0}'".format(type(apply_smoothing)))

	if type(flag_intersections) != bool:
		raise ValueError("[flag_intersections]: Must be a bool, current type = '{0}'".format(type(flag_intersections)))

	if type(remove_intersections) != bool:
		raise ValueError("[remove_intersections]: Must be a bool, current type = '{0}'".format(type(remove_intersections)))

	if type(coordinate_unit) != str:
		raise ValueError("[coordinate_unit]: Must be a str, current type = '{0}'".format(type(coordinate_unit)))
	else:
		coordinate_unit_options = ["Decimal Degrees", "Relative Distance"]
		if coordinate_unit.title() not in coordinate_unit_options:
			raise ValueError("[coordinate_unit]: Must be an available option in {0}, current option = '{1}'".format(coordinate_unit_options, coordinate_unit))

## Error Handling: centerline.py
def errorHandlingRiverWidthFromCenterline(river_object=None,
										transect_span_distance=None,
										apply_smoothing=None,
										remove_intersections=None,
										coordinate_unit=None,
										save_to_csv=None):
	# Error Handling for riverWidthFromCenterline()
	if river_object is None:
		raise ValueError("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			raise ValueError("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))

	if transect_span_distance is not None:
		if type(transect_span_distance) != int:
			raise ValueError("[transect_span_distance]: Must be a int, current type = '{0}'".format(type(transect_span_distance)))
		else:
			if transect_span_distance < 3:
				raise ValueError("[transect_span_distance]: Must be greater than 2, currently = '{0}'".format(transect_span_distance))

	if type(apply_smoothing) != bool:
		raise ValueError("[apply_smoothing]: Must be a bool, current type = '{0}'".format(type(apply_smoothing)))

	if type(remove_intersections) != bool:
		raise ValueError("[remove_intersections]: Must be a bool, current type = '{0}'".format(type(remove_intersections)))

	if type(coordinate_unit) != str:
		raise ValueError("[coordinate_unit]: Must be a str, current type = '{0}'".format(type(coordinate_unit)))
		exit()
	else:
		coordinate_unit_options = ["Decimal Degrees", "Relative Distance"]
		if coordinate_unit.title() not in coordinate_unit_options:
			raise ValueError("[coordinate_unit]: Must be an available option in {0}, current option = '{1}'".format(coordinate_unit_options, coordinate_unit))

	if save_to_csv is not None:
		if type(save_to_csv) != str:
			raise ValueError("[save_to_csv]: Must be a str, current type = '{0}'".format(type(save_to_csv)))
		if not save_to_csv.lower().endswith(".csv"):
			raise ValueError("[save_to_csv]: Extension must be a .csv file, current extension = '{0}'".format(save_to_csv.split(".")[1]))

def errorHandlingSaveCenterlineCSV(river_object=None,
								latitude_header=None,
								longitude_header=None,
								save_to_csv=None,
								centerline_type=None,
								coordinate_unit=None):
	# Error Handling for saveCenterlineCSV()
	if river_object is None:
		raise ValueError("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			raise ValueError("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))

	if latitude_header is not None and type(latitude_header) != str:
		raise ValueError("[latitude_header]: Must be a str, current type = '{0}'".format(type(latitude_header)))

	if longitude_header is not None and type(longitude_header) != str:
		raise ValueError("[longitude_header]: Must be a str, current type = '{0}'".format(type(longitude_header)))

	if save_to_csv is None:
		raise ValueError("[save_to_csv]: Requires csv filename")
	else:
		if type(save_to_csv) != str:
			raise ValueError("[save_to_csv]: Must be a str, current type = '{0}'".format(type(save_to_csv)))
		else:
			if not save_to_csv.lower().endswith(".csv"):
				raise ValueError("[save_to_csv]: Extension must be a .csv file, current extension = '{0}'".format(save_to_csv.split(".")[1]))

	if type(centerline_type) != str:
		raise ValueError("[centerline_type]: Must be a str, current type = '{0}'".format(type(centerline_type)))
	else:
		if centerline_type.title() not in centerline_type_options:
			raise ValueError("[centerline_type]: Must be an available option in {0}, current option = '{1}'".format(centerline_type_options, centerline_type))

	if type(coordinate_unit) != str:
		raise ValueError("[coordinate_unit]: Must be a str, current type = '{0}'".format(type(coordinate_unit)))
	else:
		coordinate_unit_options = ["Decimal Degrees", "Relative Distance"]
		if coordinate_unit.title() not in coordinate_unit_options:
			raise ValueError("[coordinate_unit]: Must be an available option in {0}, current option = '{1}'".format(coordinate_unit_options, coordinate_unit))

def errorHandlingSaveCenterlineMAT(river_object=None,
								latitude_header=None,
								longitude_header=None,
								save_to_mat=None,
								centerline_type=None,
								coordinate_unit=None):
	# Error Handling for saveCenterlineMAT()
	if river_object is None:
		raise ValueError("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")
	else:
		if not isinstance(river_object, centerline_width.riverCenterline):
			raise ValueError("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(type(river_object)))

	if latitude_header is not None:
		if type(latitude_header) != str:
			raise ValueError("[latitude_header]: Must be a str, current type = '{0}'".format(type(latitude_header)))
		if any(not character.isalnum() for character in latitude_header):
			raise ValueError("[latitude_header]: Column names cannot contain any whitespace or non-alphanumeric characters, currently = '{0}'".format(latitude_header))

	if longitude_header is not None:
		if type(longitude_header) != str:
			raise ValueError("[longitude_header]: Must be a str, current type = '{0}'".format(type(longitude_header)))
		if any(not character.isalnum() for character in longitude_header):
			raise ValueError("[longitude_header]: Column names cannot contain any whitespace or non-alphanumeric characters, currently = '{0}'".format(longitude_header))

	if save_to_mat is None:
		raise ValueError("\nCRITICAL ERROR, [save_to_mat]: Requires mat filename")
	else:
		if type(save_to_mat) != str:
			raise ValueError("[save_to_mat]: Must be a str, current type = '{0}'".format(type(save_to_mat)))
		else:
			if not save_to_mat.lower().endswith(".mat"):
				raise ValueError("[save_to_mat]: Extension must be a .mat file, current extension = '{0}'".format(save_to_mat.split(".")[1]))

	if type(centerline_type) != str:
		raise ValueError("[centerline_type]: Must be a str, current type = '{0}'".format(type(centerline_type)))
	else:
		if centerline_type.title() not in centerline_type_options:
			raise ValueError("[centerline_type]: Must be an available option in {0}, current option = '{1}'".format(centerline_type_options, centerline_type))

	if type(coordinate_unit) != str:
		raise ValueError("[coordinate_unit]: Must be a str, current type = '{0}'".format(type(coordinate_unit)))
	else:
		coordinate_unit_options = ["Decimal Degrees", "Relative Distance"]
		if coordinate_unit.title() not in coordinate_unit_options:
			raise ValueError("[coordinate_unit]: Must be an available option in {0}, current option = '{1}'".format(coordinate_unit_options, coordinate_unit))

# Error Handling: getCoordinatesKML.py
def errorHandlingExtractPointsToTextFile(left_kml=None, right_kml=None, text_output_name=None):
	# Error Handling for extractPointsToTextFile()
	if left_kml is None:
		raise ValueError("[left_kml]: Requires left_kml file")
	else:
		if type(left_kml) != str:
			raise ValueError("[left_kml]: Must be a str, current type = '{0}'".format(type(left_kml)))
		if not left_kml.lower().endswith(".kml"):
			raise ValueError("[left_kml]: Extension must be a .kml file, current extension = '{0}'".format(left_kml.split(".")[1]))

	if right_kml is None:
		raise ValueError("[right_kml]: Requires right_kml file")
	else:
		if type(right_kml) != str:
			raise ValueError("[right_kml]: Must be a str, current type = '{0}'".format(type(right_kml)))
		if not right_kml.lower().endswith(".kml"):
			raise ValueError("[right_kml]: Extension must be a .kml file, current extension = '{0}'".format(right_kml.split(".")[1]))

	if right_kml == left_kml:
		raise ValueError("right_kml and left_kml are set to the same file (needs a seperate left and right bank): right_kml='{0}' and left_kml='{1}'".format(right_kml, left_kml))

	if text_output_name is None:
		raise ValueError("[text_output_name]: Requires output file name")
	else:
		if type(text_output_name) != str:
			raise ValueError("[text_output_name]: Must be a str, current type = '{0}'".format(type(text_output_name)))

## Error Handling: riverCenterlineClass.py
def errorHandlingRiverCenterlineClass(csv_data=None,
									optional_cutoff=None,
									interpolate_data=None,
									interpolate_n=None,
									interpolate_n_centerpoints=None,
									equal_distance=None,
									ellipsoid=None):
	# Error Handling for riverCenterlineClass()
	if csv_data is None:
		raise ValueError("[csv_data]: Requires csv_data location")
	else:
		if type(csv_data) != str and not isinstance(csv_data, StringIO): 
			# StringIO accounts for testing against a StringIO instead of a CSV (used in pytests)
			raise ValueError("[csv_data]: Must be a str, current type = '{0}'".format(type(csv_data)))

	if optional_cutoff is not None:
		if type(optional_cutoff) != int:
			raise ValueError("[optional_cutoff]: Must be a int, current type = '{0}'".format(type(optional_cutoff)))

	if type(interpolate_data) != bool:
		raise ValueError("[interpolate_data]: Must be a bool, current type = '{0}'".format(type(interpolate_data)))

	if type(interpolate_n) != int:
		raise ValueError("[interpolate_n]: Must be a int, current type = '{0}'".format(type(interpolate_n)))
		if interpolate_n > 15:
			logger.warn("WARNING, [interpolate_n]: Setting interpolate_n above 15 will cause the code to execute exponentially slower")

	if interpolate_n_centerpoints is not None:
		if type(interpolate_n_centerpoints) != int:
			raise ValueError("[interpolate_n_centerpoints]: Must be a int, current type = '{0}'".format(type(interpolate_n_centerpoints)))
		else:
			if interpolate_n_centerpoints < 2:
				raise ValueError("[interpolate_n_centerpoints]: Must be a greater than 1, currently = '{0}'".format(interpolate_n_centerpoints))

	if type(equal_distance) != int and type(equal_distance) != float:
		raise ValueError("[equal_distance]: Must be a int or float, current type = '{0}'".format(type(equal_distance)))
		if equal_distance <= 0:
			raise ValueError("[equal_distance]: Must be a postive value, greater than 0, currently = '{0}'".format(equal_distance))

	ellipsoid_options = ["GRS80", "airy", "bessel", "clrk66", "intl", "WGS60", "WGS66", "WGS72", "WGS84", "sphere"]
	if type(ellipsoid) != str:
		raise ValueError("[ellipsoid]: Must be a str, current type = '{0}'".format(type(ellipsoid)))
	else:
		if ellipsoid not in ellipsoid_options:
			raise ValueError("[ellipsoid]: Must be an available option in {0}, current option = '{1}'".format(ellipsoid_options, ellipsoid))
