# Verify Outputs from width.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifyWidth.py -xv

# Pytests to Compare and Verify Expected Outputs
import re
from io import StringIO

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


def generate_testRiver():
    csv_example = StringIO()
    csv_example.write("llat,llon,rlat,rlon\n")
    csv_example.write(
        "48.286399957085044,-4.259939230629442,48.28244110043403,-4.255739731090472\n"
    )
    csv_example.write(
        "48.2850027485986,-4.2625639178417885,48.280578002893776,-4.2602891889242755\n"
    )
    csv_example.write(
        "48.283954817150175,-4.265713542496371,48.28011221789134,-4.265888521643745\n"
    )
    csv_example.write(
        "48.283954817160175,-4.26833822970741,48.28011221789134,-4.2711378960671595\n"
    )
    csv_example.write(
        "48.28558492344624,-4.271312875214591,48.28244110043403,-4.276212291343171\n"
    )
    csv_example.write(
        "49.287447838366376,-4.27393756242688,48.28581779152722,-4.278836978555489\n"
    )
    csv_example.seek(0)

    return centerline_width.CenterlineWidth(csv_data=csv_example)


def generate_expectedCenterline(span_distance=None):
    # group points inclusive of previous point: [A, B, C, D] = [A, B], [B, C], [C, D]
    groups_of_n_points = []
    for i in range(0, len(test_river.centerline_evenly_spaced), span_distance):
        if i == 0:
            groups_of_n_points.append(
                test_river.centerline_evenly_spaced[0:span_distance])
        else:
            groups_of_n_points.append(
                test_river.centerline_evenly_spaced[i - 1:i + span_distance])

    centerline_slope_expected = []
    for group_points in groups_of_n_points:
        middle_of_list = (len(group_points) + 1) // 2
        centerline_slope_expected.append(group_points[middle_of_list])
    return centerline_slope_expected


## width() #####################################################
test_river = generate_testRiver()
span_distance = 3
centerline_slope_expected = generate_expectedCenterline(span_distance)


def test_width_transectSlopeAverage_RelativeCenterline():
    river_width_dict = test_river.width(transect_slope="Average",
                                        transect_span_distance=span_distance,
                                        coordinate_reference="Centerline",
                                        apply_smoothing=False)
    # Verify same keys are used
    assert list(
        river_width_dict.keys()) == pytest.approx(centerline_slope_expected)
    # Verify output
    assert river_width_dict == pytest.approx({
        (-4.269872495291112, 48.28213146317461):
        0.515263253111841,
        (-4.263272551474902, 48.281909175456114):
        0.47396221154877105
    })


def test_width_transectSlopeDirect_RelativeCenterline():
    river_width_dict = test_river.width(transect_slope="Direct",
                                        transect_span_distance=span_distance,
                                        coordinate_reference="Centerline",
                                        apply_smoothing=False)
    # Verify same keys are used
    assert list(
        river_width_dict.keys()) == pytest.approx(centerline_slope_expected)
    # Verify output
    assert river_width_dict == pytest.approx({
        (-4.269872495291112, 48.28213146317461):
        0.515263253111841,
        (-4.263272551474902, 48.281909175456114):
        0.47396221154877105
    })


def test_width_futureWarning_functionName():
    # Pending Deprecation: TO BE REMOVED
    with pytest.warns(
            FutureWarning,
            match=re.escape(
                "riverWidthFromCenterline() has been replaced with width() and will be removed in the future"
            )):
        river_width_dict = test_river.riverWidthFromCenterline(
            transect_slope="Average",
            transect_span_distance=span_distance,
            coordinate_reference="Centerline",
            apply_smoothing=False)
        # Verify same keys are used
        assert list(river_width_dict.keys()) == pytest.approx(
            centerline_slope_expected)
        # Verify output
        assert river_width_dict == pytest.approx({
            (-4.269872495291112, 48.28213146317461):
            0.515263253111841,
            (-4.263272551474902, 48.281909175456114):
            0.47396221154877105
        })
