#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      plotDiagrams.py plots river coordinates and width with Matplotlib                          #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - plotCenterlineBackend: backend share                    #
#                                              components for each plot                           #
#                                              csv                                                #
#                                                                                                 #
#                                       - plot_centerline: plot centerline and                    #
#                                              river points/polygons                              #
#                                                                                                 #
#                                       - plot_centerline_width: plot centerline                  #
#                                              and river with width lines                         #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# Built-in Python functions
import math
import logging

# External Python libraries
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def plotCenterlineBackend(
        river_object: centerline_width.CenterlineWidth = None,
        display_true_centerline: bool = True,
        centerline_type: str = "Voronoi",
        marker_type: str = "line",
        centerline_color: str = "black",
        dark_mode: bool = False,
        equal_axis: bool = False,
        coordinate_unit: str = None):
    # Shared components between plot_centerline() and plotCenterlineWidth
    coordinate_unit = coordinate_unit.title()

    # set plot to dark background and alternate centerline color default
    if dark_mode:
        plt.style.use('dark_background')
        if centerline_color == "black":
            centerline_color = "white"
    if not dark_mode:
        plt.style.use('default')  # revert to white background

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # set x/y axes equal (useful to see width lines as perpendicular)
    if equal_axis:
        ax.set_aspect('equal', adjustable='datalim')
    if not equal_axis:
        ax.set_aspect('auto')

    scatter_plot_size = 4
    # Plot River as a Polygon
    if coordinate_unit == "Decimal Degrees":
        plt.plot(*river_object.bank_polygon.exterior.xy, c="gainsboro")
        plt.plot(*river_object.top_bank.xy, c="forestgreen")
        plt.plot(*river_object.bottom_bank.xy, c="lightcoral")
    if coordinate_unit == "Relative Distance":
        plt.plot(*river_object.bank_polygon_relative.exterior.xy,
                 c="gainsboro")
        plt.plot(*river_object.top_bank_relative.xy, c="forestgreen")
        plt.plot(*river_object.bottom_bank_relative.xy, c="lightcoral")

    # Choose between Decimal Degrees and Relative Distances for X, Y coordinates
    if coordinate_unit == "Decimal Degrees":
        right_coords = river_object.right_bank_coordinates
        left_coords = river_object.left_bank_coordinates
    if coordinate_unit == "Relative Distance":
        right_coords = river_object.right_bank_relative_coordinates
        left_coords = river_object.left_bank_relative_coordinates

    x = [i[0] for i in right_coords]
    y = [i[1] for i in right_coords]
    plt.scatter(x, y, c="dodgerblue", s=scatter_plot_size, label="Right Bank")
    x = [i[0] for i in left_coords]
    y = [i[1] for i in left_coords]
    plt.scatter(x, y, c="orange", s=scatter_plot_size, label="Left Bank")

    # Plot centerline found from NetworkX
    valid_path_through = False

    centerline_type = centerline_type.title()
    marker_type = marker_type.title()

    # Choose between Decimal Degrees and Centerline Type
    if centerline_type == "Voronoi":
        centerline_legend = "Voronoi Centerline Coordinates"
        if coordinate_unit == "Decimal Degrees":
            centerline_coordinates_by_type = river_object.centerline_voronoi
        if coordinate_unit == "Relative Distance":
            centerline_coordinates_by_type = river_object.centerlineVoronoiRelative

    if centerline_type == "Equal Distance":
        centerline_legend = "Equal Distance Centerline Coordinates"
        if coordinate_unit == "Decimal Degrees":
            centerline_coordinates_by_type = river_object.centerlineEqualDistance
        if coordinate_unit == "Relative Distance":
            centerline_coordinates_by_type = river_object.centerlineEqualDistanceRelative

    if centerline_type == "Evenly Spaced":
        centerline_legend = "Evenly Spaced Centerline Coordinates"
        if coordinate_unit == "Decimal Degrees":
            centerline_coordinates_by_type = river_object.centerlineEvenlySpaced
        if coordinate_unit == "Relative Distance":
            centerline_coordinates_by_type = river_object.centerlineEvenlySpacedRelative

    if centerline_type == "Smoothed":
        centerline_legend = "Smoothed Centerline Coordinates"
        if coordinate_unit == "Decimal Degrees":
            centerline_coordinates_by_type = river_object.centerlineSmoothed
        if coordinate_unit == "Relative Distance":
            centerline_coordinates_by_type = river_object.centerlineSmoothedRelative

    # Plot the centerline coordinates
    if centerline_coordinates_by_type:
        valid_path_through = True
        if display_true_centerline:
            if marker_type == "Line":
                plt.plot(*zip(*centerline_coordinates_by_type),
                         c=centerline_color,
                         label=centerline_legend,
                         zorder=10)
            if marker_type == "Scatter":
                x = []
                y = []
                for k, v in centerline_coordinates_by_type:
                    x.append(k)
                    y.append(v)
                    # Plot labels for each point
                    #display_labels = True
                    #if display_labels:
                    #    ax.annotate(f"{k}, {v}", (k, v), fontsize=8)
                plt.scatter(x,
                            y,
                            c=centerline_color,
                            label=centerline_legend,
                            s=8,
                            zorder=10)

    # Dynamically assign the starting and ending
    if river_object.starting_node is not None:  # error handling for when data is too small to generate centerline coordinates
        ss = 45  # scatter size
        if coordinate_unit == "Decimal Degrees":
            plt.scatter(river_object.starting_node[0],
                        river_object.starting_node[1],
                        c="green",
                        label="Starting Node",
                        s=ss)
            plt.scatter(river_object.ending_node[0],
                        river_object.ending_node[1],
                        c="red",
                        label="Ending Node",
                        s=ss)
        if coordinate_unit == "Relative Distance":
            plt.scatter(river_object.starting_node_relative[0],
                        river_object.starting_node_relative[1],
                        c="green",
                        label="Starting Node",
                        s=ss)
            plt.scatter(river_object.ending_node_relative[0],
                        river_object.ending_node_relative[1],
                        c="red",
                        label="Ending Node",
                        s=ss)

    return fig, ax, valid_path_through


def plot_centerline(river_object: centerline_width.CenterlineWidth = None,
                    centerline_type: str = "Voronoi",
                    marker_type: str = "line",
                    centerline_color: str = "black",
                    dark_mode: bool = False,
                    equal_axis: bool = False,
                    display_all_possible_paths: bool = False,
                    plot_title: str = None,
                    save_plot_name: str = None,
                    display_voronoi: bool = False,
                    show_plot: bool = True,
                    coordinate_unit: str = "Decimal Degrees") -> None:
    # Plot Centerline of River
    centerline_width.errorHandlingPlotCenterline(
        river_object=river_object,
        centerline_type=centerline_type,
        marker_type=marker_type,
        centerline_color=centerline_color,
        dark_mode=dark_mode,
        equal_axis=equal_axis,
        display_all_possible_paths=display_all_possible_paths,
        plot_title=plot_title,
        save_plot_name=save_plot_name,
        display_voronoi=display_voronoi,
        show_plot=show_plot,
        coordinate_unit=coordinate_unit)

    fig, ax, valid_path_through = plotCenterlineBackend(
        river_object=river_object,
        display_true_centerline=True,
        centerline_type=centerline_type,
        marker_type=marker_type,
        centerline_color=centerline_color,
        dark_mode=dark_mode,
        equal_axis=equal_axis,
        coordinate_unit=coordinate_unit)

    coordinate_unit = coordinate_unit.title()

    # Display the Voronoi Diagram
    if display_voronoi:
        voronoi_line_color = 'black'
        if dark_mode: voronoi_line_color = 'moccasin'
        if coordinate_unit == "Decimal Degrees":
            voronoi_plot_2d(river_object.bank_voronoi,
                            show_points=True,
                            point_size=1,
                            line_colors=voronoi_line_color,
                            ax=ax)
        if coordinate_unit == "Relative Distance":
            voronoi_plot_2d(river_object.bank_voronoi_relative,
                            show_points=True,
                            point_size=1,
                            line_colors=voronoi_line_color,
                            ax=ax)

    # Plot all possible paths with text for positions
    if display_all_possible_paths:
        if coordinate_unit == "Decimal Degrees":
            for i in range(len(river_object.x_voronoi_ridge_point)):
                plt.plot(river_object.x_voronoi_ridge_point[i],
                         river_object.y_voronoi_ridge_point[i],
                         'cyan',
                         linewidth=1,
                         zorder=1)
        if coordinate_unit == "Relative Distance":
            for i in range(len(river_object.x_voronoi_ridge_point_relative)):
                plt.plot(river_object.x_voronoi_ridge_point_relative[i],
                         river_object.y_voronoi_ridge_point_relative[i],
                         'cyan',
                         linewidth=1,
                         zorder=1)

    # Plot Title, Legends, and Axis Labels
    if not plot_title:
        plt.title(
            f"River Coordinates: Valid Centerline = {valid_path_through}, Valid Polygon = {river_object.bank_polygon.is_valid}, Interpolated = {river_object.interpolate_data}"
        )
    else:
        plt.title(plot_title)

    if coordinate_unit == "Decimal Degrees":
        plt.xlabel("Longitude (°)")
        plt.ylabel("Latitude (°)")
    if coordinate_unit == "Relative Distance":
        plt.xlabel("Relative Distance X (m)")
        plt.ylabel("Relative Distance Y (m)")

    plt.legend(loc="upper right")
    if show_plot: plt.show()
    if not show_plot: plt.close()
    if save_plot_name: fig.savefig(save_plot_name)


def plot_centerline_width(
        river_object: centerline_width.CenterlineWidth = None,
        plot_title: str = None,
        save_plot_name: str = None,
        display_true_centerline: bool = True,
        transect_span_distance: int = 3,
        transect_slope: str = "Average",
        apply_smoothing: bool = False,
        flag_intersections: bool = True,
        remove_intersections: bool = False,
        dark_mode: bool = False,
        equal_axis: bool = False,
        show_plot: bool = True,
        coordinate_unit: str = "Decimal Degrees") -> None:
    # Plot Width Lines based on Centerline
    centerline_width.errorHandlingPlotCenterlineWidth(
        river_object=river_object,
        plot_title=plot_title,
        save_plot_name=save_plot_name,
        display_true_centerline=display_true_centerline,
        transect_span_distance=transect_span_distance,
        transect_slope=transect_slope,
        apply_smoothing=apply_smoothing,
        flag_intersections=flag_intersections,
        remove_intersections=remove_intersections,
        dark_mode=dark_mode,
        equal_axis=equal_axis,
        show_plot=show_plot,
        coordinate_unit=coordinate_unit)

    fig, ax, valid_path_through = plotCenterlineBackend(
        river_object=river_object,
        display_true_centerline=display_true_centerline,
        centerline_type="Voronoi",
        marker_type="line",
        centerline_color="black",
        dark_mode=dark_mode,
        equal_axis=equal_axis,
        coordinate_unit=coordinate_unit)

    coordinate_unit = coordinate_unit.title()
    transect_slope = transect_slope.title()

    # Determine the Width of River
    number_of_evenly_spaced_points = ""

    if river_object.centerline_voronoi is not None:
        number_of_evenly_spaced_points = f"\nCenterline made of {river_object.interpolate_n_centerpoints} Fixed Points, width lines generated every {transect_span_distance} points"
        if river_object.starting_node is not None:  # error handling for when data is too small to generate centerline coordinates

            # if using smoothing, replace left/right coordinates with the smoothed variation
            if apply_smoothing:
                right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(
                    river_object=river_object,
                    centerline_coordinates=river_object.centerlineSmoothed,
                    transect_span_distance=transect_span_distance,
                    transect_slope=transect_slope,
                    remove_intersections=remove_intersections,
                    coordinate_unit=coordinate_unit)
                x = []
                y = []
                if coordinate_unit == "Decimal Degrees":
                    smoothed_coords = river_object.centerlineSmoothed
                if coordinate_unit == "Relative Distance":
                    smoothed_coords = river_object.centerlineSmoothedRelative
                for k, v in smoothed_coords:
                    x.append(k)
                    y.append(v)
                plt.scatter(x,
                            y,
                            c="blue",
                            label="Smoothed Centerline Coordinates",
                            s=5)
            else:
                # recreate the centerline with evenly spaced points
                right_width_coordinates, left_width_coordinates, num_intersection_coordinates = centerline_width.riverWidthFromCenterlineCoordinates(
                    river_object=river_object,
                    centerline_coordinates=river_object.centerlineEvenlySpaced,
                    transect_span_distance=transect_span_distance,
                    transect_slope=transect_slope,
                    remove_intersections=remove_intersections,
                    coordinate_unit=coordinate_unit)

            invalid_label_added = False  # prevent legend for width lines from being generated more than once (because is inside a loop)
            valid_label_added = False  # prevent legend for width lines from being generated more than once (because is inside a loop)
            # plot width lines
            for center_coord, edge_coord in right_width_coordinates.items():
                x_points = (right_width_coordinates[center_coord][0],
                            left_width_coordinates[center_coord][0])
                y_points = (right_width_coordinates[center_coord][1],
                            left_width_coordinates[center_coord][1])
                if flag_intersections:
                    if num_intersection_coordinates[center_coord] > 0:
                        if remove_intersections:
                            logger.error(
                                "\nERROR: Unable to completely resolve all intersections lines to be removed"
                            )
                        if not invalid_label_added:
                            plt.plot(x_points,
                                     y_points,
                                     'red',
                                     label="Intersecting Width",
                                     linewidth=1)
                            invalid_label_added = True
                        else:
                            plt.plot(x_points, y_points, 'red', linewidth=1)
                    else:
                        if not valid_label_added:
                            plt.plot(x_points,
                                     y_points,
                                     'green',
                                     label="Non-Intersecting Width",
                                     linewidth=1)
                            valid_label_added = True
                        else:
                            plt.plot(x_points, y_points, 'green', linewidth=1)
                else:
                    # display all width lines as green since flag_instersection=False
                    if not valid_label_added:
                        plt.plot(x_points,
                                 y_points,
                                 'green',
                                 label="Width",
                                 linewidth=1)
                        valid_label_added = True
                    else:
                        plt.plot(x_points, y_points, 'green', linewidth=1)

    # Plot Title, Legends, and Axis Labels
    if not plot_title:
        plt.title(
            f"River Width Coordinates: Valid Centerline = {valid_path_through}, Valid Polygon = {river_object.bank_polygon.is_valid}{number_of_evenly_spaced_points}, Interpolated = {river_object.interpolate_data}"
        )
    else:
        plt.title(plot_title)

    if coordinate_unit == "Decimal Degrees":
        plt.xlabel("Longitude (°)")
        plt.ylabel("Latitude (°)")
    if coordinate_unit == "Relative Distance":
        plt.xlabel("Relative Distance X (m)")
        plt.ylabel("Distance Distance Y (m)")

    plt.legend(loc="upper right")
    if show_plot: plt.show()
    if not show_plot: plt.close()
    if save_plot_name: fig.savefig(save_plot_name)
