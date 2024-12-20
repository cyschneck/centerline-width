#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      saveOutput.py is saving the output (either from centerline coordinates or width            #
#      intersections) and returning the values as either a .csv or .mat format                    #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - save_centerline_csv: saves the centerline               #
#                                              coordinates to a .csv file                         #
#                                                                                                 #
#                                       - save_centerline_mat: saves the centerline               #
#                                              coordinates to a .mat file                         #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Standard Library Imports
import csv
import logging

# Related Third Party Imports
import numpy as np
from scipy.io import savemat

# Internal Local Imports
import centerline_width

## Logging set up for .CRITICAL
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def save_centerline_csv(river_object: centerline_width.CenterlineWidth = None,
                        save_to_csv: str = None,
                        latitude_header: str = None,
                        longitude_header: str = None,
                        centerline_type: str = "Voronoi",
                        coordinate_unit: str = "Decimal Degrees") -> None:
    # Save Centerline Coordinates to .CSV

    centerline_width._error_handling_save_centerline_csv(
        river_object=river_object,
        save_to_csv=save_to_csv,
        latitude_header=latitude_header,
        longitude_header=longitude_header,
        centerline_type=centerline_type,
        coordinate_unit=coordinate_unit)
    centerline_type = centerline_type.title()
    coordinate_unit = coordinate_unit.title()

    # set coordinate type and unit
    if coordinate_unit == "Decimal Degrees":
        if centerline_type == "Voronoi":
            centerline_coordinates_by_type = river_object.centerline_voronoi
        if centerline_type == "Equal Distance":
            centerline_coordinates_by_type = river_object.centerline_equal_distance
        if centerline_type == "Evenly Spaced":
            centerline_coordinates_by_type = river_object.centerline_evenly_spaced
        if centerline_type == "Smoothed":
            centerline_coordinates_by_type = river_object.centerline_smoothed
    if coordinate_unit == "Relative Distance":
        if centerline_type == "Voronoi":
            centerline_coordinates_by_type = river_object.centerline_voronoi_relative
        if centerline_type == "Equal Distance":
            centerline_coordinates_by_type = river_object.centerline_equal_distance_relative
        if centerline_type == "Evenly Spaced":
            centerline_coordinates_by_type = river_object.centerline_evenly_spaced_relative
        if centerline_type == "Smoothed":
            centerline_coordinates_by_type = river_object.centerline_smoothed_relative

    # set default latitude/longitude headers
    if coordinate_unit == "Decimal Degrees":
        if latitude_header is None:
            latitude_header = f"{centerline_type} Centerline Latitude (Deg)"
        if longitude_header is None:
            longitude_header = f"{centerline_type} Centerline Longitude (Deg)"
    if coordinate_unit == "Relative Distance":
        if latitude_header is None:
            latitude_header = f"{centerline_type} Relative Distance Y (from Latitude) (m)"
        if longitude_header is None:
            longitude_header = f"{centerline_type} Relative Distance X (from Longitude) (m)"

    # save csv output
    with open(save_to_csv, "w") as csv_file_output:
        writer = csv.writer(csv_file_output)
        writer.writerow([latitude_header, longitude_header])
        if centerline_coordinates_by_type is not None:
            for latitude_longitude in centerline_coordinates_by_type:
                writer.writerow([latitude_longitude[1], latitude_longitude[0]])
        else:
            logger.warn(
                f"\nWARNING, no {centerline_type} centerline coordinates found, {save_to_csv} file generated will be empty"
            )


def save_centerline_mat(river_object: centerline_width.CenterlineWidth = None,
                        save_to_mat: str = None,
                        latitude_header: str = None,
                        longitude_header: str = None,
                        centerline_type: str = "Voronoi",
                        coordinate_unit: str = "Decimal Degrees") -> None:
    # Save Centerline Coordinates generated by Voronoi Diagram to .MAT

    centerline_width._error_handling_save_centerline_mat(
        river_object=river_object,
        save_to_mat=save_to_mat,
        latitude_header=latitude_header,
        longitude_header=longitude_header,
        centerline_type=centerline_type,
        coordinate_unit=coordinate_unit)
    centerline_type = centerline_type.title()
    coordinate_unit = coordinate_unit.title()

    # set coordinate type and unit
    if coordinate_unit == "Decimal Degrees":
        if centerline_type == "Voronoi":
            centerline_coordinates_by_type = river_object.centerline_voronoi
        if centerline_type == "Equal Distance":
            centerline_coordinates_by_type = river_object.centerline_equal_distance
        if centerline_type == "Evenly Spaced":
            centerline_coordinates_by_type = river_object.centerline_evenly_spaced
        if centerline_type == "Smoothed":
            centerline_coordinates_by_type = river_object.centerline_smoothed
    if coordinate_unit == "Relative Distance":
        if centerline_type == "Voronoi":
            centerline_coordinates_by_type = river_object.centerline_voronoi_relative
        if centerline_type == "Equal Distance":
            centerline_coordinates_by_type = river_object.centerline_equal_distance_relative
        if centerline_type == "Evenly Spaced":
            centerline_coordinates_by_type = river_object.centerline_evenly_spaced_relative
        if centerline_type == "Smoothed":
            centerline_coordinates_by_type = river_object.centerline_smoothed_relative

    # .mat files do not allow for spaces or special characters in the header
    # convert spaces/special characters to underscores
    if coordinate_unit == "Decimal Degrees":
        if latitude_header is None:
            latitude_header = f"{centerline_type.replace(' ', '_')}_Centerline_Latitude_Deg"
        if longitude_header is None:
            longitude_header = f"{centerline_type.replace(' ', '_')}_Centerline_Longitude_Deg"
    if coordinate_unit == "Relative Distance":
        if latitude_header is None:
            latitude_header = f"{centerline_type.replace(' ', '_')}_Relative_Distance_Y_From_Latitude_m"
        if longitude_header is None:
            longitude_header = f"{centerline_type.replace(' ', '_')}_Relative_Distance_X_From_Longitude_m"

    latitude_lst = []
    longtiude_lst = []

    if centerline_coordinates_by_type is not None:
        for latitude_longitude in centerline_coordinates_by_type:
            longtiude_lst.append(latitude_longitude[0])
            latitude_lst.append(latitude_longitude[1])
    else:
        logger.warn(
            f"\nWARNING, no {centerline_type} centerline coordinates found, {save_to_mat} file generated will be empty"
        )

    # Centerline dictionary of latitude and longtiude centerline coordinates
    centerline_dict = {
        latitude_header: np.asarray(latitude_lst),
        longitude_header: np.asarray(longtiude_lst)
    }

    # Save to matlab format (.mat)
    savemat(save_to_mat, mdict=centerline_dict)
