########################################################################
# Example script of centerline-width package with built-in data
# Data file .kml for left bank: 43deg44_18dot23_N_101deg27_7dot61_W_lb
# Data file .kml for right bank: 43deg44_18dot23_N_101deg27_7dot61_W_lb
#
# To run in terminal:
#            python centerline_width_example_script.py
#
########################################################################

import centerline_width as cw


def main():

    if __name__ != '__main__':
        raise RuntimeError(
            "Calling function in a context other than __main__ is not supported."
        )

    # create txt file of bank points
    cw.extractPointsToTextFile(
        left_kml="43deg44_18dot23_N_101deg27_7dot61_W_lb.kml",
        right_kml="43deg44_18dot23_N_101deg27_7dot61_W_rb.kml",
        text_output_name="43deg44_18dot23_N_101deg27_7dot61_W.txt")

    # convert txt file to csv file for digesting with centerline-width
    cw.convertColumnsToCSV(text_file="43deg44_18dot23_N_101deg27_7dot61_W.txt")

    # create river object
    ro = cw.CenterlineWidth(csv_data="43deg44_18dot23_N_101deg27_7dot61_W.csv",
                            optional_cutoff=None,
                            interpolate_data=True,
                            interpolate_n=7,
                            interpolate_n_centerpoints=1200,
                            equal_distance=5,
                            ellipsoid="WGS84")

    # plot the centerline with Decimal Degrees (by default)
    ro.plot_centerline(
        centerline_type="Equal Distance",
        display_all_possible_paths=False,
        save_plot_name="43deg44_18dot23_N_101deg27_7dot61_W_centerline.png")

    # plot the centerline with Relative Distance
    ro.plot_centerline(
        centerline_type="Equal Distance",
        display_all_possible_paths=False,
        coordinate_unit="Relative Distance",
        save_plot_name="43deg44_18dot23_N_101deg27_7dot61_W_centerline.png")

    # save to csv to import back into google earth pro
    ro.save_centerline_csv(save_to_csv="equal_distance_coordinates.csv",
                           centerline_type="Equal Distance",
                           latitude_header="lat",
                           longitude_header="lon")

    # save to mat to import into matlab
    ro.save_centerline_mat(save_to_mat="equal_distance_coordinates.mat",
                           centerline_type="Equal Distance",
                           latitude_header="lat",
                           longitude_header="lon")

    # plot width lines
    ro.plot_centerline_width(
        display_true_centerline=True,
        transect_span_distance=3,
        apply_smoothing=True,
        remove_intersections=True,
        save_plot_name="43deg44_18dot23_N_101deg27_7dot61_W_width.png")

    # save width distance and coordinates to .csv
    river_width_dict = ro.width(transect_span_distance=3,
                                apply_smoothing=True,
                                remove_intersections=True,
                                save_to_csv="width_distance.csv")


if __name__ == '__main__':
    main()
