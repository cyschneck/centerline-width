# Built in Python functions
import re

# External Python libraries (installed via pip install)
import pandas as pd
from pykml import parser

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width


def extractPointsToTextFile(left_kml=None,
                            right_kml=None,
                            text_output_name=None):
    # Extract points from KML files from Google Earth Pro and exports coordinates into a text file with headers: llat, llong, rlat, rlong

    centerline_width.errorHandlingExtractPointsToTextFile(
        left_kml=left_kml,
        right_kml=right_kml,
        text_output_name=text_output_name)

    # extract points from kml file
    with open(left_kml) as f:
        doc = parser.parse(f)
    root = doc.getroot()
    coords = root.Document.Placemark.LineString.coordinates.text
    llon = []
    llat = []
    coords = coords.replace('\n', '').replace('\t', '')
    for coord in coords.split(
            " "
    ):  # split coordinates based on commas (excluding preceding 0's)
        if coord != "":
            llon.append(coord.split(",")[0])
            llat.append(coord.split(",")[1])

    with open(right_kml) as f:
        doc = parser.parse(f)
    root = doc.getroot()
    coords = root.Document.Placemark.LineString.coordinates.text
    rlon = []
    rlat = []
    coords = coords.replace('\n', '').replace('\t', '')
    for coord in coords.split(
            " "
    ):  # split coordinates based on commas (excluding preceding 0's)
        if coord != "":
            rlon.append(coord.split(",")[0])
            rlat.append(coord.split(",")[1])

    df_lb = pd.DataFrame({'llat': llat, 'llon': llon})
    df_rb = pd.DataFrame({'rlat': rlat, 'rlon': rlon})
    df = pd.concat([df_lb, df_rb], axis=1)

    open(text_output_name,
         'w').close()  # empty original file to avoid overwriting

    with open(text_output_name, 'a') as f:
        dfAsString = df.to_string(header=True, index=False)
        f.write(dfAsString)
