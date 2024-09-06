# Verify Outputs from saveOutput.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifySaveOutput.py -xv

# Pytests to Compare and Verify Expected Outputs
import re
from io import StringIO

# External Python libraries (installed via pip install)
import pytest
import pandas as pd
import scipy.io as sio

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


def river_class_object():
    csv_example = StringIO()
    csv_example.write("llat,llon,rlat,rlon\n")
    csv_example.write(
        "30.03758064742554,-92.86856870164003,30.03744106431763,-92.867475846432\n"
    )
    csv_example.write(
        "30.03761289873068,-92.86854932864129,30.03744779451432,-92.86747357248917\n"
    )
    csv_example.write(
        "30.03764767910492,-92.86854615646305,30.03748158510661,-92.86744912321454\n"
    )
    csv_example.write(
        "30.03767440933011,-92.86853555132092,30.03750644719021,-92.86743200196584\n"
    )
    csv_example.write(
        "30.03770236278642,-92.8685329553435,30.03752454918347,-92.86743019872145\n"
    )
    csv_example.write(
        "30.03772919351539,-92.86852225012414,30.0375426005056,-92.8674152219088\n"
    )
    csv_example.write(
        "30.0377490549762,-92.86851215967346,30.0375721590616,-92.8674007572212\n"
    )
    csv_example.write(
        "30.03778301480612,-92.86850070336355,30.03760885519144,-92.86738399853574\n"
    )
    csv_example.write(
        "30.03781601910584,-92.86848128471483,30.03763647218977,-92.86736152540908\n"
    )
    csv_example.write(
        "30.03784317873953,-92.86847053431235,30.0376710739572,-92.86733658820407\n"
    )
    csv_example.write(
        "30.03787040125924,-92.8684597471607,30.03771036353054,-92.86730115646196\n"
    )
    csv_example.write(
        "30.03790600092315,-92.86845640697538,30.0377475921359,-92.86728394049267\n"
    )
    csv_example.write(
        "30.0379404991904,-92.86844485391589,30.03778027570281,-92.86726385834064\n"
    )
    csv_example.write(
        "30.03796197755238,-92.86844283088163,30.03779189842327,-92.86725099533921\n"
    )
    csv_example.write(
        "30.03801823414788,-92.86842918514924,30.03782231186275,-92.86723594951347\n"
    )
    csv_example.write(
        "30.03804707600122,-92.8684264587786,30.03785992478739,-92.86721837516968\n"
    )
    csv_example.write(
        "30.03807720971334,-92.86843197572428,30.0378789421227,-92.86721621096019\n"
    )
    csv_example.write(
        "30.03811467808153,-92.86843682562265,30.03791228279507,-92.86720907194727\n"
    )
    csv_example.write(
        "30.03814498173742,-92.86844237100571,30.03794600661214,-92.86720200245374\n"
    )
    csv_example.write(
        "30.03817536147593,-92.8684479304092,30.03798495119786,-92.86719775057487\n"
    )
    csv_example.write(
        "30.03821313704282,-92.86845282481077,30.03800676992721,-92.86719028007494\n"
    )
    csv_example.write(
        "30.03825342965967,-92.86847428143609,30.03803846552586,-92.86718833685659\n"
    )
    csv_example.write(
        "30.03827667158946,-92.8684805380621,30.038070336302,-92.86718638873742\n"
    )
    csv_example.write(
        "30.03831604066361,-92.86849386447184,30.03810236991961,-92.8671844310125\n"
    )
    csv_example.write(
        "30.03834805225929,-92.8685078614063,30.03812214148239,-92.86718218364435\n"
    )
    csv_example.write(
        "30.03839386704537,-92.86851230357081,30.03816179178459,-92.86717763639089\n"
    )
    csv_example.write(
        "30.03841988914808,-92.86853539844006,30.03818675848181,-92.86717816057062\n"
    )
    csv_example.write(
        "30.03845220839587,-92.86854953231291,30.0382094597554,-92.86718407029464\n"
    )
    csv_example.write(
        "30.03849208414191,-92.86856303294287,30.03825237810393,-92.8671877169286\n"
    )
    csv_example.seek(0)
    return centerline_width.CenterlineWidth(csv_data=csv_example)


river_class_example = river_class_object()

## saveOutput() CSV #####################################################
# create temp pytest.csv to test against and discard after run is complete via pytest.fixture


@pytest.fixture(scope="session")
def generate_csv_centerlineDecimalDegreesVoronoi(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(save_to_csv=str(temp_path),
                                            centerline_type="Voronoi",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesVoronoiCSV(
        generate_csv_centerlineDecimalDegreesVoronoi):
    expected_df = pd.DataFrame({
        'Voronoi Centerline Latitude (Deg)': [
            30.03824341873465, 30.038177751740243, 30.038175253152005,
            30.038158019738557, 30.03812438147423, 30.03810952010084,
            30.03807266736669, 30.038055708012667, 30.03800198478457,
            30.037997843584765, 30.037977320320103, 30.0378681399185,
            30.03783447609429, 30.03779098752061, 30.03775407015797,
            30.03765923882617, 30.03763224053904, 30.037616220602292,
            30.0375560897554, 30.03754989867807, 30.03752504557166
        ],
        'Voronoi Centerline Longitude (Deg)': [
            -92.86781887353752, -92.86781163449848, -92.86781140564726,
            -92.86780915319046, -92.8678076556463, -92.86780737688784,
            -92.86780924020157, -92.86781368569092, -92.86783222004176,
            -92.86783381675426, -92.8678424441544, -92.86788520796163,
            -92.86789573192702, -92.86791355972964, -92.86792596123112,
            -92.867966599428, -92.86797730665528, -92.8679831604442,
            -92.86800558484292, -92.86800742482134, -92.86801289742836
        ]
    })
    csv_output_df = pd.read_csv(generate_csv_centerlineDecimalDegreesVoronoi)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Voronoi Centerline Latitude (Deg)"]) == pytest.approx(
            list(csv_output_df["Voronoi Centerline Latitude (Deg)"]))
    assert list(
        expected_df["Voronoi Centerline Longitude (Deg)"]) == pytest.approx(
            list(csv_output_df["Voronoi Centerline Longitude (Deg)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineDecimalDegreesEqualDistance(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(save_to_csv=str(temp_path),
                                            centerline_type="Equal Distance",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesEqualDistanceCSV(
        generate_csv_centerlineDecimalDegreesEqualDistance):
    expected_df = pd.DataFrame({
        'Equal Distance Centerline Latitude (Deg)': [
            30.03824341873465, 30.03815351096445, 30.03806333997104,
            30.037977420763955, 30.037891501548163, 30.03780557833354,
            30.03772036010588, 30.03763512429645, 30.037548493536654
        ],
        'Equal Distance Centerline Longitude (Deg)': [
            -92.86781887353752, -92.86781040076286, -92.867813429355,
            -92.86784502344554, -92.86787661748156, -92.86790819712552,
            -92.86794220669722, -92.86797615799244, -92.86800507153627
        ]
    })
    csv_output_df = pd.read_csv(
        generate_csv_centerlineDecimalDegreesEqualDistance)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Equal Distance Centerline Latitude (Deg)"]
    ) == pytest.approx(
        list(csv_output_df["Equal Distance Centerline Latitude (Deg)"]))
    assert list(
        expected_df["Equal Distance Centerline Longitude (Deg)"]
    ) == pytest.approx(
        list(csv_output_df["Equal Distance Centerline Longitude (Deg)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineDecimalDegreesEvenlySpaced(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(save_to_csv=str(temp_path),
                                            centerline_type="Evenly Spaced",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesEvenlySpacedCSV(
        generate_csv_centerlineDecimalDegreesEvenlySpaced):
    expected_df = pd.DataFrame({
        'Evenly Spaced Centerline Latitude (Deg)': [
            30.03824341873465, 30.038216571334427, 30.03818972393421,
            30.03816290193235, 30.038135955272256, 30.038108960025653,
            30.038081984444297, 30.038055567399777, 30.03803003417103,
            30.03800450094228, 30.037979489365146, 30.037954361467868,
            30.037929211772752, 30.037904062077637, 30.03787891238252,
            30.03785340255458, 30.037827832387137, 30.037802840789546,
            30.03777752725159, 30.03775198845441, 30.03772716195012,
            30.037702335445832, 30.03767750894154, 30.037652608199384,
            30.037627451162937, 30.03760211626088, 30.037576808763976,
            30.03755139550792, 30.03752504557166
        ],
        'Evenly Spaced Centerline Longitude (Deg)': [
            -92.86781887353752, -92.86781591391708, -92.86781295429664,
            -92.86780979130728, -92.867808170901, -92.86780740520584,
            -92.86780876912016, -92.86781373420196, -92.86782254308848,
            -92.86783135197496, -92.8678415323492, -92.86785143668344,
            -92.86786128732236, -92.8678711379613, -92.86788098860022,
            -92.86788981514788, -92.8678984554631, -92.8679087005742,
            -92.8679180813838, -92.86792685330632, -92.86793749224124,
            -92.8679481311762, -92.86795877011112, -92.86796922906252,
            -92.8679790567244, -92.8679884203298, -92.8679978581713,
            -92.86800697996588, -92.86801289742836
        ]
    })
    csv_output_df = pd.read_csv(
        generate_csv_centerlineDecimalDegreesEvenlySpaced)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Evenly Spaced Centerline Latitude (Deg)"]
    ) == pytest.approx(
        list(csv_output_df["Evenly Spaced Centerline Latitude (Deg)"]))
    assert list(
        expected_df["Evenly Spaced Centerline Longitude (Deg)"]
    ) == pytest.approx(
        list(csv_output_df["Evenly Spaced Centerline Longitude (Deg)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineDecimalDegreesSmoothed(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(save_to_csv=str(temp_path),
                                            centerline_type="Smoothed",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesSmoothedCSV(
        generate_csv_centerlineDecimalDegreesSmoothed):
    expected_df = pd.DataFrame({
        'Smoothed Centerline Latitude (Deg)': [
            30.03824388764834, 30.03821641344848, 30.038189206812227,
            30.03816225236923, 30.038135534749127, 30.038109038581545,
            30.038082748496144, 30.03805664912257, 30.03803072509044,
            30.03800496102941, 30.037979341569123, 30.037953851339218,
            30.03792847496932, 30.037903197089097, 30.03787800232817,
            30.03785287531619, 30.03782780068279, 30.037802763057627,
            30.03777774707033, 30.037752737350534, 30.03772771852789,
            30.03770267523204, 30.037677592092614, 30.03765245373926,
            30.037627244801627, 30.037601949909348, 30.037576553692062,
            30.03755104077941, 30.03752539580104
        ],
        'Smoothed Centerline Longitude (Deg)': [
            -92.86781709744432, -92.8678128931592, -92.86781038736042,
            -92.86780947907572, -92.86781006733284, -92.86781205115943,
            -92.86781532958338, -92.86781980163234, -92.86782536633405,
            -92.86783192271623, -92.86783936980667, -92.86784760663308,
            -92.86785653222316, -92.86786604560471, -92.86787604580542,
            -92.86788643185304, -92.8678971027753, -92.86790795759995,
            -92.86791889535476, -92.86792981506736, -92.8679406157656,
            -92.86795119647716, -92.86796145622978, -92.8679712940512,
            -92.86798060896916, -92.86798930001142, -92.86799726620568,
            -92.86800440657969, -92.86801062016116
        ]
    })
    csv_output_df = pd.read_csv(generate_csv_centerlineDecimalDegreesSmoothed)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Smoothed Centerline Latitude (Deg)"]) == pytest.approx(
            list(csv_output_df["Smoothed Centerline Latitude (Deg)"]))
    assert list(
        expected_df["Smoothed Centerline Longitude (Deg)"]) == pytest.approx(
            list(csv_output_df["Smoothed Centerline Longitude (Deg)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineRelativeDistanceVoronoi(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(
        save_to_csv=str(temp_path),
        centerline_type="Voronoi",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceVoronoiCSV(
        generate_csv_centerlineRelativeDistanceVoronoi):
    expected_df = pd.DataFrame({
        'Voronoi Relative Distance Y (from Latitude) (m)': [
            72.32036803406206, 73.01861616268259, 73.04069054140477,
            73.25795116544131, 73.4024131140832, 73.42931015169982,
            73.24962178111167, 72.82086927259678, 71.033279741361,
            70.87928057011669, 70.04718656690324, 65.92271011587445,
            64.90769952587254, 63.18824163185736, 61.99214349513374,
            58.07265538770096, 57.03996061049505, 56.47537260188891,
            54.31257503764738, 54.1351126169003, 53.60729340259522
        ],
        'Voronoi Relative Distance X (from Longitude) (m)': [
            73.47047894946884, 66.19109452005578, 65.91411844882091,
            64.0037428249338, 60.27483839167165, 58.62740948044334,
            54.54216902746018, 52.662169490597385, 46.70677234597137,
            46.24770658879016, 43.97263411803791, 31.869624721133302,
            28.1378800855557, 23.31702777301794, 19.224617662134147,
            8.712251306382981, 5.719402714977766, 3.943540534289469,
            -2.722159670063122, -3.4084605052625445, -6.163506358375243
        ]
    })
    csv_output_df = pd.read_csv(generate_csv_centerlineRelativeDistanceVoronoi)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Voronoi Relative Distance Y (from Latitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df["Voronoi Relative Distance Y (from Latitude) (m)"]))
    assert list(
        expected_df["Voronoi Relative Distance X (from Longitude) (m)"]
    ) == pytest.approx(
        list(
            csv_output_df["Voronoi Relative Distance X (from Longitude) (m)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineRelativeDistanceEqualDistance(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(
        save_to_csv=str(temp_path),
        centerline_type="Equal Distance",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceEqualDistanceCSV(
        generate_csv_centerlineRelativeDistanceEqualDistance):
    expected_df = pd.DataFrame({
        'Equal Distance Relative Distance Y (from Latitude) (m)': [
            72.32036803406206, 73.13762693464152, 72.84558714881928,
            69.79841510076358, 66.75124305318677, 63.705453863664026,
            60.42529301459804, 57.15074732117381, 54.3620875729232
        ],
        'Equal Distance Relative Distance X (from Longitude) (m)': [
            73.47047894946884, 63.50393050487748, 53.508195776029744,
            43.98376705199728, 34.45933832807993, 24.93446729527972,
            15.487745916352775, 6.039076670446599, -3.5642236371955707
        ]
    })
    csv_output_df = pd.read_csv(
        generate_csv_centerlineRelativeDistanceEqualDistance)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Equal Distance Relative Distance Y (from Latitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df[
            "Equal Distance Relative Distance Y (from Latitude) (m)"]))
    assert list(
        expected_df["Equal Distance Relative Distance X (from Longitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df[
            "Equal Distance Relative Distance X (from Longitude) (m)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineRelativeDistanceEvenlySpaced(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(
        save_to_csv=str(temp_path),
        centerline_type="Evenly Spaced",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceEvenlySpacedCSV(
        generate_csv_centerlineRelativeDistanceEvenlySpaced):
    expected_df = pd.DataFrame({
        'Evenly Spaced Relative Distance Y (from Latitude) (m)': [
            72.32036803406206, 72.6058408175882, 72.8913137541397,
            73.19640162890293, 73.35270859476822, 73.42657931165552,
            73.29505045660417, 72.81619051381901, 71.9665967492164,
            71.11700254915932, 70.13512821283742, 69.17987739758551,
            68.22980500286151, 67.27973212942103, 66.3296587753789,
            65.47835841428247, 64.64501971102429, 63.65689814521912,
            62.75213791998301, 61.90610437211858, 60.87999704997809,
            59.853889213882105, 58.82778087066884, 57.819031437171255,
            56.871169431812966, 55.96806524308548, 55.05780051346679,
            54.17801808352102, 53.60729340259522
        ],
        'Evenly Spaced Relative Distance X (from Longitude) (m)': [
            73.47047894946884, 70.49436362993764, 67.51824832917079,
            64.54494866547263, 61.55782928287779, 58.56532340111277,
            55.57499611922763, 52.64658208714705, 49.81613936752694,
            46.98569672418084, 44.21308000510999, 41.42756910548077,
            38.63964197339556, 35.85171493327896, 33.06378798515458,
            30.2359398832678, 27.401403142173283, 24.63100183091961,
            21.82491301311322, 18.993853929699387, 16.241753788045347,
            13.489653752047698, 10.737553821235773, 7.977224591714642,
            5.1884847669934535, 2.380028311306907, -0.4253901493014589,
            -3.242532102266962, -6.163506358375243
        ]
    })
    csv_output_df = pd.read_csv(
        generate_csv_centerlineRelativeDistanceEvenlySpaced)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Evenly Spaced Relative Distance Y (from Latitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df[
            "Evenly Spaced Relative Distance Y (from Latitude) (m)"]))
    assert list(
        expected_df["Evenly Spaced Relative Distance X (from Longitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df[
            "Evenly Spaced Relative Distance X (from Longitude) (m)"]))


@pytest.fixture(scope="session")
def generate_csv_centerlineRelativeDistanceSmoothed(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
    river_class_example.save_centerline_csv(
        save_to_csv=str(temp_path),
        centerline_type="Smoothed",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceSmoothedCSV(
        generate_csv_centerlineRelativeDistanceSmoothed):
    expected_df = pd.DataFrame({
        'Smoothed Relative Distance Y (from Latitude) (m)': [
            72.49167057298256, 72.89719088368028, 73.13889337599008,
            73.22651663345209, 73.16979925331094, 72.97847984747328,
            72.66229702831498, 72.23098943594705, 71.69429571185793,
            71.06195451243896, 70.34370450388619, 69.54928435982654,
            68.68843277442548, 67.77088843133382, 66.8063900482929,
            65.80467633557458, 64.77548601727342, 63.72855782918015,
            62.6736305141248, 61.62044282701308, 60.578733527598864,
            59.55824138584031, 58.5687051825966, 57.61986370968384,
            56.721455760301126, 55.88322014553281, 55.11489568434156,
            54.426221205172425, 53.82693554243374
        ],
        'Smoothed Relative Distance X (from Longitude) (m)': [
            73.52246060342735, 70.47686340416793, 67.46092539809182,
            64.47294278905704, 61.51121178204252, 58.57402859226012,
            55.65968944059493, 52.76649055007566, 49.89272814233502,
            47.03669844605679, 44.19669768853295, 41.3710220936643,
            38.5579678858772, 35.755831292628294, 32.96290853185903,
            30.177495823357827, 27.39788938294477, 24.62238542287834,
            21.849280150901333, 19.076869773558865, 16.30345049014976,
            13.527318499720732, 10.746769996134985, 7.960101170471288,
            5.165608210991695, 2.361587302227178, -0.4536653713600583,
            -3.281853627480111, -6.124681286895994
        ]
    })
    csv_output_df = pd.read_csv(
        generate_csv_centerlineRelativeDistanceSmoothed)
    assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
    assert list(
        expected_df["Smoothed Relative Distance Y (from Latitude) (m)"]
    ) == pytest.approx(
        list(
            csv_output_df["Smoothed Relative Distance Y (from Latitude) (m)"]))
    assert list(
        expected_df["Smoothed Relative Distance X (from Longitude) (m)"]
    ) == pytest.approx(
        list(csv_output_df["Smoothed Relative Distance X (from Longitude) (m)"]
             ))


def test_saveCenterlineCSV_futureWarning_functionName(tmpdir_factory):
    # Pending Deprecation: TO BE REMOVED
    with pytest.warns(
            FutureWarning,
            match=re.escape(
                "saveCenterlineCSV() has been replaced with save_centerline_csv() and will be removed in the future"
            )):
        temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.csv")
        river_class_example.saveCenterlineCSV(
            save_to_csv=str(temp_path),
            centerline_type="Smoothed",
            coordinate_unit="Relative Distance")
        expected_df = pd.DataFrame({
            'Smoothed Relative Distance Y (from Latitude) (m)': [
                72.49167057298256, 72.89719088368028, 73.13889337599008,
                73.22651663345209, 73.16979925331094, 72.97847984747328,
                72.66229702831498, 72.23098943594705, 71.69429571185793,
                71.06195451243896, 70.34370450388619, 69.54928435982654,
                68.68843277442548, 67.77088843133382, 66.8063900482929,
                65.80467633557458, 64.77548601727342, 63.72855782918015,
                62.6736305141248, 61.62044282701308, 60.578733527598864,
                59.55824138584031, 58.5687051825966, 57.61986370968384,
                56.721455760301126, 55.88322014553281, 55.11489568434156,
                54.426221205172425, 53.82693554243374
            ],
            'Smoothed Relative Distance X (from Longitude) (m)': [
                73.52246060342735, 70.47686340416793, 67.46092539809182,
                64.47294278905704, 61.51121178204252, 58.57402859226012,
                55.65968944059493, 52.76649055007566, 49.89272814233502,
                47.03669844605679, 44.19669768853295, 41.3710220936643,
                38.5579678858772, 35.755831292628294, 32.96290853185903,
                30.177495823357827, 27.39788938294477, 24.62238542287834,
                21.849280150901333, 19.076869773558865, 16.30345049014976,
                13.527318499720732, 10.746769996134985, 7.960101170471288,
                5.165608210991695, 2.361587302227178, -0.4536653713600583,
                -3.281853627480111, -6.124681286895994
            ]
        })
        csv_output_df = pd.read_csv(temp_path)
        assert expected_df.columns.tolist() == csv_output_df.columns.tolist()
        assert list(
            expected_df["Smoothed Relative Distance Y (from Latitude) (m)"]
        ) == pytest.approx(
            list(csv_output_df[
                "Smoothed Relative Distance Y (from Latitude) (m)"]))
        assert list(
            expected_df["Smoothed Relative Distance X (from Longitude) (m)"]
        ) == pytest.approx(
            list(csv_output_df[
                "Smoothed Relative Distance X (from Longitude) (m)"]))


## saveOutput() MAT #####################################################


@pytest.fixture(scope="session")
def generate_mat_centerlineDecimalDegreesVoronoi(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(save_to_mat=str(temp_path),
                                            centerline_type="Voronoi",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesVoronoiMAT(
        generate_mat_centerlineDecimalDegreesVoronoi):
    expected_df = pd.DataFrame({
        'Voronoi_Centerline_Latitude_Deg': [
            30.03824341873465, 30.038177751740243, 30.038175253152005,
            30.038158019738557, 30.03812438147423, 30.03810952010084,
            30.03807266736669, 30.038055708012667, 30.03800198478457,
            30.037997843584765, 30.037977320320103, 30.0378681399185,
            30.03783447609429, 30.03779098752061, 30.03775407015797,
            30.03765923882617, 30.03763224053904, 30.037616220602292,
            30.0375560897554, 30.03754989867807, 30.03752504557166
        ],
        'Voronoi_Centerline_Longitude_Deg': [
            -92.86781887353752, -92.86781163449848, -92.86781140564726,
            -92.86780915319046, -92.8678076556463, -92.86780737688784,
            -92.86780924020157, -92.86781368569092, -92.86783222004176,
            -92.86783381675426, -92.8678424441544, -92.86788520796163,
            -92.86789573192702, -92.86791355972964, -92.86792596123112,
            -92.867966599428, -92.86797730665528, -92.8679831604442,
            -92.86800558484292, -92.86800742482134, -92.86801289742836
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineDecimalDegreesVoronoi))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Voronoi_Centerline_Latitude_Deg"]) == pytest.approx(
            mat_output_dict["Voronoi_Centerline_Latitude_Deg"][0].tolist())
    assert list(
        expected_df["Voronoi_Centerline_Longitude_Deg"]) == pytest.approx(
            mat_output_dict["Voronoi_Centerline_Longitude_Deg"][0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineDecimalDegreesEqualDistance(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(save_to_mat=str(temp_path),
                                            centerline_type="Equal Distance",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesEqualDistanceMAT(
        generate_mat_centerlineDecimalDegreesEqualDistance):
    expected_df = pd.DataFrame({
        'Equal_Distance_Centerline_Latitude_Deg': [
            30.03824341873465, 30.03815351096445, 30.03806333997104,
            30.037977420763955, 30.037891501548163, 30.03780557833354,
            30.03772036010588, 30.03763512429645, 30.037548493536654
        ],
        'Equal_Distance_Centerline_Longitude_Deg': [
            -92.86781887353752, -92.86781040076286, -92.867813429355,
            -92.86784502344554, -92.86787661748156, -92.86790819712552,
            -92.86794220669722, -92.86797615799244, -92.86800507153627
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineDecimalDegreesEqualDistance))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Equal_Distance_Centerline_Latitude_Deg"]
    ) == pytest.approx(
        mat_output_dict["Equal_Distance_Centerline_Latitude_Deg"][0].tolist())
    assert list(
        expected_df["Equal_Distance_Centerline_Longitude_Deg"]
    ) == pytest.approx(
        mat_output_dict["Equal_Distance_Centerline_Longitude_Deg"][0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineDecimalDegreesEvenlySpaced(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(save_to_mat=str(temp_path),
                                            centerline_type="Evenly Spaced",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesEvenlySpacedMAT(
        generate_mat_centerlineDecimalDegreesEvenlySpaced):
    expected_df = pd.DataFrame({
        'Evenly_Spaced_Centerline_Latitude_Deg': [
            30.03824341873465, 30.038216571334427, 30.03818972393421,
            30.03816290193235, 30.038135955272256, 30.038108960025653,
            30.038081984444297, 30.038055567399777, 30.03803003417103,
            30.03800450094228, 30.037979489365146, 30.037954361467868,
            30.037929211772752, 30.037904062077637, 30.03787891238252,
            30.03785340255458, 30.037827832387137, 30.037802840789546,
            30.03777752725159, 30.03775198845441, 30.03772716195012,
            30.037702335445832, 30.03767750894154, 30.037652608199384,
            30.037627451162937, 30.03760211626088, 30.037576808763976,
            30.03755139550792, 30.03752504557166
        ],
        'Evenly_Spaced_Centerline_Longitude_Deg': [
            -92.86781887353752, -92.86781591391708, -92.86781295429664,
            -92.86780979130728, -92.867808170901, -92.86780740520584,
            -92.86780876912016, -92.86781373420196, -92.86782254308848,
            -92.86783135197496, -92.8678415323492, -92.86785143668344,
            -92.86786128732236, -92.8678711379613, -92.86788098860022,
            -92.86788981514788, -92.8678984554631, -92.8679087005742,
            -92.8679180813838, -92.86792685330632, -92.86793749224124,
            -92.8679481311762, -92.86795877011112, -92.86796922906252,
            -92.8679790567244, -92.8679884203298, -92.8679978581713,
            -92.86800697996588, -92.86801289742836
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineDecimalDegreesEvenlySpaced))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Evenly_Spaced_Centerline_Latitude_Deg"]) == pytest.approx(
            mat_output_dict["Evenly_Spaced_Centerline_Latitude_Deg"]
            [0].tolist())
    assert list(
        expected_df["Evenly_Spaced_Centerline_Longitude_Deg"]
    ) == pytest.approx(
        mat_output_dict["Evenly_Spaced_Centerline_Longitude_Deg"][0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineDecimalDegreesSmoothed(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(save_to_mat=str(temp_path),
                                            centerline_type="Smoothed",
                                            coordinate_unit="Decimal Degrees")
    return temp_path


def test_saveOutput_centerlineDecimalDegreesSmoothedMAT(
        generate_mat_centerlineDecimalDegreesSmoothed):
    expected_df = pd.DataFrame({
        'Smoothed_Centerline_Latitude_Deg': [
            30.03824388764834, 30.03821641344848, 30.038189206812227,
            30.03816225236923, 30.038135534749127, 30.038109038581545,
            30.038082748496144, 30.03805664912257, 30.03803072509044,
            30.03800496102941, 30.037979341569123, 30.037953851339218,
            30.03792847496932, 30.037903197089097, 30.03787800232817,
            30.03785287531619, 30.03782780068279, 30.037802763057627,
            30.03777774707033, 30.037752737350534, 30.03772771852789,
            30.03770267523204, 30.037677592092614, 30.03765245373926,
            30.037627244801627, 30.037601949909348, 30.037576553692062,
            30.03755104077941, 30.03752539580104
        ],
        'Smoothed_Centerline_Longitude_Deg': [
            -92.86781709744432, -92.8678128931592, -92.86781038736042,
            -92.86780947907572, -92.86781006733284, -92.86781205115943,
            -92.86781532958338, -92.86781980163234, -92.86782536633405,
            -92.86783192271623, -92.86783936980667, -92.86784760663308,
            -92.86785653222316, -92.86786604560471, -92.86787604580542,
            -92.86788643185304, -92.8678971027753, -92.86790795759995,
            -92.86791889535476, -92.86792981506736, -92.8679406157656,
            -92.86795119647716, -92.86796145622978, -92.8679712940512,
            -92.86798060896916, -92.86798930001142, -92.86799726620568,
            -92.86800440657969, -92.86801062016116
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineDecimalDegreesSmoothed))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Smoothed_Centerline_Latitude_Deg"]) == pytest.approx(
            mat_output_dict["Smoothed_Centerline_Latitude_Deg"][0].tolist())
    assert list(
        expected_df["Smoothed_Centerline_Longitude_Deg"]) == pytest.approx(
            mat_output_dict["Smoothed_Centerline_Longitude_Deg"][0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineRelativeDistanceVoronoi(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(
        save_to_mat=str(temp_path),
        centerline_type="Voronoi",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceVoronoiMAT(
        generate_mat_centerlineRelativeDistanceVoronoi):
    expected_df = pd.DataFrame({
        'Voronoi_Relative_Distance_Y_From_Latitude_m': [
            72.32036803406206, 73.01861616268259, 73.04069054140477,
            73.25795116544131, 73.4024131140832, 73.42931015169982,
            73.24962178111167, 72.82086927259678, 71.033279741361,
            70.87928057011669, 70.04718656690324, 65.92271011587445,
            64.90769952587254, 63.18824163185736, 61.99214349513374,
            58.07265538770096, 57.03996061049505, 56.47537260188891,
            54.31257503764738, 54.1351126169003, 53.60729340259522
        ],
        'Voronoi_Relative_Distance_X_From_Longitude_m': [
            73.47047894946884, 66.19109452005578, 65.91411844882091,
            64.0037428249338, 60.27483839167165, 58.62740948044334,
            54.54216902746018, 52.662169490597385, 46.70677234597137,
            46.24770658879016, 43.97263411803791, 31.869624721133302,
            28.1378800855557, 23.31702777301794, 19.224617662134147,
            8.712251306382981, 5.719402714977766, 3.943540534289469,
            -2.722159670063122, -3.4084605052625445, -6.163506358375243
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineRelativeDistanceVoronoi))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Voronoi_Relative_Distance_Y_From_Latitude_m"]
    ) == pytest.approx(
        mat_output_dict["Voronoi_Relative_Distance_Y_From_Latitude_m"]
        [0].tolist())
    assert list(
        expected_df["Voronoi_Relative_Distance_X_From_Longitude_m"]
    ) == pytest.approx(
        mat_output_dict["Voronoi_Relative_Distance_X_From_Longitude_m"]
        [0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineRelativeDistanceEqualDistance(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(
        save_to_mat=str(temp_path),
        centerline_type="Equal Distance",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceEqualDistanceMAT(
        generate_mat_centerlineRelativeDistanceEqualDistance):
    expected_df = pd.DataFrame({
        'Equal_Distance_Relative_Distance_Y_From_Latitude_m': [
            72.32036803406206, 73.13762693464152, 72.84558714881928,
            69.79841510076358, 66.75124305318677, 63.705453863664026,
            60.42529301459804, 57.15074732117381, 54.3620875729232
        ],
        'Equal_Distance_Relative_Distance_X_From_Longitude_m': [
            73.47047894946884, 63.50393050487748, 53.508195776029744,
            43.98376705199728, 34.45933832807993, 24.93446729527972,
            15.487745916352775, 6.039076670446599, -3.5642236371955707
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineRelativeDistanceEqualDistance))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Equal_Distance_Relative_Distance_Y_From_Latitude_m"]
    ) == pytest.approx(
        mat_output_dict["Equal_Distance_Relative_Distance_Y_From_Latitude_m"]
        [0].tolist())
    assert list(
        expected_df["Equal_Distance_Relative_Distance_X_From_Longitude_m"]
    ) == pytest.approx(
        mat_output_dict["Equal_Distance_Relative_Distance_X_From_Longitude_m"]
        [0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineRelativeDistanceEvenlySpaced(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(
        save_to_mat=str(temp_path),
        centerline_type="Evenly Spaced",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceEvenlySpacedMAT(
        generate_mat_centerlineRelativeDistanceEvenlySpaced):
    expected_df = pd.DataFrame({
        'Evenly_Spaced_Relative_Distance_Y_From_Latitude_m': [
            72.32036803406206, 72.6058408175882, 72.8913137541397,
            73.19640162890293, 73.35270859476822, 73.42657931165552,
            73.29505045660417, 72.81619051381901, 71.9665967492164,
            71.11700254915932, 70.13512821283742, 69.17987739758551,
            68.22980500286151, 67.27973212942103, 66.3296587753789,
            65.47835841428247, 64.64501971102429, 63.65689814521912,
            62.75213791998301, 61.90610437211858, 60.87999704997809,
            59.853889213882105, 58.82778087066884, 57.819031437171255,
            56.871169431812966, 55.96806524308548, 55.05780051346679,
            54.17801808352102, 53.60729340259522
        ],
        'Evenly_Spaced_Relative_Distance_X_From_Longitude_m': [
            73.47047894946884, 70.49436362993764, 67.51824832917079,
            64.54494866547263, 61.55782928287779, 58.56532340111277,
            55.57499611922763, 52.64658208714705, 49.81613936752694,
            46.98569672418084, 44.21308000510999, 41.42756910548077,
            38.63964197339556, 35.85171493327896, 33.06378798515458,
            30.2359398832678, 27.401403142173283, 24.63100183091961,
            21.82491301311322, 18.993853929699387, 16.241753788045347,
            13.489653752047698, 10.737553821235773, 7.977224591714642,
            5.1884847669934535, 2.380028311306907, -0.4253901493014589,
            -3.242532102266962, -6.163506358375243
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineRelativeDistanceEvenlySpaced))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Evenly_Spaced_Relative_Distance_Y_From_Latitude_m"]
    ) == pytest.approx(
        mat_output_dict["Evenly_Spaced_Relative_Distance_Y_From_Latitude_m"]
        [0].tolist())
    assert list(
        expected_df["Evenly_Spaced_Relative_Distance_X_From_Longitude_m"]
    ) == pytest.approx(
        mat_output_dict["Evenly_Spaced_Relative_Distance_X_From_Longitude_m"]
        [0].tolist())


@pytest.fixture(scope="session")
def generate_mat_centerlineRelativeDistanceSmoothed(tmpdir_factory):
    temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
    river_class_example.save_centerline_mat(
        save_to_mat=str(temp_path),
        centerline_type="Smoothed",
        coordinate_unit="Relative Distance")
    return temp_path


def test_saveOutput_centerlineRelativeDistanceSmoothedMAT(
        generate_mat_centerlineRelativeDistanceSmoothed):
    expected_df = pd.DataFrame({
        'Smoothed_Relative_Distance_Y_From_Latitude_m': [
            72.49167057298256, 72.89719088368028, 73.13889337599008,
            73.22651663345209, 73.16979925331094, 72.97847984747328,
            72.66229702831498, 72.23098943594705, 71.69429571185793,
            71.06195451243896, 70.34370450388619, 69.54928435982654,
            68.68843277442548, 67.77088843133382, 66.8063900482929,
            65.80467633557458, 64.77548601727342, 63.72855782918015,
            62.6736305141248, 61.62044282701308, 60.578733527598864,
            59.55824138584031, 58.5687051825966, 57.61986370968384,
            56.721455760301126, 55.88322014553281, 55.11489568434156,
            54.426221205172425, 53.82693554243374
        ],
        'Smoothed_Relative_Distance_X_From_Longitude_m': [
            73.52246060342735, 70.47686340416793, 67.46092539809182,
            64.47294278905704, 61.51121178204252, 58.57402859226012,
            55.65968944059493, 52.76649055007566, 49.89272814233502,
            47.03669844605679, 44.19669768853295, 41.3710220936643,
            38.5579678858772, 35.755831292628294, 32.96290853185903,
            30.177495823357827, 27.39788938294477, 24.62238542287834,
            21.849280150901333, 19.076869773558865, 16.30345049014976,
            13.527318499720732, 10.746769996134985, 7.960101170471288,
            5.165608210991695, 2.361587302227178, -0.4536653713600583,
            -3.281853627480111, -6.124681286895994
        ]
    })
    mat_output_dict = sio.loadmat(
        str(generate_mat_centerlineRelativeDistanceSmoothed))
    assert set(expected_df.columns.tolist()) <= set(
        list(mat_output_dict.keys()))
    assert list(
        expected_df["Smoothed_Relative_Distance_Y_From_Latitude_m"]
    ) == pytest.approx(
        mat_output_dict["Smoothed_Relative_Distance_Y_From_Latitude_m"]
        [0].tolist())
    assert list(
        expected_df["Smoothed_Relative_Distance_X_From_Longitude_m"]
    ) == pytest.approx(
        mat_output_dict["Smoothed_Relative_Distance_X_From_Longitude_m"]
        [0].tolist())


def test_saveCenterlineMAT_futureWarning_functionName(tmpdir_factory):
    # Pending Deprecation: TO BE REMOVED
    with pytest.warns(
            FutureWarning,
            match=re.escape(
                "saveCenterlineMAT() has been replaced with save_centerline_mat() and will be removed in the future"
            )):
        temp_path = tmpdir_factory.mktemp("temp_data").join("pytest.mat")
        river_class_example.saveCenterlineMAT(
            save_to_mat=str(temp_path),
            centerline_type="Smoothed",
            coordinate_unit="Relative Distance")
        expected_df = pd.DataFrame({
            'Smoothed_Relative_Distance_Y_From_Latitude_m': [
                72.49167057298256, 72.89719088368028, 73.13889337599008,
                73.22651663345209, 73.16979925331094, 72.97847984747328,
                72.66229702831498, 72.23098943594705, 71.69429571185793,
                71.06195451243896, 70.34370450388619, 69.54928435982654,
                68.68843277442548, 67.77088843133382, 66.8063900482929,
                65.80467633557458, 64.77548601727342, 63.72855782918015,
                62.6736305141248, 61.62044282701308, 60.578733527598864,
                59.55824138584031, 58.5687051825966, 57.61986370968384,
                56.721455760301126, 55.88322014553281, 55.11489568434156,
                54.426221205172425, 53.82693554243374
            ],
            'Smoothed_Relative_Distance_X_From_Longitude_m': [
                73.52246060342735, 70.47686340416793, 67.46092539809182,
                64.47294278905704, 61.51121178204252, 58.57402859226012,
                55.65968944059493, 52.76649055007566, 49.89272814233502,
                47.03669844605679, 44.19669768853295, 41.3710220936643,
                38.5579678858772, 35.755831292628294, 32.96290853185903,
                30.177495823357827, 27.39788938294477, 24.62238542287834,
                21.849280150901333, 19.076869773558865, 16.30345049014976,
                13.527318499720732, 10.746769996134985, 7.960101170471288,
                5.165608210991695, 2.361587302227178, -0.4536653713600583,
                -3.281853627480111, -6.124681286895994
            ]
        })
        mat_output_dict = sio.loadmat(str(temp_path))
        assert set(expected_df.columns.tolist()) <= set(
            list(mat_output_dict.keys()))
        assert list(
            expected_df["Smoothed_Relative_Distance_Y_From_Latitude_m"]
        ) == pytest.approx(
            mat_output_dict["Smoothed_Relative_Distance_Y_From_Latitude_m"]
            [0].tolist())
        assert list(
            expected_df["Smoothed_Relative_Distance_X_From_Longitude_m"]
        ) == pytest.approx(
            mat_output_dict["Smoothed_Relative_Distance_X_From_Longitude_m"]
            [0].tolist())
