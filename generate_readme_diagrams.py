# generates plots for README.md documentation
import centerline_width
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d
import networkx as nx

if __name__ == "__main__":
    centerline_width.kml_to_csv(left_kml="data/leftbank.kml",
                                right_kml="data/rightbank.kml",
                                flip_direction=True,
                                csv_output="data/river_coords.csv")
    ro_5 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                            optional_cutoff=5)
    ro_10 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                             optional_cutoff=10)
    ro_15 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                             optional_cutoff=15)
    ro_250 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                              optional_cutoff=250)
    ro_550 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                              optional_cutoff=550)
    ro_725 = centerline_width.riverCenterline(csv_data="data/river_coords.csv",
                                              optional_cutoff=725)
    is_debug = False  # set to False when generating, True when debugging to view all plots

    ################### Introduction and Quickstart ##########################################

    river_object = centerline_width.riverCenterline(
        csv_data="data/river_coords.csv")
    river_object.plot_centerline(
        plot_title="Centerline with Riverbanks",
        save_plot_name="data/doc_examples/river_example.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        save_plot_name="data/doc_examples/river_coords_centerline.png",
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_width.png",
        apply_smoothing=True,
        remove_intersections=True,
        display_true_centerline=False,
        show_plot=is_debug)
    ro_550.plot_centerline(
        save_plot_name=
        "data/doc_examples/river_relative_distance_coords_centerline.png",
        coordinate_unit="Relative Distance",
        show_plot=is_debug)

    ################### Centerline and Width ################################################

    ro_550_interpolate_centerline_75 = centerline_width.riverCenterline(
        csv_data="data/river_coords.csv",
        optional_cutoff=550,
        interpolate_n_centerpoints=75)
    ro_550_interpolate_centerline_75.plot_centerline(
        save_plot_name="data/doc_examples/interpolate_n_centerpoints_75.png",
        centerline_type="Evenly Spaced",
        centerline_color="fuchsia",
        marker_type="scatter",
        show_plot=is_debug)
    ro_550_interpolate_centerline_200 = centerline_width.riverCenterline(
        csv_data="data/river_coords.csv",
        optional_cutoff=550,
        interpolate_n_centerpoints=200)
    ro_550_interpolate_centerline_200.plot_centerline(
        save_plot_name="data/doc_examples/interpolate_n_centerpoints_200.png",
        centerline_type="Evenly Spaced",
        centerline_color="fuchsia",
        marker_type="scatter",
        show_plot=is_debug)

    ################### Types of Centerlines ################################################
    ro_550.plot_centerline(
        save_plot_name="data/doc_examples/voronoi_centerline.png",
        centerline_type="Voronoi",
        centerline_color="black",
        marker_type="scatter",
        plot_title="Centerline Formed by Voronoi Diagram",
        show_plot=is_debug)
    ro_550.plot_centerline(
        save_plot_name="data/doc_examples/voronoi_centerline_relative.png",
        centerline_type="Voronoi",
        centerline_color="black",
        marker_type="scatter",
        coordinate_unit="Relative Distance",
        plot_title=
        "Centerline Formed by Voronoi Diagram with Relative Distance",
        show_plot=is_debug)
    ro_550.plot_centerline(
        save_plot_name="data/doc_examples/equal_distance_centerline.png",
        centerline_type="Equal Distance",
        centerline_color="mediumorchid",
        marker_type="scatter",
        plot_title=
        f"Centerline Formed by Points Equally Distanced Apart Every {ro_550.equal_distance} Meters",
        show_plot=is_debug)
    ro_550.plot_centerline(
        save_plot_name=
        "data/doc_examples/equal_distance_centerline_relative.png",
        centerline_type="Equal Distance",
        centerline_color="mediumorchid",
        marker_type="scatter",
        coordinate_unit="Relative Distance",
        plot_title=
        f"Centerline Formed by Points Equally Distanced Apart Every {ro_550.equal_distance} Meters with Relative Distance",
        show_plot=is_debug)
    ro_550_interpolate_centerline_200.plot_centerline(
        save_plot_name="data/doc_examples/evenly_spaced_centerline.png",
        centerline_type="Evenly Spaced",
        centerline_color="fuchsia",
        marker_type="scatter",
        plot_title=
        f"Centerline Formed by {ro_550_interpolate_centerline_200.interpolate_n_centerpoints} Evenly Spaced Centerline Points",
        show_plot=is_debug)
    ro_550_interpolate_centerline_200.plot_centerline(
        save_plot_name=
        "data/doc_examples/evenly_spaced_centerline_relative.png",
        centerline_type="Evenly Spaced",
        centerline_color="fuchsia",
        marker_type="scatter",
        coordinate_unit="Relative Distance",
        plot_title=
        f"Centerline Formed by {ro_550_interpolate_centerline_200.interpolate_n_centerpoints} Evenly Spaced Centerline Points with Relative Distance",
        show_plot=is_debug)
    ro_550_interpolate_centerline_200.plot_centerline(
        save_plot_name="data/doc_examples/smoothed_centerline.png",
        centerline_type="Smoothed",
        centerline_color="blue",
        marker_type="scatter",
        plot_title=
        f"Centerline Formed by {ro_550_interpolate_centerline_200.interpolate_n_centerpoints} Smoothed Centerline Coordinates",
        show_plot=is_debug)
    ro_550_interpolate_centerline_200.plot_centerline(
        save_plot_name="data/doc_examples/smoothed_centerline_relative.png",
        centerline_type="Smoothed",
        centerline_color="blue",
        marker_type="scatter",
        coordinate_unit="Relative Distance",
        plot_title=
        f"Centerline Formed by {ro_550_interpolate_centerline_200.interpolate_n_centerpoints} Smoothed Centerline Coordinates with Relative Distance",
        show_plot=is_debug)

    ################### Plot plot_centerline() #############################################

    ro_550.plot_centerline(
        centerline_type="Smoothed",
        save_plot_name="data/doc_examples/river_centerline_type_smoothed.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        marker_type="Scatter",
        save_plot_name="data/doc_examples/river_marker_type_scatter.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        centerline_color="palegreen",
        save_plot_name="data/doc_examples/river_centerline_color.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        dark_mode=True,
        save_plot_name="data/doc_examples/river_dark_mode.png",
        show_plot=is_debug)
    ro_15.plot_centerline(
        equal_axis=False,
        save_plot_name="data/doc_examples/river_equal_axis_false.png",
        show_plot=is_debug)
    ro_15.plot_centerline(
        equal_axis=True,
        save_plot_name="data/doc_examples/river_equal_axis_true.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        display_all_possible_paths=True,
        save_plot_name=
        "data/doc_examples/river_display_all_possible_paths_true.png",
        show_plot=is_debug)
    ro_15.plot_centerline(
        display_voronoi=False,
        save_plot_name="data/doc_examples/river_display_voronoi_false.png",
        show_plot=is_debug)
    ro_15.plot_centerline(
        display_voronoi=True,
        save_plot_name="data/doc_examples/river_display_voronoi_true.png",
        show_plot=is_debug)
    ro_550.plot_centerline(
        coordinate_unit="Relative Distance",
        save_plot_name="data/doc_examples/river_coordinate_unit_rd.png",
        show_plot=is_debug)

    ################### Plot plot_centerline_width() ########################################

    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_with_centerline.png",
        display_true_centerline=True,
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_without_centerline.png",
        display_true_centerline=False,
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_without_smoothing.png",
        display_true_centerline=True,
        apply_smoothing=False,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_with_smoothing.png",
        display_true_centerline=False,
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_width_transect_6.png",
        display_true_centerline=False,
        transect_span_distance=6,
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_width_transect_30.png",
        display_true_centerline=False,
        transect_span_distance=30,
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_transect_avg.png",
        display_true_centerline=False,
        transect_slope="Average",
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_transect_direct.png",
        display_true_centerline=False,
        transect_slope="Direct",
        apply_smoothing=True,
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_keep_intersections.png",
        display_true_centerline=False,
        remove_intersections=False,
        apply_smoothing=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_remove_intersections.png",
        display_true_centerline=False,
        remove_intersections=True,
        apply_smoothing=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_dark_mode_false.png",
        display_true_centerline=True,
        remove_intersections=False,
        dark_mode=False,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_dark_mode_true.png",
        display_true_centerline=True,
        remove_intersections=False,
        dark_mode=True,
        show_plot=is_debug)
    ro_10.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_not_equal_default_ax.png",
        display_true_centerline=True,
        remove_intersections=True,
        equal_axis=False,
        show_plot=is_debug)
    ro_10.plot_centerline_width(
        save_plot_name="data/doc_examples/river_coords_equal_ax.png",
        display_true_centerline=True,
        remove_intersections=True,
        equal_axis=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_decimal_degrees.png",
        display_true_centerline=False,
        apply_smoothing=True,
        coordinate_unit="Decimal Degrees",
        remove_intersections=True,
        show_plot=is_debug)
    ro_550.plot_centerline_width(
        save_plot_name=
        "data/doc_examples/river_coords_width_relative_distance.png",
        display_true_centerline=False,
        apply_smoothing=True,
        coordinate_unit="Relative Distance",
        remove_intersections=True,
        show_plot=is_debug)

    ################### Algorithm to Determine Centerline ###############################


    def plotAlgorithm(fig_save_name=None,
                      plot_polygon=False,
                      plot_voronoi=False,
                      plot_all_possible_paths=False,
                      total_number_of_connections=0,
                      plot_top_bottom_banks=False,
                      plot_start_end_node=False,
                      plot_point_labels=False,
                      plot_centerline=False):
        left_bank = ro_15.left_bank_coordinates
        right_bank = ro_15.right_bank_coordinates

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        scatter_plot_size = 4

        right_coords = ro_15.right_bank_coordinates
        left_coords = ro_15.left_bank_coordinates

        if plot_polygon:
            plt.plot(*ro_15.bank_polygon.exterior.xy, c="gainsboro")

        x = [i[0] for i in right_coords]
        y = [i[1] for i in right_coords]
        plt.scatter(x,
                    y,
                    c="dodgerblue",
                    s=scatter_plot_size,
                    label="Right Bank")
        x = [i[0] for i in left_coords]
        y = [i[1] for i in left_coords]
        plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank")

        if plot_voronoi:
            voronoi_plot_2d(ro_15.bank_voronoi,
                            show_points=True,
                            point_size=1,
                            ax=ax)
        if plot_all_possible_paths:
            starting_node, ending_node, x_ridge_point, y_ridge_point, shortest_path_coordinates = centerline_width.centerlinePath(
                ro_15.bank_voronoi, ro_15.bank_polygon, ro_15.top_bank,
                ro_15.bottom_bank, total_number_of_connections)
            for i in range(len(x_ridge_point)):
                plt.plot(x_ridge_point[i],
                         y_ridge_point[i],
                         'cyan',
                         linewidth=1,
                         zorder=1)

        if plot_top_bottom_banks:
            plt.plot(*ro_15.top_bank.xy, c="forestgreen")
            plt.plot(*ro_15.bottom_bank.xy, c="lightcoral")

        if plot_start_end_node:
            plt.scatter(ro_15.starting_node[0],
                        ro_15.starting_node[1],
                        c="green",
                        label="Starting Node",
                        s=45)
            plt.scatter(ro_15.ending_node[0],
                        ro_15.ending_node[1],
                        c="red",
                        label="Ending Node",
                        s=45)

        if plot_point_labels:
            values_plotted = []
            for i in range(len(x_ridge_point)):
                first_connection = f"({x_ridge_point[i][0]}, {y_ridge_point[i][0]})"
                if first_connection not in values_plotted:
                    ax.annotate(first_connection,
                                (x_ridge_point[i][0], y_ridge_point[i][0]),
                                fontsize=6)
                    values_plotted.append(first_connection)
                second_connection = f"({x_ridge_point[i][1]}, {y_ridge_point[i][1]})"
                if second_connection not in values_plotted:
                    ax.annotate(second_connection,
                                (x_ridge_point[i][1], y_ridge_point[i][1]),
                                fontsize=6)
                    values_plotted.append(second_connection)

        if plot_centerline:
            plt.plot(*zip(*shortest_path_coordinates),
                     c="black",
                     label="Centerline",
                     zorder=10)

        plt.title("River Coordinates")
        plt.xlabel("Longitude (°)")
        plt.ylabel("Latitude (°)")

        if is_debug: plt.show()
        if not is_debug: plt.close()
        fig.savefig(fig_save_name)

        return fig, ax

    def plotNetworkXGraph(fig_save_name=None):
        # Draw NetworkX Graph
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        start_end_points_dict = centerline_width.pointsFromVoronoi(
            ro_15.bank_voronoi, ro_15.bank_polygon)
        nx_graphs, largest_subgraph_nodes = centerline_width.generateNXGraph(
            start_end_points_dict)
        nx.draw(nx_graphs, with_labels=True, font_size=10)
        plt.draw()
        if is_debug: plt.show()
        if not is_debug: plt.close()
        fig.savefig(fig_save_name)

    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step1.png")
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step2.png",
                  plot_polygon=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step3.png",
                  plot_polygon=True,
                  plot_voronoi=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step4.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step5.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True,
                  plot_top_bottom_banks=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step6.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True,
                  plot_top_bottom_banks=True,
                  plot_start_end_node=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step7.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True,
                  plot_top_bottom_banks=True,
                  plot_start_end_node=True,
                  plot_point_labels=True)
    plotNetworkXGraph(fig_save_name="data/doc_examples/algorithm_step8.png")
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step9.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True,
                  plot_top_bottom_banks=True,
                  plot_start_end_node=True,
                  plot_centerline=True)
    plotAlgorithm(fig_save_name="data/doc_examples/algorithm_step10.png",
                  plot_polygon=True,
                  plot_all_possible_paths=True,
                  plot_top_bottom_banks=True,
                  total_number_of_connections=1)

    ################### Debugging, Error Handling, and Edge Cases ###############################

    ro_725.plot_centerline(
        save_plot_name="data/doc_examples/invalid_too_wide.png",
        display_all_possible_paths=True,
        show_plot=is_debug)
    ro_250.plot_centerline(
        save_plot_name="data/doc_examples/invalid_minor_polygon.png",
        display_all_possible_paths=True,
        show_plot=is_debug)
    ro_1000 = centerline_width.riverCenterline(
        csv_data="data/river_coords.csv", optional_cutoff=1000)
    ro_1000.plot_centerline(
        save_plot_name="data/doc_examples/invalid_major_polygon.png",
        display_all_possible_paths=True,
        show_plot=is_debug)
    ro_5.plot_centerline(
        save_plot_name="data/doc_examples/invalid_too_small.png",
        display_voronoi=True,
        show_plot=is_debug)

    centerline_width.txt_to_csv(txt_input="data/river_coords.txt",
                                flip_direction=False)
    ro_400 = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
    ro_400.plot_centerline(
        save_plot_name="data/doc_examples/invalid_flipped_banks.png",
        show_plot=is_debug)
