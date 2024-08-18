#                                                                                                 #
#                                                                                                 #
#                                                                                                 #
#      riverCenterlineClass.py builds and defines the values for the river class                  #
#      that are used in the centerline, width, and plotting functions                             #
#                                                                                                 #
#      This includes the functions for:                                                           #
#                                       - CenterlineWidth: river class that holds all             #
#                                              centerline/width features and functions            #
#                                                                                                 #
#                                                                                                 #
#                                                                                                 #

# River object class used for all functions and centerline functions

# Built-in Python functions
import warnings  # Pending Deprecation

# External Python libraries
import pandas as pd

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width


class CenterlineWidth:

    def __init__(self,
                 csv_data: str = None,
                 cutoff: int = None,
                 optional_cutoff: int = None,
                 interpolate_data: bool = False,
                 interpolate_n: int = 5,
                 interpolate_n_centerpoints: int = None,
                 equal_distance: int = 10,
                 ellipsoid: str = "WGS84"):

        centerline_width.errorHandlingCenterlineWidth(
            csv_data=csv_data,
            cutoff=cutoff,
            interpolate_data=interpolate_data,
            interpolate_n=interpolate_n,
            interpolate_n_centerpoints=interpolate_n_centerpoints,
            equal_distance=equal_distance,
            ellipsoid=ellipsoid)

        if optional_cutoff is not None and cutoff is None:
            ### Pending Deprecation for function name replaced with cutoff()
            ## To be removed
            warnings.warn(
                "optional_cutoff has been replaced with cutoff and will be removed in the future",
                FutureWarning,
                stacklevel=2)
            cutoff = optional_cutoff

        # Description and dataframe
        self.river_name = csv_data
        self.interpolate_data = interpolate_data
        self.interpolate_n = interpolate_n
        df = pd.read_csv(csv_data)
        if cutoff:
            df = df.head(cutoff)
        self.df_len = len(df)
        self.interpolate_n_centerpoints = interpolate_n_centerpoints
        if self.interpolate_n_centerpoints is None:
            self.interpolate_n_centerpoints = self.df_len
        self.ellipsoid = ellipsoid

        # Left and Right Coordinates from the given csv data and data cutoff
        left_bank_coordinates, right_bank_coordinates = centerline_width.leftRightCoordinates(
            df)
        if interpolate_data:
            right_bank_coordinates, left_bank_coordinates = centerline_width.interpolateBetweenPoints(
                left_bank_coordinates, right_bank_coordinates, interpolate_n)
        self.left_bank_coordinates = left_bank_coordinates
        self.right_bank_coordinates = right_bank_coordinates
        self.left_bank_relative_coordinates, self.right_bank_relative_coordinates = centerline_width.relativeBankCoordinates(
            self.left_bank_coordinates, self.right_bank_coordinates,
            self.ellipsoid)

        # Right/Length Bank Length
        self.rightBankLength = centerline_width.centerlineLength(
            centerline_coordinates=right_bank_coordinates,
            ellipsoid=self.ellipsoid)  # Pending Deprecation
        self.right_bank_length = centerline_width.centerlineLength(
            centerline_coordinates=right_bank_coordinates,
            ellipsoid=self.ellipsoid)
        self.leftBankLength = centerline_width.centerlineLength(
            centerline_coordinates=left_bank_coordinates,
            ellipsoid=self.ellipsoid)  # Pending Deprecation
        self.left_bank_length = centerline_width.centerlineLength(
            centerline_coordinates=left_bank_coordinates,
            ellipsoid=self.ellipsoid)

        # Decimal Degrees: River polygon, position of the top/bottom polygon
        river_bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(
            self.left_bank_coordinates,
            self.right_bank_coordinates,
            coord_type="Decimal Degrees")
        self.bank_polygon = river_bank_polygon
        self.top_bank = top_bank
        self.bottom_bank = bottom_bank

        # Area contained within river polygon
        self.area = centerline_width.calculateRiverArea(
            self.bank_polygon, self.ellipsoid)

        # Relative Coordinates: River polygon, position of the top/bottom polygon
        river_bank_polygon, top_bank, bottom_bank = centerline_width.generatePolygon(
            self.left_bank_relative_coordinates,
            self.right_bank_relative_coordinates,
            coord_type="Relative Distance")
        self.bank_polygon_relative = river_bank_polygon
        self.top_bank_relative = top_bank
        self.bottom_bank_relative = bottom_bank

        # Decimal Degrees; Voronoi generated by left/right bank coordinates
        river_bank_voronoi = centerline_width.generateVoronoi(
            self.left_bank_coordinates,
            self.right_bank_coordinates,
            coord_type="Decimal Degrees")
        self.bank_voronoi = river_bank_voronoi

        # Relative Distance; Voronoi generated by left/right bank coordinates
        river_bank_voronoi = centerline_width.generateVoronoi(
            self.left_bank_relative_coordinates,
            self.right_bank_relative_coordinates,
            coord_type="Relative Distance")
        self.bank_voronoi_relative = river_bank_voronoi

        # Decimal Degrees all possible paths: starting/ending node, all possible paths (ridges), paths dictionary
        starting_node, ending_node, x_ridge_point, y_ridge_point, shortest_path_coordinates = centerline_width.centerlinePath(
            self.bank_voronoi, self.bank_polygon, self.top_bank,
            self.bottom_bank)
        self.starting_node = starting_node  # starting position for centerline
        self.ending_node = ending_node  # ending position for centerline
        self.x_voronoi_ridge_point = x_ridge_point  # Voronoi x positions
        self.y_voronoi_ridge_point = y_ridge_point  # Voronoi y positions

        # Relative Distances all possible paths: starting/ending node, all possible paths (ridges), paths dictionary
        self.starting_node_relative = centerline_width.relativeSingleCoordinate(
            self.left_bank_coordinates[0], self.starting_node,
            self.ellipsoid)  # starting position for centerline
        self.ending_node_relative = centerline_width.relativeSingleCoordinate(
            self.left_bank_coordinates[0], self.ending_node,
            self.ellipsoid)  # ending position for centerline
        x_relative_ridges, y_relative_ridges = centerline_width.relativeRidgeCoordinates(
            self.left_bank_coordinates[0], self.x_voronoi_ridge_point,
            self.y_voronoi_ridge_point, self.ellipsoid)
        self.x_voronoi_ridge_point_relative = x_relative_ridges  # Voronoi relative x positions
        self.y_voronoi_ridge_point_relative = y_relative_ridges  # Voronoi relative y positions

        # Voronoi Centerline Coordinates
        self.centerlineVoronoi = shortest_path_coordinates  # pending deprecation
        self.centerline_voronoi = shortest_path_coordinates

        # Centerline length
        self.centerlineLength = centerline_width.centerlineLength(
            centerline_coordinates=shortest_path_coordinates,
            ellipsoid=self.ellipsoid)  # Pending Deprecation
        self.centerline_length = centerline_width.centerlineLength(
            centerline_coordinates=shortest_path_coordinates,
            ellipsoid=self.ellipsoid)

        # Set the different types of Centerline coordinates
        self.equal_distance = equal_distance

        self.centerlineEqualDistance = centerline_width.equalDistanceCenterline(
            centerline_coordinates=self.centerline_voronoi,
            equal_distance=self.equal_distance,
            ellipsoid=self.ellipsoid)  # Pending Deprecation
        self.centerline_equal_distance = centerline_width.equalDistanceCenterline(
            centerline_coordinates=self.centerline_voronoi,
            equal_distance=self.equal_distance,
            ellipsoid=self.ellipsoid)

        self.centerlineEvenlySpaced = centerline_width.evenlySpacedCenterline(
            centerline_coordinates=self.centerline_voronoi,
            number_of_fixed_points=self.interpolate_n_centerpoints
        )  # Pending Deprecation
        self.centerline_evenly_spaced = centerline_width.evenlySpacedCenterline(
            centerline_coordinates=self.centerline_voronoi,
            number_of_fixed_points=self.interpolate_n_centerpoints)

        self.centerlineSmoothed = centerline_width.smoothedCoordinates(
            river_object=self,
            centerline_coordinates=self.centerline_evenly_spaced,
            interprolate_num=self.interpolate_n_centerpoints
        )  # Pending Deprecation
        self.centerline_smoothed = centerline_width.smoothedCoordinates(
            river_object=self,
            centerline_coordinates=self.centerline_evenly_spaced,
            interprolate_num=self.interpolate_n_centerpoints)

        # Relative Distance from bottom left bank point to each Centerline coordinates
        self.centerlineVoronoiRelative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_voronoi,
            self.ellipsoid)  # Pending Deprecation
        self.centerline_voronoi_relative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_voronoi,
            self.ellipsoid)

        self.centerlineEqualDistanceRelative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_equal_distance,
            self.ellipsoid)  # Pending Deprecation
        self.centerline_equal_distance_relative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_equal_distance,
            self.ellipsoid)

        self.centerlineEvenlySpacedRelative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_evenly_spaced,
            self.ellipsoid)  # Pending Deprecation
        self.centerline_evenly_spaced_relative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_evenly_spaced,
            self.ellipsoid)

        self.centerlineSmoothedRelative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_smoothed,
            self.ellipsoid)  # Pending Deprecation
        self.centerline_smoothed_relative = centerline_width.relativeCenterlineCoordinates(
            self.left_bank_coordinates[0], self.centerline_smoothed,
            self.ellipsoid)

        # Overall Sinuosity
        self.sinuosity = centerline_width.calculateSinuosity(
            self.centerline_evenly_spaced, self.ellipsoid)

    def incremental_sinuosity(self,
                              incremental_points: int = 10,
                              save_to_csv: str = None):
        # Incremental Sinuosity
        return centerline_width.incremental_sinuosity(
            river_object=self,
            incremental_points=incremental_points,
            save_to_csv=save_to_csv)

    def plotCenterline(self,
                       centerline_type: str = "Voronoi",
                       marker_type: str = "line",
                       centerline_color: str = "black",
                       dark_mode: bool = False,
                       equal_axis: bool = False,
                       display_all_possible_paths: bool = False,
                       plot_title: str = None,
                       save_plot_name: str = None,
                       save_plot: str = None,
                       show_plot: bool = True,
                       display_voronoi: bool = False,
                       coordinate_unit: str = "Decimal Degrees"):
        ### Pending Deprecation for function name replaced with plot_centerline()
        ## To be removed
        warnings.warn(
            "plotCenterline() has been replaced with plot_centerline() and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        centerline_width.plot_centerline(
            river_object=self,
            centerline_type=centerline_type,
            marker_type=marker_type,
            centerline_color=centerline_color,
            dark_mode=dark_mode,
            equal_axis=equal_axis,
            display_all_possible_paths=display_all_possible_paths,
            plot_title=plot_title,
            save_plot_name=save_plot_name,
            save_plot=save_plot,
            display_voronoi=display_voronoi,
            show_plot=show_plot,
            coordinate_unit=coordinate_unit)

    def plot_centerline(self,
                        centerline_type: str = "Voronoi",
                        marker_type: str = "line",
                        centerline_color: str = "black",
                        dark_mode: bool = False,
                        equal_axis: bool = False,
                        display_all_possible_paths: bool = False,
                        plot_title: str = None,
                        save_plot_name: str = None,
                        save_plot: str = None,
                        show_plot: bool = True,
                        display_voronoi: bool = False,
                        coordinate_unit: str = "Decimal Degrees"):
        centerline_width.plot_centerline(
            river_object=self,
            centerline_type=centerline_type,
            marker_type=marker_type,
            centerline_color=centerline_color,
            dark_mode=dark_mode,
            equal_axis=equal_axis,
            display_all_possible_paths=display_all_possible_paths,
            plot_title=plot_title,
            save_plot_name=save_plot_name,
            save_plot=save_plot,
            display_voronoi=display_voronoi,
            show_plot=show_plot,
            coordinate_unit=coordinate_unit)

    def plotCenterlineWidth(self,
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
                            coordinate_unit: str = "Decimal Degrees"):
        ### Pending Deprecation for function name replaced with plot_centerline()
        ## To be removed
        warnings.warn(
            "plotCenterlineWidth() has been replaced with plot_centerline_width() and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        centerline_width.plot_centerline_width(
            river_object=self,
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

    def plot_centerline_width(self,
                              plot_title: str = None,
                              save_plot: str = None,
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
                              coordinate_unit: str = "Decimal Degrees"):
        centerline_width.plot_centerline_width(
            river_object=self,
            plot_title=plot_title,
            save_plot=save_plot,
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

    def riverWidthFromCenterline(self,
                                 transect_span_distance: int = 3,
                                 transect_slope: str = "Average",
                                 apply_smoothing: bool = True,
                                 remove_intersections: bool = False,
                                 coordinate_unit: str = "Decimal Degrees",
                                 coordinate_reference: str = "Centerline",
                                 save_to_csv: str = None):
        ### Pending Deprecation for function name replaced with width()
        ## To be removed
        warnings.warn(
            "riverWidthFromCenterline() has been replaced with width() and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        return centerline_width.width(
            river_object=self,
            transect_span_distance=transect_span_distance,
            transect_slope=transect_slope,
            apply_smoothing=apply_smoothing,
            remove_intersections=remove_intersections,
            coordinate_unit=coordinate_unit,
            coordinate_reference=coordinate_reference,
            save_to_csv=save_to_csv)

    def width(self,
              transect_span_distance: int = 3,
              transect_slope: str = "Average",
              apply_smoothing: bool = True,
              remove_intersections: bool = False,
              coordinate_unit: str = "Decimal Degrees",
              coordinate_reference: str = "Centerline",
              save_to_csv: str = None):
        return centerline_width.width(
            river_object=self,
            transect_span_distance=transect_span_distance,
            transect_slope=transect_slope,
            apply_smoothing=apply_smoothing,
            remove_intersections=remove_intersections,
            coordinate_unit=coordinate_unit,
            coordinate_reference=coordinate_reference,
            save_to_csv=save_to_csv)

    def saveCenterlineCSV(self,
                          save_to_csv: str = None,
                          latitude_header: str = None,
                          longitude_header: str = None,
                          centerline_type: str = "Voronoi",
                          coordinate_unit: str = "Decimal Degrees"):
        ### Pending Deprecation for function name replaced with save_centerline_csv()
        ## To be removed
        warnings.warn(
            "saveCenterlineCSV() has been replaced with save_centerline_csv() and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        return centerline_width.save_centerline_csv(
            river_object=self,
            save_to_csv=save_to_csv,
            latitude_header=latitude_header,
            longitude_header=longitude_header,
            centerline_type=centerline_type,
            coordinate_unit=coordinate_unit)

    def save_centerline_csv(self,
                            save_to_csv: str = None,
                            latitude_header: str = None,
                            longitude_header: str = None,
                            centerline_type: str = "Voronoi",
                            coordinate_unit: str = "Decimal Degrees"):
        return centerline_width.save_centerline_csv(
            river_object=self,
            save_to_csv=save_to_csv,
            latitude_header=latitude_header,
            longitude_header=longitude_header,
            centerline_type=centerline_type,
            coordinate_unit=coordinate_unit)

    def saveCenterlineMAT(self,
                          save_to_mat: str = None,
                          latitude_header: str = None,
                          longitude_header: str = None,
                          centerline_type: str = "Voronoi",
                          coordinate_unit: str = "Decimal Degrees"):
        ### Pending Deprecation for function name replaced with save_centerline_mat()
        ## To be removed
        warnings.warn(
            "saveCenterlineMAT() has been replaced with save_centerline_mat() and will be removed in the future",
            FutureWarning,
            stacklevel=2)

        return centerline_width.save_centerline_mat(
            river_object=self,
            save_to_mat=save_to_mat,
            latitude_header=latitude_header,
            longitude_header=longitude_header,
            centerline_type=centerline_type,
            coordinate_unit=coordinate_unit)

    def save_centerline_mat(self,
                            save_to_mat: str = None,
                            latitude_header: str = None,
                            longitude_header: str = None,
                            centerline_type: str = "Voronoi",
                            coordinate_unit: str = "Decimal Degrees"):
        return centerline_width.save_centerline_mat(
            river_object=self,
            save_to_mat=save_to_mat,
            latitude_header=latitude_header,
            longitude_header=longitude_header,
            centerline_type=centerline_type,
            coordinate_unit=coordinate_unit)


class riverCenterline(CenterlineWidth):
    ### Pending Deprecation for class name replaced with CenterlineWidth()
    ## To be removed
    def __init__(self,
                 csv_data: str = None,
                 optional_cutoff: int = None,
                 cutoff: int = None,
                 interpolate_data: bool = False,
                 interpolate_n: int = 5,
                 interpolate_n_centerpoints: int = None,
                 equal_distance: int = 10,
                 ellipsoid: str = "WGS84"):
        warnings.warn(
            "riverCenterline() has been replaced with CenterlineWidth() and will be removed in the future",
            FutureWarning,
            stacklevel=2)
        CenterlineWidth.__init__(
            self,
            csv_data=csv_data,
            optional_cutoff=optional_cutoff,
            cutoff=cutoff,
            interpolate_data=interpolate_data,
            interpolate_n=interpolate_n,
            interpolate_n_centerpoints=interpolate_n_centerpoints,
            equal_distance=equal_distance,
            ellipsoid=ellipsoid)
