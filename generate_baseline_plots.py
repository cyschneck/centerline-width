# generates baseline images for all plot types (pytest)
import centerline_width
import matplotlib.pyplot as plt

if __name__ == "__main__":
    centerline_width.extractPointsToTextFile(
        left_kml="data/leftbank.kml",
        right_kml="data/rightbank.kml",
        text_output_name="data/river_coords.txt")
    centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt",
                                         flipBankDirection=True)

    river_object = centerline_width.riverCenterline(
        csv_data="data/river_coords.csv", optional_cutoff=550)
    is_debug = False  # set to False when generating, True when debugging to view all plots

    ################### plotCenterline() ##########################################################

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
                river_object.plotCenterline(
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
        river_object.plotCenterline(
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
        river_object.plotCenterline(
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
        river_object.plotCenterline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/dark_mode_{dark_mode_option}",
            dark_mode=is_dark_mode,
            show_plot=is_debug)
        plt.close()

    # display equal axis
    equal_axis_option = [True, False]
    for is_equal_axis in equal_axis_option:
        equal_axis_option = str(is_equal_axis).lower()
        river_object.plotCenterline(
            save_plot_name=
            f"centerline_width/pytests/baseline_plots/equal_axis_{equal_axis_option}",
            equal_axis=is_equal_axis,
            dark_mode=is_debug,
            show_plot=is_debug)
        plt.close()

    ################### plotCenterlineWidth() ########################################################
    coord_type_options = ["Relative Distance", "Decimal Degrees"]
    is_apply_smoothing = [True, False]

    # Plot combinations of coordinate units and apply_smoothing
    for is_smoothed in is_apply_smoothing:
        for coord_type in coord_type_options:
            coord_option = coord_type.replace(" ", "_").lower()
            is_smoothed_option = str(is_smoothed).lower()
            river_object.plotCenterlineWidth(
                save_plot_name=
                f"centerline_width/pytests/baseline_plots/width_{coord_option}_isSmoothed_{is_smoothed_option}",
                apply_smoothing=is_smoothed,
                coordinate_unit=coord_type,
                show_plot=False)
            plt.close()

    display_centerline = [True, False]
    transect_span_distance_type = ["Direct", "Average"]
    is_flag_intersections = [True, False]
    is_remove_intersections = [True, False]
    is_dark_mode = [True, False]
    is_dark_mode = [True, False]
    is_equal_axis = [True, False]
