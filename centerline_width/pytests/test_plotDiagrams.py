# Pytest for plotDiagram.py
# centerline-width/: python3 -m pytest centerline_width/pytests/ -v
import logging

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

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

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
def test_plotCenterline_displayAllPossiblePathsInvalidTypes(caplog, mocker, display_all_possible_paths_invalid, display_all_possible_paths_error_output):
	with pytest.raises(SystemExit):
		mock_river_object = mocker.patch("centerline_width.riverCenterline") # mock an instance of the riverCenterline class
		centerline_width.plotCenterline(river_object=mock_river_object,
										display_all_possible_paths=display_all_possible_paths_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [display_all_possible_paths]: Must be a bool, current type = '{0}'".format(display_all_possible_paths_error_output)

@pytest.mark.parametrize("plot_title_invalid, plot_title_error_output", invalid_non_str_options)
def test_plotCenterline_plotTitleInvalidTypes(caplog, mocker, plot_title_invalid, plot_title_error_output):
	with pytest.raises(SystemExit):
		mock_river_object = mocker.patch("centerline_width.riverCenterline") # mock an instance of the riverCenterline class
		centerline_width.plotCenterline(river_object=mock_river_object,
										plot_title=plot_title_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [plot_title]: Must be a str, current type = '{0}'".format(plot_title_error_output)

@pytest.mark.parametrize("display_voronoi_name_invalid, display_voronoi_error_output", invalid_non_bool_options)
def test_plotCenterline_displayVoronoiInvalidTypes(caplog, mocker, display_voronoi_name_invalid, display_voronoi_error_output):
	with pytest.raises(SystemExit):
		mock_river_object = mocker.patch("centerline_width.riverCenterline") # mock an instance of the riverCenterline class
		centerline_width.plotCenterline(river_object=mock_river_object,
										display_voronoi=display_voronoi_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [display_voronoi]: Must be a bool, current type = '{0}'".format(display_voronoi_error_output)

## plotCenterlineWidth() #####################################################
