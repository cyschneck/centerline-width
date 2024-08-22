# Test Expected Error Messages from getCoordinatesKML.py
# centerline-width/: python3 -m pytest -v
# python -m pytest -k test_errorGetCoordinatesKML -xv

import re

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_str_options = [(1961, "<class 'int'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]

invalid_non_bool_options = [(1961, "<class 'int'>"),
                            (3.1415, "<class 'float'>"),
                            ([], "<class 'list'>"),
                            ("testing_string", "<class 'str'>")]


## kml_to_csv() #####################################################
def test_kmlToCSV_leftKMLRequired():
    with pytest.raises(ValueError,
                       match=re.escape("[left_kml]: Requires left_kml file")):
        centerline_width.kml_to_csv(left_kml=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_kmlToCSV_leftKMLInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[left_kml]: Must be a str, current type = '{error_output}'")
    ):
        centerline_width.kml_to_csv(left_kml=invalid_input)


def test_kmlToCSV_leftKMLInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[left_kml]: Extension must be a .kml file, current extension = 'txt'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.txt")


def test_kmlToCSV_rightKMLRequired():
    with pytest.raises(
            ValueError,
            match=re.escape("[right_kml]: Requires right_kml file")):
        centerline_width.kml_to_csv(left_kml="left_kml.kml", right_kml=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_kmlToCSV_rightKMLInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[right_kml]: Must be a str, current type = '{error_output}'")
    ):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml=invalid_input)


def test_kmlToCSV_rightKMLInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[right_kml]: Extension must be a .kml file, current extension = 'txt'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.txt")


def test_kmlToCSV_textOutputNameRequired():
    # Pending Deprecation
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[csv_output/text_output_name]: Requires output file name")):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    text_output_name=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_kmlToCSV_TxtOutputNameInvalidTypes(invalid_input, error_output):
    # Pending Deprecation
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[text_output_name]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    text_output_name=invalid_input)


def test_kmlToCSV_textOutputNameInvalidExtension():
    # Pending Deprecation
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[text_output_name]: Extension must be a .txt file, current extension = 'csv"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    text_output_name="csv_output.csv")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_kmlToCSV_CSVOutputNameInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[csv_output]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    csv_output=invalid_input)


def test_kmlToCSV_rightAndLeftKMLMatchInvalid():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "right_kml and left_kml are set to the same file (needs a separate left and right bank): right_kml='same_kml.kml' and left_kml='same_kml.kml'"
            )):
        centerline_width.kml_to_csv(left_kml="same_kml.kml",
                                    right_kml="same_kml.kml",
                                    csv_output=None)


def test_kmlToCSV_textFileRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                '[csv_output/text_output_name]: Requires output file name')):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    csv_output=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_kmlToCSV_textFileInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[csv_output]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    csv_output=invalid_input)


def test_kmlToCSV_textFileInvalidExtensions():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[csv_output]: Extension must be a .csv file, current extension = 'txt'"
            )):
        centerline_width.kml_to_csv(left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    csv_output="text_file.txt")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_bool_options)
def test_kmlToCSV_flipDirectionInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flip_direction]: Must be a bool, current type = '{error_output}'"
            )):
        centerline_width.kml_to_csv(csv_output="text_file.csv",
                                    left_kml="left_kml.kml",
                                    right_kml="right_kml.kml",
                                    flip_direction=invalid_input)


## txt_to_csv() #####################################################
def test_txtToCSV_txtInputRequired():
    with pytest.raises(ValueError,
                       match=re.escape("[txt_input]: Requires text file")):
        centerline_width.txt_to_csv(txt_input=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_txtToCSV_txtInputInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[txt_input]: Must be a str, current type = '{error_output}'")
    ):
        centerline_width.txt_to_csv(txt_input=invalid_input)


def test_txtToCSV_textFileInvalidExtensions():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[txt_input]: Extension must be a .txt file, current extension = 'csv'"
            )):
        centerline_width.txt_to_csv(txt_input="csv_file.csv")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_bool_options)
def test_txtToCSV_flipDirectionInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[flip_direction]: Must be a bool, current type = '{error_output}'"
            )):
        centerline_width.txt_to_csv(txt_input="text_file.txt",
                                    flip_direction=invalid_input)
