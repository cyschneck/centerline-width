# Pytest for getCoordinatesKML.py
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


## extractPointsToTextFile() #####################################################
def test_extractPointsToTextFile_leftKMLRequired():
    with pytest.raises(ValueError,
                       match=re.escape("[left_kml]: Requires left_kml file")):
        centerline_width.extractPointsToTextFile(left_kml=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_plotCenterline_leftKMLInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[left_kml]: Must be a str, current type = '{error_output}'")
    ):
        centerline_width.extractPointsToTextFile(left_kml=invalid_input)


def test_extractPointsToTextFile_leftKMLInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[left_kml]: Extension must be a .kml file, current extension = 'txt'"
            )):
        centerline_width.extractPointsToTextFile(left_kml="left_kml.txt")


def test_extractPointsToTextFile_rightKMLRequired():
    with pytest.raises(
            ValueError,
            match=re.escape("[right_kml]: Requires right_kml file")):
        centerline_width.extractPointsToTextFile(left_kml="left_kml.kml",
                                                 right_kml=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_plotCenterline_rightKMLInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[right_kml]: Must be a str, current type = '{error_output}'")
    ):
        centerline_width.extractPointsToTextFile(left_kml="left_kml.kml",
                                                 right_kml=invalid_input)


def test_extractPointsToTextFile_rightKMLInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[right_kml]: Extension must be a .kml file, current extension = 'txt'"
            )):
        centerline_width.extractPointsToTextFile(left_kml="left_kml.kml",
                                                 right_kml="right_kml.txt")


def test_extractPointsToTextFile_textOutputNameRequired():
    with pytest.raises(
            ValueError,
            match=re.escape("[text_output_name]: Requires output file name")):
        centerline_width.extractPointsToTextFile(left_kml="left_kml.kml",
                                                 right_kml="right_kml.kml",
                                                 text_output_name=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_plotCenterline_textOutputNameInvalidTypes(invalid_input,
                                                   error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[text_output_name]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.extractPointsToTextFile(
            left_kml="left_kml.kml",
            right_kml="right_kml.kml",
            text_output_name=invalid_input)


def test_extractPointsToTextFile_rightAndLeftKMLMatchInvalid():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "right_kml and left_kml are set to the same file (needs a separate left and right bank): right_kml='same_kml.kml' and left_kml='same_kml.kml'"
            )):
        centerline_width.extractPointsToTextFile(left_kml="same_kml.kml",
                                                 right_kml="same_kml.kml",
                                                 text_output_name=None)
