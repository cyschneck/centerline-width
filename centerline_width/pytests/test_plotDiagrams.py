# Pytest for plotDiagram.py
# centerline-width/: python3 -m pytest -v
import logging
from io import StringIO

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_class_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>"),
						(False, "<class 'bool'>")]

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>")]

invalid_non_int_options = [("testing_string", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

def river_class_object():
	# Example csv file created in StringIO
	csv_example = StringIO()
	csv_example.write("llat,llon,rlat,rlon\n")
	csv_example.write("30.037581,-92.868569,30.037441,-92.867476\n")
	csv_example.write("30.137581,-92.868569,30.037441,-92.867476\n")
	csv_example.write("30.237581,-92.868569,30.037441,-92.867476\n")
	csv_example.seek(0)
	return centerline_width.riverCenterline(csv_data=csv_example)

river_class_example = river_class_object()

## plotCenterline() #####################################################
def test_plotCenterline_riverObjectRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)"

@pytest.mark.parametrize("river_object_invalid, river_object_error_output", invalid_non_class_options)
def test_plotCenterline_riverObjectInvalidTypes(caplog, river_object_invalid, river_object_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=river_object_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(river_object_error_output)

@pytest.mark.parametrize("display_all_possible_paths_invalid, display_all_possible_paths_error_output", invalid_non_bool_options)
def test_plotCenterline_displayAllPossiblePathsInvalidTypes(caplog, display_all_possible_paths_invalid, display_all_possible_paths_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=river_class_example,
											display_all_possible_paths=display_all_possible_paths_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [display_all_possible_paths]: Must be a bool, current type = '{0}'".format(display_all_possible_paths_error_output)

@pytest.mark.parametrize("plot_title_invalid, plot_title_error_output", invalid_non_str_options)
def test_plotCenterline_plotTitleInvalidTypes(caplog, plot_title_invalid, plot_title_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=river_class_example,
										plot_title=plot_title_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [plot_title]: Must be a str, current type = '{0}'".format(plot_title_error_output)

@pytest.mark.parametrize("save_plot_name_invalid, save_plot_name_error_output", invalid_non_str_options)
def test_plotCenterline_savePlotNameInvalidTypes(caplog, save_plot_name_invalid, save_plot_name_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=river_class_example,
										save_plot_name=save_plot_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [save_plot_name]: Must be a str, current type = '{0}'".format(save_plot_name_error_output)

@pytest.mark.parametrize("display_voronoi_name_invalid, display_voronoi_error_output", invalid_non_bool_options)
def test_plotCenterline_displayVoronoiInvalidTypes(caplog, display_voronoi_name_invalid, display_voronoi_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterline(river_object=river_class_example,
										display_voronoi=display_voronoi_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [display_voronoi]: Must be a bool, current type = '{0}'".format(display_voronoi_error_output)

## plotCenterlineWidth() #####################################################
def test_plotCenterlineWidth_riverObjectRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [river_object]: Requires a river object (see: centerline_width.riverCenterline)"

@pytest.mark.parametrize("river_object_invalid, river_object_error_output", invalid_non_class_options)
def test_plotCenterlineWidth_riverObjectInvalidTypes(caplog, river_object_invalid, river_object_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_object_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(river_object_error_output)

@pytest.mark.parametrize("plot_title_invalid, plot_title_error_output", invalid_non_str_options)
def test_plotCenterlineWidth_plotTitleInvalidTypes(caplog, plot_title_invalid, plot_title_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											plot_title=plot_title_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [plot_title]: Must be a str, current type = '{0}'".format(plot_title_error_output)

@pytest.mark.parametrize("save_plot_name_invalid, save_plot_name_error_output", invalid_non_str_options)
def test_plotCenterlineWidth_savePlotNameInvalidTypes(caplog, save_plot_name_invalid, save_plot_name_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											save_plot_name=save_plot_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [save_plot_name]: Must be a str, current type = '{0}'".format(save_plot_name_error_output)

@pytest.mark.parametrize("display_true_centerline_invalid, display_true_centerline_error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_displayTrueCenterlineInvalidTypes(caplog, display_true_centerline_invalid, display_true_centerline_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											display_true_centerline=display_true_centerline_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [display_true_centerline]: Must be a bool, current type = '{0}'".format(display_true_centerline_error_output)

@pytest.mark.parametrize("transect_span_distance_invalid, transect_span_distance_error_output", invalid_non_int_options)
def test_plotCenterlineWidth_transectSpanDistanceInvalidTypes(caplog, transect_span_distance_invalid, transect_span_distance_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											transect_span_distance=transect_span_distance_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [transect_span_distance]: Must be a int, current type = '{0}'".format(transect_span_distance_error_output)

@pytest.mark.parametrize("apply_smoothing_invalid, apply_smoothing_error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_applySmoothingInvalidTypes(caplog, apply_smoothing_invalid, apply_smoothing_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											apply_smoothing=apply_smoothing_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [apply_smoothing]: Must be a bool, current type = '{0}'".format(apply_smoothing_error_output)

@pytest.mark.parametrize("flag_intersections_invalid, flag_intersections_error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_flagIntersectionsInvalidTypes(caplog, flag_intersections_invalid, flag_intersections_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											flag_intersections=flag_intersections_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flag_intersections]: Must be a bool, current type = '{0}'".format(flag_intersections_error_output)

@pytest.mark.parametrize("remove_intersections_invalid, remove_intersections_error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_removeIntersectionsInvalidTypes(caplog, remove_intersections_invalid, remove_intersections_error_output):
	with pytest.raises(SystemExit):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											remove_intersections=remove_intersections_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [remove_intersections]: Must be a bool, current type = '{0}'".format(remove_intersections_error_output)
