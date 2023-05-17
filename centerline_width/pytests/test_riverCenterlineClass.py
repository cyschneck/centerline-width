# Pytest for riverCenterlineClass.py
# centerline-width/: python3 -m pytest -v
import logging
from io import StringIO

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_int_options = [("testing_string", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
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
