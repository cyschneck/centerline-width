#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      getCoordinatesKML.py handles converting input KML files to readable                        #
#      coordinates                                                                                #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - kml_to_csv: extract KML points to a readable            #
#                                              csv file                                           #
#                                       - txt_to_csv: extract txt points to a readable            #
#                                              csv file                                           #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Built-in Python functions
import re
import os
import warnings  # Pending Deprecation

# External Python libraries
import pandas as pd
import numpy as np
from pykml import parser

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width


def extractPointsToTextFile(left_kml: str = None,
                            right_kml: str = None,
                            flip_direction: bool = False,
                            text_output_name: str = None,
                            csv_output: str = None) -> None:
    ### Pending Deprecation for function name replaced with kml_to_csv
    warnings.warn(
        "extractPointsToTextFile() has been replaced with kml_to_csv() and will be removed in the future",
        FutureWarning,
        stacklevel=2)

    kml_to_csv(left_kml=left_kml,
               right_kml=right_kml,
               text_output_name=text_output_name,
               csv_output=csv_output)


def convertColumnsToCSV(text_file: str = None,
                        txt_input: str = None,
                        flip_direction: bool = False) -> None:
    ### Pending Deprecation for function name: replaced with txt_to_csv
    warnings.warn(
        "convertColumnsToCSV() has been replaced with kml_to_csv() and will be removed in the future",
        FutureWarning,
        stacklevel=2)
    txt_to_csv(text_file=text_file,
               txt_input=txt_input,
               flip_direction=flip_direction)


def kml_to_csv(left_kml: str = None,
               right_kml: str = None,
               flip_direction: bool = False,
               text_output_name: str = None,
               csv_output: str = None) -> None:
    # Extract points from KML files from Google Earth Pro and exports coordinates into a text file with headers: llat, llong, rlat, rlong

    ### Pending Deprecated argument "text_output_name" replaced with "csv_output"

    centerline_width.errorHandlingExtractPointsToTextFile(
        left_kml=left_kml,
        right_kml=right_kml,
        flip_direction=flip_direction,
        csv_output=csv_output,
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

    # reverse the direction for the right bank
    if flip_direction:
        rlon = rlon[::-1]
        rlat = rlat[::-1]

    df_lb = pd.DataFrame({'llat': llat, 'llon': llon})
    df_rb = pd.DataFrame({'rlat': rlat, 'rlon': rlon})
    df = pd.concat([df_lb, df_rb], axis=1)

    ### Pending Deprecated argument "text_output_name": replaced with "csv_output"
    if text_output_name:  # Remove and replace with just the "else" statement when deprecated
        warnings.warn(
            "text_output_name has been replaced with txt_to_csv() function and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        open(text_output_name,
             'w').close()  # empty original file to avoid overwriting

        with open(text_output_name, 'a') as f:
            dfAsString = df.to_string(header=True, index=False)
            f.write(dfAsString)
    else:
        df.to_csv(csv_output, index=False, header=True)


def txt_to_csv(txt_input: str = None,
               text_file: str = None,
               flip_direction: bool = False) -> None:
    # Convert txt file to a comma-separated version of the file

    ### Pending Deprecated argument "text_file": replaced with "txt_input"
    if text_file is not None:
        warnings.warn(
            "text_file has been replaced with txt_input and will be removed in the future",
            FutureWarning,
            stacklevel=2)
        txt_input = text_file

    centerline_width.errrorHandlingConvertColumnsToCSV(
        txt_input=txt_input, flip_direction=flip_direction)

    left_rows = []
    right_rows = []
    with open(txt_input) as input_file:
        lines = input_file.readlines()
        for i, line in enumerate(lines):
            line = line.strip().split(" ")
            line = [x for x in line if x != '']
            if i == 0:
                header_fields = line
                if header_fields != ['llat', 'llon', 'rlat', 'rlon']:
                    ValueError(
                        f"Invalid headers, expected ['llat', 'llon', 'rlat', 'rlon'], found = {header_fields}"
                    )
                llat = []
                llon = []
                rlat = []
                rlon = []
            else:
                # fill in each lat/lon value, default to NaN if does not exist
                default_value = np.nan
                llat_value, llon_value, rlat_value, rlon_value = [
                    *line, *([default_value] * (4 - len(line)))
                ]
                llat.append(llat_value)
                llon.append(llon_value)
                rlat.append(rlat_value)
                rlon.append(rlon_value)

    # reverse the direction for the right bank
    if flip_direction:
        rlat = rlat[::-1]
        rlon = rlon[::-1]

    # account for relative and absolute paths to use txt_input name and location for .csv
    if text_file is not None and txt_input is None:
        txt_input = text_file  # Pending Deprecation
    full_path, filename = os.path.split(os.path.abspath(txt_input))
    csv_file_name = filename.split(".")[0] + ".csv"

    # save to csv
    df_lb = pd.DataFrame({'llat': llat, 'llon': llon})
    df_rb = pd.DataFrame({'rlat': rlat, 'rlon': rlon})
    df = pd.concat([df_lb, df_rb], axis=1)
    df.to_csv(os.path.join(full_path, csv_file_name), index=False, header=True)
