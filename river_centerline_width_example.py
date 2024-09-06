# Find the center point and width between latitude/longitude points along right/left river bank
import centerline_width

if __name__ == "__main__":
    centerline_width.kml_to_csv(left_kml="data/leftbank.kml",
                                right_kml="data/rightbank.kml",
                                flip_direction=True,
                                csv_output="data/river_coords.csv")

    #centerline_width.extractPointsToTextFile(left_kml="data/59deg48_18dot87_N_69deg46_59dot57_E_lb.kml",
    #                                        right_kml="data/59deg48_18dot87_N_69deg46_59dot57_E_rb.kml",
    #                                        text_output_name="data/N_output.txt")
    #centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt", flip_direction=True)

    # Valid Examples
    cutoff = None
    #cutoff = 10
    #cutoff = 15  # valid centerline, valid path, valid polygon, valid starting node, valid ending node
    #cutoff = 30
    #cutoff = 100 # valid centerline, valid path, valid polygon, valid starting node, valid ending node
    cutoff = 550  # valid centerline, valid path, valid polygon, valid starting node, valid ending node
    # Invalid Examples
    #cutoff = 5 # invalid centerline, invalid path, valid polygon, invalid starting node, invalid ending nodes
    #cutoff = 250 # valid centerline, valid path, invalid polygon, valid starting node, valid ending nodes
    #cutoff = 40 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
    #cutoff = 700 # invalid centerline, valid path, valid polgyon, invalid starting node, valid ending node
    #cutoff = 1000 # invalid centerline, invalid path, invalid polgyon, invalid starting node, valid ending node

    river = centerline_width.CenterlineWidth(csv_data="data/river_coords.csv",
                                             cutoff=cutoff,
                                             interpolate_data=False,
                                             interpolate_n_centerpoints=None,
                                             ellipsoid="WGS84")

    #print(river)
    #print(river.__dict__.keys())
    print(f"centerline_voronoi = {river.centerline_voronoi}")
    print(f"centerline_equal_distance = {river.centerline_equal_distance}")
    print(f"centerline_evenly_spaced = {river.centerline_evenly_spaced}")
    print(f"centerline_smoothed = {river.centerline_smoothed}")
    print(f"\nCenterline Length = {river.centerline_length} km")
    print(f"Right Bank Length = {river.right_bank_length} km")
    print(f"Left Bank Length = {river.left_bank_length} km")
    print("centerline_voronoi_relative = {river.centerline_voronoi_relative}")
    print(
        f"centerline_equal_distance_relative = {river.centerline_equal_distance_relative}"
    )
    print(
        f"centerline_evenly_spaced_relative = {river.centerline_evenly_spaced_relative}"
    )
    print(
        f"centerline_smoothed_relative = {river.centerline_smoothed_relative}")
    print(f"Centerline Length = {river.centerline_length * 1000} m")
    print(f"ellipsoid = {river.ellipsoid}")
    print(river.right_bank_relative_coordinates)
    print(river.left_bank_relative_coordinates)
    print(f"area = {river.area} km^2")
    print(f"sinuosity  = {river.sinuosity}")
    incremental_sinuosity = river.incremental_sinuosity(incremental_points=215,
                                                        save_to_csv=None)
    print(f"incremental sinuosity  = {incremental_sinuosity}")

    #coord_type = "relative DIStance"
    coord_type = "decimal degrees"
    center_type = "VorOnoi"

    #river.save_centerline_csv(save_to_csv="centerline_for_csv.csv",
    #                          centerline_type=center_type,
    #                          coordinate_unit=coord_type)
    #river.saveCenterlineMAT(save_to_mat="centerline_for_matlab.mat", centerline_type=center_type, coordinate_unit=coord_type)
    river.save_centerline_csv(save_to_csv="centerline_for_csv.csv",
                              latitude_header="lat",
                              longitude_header="long",
                              centerline_type="Equal Distance")
    river.save_centerline_mat(save_to_mat="centerline_for_matlab.mat",
                              latitude_header="lat",
                              longitude_header="long",
                              centerline_type="Evenly Spaced")

    river.plot_centerline(centerline_type="Evenly Spaced",
                          centerline_color="fuchsia",
                          marker_type="scatter",
                          dark_mode=True)

    # Plot river bank centerline
    river.plot_centerline(save_plot=None,
                          centerline_type=center_type,
                          marker_type="line",
                          centerline_color="black",
                          display_all_possible_paths=False,
                          display_voronoi=False,
                          plot_title=None,
                          dark_mode=True,
                          equal_axis=True,
                          show_plot=True,
                          coordinate_unit=coord_type)

    transect = 5
    slope_type = "average"

    # Plot river bank width line
    river.plot_centerline_width(save_plot=None,
                                plot_title=None,
                                display_true_centerline=False,
                                transect_span_distance=transect,
                                transect_slope=slope_type,
                                apply_smoothing=True,
                                flag_intersections=True,
                                remove_intersections=True,
                                dark_mode=True,
                                equal_axis=False,
                                show_plot=True,
                                coordinate_unit=coord_type)

    # Return width line for each centerline coordinates
    river_width_dict = river.width(transect_span_distance=transect,
                                   transect_slope=slope_type,
                                   apply_smoothing=False,
                                   remove_intersections=False,
                                   save_to_csv=None,
                                   coordinate_reference="banks",
                                   coordinate_unit=coord_type)

    print(f"\nriver width dict = {river_width_dict}\n")
