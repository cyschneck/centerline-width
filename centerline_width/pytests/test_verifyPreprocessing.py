# centerline-width/: python -m pytest -v
# Pytests to Compare and Verify Expected Outputs
from io import StringIO
import re

# External Python libraries (installed via pip install)
import pytest

# Internal centerline-width reference to access functions, global variables, and error handling
import centerline_width


def test_preprocessing_emptyRightBankCSV():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, right bank data is empty (or NaN)")):
        csv_example = StringIO()
        csv_example.write("llat,llon,rlat,rlon\n")
        csv_example.write("30.037581,-92.868569,,\n")
        csv_example.seek(0)
        centerline_width.riverCenterline(csv_data=csv_example)


def test_preprocessing_emptyLeftBankCSV():
    with pytest.raises(
            ValueError,
            match=re.escape(
                "CRITICAL ERROR, left bank data is empty (or NaN)")):
        csv_example = StringIO()
        csv_example.write("llat,llon,rlat,rlon\n")
        csv_example.write(",,30.037441,-92.867476\n")
        csv_example.seek(0)
        centerline_width.riverCenterline(csv_data=csv_example)
