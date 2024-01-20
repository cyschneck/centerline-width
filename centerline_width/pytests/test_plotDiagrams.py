# Pytest for plotDiagram.py
# centerline-width/: python3 -m pytest -v
from io import StringIO
import re

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

invalid_non_class_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>"),
						(False, "<class 'bool'>")]

invalid_non_bool_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						("testing_string", "<class 'str'>")]

invalid_non_int_options = [("testing_string", "<class 'str'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

def river_class_object():
	# Example csv file created in StringIO
	csv_example = StringIO()
	csv_example.write("llat,llon,rlat,rlon\n")
	csv_example.write("30.037581,-92.868569,30.037441,-92.867476\n")
	csv_example.write("30.137581,-92.868569,30.037441,-92.867476\n")
	csv_example.write("30.237581,-92.868569,30.037441,-92.867476\n")
	csv_example.seek(0)
	return centerline_width.riverCenterline(csv_data=csv_example)

river_class_example = river_class_object()

## plotCenterline() #####################################################
def test_plotCenterline_riverObjectRequired():
	with pytest.raises(ValueError, match=re.escape("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")):
		centerline_width.plotCenterline(river_object=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_class_options)
def test_plotCenterline_riverObjectInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(error_output))):
		centerline_width.plotCenterline(river_object=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_centerlineTypeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[centerline_type]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										centerline_type=invalid_input)

def test_plotCenterline_centerlineTypeInvalidOption():
	with pytest.raises(ValueError, match=re.escape("[centerline_type]: Must be an available option in ['Voronoi', 'Evenly Spaced', 'Smoothed', 'Equal Distance'], current option = 'invalid centerline'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										centerline_type="invalid centerline")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_markerTypeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[marker_type]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										marker_type=invalid_input)

def test_plotCenterline_markerTypeInvalidOption():
	with pytest.raises(ValueError, match=re.escape("[marker_type]: Must be an available option in ['Line', 'Scatter'], current option = 'invalid marker'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										marker_type="invalid marker")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_centerlineColorInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[centerline_color]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										centerline_color=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterline_darkModeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[dark_mode]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										dark_mode=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterline_displayAllPossiblePathsInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[display_all_possible_paths]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
											display_all_possible_paths=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_plotTitleInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[plot_title]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										plot_title=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_savePlotNameInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[save_plot_name]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										save_plot_name=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterline_displayVoronoiInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[display_voronoi]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										display_voronoi=invalid_input)

def test_plotCenterline_coordinateUnitInvalidOption():
	with pytest.raises(ValueError, match=re.escape("[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										coordinate_unit="Invalid Option")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterline_coordinateUnitInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[coordinate_unit]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterline(river_object=river_class_example,
										coordinate_unit=invalid_input)

## plotCenterlineWidth() #####################################################
def test_plotCenterlineWidth_riverObjectRequired():
	with pytest.raises(ValueError, match=re.escape("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")):
		centerline_width.plotCenterlineWidth(river_object=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_class_options)
def test_plotCenterlineWidth_riverObjectInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(error_output))):
		centerline_width.plotCenterlineWidth(river_object=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterlineWidth_plotTitleInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[plot_title]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											plot_title=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterlineWidth_savePlotNameInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[save_plot_name]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											save_plot_name=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_displayTrueCenterlineInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[display_true_centerline]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											display_true_centerline=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_plotCenterlineWidth_transectSpanDistanceInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[transect_span_distance]: Must be a int, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											transect_span_distance=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_applySmoothingInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[apply_smoothing]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											apply_smoothing=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_flagIntersectionsInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[flag_intersections]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											flag_intersections=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_removeIntersectionsInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[remove_intersections]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											remove_intersections=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_plotCenterlineWidth_darkModeInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[dark_mode]: Must be a bool, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
											dark_mode=invalid_input)

def test_plotCenterlineWidth_coordinateUnitInvalidOption():
	with pytest.raises(ValueError, match=re.escape("[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
										coordinate_unit="Invalid Option")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_plotCenterlineWidth_coordinateUnitInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape(f"[coordinate_unit]: Must be a str, current type = '{error_output}'")):
		centerline_width.plotCenterlineWidth(river_object=river_class_example,
										coordinate_unit=invalid_input)
