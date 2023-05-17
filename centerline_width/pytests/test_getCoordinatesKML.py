# Pytest for getCoordinatesKML.py
# centerline-width/: python3 -m pytest -v
import logging

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

## extractPointsToTextFile() #####################################################
def test_extractPointsToTextFile_leftKMLRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.extractPointsToTextFile(left_kml=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [left_kml]: Requires left_kml file"

@pytest.mark.parametrize("left_kml_invalid, left_kml_error_output", invalid_non_str_options)
def test_plotCenterline_leftKMLInvalidTypes(caplog, left_kml_invalid, left_kml_error_output):
	with pytest.raises(SystemExit):
			centerline_width.extractPointsToTextFile(left_kml=left_kml_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [left_kml]: Must be a str, current type = '{0}'".format(left_kml_error_output)

def test_extractPointsToTextFile_leftKMLInvalidExtension(caplog):
	with pytest.raises(SystemExit):
		centerline_width.extractPointsToTextFile(left_kml="left_kml.txt")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [left_kml]: Extension must be a .kml file, current extension = 'txt'"

def test_extractPointsToTextFile_rightKMLRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.extractPointsToTextFile(left_kml="left_kml.kml", right_kml=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [right_kml]: Requires right_kml file"

@pytest.mark.parametrize("right_kml_invalid, right_kml_error_output", invalid_non_str_options)
def test_plotCenterline_rightKMLInvalidTypes(caplog, right_kml_invalid, right_kml_error_output):
	with pytest.raises(SystemExit):
			centerline_width.extractPointsToTextFile(left_kml="left_kml.kml", right_kml=right_kml_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [right_kml]: Must be a str, current type = '{0}'".format(right_kml_error_output)

def test_extractPointsToTextFile_rightKMLInvalidExtension(caplog):
	with pytest.raises(SystemExit):
		centerline_width.extractPointsToTextFile(left_kml="left_kml.kml", right_kml="right_kml.txt")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [right_kml]: Extension must be a .kml file, current extension = 'txt'"

def test_extractPointsToTextFile_textOutputNameRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.extractPointsToTextFile(left_kml="left_kml.kml", right_kml="right_kml.kml", text_output_name=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [text_output_name]: Requires output file name"

@pytest.mark.parametrize("text_output_name_invalid, text_output_name_error_output", invalid_non_str_options)
def test_plotCenterline_textOutputNameInvalidTypes(caplog, text_output_name_invalid, text_output_name_error_output):
	with pytest.raises(SystemExit):
			centerline_width.extractPointsToTextFile(left_kml="left_kml.kml", right_kml="right_kml.kml", text_output_name=text_output_name_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [text_output_name]: Must be a str, current type = '{0}'".format(text_output_name_error_output)
