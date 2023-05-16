# Pytest for preprocessing.py
# centerline-width/: python3 -m pytest centerline_width/pytests/ -v
import logging

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>")]

## convertColumnsToCSV() #####################################################
def test_convertColumnsToCSV_textFileRequired(caplog):
	with pytest.raises(SystemExit):
		centerline_width.convertColumnsToCSV(text_file=None)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [text_file]: Requires text file"

@pytest.mark.parametrize("text_file_invalid, text_file_error_output", invalid_non_str_options)
def test_convertColumnsToCSV_textFileInvalidTypes(caplog, text_file_invalid, text_file_error_output):
	with pytest.raises(SystemExit):
		centerline_width.convertColumnsToCSV(text_file=text_file_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [text_file]: Must be a str, current type = '{0}'".format(text_file_error_output)

def test_convertColumnsToCSV_textFileInvalidExtensions(caplog):
	with pytest.raises(SystemExit):
		centerline_width.convertColumnsToCSV(text_file="text_file.csv")
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [text_file]: Extension must be a .txt file, current extension = 'csv'"

@pytest.mark.parametrize("flipBankDirection_invalid, flipBankDirection_error_output", invalid_non_bool_options)
def test_convertColumnsToCSV_flipBankDirectionInvalidTypes(caplog, flipBankDirection_invalid, flipBankDirection_error_output):
	with pytest.raises(SystemExit):
		centerline_width.convertColumnsToCSV(text_file="text_file.txt", flipBankDirection=flipBankDirection_invalid)
	log_record = caplog.records[0]
	assert log_record.levelno == logging.CRITICAL
	assert log_record.message == "\nCRITICAL ERROR, [flipBankDirection]: Must be a bool, current type = '{0}'".format(flipBankDirection_error_output)
