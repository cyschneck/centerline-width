# Pytest for preprocessing.py
# centerline-width/: python3 -m pytest -v
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
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
						(False, "<class 'bool'>")]

invalid_non_str_options = [(1961, "<class 'int'>"),
						(3.1415, "<class 'float'>"),
						([], "<class 'list'>"),
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

## riverWidthFromCenterlineCoordinates() #####################################################
def test_riverWidthFromCenterline_riverObjectRequired():
	with pytest.raises(ValueError, match=re.escape("[river_object]: Requires a river object (see: centerline_width.riverCenterline)")):
		centerline_width.riverWidthFromCenterline(river_object=None)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_class_options)
def test_riverWidthFromCenterline_riverObjectInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[river_object]: Must be a river object (see: centerline_width.riverCenterline), current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_int_options)
def test_riverWidthFromCenterline_transectSpanDistanceInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[transect_span_distance]: Must be a int, current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
											transect_span_distance=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_riverWidthFromCenterline_applySmoothingInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[apply_smoothing]: Must be a bool, current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
											apply_smoothing=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_bool_options)
def test_riverWidthFromCenterline_removeIntersectionsInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[remove_intersections]: Must be a bool, current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
											remove_intersections=invalid_input)

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_riverWidthFromCenterline_saveToCSVInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[save_to_csv]: Must be a str, current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
											save_to_csv=invalid_input)

def test_riverWidthFromCenterline_csvInvalidExtension():
	with pytest.raises(ValueError, match=re.escape("[save_to_csv]: Extension must be a .csv file, current extension = 'txt'")):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
												save_to_csv="filename.txt")

def test_riverWidthFromCenterline_coordinateUnitInvalidOption():
	with pytest.raises(ValueError, match=re.escape("[coordinate_unit]: Must be an available option in ['Decimal Degrees', 'Relative Distance'], current option = 'Invalid Option'")):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
										coordinate_unit="Invalid Option")

@pytest.mark.parametrize("invalid_input, error_output", invalid_non_str_options)
def test_riverWidthFromCenterline_coordinateUnitInvalidTypes(invalid_input, error_output):
	with pytest.raises(ValueError, match=re.escape("[coordinate_unit]: Must be a str, current type = '{0}'".format(error_output))):
		centerline_width.riverWidthFromCenterline(river_object=river_class_example,
										coordinate_unit=invalid_input)

def test_riverCenterline_centerlineLength():
	csv_example = StringIO()
	csv_example.write("llat,llon,rlat,rlon\n")
	csv_example.write("48.286399957085024,-4.259939230629442,48.28244110043403,-4.255739731090472\n")
	csv_example.write("48.28500274859866,-4.2625639178417885,48.280578002893776,-4.2602891889242755\n")
	csv_example.write("48.283954817150175,-4.265713542496371,48.28011221789134,-4.265888521643745\n")
	csv_example.write("48.283954817150175,-4.26833822970741,48.28011221789134,-4.2711378960671595\n")
	csv_example.write("48.28558492344624,-4.271312875214591,48.28244110043403,-4.276212291343171\n")
	csv_example.write("48.287447838366376,-4.27393756242688,48.28581779152722,-4.278836978555489\n")
	csv_example.seek(0)
	test_river = centerline_width.riverCenterline(csv_data=csv_example)
	assert test_river.centerlineLength == 1.3534252753118123

def test_riverWidthFromCenterline():
	csv_example = StringIO()
	csv_example.write("llat,llon,rlat,rlon\n")
	csv_example.write("48.286399957085024,-4.259939230629442,48.28244110043403,-4.255739731090472\n")
	csv_example.write("48.28500274859866,-4.2625639178417885,48.280578002893776,-4.2602891889242755\n")
	csv_example.write("48.283954817150175,-4.265713542496371,48.28011221789134,-4.265888521643745\n")
	csv_example.write("48.283954817150175,-4.26833822970741,48.28011221789134,-4.2711378960671595\n")
	csv_example.write("48.28558492344624,-4.271312875214591,48.28244110043403,-4.276212291343171\n")
	csv_example.write("48.287447838366376,-4.27393756242688,48.28581779152722,-4.278836978555489\n")
	csv_example.seek(0)
	test_river = centerline_width.riverCenterline(csv_data=csv_example)
	river_width_dict = test_river.riverWidthFromCenterline()
	assert river_width_dict == {
		(-4.271614588856146, 48.282642262514564): 0.5026142454914809,
		(-4.2628112256127935, 48.282290840533314): 0.48351741792900327,
	}
