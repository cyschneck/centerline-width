# generates baseline images for all plot types (pytest)
import centerline_width
import matplotlib.pyplot as plt

if __name__ == "__main__":
    centerline_width.kml_to_csv(left_kml="data/leftbank.kml",
                                right_kml="data/rightbank.kml",
                                flip_direction=True,
                                csv_output="data/river_coords.csv")

    river_object = centerline_width.CenterlineWidth(
        csv_data="data/river_coords.csv", cutoff=100)
    is_debug = False  # set to False when generating, True when debugging to view all plots

    ################### plot_centerline() ##########################################################

    center_type_options = [("Voronoi", "Black"),
                           ("Equal Distance", "mediumorchid"),
                           ("Evenly Spaced", "fuchsia"), ("Smoothed", "blue")]
    coord_type_options = ["Relative Distance", "Decimal Degrees"]
    mark_type_options = ["Line", "Scatter"]

    # Plot combinations of centerline types, colors, and coordinate units
    for mark_type in mark_type_options:
        for coord_type in coord_type_options:
            for center_type in center_type_options:
                centerline_option = center_type[0].replace(" ", "_").lower()
                coord_option = coord_type.replace(" ", "_").lower()
                marker_option = mark_type.lower()
                river_object.plot_centerline(
                    save_plot_name=
                    f"centerline_width/pytests/baseline_plots/{centerline_option}_{coord_option}_{marker_option}",
                    centerline_type=center_type[0],
                    centerline_color=center_type[1],
                    coordinate_unit=coord_type,
                    marker_type=mark_type,
                    dark_mode=is_debug,
                    show_plot=is_debug)
        plt.close()

    # display all possible paths
    display_all_paths = [True, False]
    for is_display_paths in display_all_paths:
        display_option = str(is_display_paths).lower()
        river_object.plot_centerline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/display_all_possible_paths_{display_option}",
            display_all_possible_paths=is_display_paths,
            dark_mode=is_debug,
            show_plot=is_debug)
        plt.close()

    # display Voronoi graphs
    display_voronoi_graph = [True, False]
    for is_display_voronoi in display_voronoi_graph:
        voronoi_option = str(is_display_voronoi).lower()
        river_object.plot_centerline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/display_voronoi_graph_{voronoi_option}",
            display_voronoi=is_display_voronoi,
            dark_mode=is_debug,
            show_plot=is_debug)
        plt.close()

    # display dark mode
    dark_mode_option = [True, False]
    for is_dark_mode in dark_mode_option:
        dark_mode_option = str(is_dark_mode).lower()
        river_object.plot_centerline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/dark_mode_{dark_mode_option}",
            dark_mode=is_dark_mode,
            show_plot=is_debug)
        plt.close()

    # display equal axis
    equal_axis_option = [True, False]
    for is_equal_axis in equal_axis_option:
        equal_axis_option = str(is_equal_axis).lower()
        river_object.plot_centerline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/equal_axis_{equal_axis_option}",
            equal_axis=is_equal_axis,
            dark_mode=is_debug,
            show_plot=is_debug)
        plt.close()

    ################### plot_centerline_width() ########################################################
    coord_type_options = ["Relative Distance", "Decimal Degrees"]
    is_apply_smoothing = [True, False]
    transect_slope_type = ["Direct", "Average"]
    is_remove_intersections = [True, False]

    # Plot combinations of coordinate units and apply_smoothing
    for is_smoothed in is_apply_smoothing:
        for coord_type in coord_type_options:
            for transect_type in transect_slope_type:
                for is_remove in is_remove_intersections:
                    coord_option = coord_type.replace(" ", "_").lower()
                    river_object.plot_centerline_width(
                        save_plot_name=
                        f"centerline_width/pytests/baseline_plots/width_{coord_option}_removeIntersections{is_remove}_smoothed{is_smoothed}_transectSlope{transect_type}",
                        apply_smoothing=is_smoothed,
                        coordinate_unit=coord_type,
                        transect_slope=transect_type,
                        remove_intersections=is_remove,
                        show_plot=False)
                    plt.close()

    # Display centerline option
    display_centerline_options = [True, False]
    for show_centerline in display_centerline_options:
        river_object.plot_centerline_width(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/width_displayCenterline{show_centerline}",
            display_true_centerline=show_centerline,
            show_plot=False)
        plt.close()

    # Display Dark Mode
    dark_mode_options = [True, False]
    for is_dark in dark_mode_options:
        river_object.plot_centerline_width(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/width_isDarkMode{is_dark}",
            dark_mode=is_dark,
            show_plot=False)
        plt.close()

    # Display Equal Axis
    equal_axis_options = [True, False]
    for is_equal_axis in equal_axis_options:
        river_object.plot_centerline_width(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/width_isEqualAxis{is_equal_axis}",
            equal_axis=is_equal_axis,
            show_plot=False)
        plt.close()

    # Flag intersections
    is_flag_intersections_options = [True, False]
    for flag_intersect in is_flag_intersections_options:
        river_object.plot_centerline_width(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/width_flagIntersections{flag_intersect}",
            flag_intersections=flag_intersect,
            show_plot=False)
        plt.close()
