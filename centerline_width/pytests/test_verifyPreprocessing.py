# centerline-width/: python -m pytest -v
# python -m pytest -k test_verifyPreprocessing -xv

# Pytests to Compare and Verify Expected Outputs
import re

# External Python libraries (installed via pip install)
import pytest
import pandas as pd

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


@pytest.fixture(scope="function")
def generate_txt_convertColumnsToCSV_noFlip(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write("30.037581,-92.868569,30.037441,-92.867476\n")
        text_file.write("30.137581,-92.868569,30.037441,-92.867476\n")
        text_file.write("30.237581,-92.868569,30.037441,-92.867476\n")
    centerline_width.convertColumnsToCSV(text_file=str(temp_text_file),
                                         flip_direction=False)

    return temp_text_file


def test_txt_convertColumnsToCSV(generate_txt_convertColumnsToCSV_noFlip):
    expected_df = pd.DataFrame({
        'llat': [30.037581, 30.137581, 30.237581],
        'llon': [-92.868569, -92.868569, -92.868569],
        'rlat': [30.037441, 30.037441, 30.037441],
        'rlon': [-92.867476, -92.867476, -92.867476]
    })
    txt_output_df = pd.read_csv(generate_txt_convertColumnsToCSV_noFlip)
    assert expected_df.columns.tolist() == txt_output_df.columns.tolist()
    assert list(expected_df["llat"]) == list(txt_output_df["llat"])
    assert list(expected_df["llon"]) == list(txt_output_df["llon"])
    assert list(expected_df["rlat"]) == list(txt_output_df["rlat"])
    assert list(expected_df["rlon"]) == list(txt_output_df["rlon"])


@pytest.fixture(scope="function")
def generate_txt_convertColumnsToCSV_emptyRight(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write("30.037581,-92.868569,,\n")
        text_file.write("30.137581,-92.868569,,\n")
        text_file.write("30.237581,-92.868569,,\n")
    centerline_width.convertColumnsToCSV(text_file=str(temp_text_file),
                                         flip_direction=False)

    return temp_text_file


def test_preprocessing_emptyRightBankCSV(
        generate_txt_convertColumnsToCSV_emptyRight):
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, right bank data is empty (or NaN)")):
        centerline_width.riverCenterline(
            csv_data=str(generate_txt_convertColumnsToCSV_emptyRight))


@pytest.fixture(scope="function")
def generate_txt_convertColumnsToCSV_emptyLeft(tmpdir):
    temp_text_file = tmpdir.join("pytest.txt")
    with open(str(temp_text_file), "w") as text_file:
        text_file.write("llat,llon,rlat,rlon\n")
        text_file.write(",,30.037441,-92.867476\n")
        text_file.write(",,30.037441,-92.867476\n")
        text_file.write(",,30.037441,-92.867476\n")
    centerline_width.convertColumnsToCSV(text_file=str(temp_text_file),
                                         flip_direction=False)

    return temp_text_file


def test_preprocessing_emptyLeftBankCSV(
        generate_txt_convertColumnsToCSV_emptyLeft):
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, left bank data is empty (or NaN)")):
        centerline_width.riverCenterline(
            csv_data=str(generate_txt_convertColumnsToCSV_emptyLeft))
