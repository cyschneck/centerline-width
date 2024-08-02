#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      getCoordinatesKML.py handles converting input KML files to readable                        #
#      coordinates                                                                                #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - extractPointsToTextFile: extract KML points             #
#                                              to a readable text file                            #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Built-in Python functions
import re

# External Python libraries
import pandas as pd
from pykml import parser

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width


def extractPointsToTextFile(left_kml: str = None,
                            right_kml: str = None,
                            text_output_name: str = None) -> None:
    # Extract points from KML files from Google Earth Pro and exports coordinates into a text file with headers: llat, llong, rlat, rlong

    centerline_width.errorHandlingExtractPointsToTextFile(
        left_kml=left_kml,
        right_kml=right_kml,
        text_output_name=text_output_name)

    def extractKML(kml_file: str = None) -> (list, list):
        # extract points from kml file for the given bank
        with open(kml_file) as f:
            doc = parser.parse(f)
        root = doc.getroot()
        coords = root.Document.Placemark.LineString.coordinates.text
        lon = []
        lat = []
        coords = coords.replace('\n', '').replace('\t', '')
        for coord in coords.split(
                " "
        ):  # split coordinates based on commas (excluding preceding 0's)
            if coord != "":
                lon.append(coord.split(",")[0])
                lat.append(coord.split(",")[1])
        return lon, lat

    # extract right and left bank files
    rlon, rlat = extractKML(right_kml)
    llon, llat = extractKML(left_kml)

    df_lb = pd.DataFrame({'llat': llat, 'llon': llon})
    df_rb = pd.DataFrame({'rlat': rlat, 'rlon': rlon})
    df = pd.concat([df_lb, df_rb], axis=1)

    open(text_output_name,
         'w').close()  # empty original file to avoid overwriting

    with open(text_output_name, 'a') as f:
        dfAsString = df.to_string(header=True, index=False)
        f.write(dfAsString)
