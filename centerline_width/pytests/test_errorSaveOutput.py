# Test Expected Error Messages from saveOutput.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_errorSaveOutput -xv

from io import StringIO
import re

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_str_options = [(1961, "<class 'int'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]


def river_class_object():
    csv_example = StringIO()
    csv_example.write("llat,llon,rlat,rlon\n")
    csv_example.write("30.037581,-92.868569,30.037441,-92.867476\n")
    csv_example.write("30.137581,-92.868569,30.037441,-92.867476\n")
    csv_example.write("30.237581,-92.868569,30.037441,-92.867476\n")
    csv_example.seek(0)
    return centerline_width.riverCenterline(csv_data=csv_example)


river_class_example = river_class_object()


## saveCenterlineCSV() #####################################################
def test_saveCenterlineCSV_riverObjectRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[river_object]: Requires a river object (see: centerline_width.riverCenterline)"
            )):
        centerline_width.saveCenterlineCSV(river_object=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_riverObjectInvalidType(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=invalid_input)


def test_saveCenterlineCSV_csvInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape("[save_to_csv]: Requires csv filename")):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_csvInvalidType(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[save_to_csv]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv=invalid_input)


def test_saveCenterlineCSV_csvRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[save_to_csv]: Extension must be a .csv file, current extension = 'txt'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="filename.txt")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_latitudeHeaderTypeInvalidTypes(
        invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[latitude_header]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           latitude_header=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_longitudeHeaderTypeInvalidTypes(
        invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[longitude_header]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           longitude_header=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_centerlineTypeInvalidTypes(invalid_input,
                                                      error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[centerline_type]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           centerline_type=invalid_input)


def test_saveCenterlineCSV_centerlineTypeInvalidOptions():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[centerline_type]: Must be an available option in ['Voronoi', 'Evenly Spaced', 'Smoothed', 'Equal Distance'], current option = 'not valid'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           centerline_type="not valid")


def test_saveCenterlineCSV_coordinateUnitInvalidOption():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           coordinate_unit="Invalid Option")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineCSV_coordinateTypeInvalidTypes(invalid_input,
                                                      error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"coordinate_unit]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineCSV(river_object=river_class_example,
                                           save_to_csv="testing.csv",
                                           coordinate_unit=invalid_input)


## saveCenterlineMAT() #####################################################
def test_saveCenterlineMAT_riverObjectRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[river_object]: Requires a river object (see: centerline_width.riverCenterline)"
            )):
        centerline_width.saveCenterlineMAT(river_object=None)


def test_saveCenterlineMAT_matInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape("[save_to_mat]: Requires mat filename")):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineMAT_matInvalidType(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[save_to_mat]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat=invalid_input)


def test_saveCenterlineMAT_matRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[save_to_mat]: Extension must be a .mat file, current extension = 'txt'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="filename.txt")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineMAT_latitudeHeaderTypeInvalidTypes(
        invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[latitude_header]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           latitude_header=invalid_input)


def test_saveCenterlineMAT_latitudeHeaderTypeInvalidAlphanumeric():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[latitude_header]: Column names cannot contain any whitespace or non-alphanumeric characters, currently = 'invalid whitespace'"
            )):
        centerline_width.saveCenterlineMAT(
            river_object=river_class_example,
            save_to_mat="testing.mat",
            latitude_header="invalid whitespace")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineMAT_longitudeHeaderTypeInvalidTypes(
        invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[longitude_header]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           longitude_header=invalid_input)


def test_saveCenterlineMAT_longitudeHeaderTypeInvalidAlphanumeric():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[longitude_header]: Column names cannot contain any whitespace or non-alphanumeric characters, currently = 'invalid whitespace'"
            )):
        centerline_width.saveCenterlineMAT(
            river_object=river_class_example,
            save_to_mat="testing.mat",
            longitude_header="invalid whitespace")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineMAT_centerlineTypeInvalidTypes(invalid_input,
                                                      error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[centerline_type]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           centerline_type=invalid_input)


def test_saveCenterlineMAT_centerlineTypeInvalidOptions():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[centerline_type]: Must be an available option in ['Voronoi', 'Evenly Spaced', 'Smoothed', 'Equal Distance'], current option = 'not valid'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           centerline_type="not valid")


def test_saveCenterlineMAT_coordinateUnitInvalidOption():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           coordinate_unit="Invalid Option")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_saveCenterlineMAT_coordinateUnitInvalidTypes(invalid_input,
                                                      error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[coordinate_unit]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.saveCenterlineMAT(river_object=river_class_example,
                                           save_to_mat="testing.mat",
                                           coordinate_unit=invalid_input)
