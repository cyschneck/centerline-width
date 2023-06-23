# Pytest for riverCenterlineClass.py
# centerline-width/: python3 -m pytest -v
import logging
from io import StringIO

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>")]

invalid_non_int_options = [("testing_string", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_num_options = [("testing_string", "<class 'str'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

## class riverCenterline #####################################################
def test_riverCenterline_csvDataRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [csv_data]: Requires csv_data location"

@pytest.mark.parametrize("csv_data_invalid, csv_data_error_output", invalid_non_str_options)
def test_riverCenterline_csvDataInvalidTypes(caplog, csv_data_invalid, csv_data_error_output):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data=csv_data_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [csv_data]: Must be a str, current type = '{0}'".format(csv_data_error_output)

@pytest.mark.parametrize("optional_cutoff_invalid, optional_cutoff_error_output", invalid_non_int_options)
def test_riverCenterline_optionalCutoffInvalidTypes(caplog, optional_cutoff_invalid, optional_cutoff_error_output):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data="csv_example.csv", optional_cutoff=optional_cutoff_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [optional_cutoff]: Must be a int, current type = '{0}'".format(optional_cutoff_error_output)

@pytest.mark.parametrize("interpolate_data_invalid, interpolate_data_error_output", invalid_non_bool_options)
def test_riverCenterline_interpolateDataInvalidTypes(caplog, interpolate_data_invalid, interpolate_data_error_output):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data="csv_example.csv", interpolate_data=interpolate_data_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [interpolate_data]: Must be a bool, current type = '{0}'".format(interpolate_data_error_output)

@pytest.mark.parametrize("interpolate_n_invalid, interpolate_n_error_output", invalid_non_int_options)
def test_riverCenterline_interpolateNInvalidTypes(caplog, interpolate_n_invalid, interpolate_n_error_output):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data="csv_example.csv", interpolate_n=interpolate_n_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [interpolate_n]: Must be a int, current type = '{0}'".format(interpolate_n_error_output)

@pytest.mark.parametrize("equal_distance_invalid, equal_distance_error_output", invalid_non_num_options)
def test_riverCenterline_equalDistanceInvalidTypes(caplog, equal_distance_invalid, equal_distance_error_output):
	with pytest.raises(SystemExit):
		centerline_width.riverCenterline(csv_data="csv_example.csv", equal_distance=equal_distance_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [equal_distance]: Must be a int or float, current type = '{0}'".format(equal_distance_error_output)
