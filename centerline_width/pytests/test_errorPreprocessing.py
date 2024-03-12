# Pytest for preprocessing.py
# centerline-width/: python3 -m pytest -v
import re

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

## convertColumnsToCSV() #####################################################
def test_convertColumnsToCSV_textFileRequired():
	with pytest.raises(ValueError, match=re.escape('[text_file]: Requires text file')):
		centerline_width.convertColumnsToCSV(text_file=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_convertColumnsToCSV_textFileInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[text_file]: Must be a str, current type = '{error_output}'")):
		centerline_width.convertColumnsToCSV(text_file=invalid_input)

def test_convertColumnsToCSV_textFileInvalidExtensions():
	with pytest.raises(ValueError, match=re.escape("[text_file]: Extension must be a .txt file, current extension = 'csv'")):
		centerline_width.convertColumnsToCSV(text_file="text_file.csv")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_convertColumnsToCSV_flipBankDirectionInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[flipBankDirection]: Must be a bool, current type = '{error_output}'")):
		centerline_width.convertColumnsToCSV(text_file="text_file.txt", flipBankDirection=invalid_input)
