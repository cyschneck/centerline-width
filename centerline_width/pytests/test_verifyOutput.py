# Pytests to Compare and Verify Expected Outputs
from io import StringIO

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width

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
	assert test_river.centerlineLength == 1.3534252753108382

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
		(-4.2628112256127935, 48.282290840533314): 0.4835174179290038,
	}
