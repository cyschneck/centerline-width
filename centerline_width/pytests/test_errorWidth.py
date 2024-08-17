# Test Expected Error Messages from width.py
# Pytest for centerline.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_errorWidth -xv

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

invalid_non_class_options = [(1961, "<class 'int'>"),
                             (3.1415, "<class 'float'>"),
                             ([], "<class 'list'>"),
                             ("testing_string", "<class 'str'>"),
                             (False, "<class 'bool'>")]

invalid_non_int_options = [("testing_string", "<class 'str'>"),
                           (3.1415, "<class 'float'>"), ([], "<class 'list'>"),
                           (False, "<class 'bool'>")]

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


## width() #####################################################
def test_width_riverObjectRequired():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[river_object]: Requires a river object (see: centerline_width.riverCenterline)"
            )):
        centerline_width.width(river_object=None)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_class_options)
def test_width_riverObjectInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'"
                .format(error_output))):
        centerline_width.width(river_object=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_int_options)
def test_width_transectSpanDistanceInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[transect_span_distance]: Must be a int, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               transect_span_distance=invalid_input)


def test_width_transectSpanDistanceInvalidRange():
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[transect_span_distance]: Must be greater than 2, currently = '1'"
            )):
        centerline_width.width(river_object=river_class_example,
                               transect_span_distance=1)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_width_transectSlopeInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[transect_slope]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               transect_slope=invalid_input)


def test_width_transectSlopeInvalidOption():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[transect_slope]: Must be an available option in ['Average', 'Direct'], current option = 'Invalid Option'"
            )):
        centerline_width.width(river_object=river_class_example,
                               transect_slope="Invalid Option")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_bool_options)
def test_width_applySmoothingInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[apply_smoothing]: Must be a bool, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               apply_smoothing=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_bool_options)
def test_width_removeIntersectionsInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[remove_intersections]: Must be a bool, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               remove_intersections=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_width_saveToCSVInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[save_to_csv]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               save_to_csv=invalid_input)


def test_width_csvInvalidExtension():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[save_to_csv]: Extension must be a .csv file, current extension = 'txt'"
            )):
        centerline_width.width(river_object=river_class_example,
                               save_to_csv="filename.txt")


def test_width_coordinateUnitInvalidOption():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'"
            )):
        centerline_width.width(river_object=river_class_example,
                               coordinate_unit="Invalid Option")


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_width_coordinateUnitInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[coordinate_unit]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               coordinate_unit=invalid_input)


@pytest.mark.parametrize("invalid_input, error_output",
                         invalid_non_str_options)
def test_width_coordinateReferenceInvalidTypes(invalid_input, error_output):
    with pytest.raises(
            ValueError,
            match=re.escape(
                f"[coordinate_reference]: Must be a str, current type = '{error_output}'"
            )):
        centerline_width.width(river_object=river_class_example,
                               coordinate_reference=invalid_input)


def test_width_coordinateReferenceInvalidOption():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "[coordinate_reference]: Must be an available option in ['Centerline', 'Banks'], current option = 'invalid centerline reference'"
            )):
        centerline_width.width(
            river_object=river_class_example,
            coordinate_reference="invalid centerline reference")
