# Pytest for riverCenterlineClass.py
# centerline-width/: python -m pytest -v
from io import StringIO
import re

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
def test_riverCenterline_csvDataRequired():
	with pytest.raises(ValueError, match=re.escape("[csv_data]: Requires csv_data location")):
		centerline_width.riverCenterline(csv_data=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_riverCenterline_csvDataInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[csv_data]: Must be a str, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_riverCenterline_optionalCutoffInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[optional_cutoff]: Must be a int, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", optional_cutoff=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_riverCenterline_interpolateDataInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[interpolate_data]: Must be a bool, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", interpolate_data=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_riverCenterline_interpolateNInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[interpolate_n]: Must be a int, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", interpolate_n=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_num_options)
def test_riverCenterline_equalDistanceInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[equal_distance]: Must be a int or float, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", equal_distance=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", [(-1, -1), (0, 0)])
def test_riverCenterline_equalDistanceInvalidRange(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[equal_distance]: Must be a positive value, greater than 0, currently = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", equal_distance=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_riverCenterline_ellipsoidInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[ellipsoid]: Must be a str, current type = '{error_output}'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", ellipsoid=invalid_input)

def test_riverCenterline_ellipsoidInvalidOptions():
	with pytest.raises(ValueError, match=re.escape("[ellipsoid]: Must be an available option in ['GRS80', 'airy', 'bessel', 'clrk66', 'intl', 'WGS60', 'WGS66', 'WGS72', 'WGS84', 'sphere'], current option = 'invalid'")):
		centerline_width.riverCenterline(csv_data="csv_example.csv", ellipsoid="invalid")
