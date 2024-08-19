# Verify Outputs from getCoordinatesKML.py
# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifyGetCoordinatesKML.py -xv

# Pytests to Compare and Verify Expected Outputs

# External Python libraries (installed via pip install)
import re
import pytest
import pandas as pd

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


@pytest.fixture(scope="function")
def generate_kmlFile_right(tmpdir):
    temp_right_kml = tmpdir.join("rightbank.kml")
    with open(str(temp_right_kml), "w") as kml_file:
        kml_file.write('<?xml version="1.0" encoding="UTF-8"?>')
        kml_file.write(
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
        )
        kml_file.write('<Document>')
        kml_file.write('<name>rightbank.kml</name>')
        kml_file.write('<StyleMap id="msn_ylw-pushpin">')
        kml_file.write('<Pair>')
        kml_file.write('<key>normal</key>')
        kml_file.write('<styleUrl>#sn_ylw-pushpin</styleUrl>')
        kml_file.write('</Pair>')
        kml_file.write('<Pair>')
        kml_file.write('<key>highlight</key>')
        kml_file.write('<styleUrl>#sh_ylw-pushpin</styleUrl>')
        kml_file.write('</Pair>')
        kml_file.write('</StyleMap>')
        kml_file.write('<Style id="sh_ylw-pushpin">')
        kml_file.write('<IconStyle>')
        kml_file.write('<scale>1.3</scale>')
        kml_file.write('<Icon>')
        kml_file.write(
            '<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
        )
        kml_file.write('</Icon>')
        kml_file.write(
            '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>')
        kml_file.write('</IconStyle>')
        kml_file.write('<BalloonStyle>')
        kml_file.write('</BalloonStyle>')
        kml_file.write('<LineStyle>')
        kml_file.write('<color>ff0000ff</color>')
        kml_file.write('</LineStyle>')
        kml_file.write('</Style>')
        kml_file.write('<Style id="sn_ylw-pushpin">')
        kml_file.write('<IconStyle>')
        kml_file.write('<scale>1.1</scale>')
        kml_file.write('<Icon>')
        kml_file.write(
            '<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
        )
        kml_file.write('</Icon>')
        kml_file.write(
            '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>')
        kml_file.write('</IconStyle>')
        kml_file.write('<BalloonStyle>')
        kml_file.write('</BalloonStyle>')
        kml_file.write('<LineStyle>')
        kml_file.write('<color>ff0000ff</color>')
        kml_file.write('</LineStyle>')
        kml_file.write('</Style>')
        kml_file.write('<Placemark>')
        kml_file.write('<name>rightbank</name>')
        kml_file.write('<styleUrl>#msn_ylw-pushpin</styleUrl>')
        kml_file.write('<LineString>')
        kml_file.write('<tessellate>1</tessellate>')
        kml_file.write(
            '<coordinates>-92.86856870164003,30.03758064742554,0 -92.86854932864129,30.03761289873068,0 -92.86854615646305,30.03764767910492,0 -92.86853555132092,30.03767440933011,0 -92.8685329553435,30.03770236278642,0 -92.86852225012414,30.03772919351539,0 -92.86851215967346,30.0377490549762,0 -92.86850070336355,30.03778301480612,0 -92.86848128471483,30.03781601910584,0 -92.86847053431235,30.03784317873953,0'
        )
        kml_file.write('</coordinates>')
        kml_file.write('</LineString>')
        kml_file.write('</Placemark>')
        kml_file.write('</Document>')
        kml_file.write('</kml>')

    return temp_right_kml


@pytest.fixture(scope="function")
def generate_kmlFile_left(tmpdir):
    temp_left_kml = tmpdir.join("leftbank.kml")
    with open(str(temp_left_kml), "w") as kml_file:
        kml_file.write('<?xml version="1.0" encoding="UTF-8"?>')
        kml_file.write(
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
        )
        kml_file.write('<Document>')
        kml_file.write('<name>leftbank.kml</name>')
        kml_file.write('<StyleMap id="msn_ylw-pushpin">')
        kml_file.write('<Pair>')
        kml_file.write('<key>normal</key>')
        kml_file.write('<styleUrl>#sn_ylw-pushpin</styleUrl>')
        kml_file.write('</Pair>')
        kml_file.write('<Pair>')
        kml_file.write('<key>highlight</key>')
        kml_file.write('<styleUrl>#sh_ylw-pushpin</styleUrl>')
        kml_file.write('</Pair>')
        kml_file.write('</StyleMap>')
        kml_file.write('<Style id="sh_ylw-pushpin">')
        kml_file.write('<IconStyle>')
        kml_file.write('<scale>1.3</scale>')
        kml_file.write('<Icon>')
        kml_file.write(
            '<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
        )
        kml_file.write('</Icon>')
        kml_file.write(
            '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>')
        kml_file.write('</IconStyle>')
        kml_file.write('<BalloonStyle>')
        kml_file.write('</BalloonStyle>')
        kml_file.write('<LineStyle>')
        kml_file.write('<color>ff0000ff</color>')
        kml_file.write('</LineStyle>')
        kml_file.write('</Style>')
        kml_file.write('<Style id="sn_ylw-pushpin">')
        kml_file.write('<IconStyle>')
        kml_file.write('<scale>1.1</scale>')
        kml_file.write('<Icon>')
        kml_file.write(
            '<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>'
        )
        kml_file.write('</Icon>')
        kml_file.write(
            '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>')
        kml_file.write('</IconStyle>')
        kml_file.write('<BalloonStyle>')
        kml_file.write('</BalloonStyle>')
        kml_file.write('<LineStyle>')
        kml_file.write('<color>ff0000ff</color>')
        kml_file.write('</LineStyle>')
        kml_file.write('</Style>')
        kml_file.write('<Placemark>')
        kml_file.write('<name>leftbank</name>')
        kml_file.write('<styleUrl>#msn_ylw-pushpin</styleUrl>')
        kml_file.write('<LineString>')
        kml_file.write('<tessellate>1</tessellate>')
        kml_file.write(
            '<coordinates>-92.86856870164003,30.03758064742554,0 -92.86854932864129,30.03761289873068,0 -92.86854615646305,30.03764767910492,0 -92.86853555132092,30.03767440933011,0 -92.8685329553435,30.03770236278642,0 -92.86852225012414,30.03772919351539,0 -92.86851215967346,30.0377490549762,0 -92.86850070336355,30.03778301480612,0 -92.86848128471483,30.03781601910584,0 -92.86847053431235,30.03784317873953,0'
        )
        kml_file.write('</coordinates>')
        kml_file.write('</LineString>')
        kml_file.write('</Placemark>')
        kml_file.write('</Document>')
        kml_file.write('</kml>')

    return temp_left_kml


@pytest.fixture(scope="function")
def generate_kmlFile(tmpdir, generate_kmlFile_right, generate_kmlFile_left):
    temp_csv_file = tmpdir.join("pytest.csv")
    centerline_width.kml_to_csv(left_kml=str(generate_kmlFile_left),
                                right_kml=str(generate_kmlFile_right),
                                csv_output=str(temp_csv_file))
    return temp_csv_file


def test_getCoordinatesKML_extractPointsToCSV(generate_kmlFile):
    expected_df = pd.DataFrame({
        'llat': [
            30.03758064742554, 30.03761289873068, 30.03764767910492,
            30.03767440933011, 30.03770236278642, 30.03772919351539,
            30.0377490549762, 30.03778301480612, 30.03781601910584,
            30.03784317873953
        ],
        'llon': [
            -92.86856870164004, -92.86854932864128, -92.86854615646304,
            -92.86853555132092, -92.8685329553435, -92.86852225012414,
            -92.86851215967346, -92.86850070336357, -92.86848128471485,
            -92.86847053431237
        ],
        'rlat': [
            30.03758064742554, 30.03761289873068, 30.03764767910492,
            30.03767440933011, 30.03770236278642, 30.03772919351539,
            30.0377490549762, 30.03778301480612, 30.03781601910584,
            30.03784317873953
        ],
        'rlon': [
            -92.86856870164004, -92.86854932864128, -92.86854615646304,
            -92.86853555132092, -92.8685329553435, -92.86852225012414,
            -92.86851215967346, -92.86850070336357, -92.86848128471485,
            -92.86847053431237
        ]
    })
    kml_output_df = pd.read_csv(generate_kmlFile)
    assert expected_df.columns.tolist() == kml_output_df.columns.tolist()
    assert list(expected_df["llat"]) == list(kml_output_df["llat"])
    assert list(expected_df["llon"]) == list(kml_output_df["llon"])
    assert list(expected_df["rlat"]) == list(kml_output_df["rlat"])
    assert list(expected_df["rlon"]) == list(kml_output_df["rlon"])


def test_txtToCSV_futureWarning_functionName(tmpdir):
    # Pending Deprecation: To Be Removed
    with pytest.warns(
            FutureWarning,
            match=re.escape(
                "convertColumnsToCSV() has been replaced with kml_to_csv() and will be removed in the future"
            )):
        temp_text_file = tmpdir.join("pytest.txt")
        with open(str(temp_text_file), "w") as text_file:
            text_file.write("llat,llon,rlat,rlon\n")
            text_file.write(",,30.037441,-92.867476\n")
            text_file.write(",,30.037441,-92.867476\n")
            text_file.write(",,30.037441,-92.867476\n")
        centerline_width.convertColumnsToCSV(txt_input=str(temp_text_file),
                                             flip_direction=False)


def test_txtToCSV_futureWarning_variableName(tmpdir):
    # Pending Deprecation: To Be Removed
    with pytest.warns(
            FutureWarning,
            match=re.escape(
                "text_file has been replaced with txt_input and will be removed in the future"
            )):
        temp_text_file = tmpdir.join("pytest.txt")
        with open(str(temp_text_file), "w") as text_file:
            text_file.write("llat,llon,rlat,rlon\n")
            text_file.write(",,30.037441,-92.867476\n")
            text_file.write(",,30.037441,-92.867476\n")
            text_file.write(",,30.037441,-92.867476\n")
        centerline_width.txt_to_csv(text_file=str(temp_text_file),
                                    flip_direction=False)


@pytest.fixture(scope="function")
def generate_txtToCSV_noFlip(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write("30.037581,-92.868569,30.037441,-92.867476\n")
        text_file.write("30.137581,-92.868569,30.037441,-92.867476\n")
        text_file.write("30.237581,-92.868569,30.037441,-92.867476\n")
    return temp_text_file


def test_txtToCSV_convertColumnsToCSV(generate_txtToCSV_noFlip):
    expected_df = pd.DataFrame({
        'llat': [30.037581, 30.137581, 30.237581],
        'llon': [-92.868569, -92.868569, -92.868569],
        'rlat': [30.037441, 30.037441, 30.037441],
        'rlon': [-92.867476, -92.867476, -92.867476]
    })
    txt_output_df = pd.read_csv(generate_txtToCSV_noFlip)
    assert expected_df.columns.tolist() == txt_output_df.columns.tolist()
    assert list(expected_df["llat"]) == list(txt_output_df["llat"])
    assert list(expected_df["llon"]) == list(txt_output_df["llon"])
    assert list(expected_df["rlat"]) == list(txt_output_df["rlat"])
    assert list(expected_df["rlon"]) == list(txt_output_df["rlon"])


@pytest.fixture(scope="function")
def generate_txtToCSV_emptyRight(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write("30.037581,-92.868569,,\n")
        text_file.write("30.137581,-92.868569,,\n")
        text_file.write("30.237581,-92.868569,,\n")
    centerline_width.txt_to_csv(txt_input=str(temp_text_file),
                                flip_direction=False)

    return temp_text_file


def test_txtToCSV_emptyRightBankCSV(generate_txtToCSV_emptyRight):
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, right bank data is empty (or NaN)")):
        centerline_width.CenterlineWidth(
            csv_data=str(generate_txtToCSV_emptyRight))


@pytest.fixture(scope="function")
def generate_txtToCSV_emptyLeft(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write(",,30.037441,-92.867476\n")
        text_file.write(",,30.037441,-92.867476\n")
        text_file.write(",,30.037441,-92.867476\n")
    centerline_width.txt_to_csv(txt_input=str(temp_text_file),
                                flip_direction=False)

    return temp_text_file


def test_txtToCSV_emptyLeftBankCSV(generate_txtToCSV_emptyLeft):
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, left bank data is empty (or NaN)")):
        centerline_width.CenterlineWidth(
            csv_data=str(generate_txtToCSV_emptyLeft))
