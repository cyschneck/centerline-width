# Built-in Python functions
import math
import logging

# External Python libraries
import numpy as np
import networkx as nx
from scipy import interpolate
from shapely.geometry import Point, LineString
from pyproj import Geod
import geopy.distance

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

## Logging set up for .INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def generateNXGraph(all_points_dict: dict = None):
    # Generate a NetworkX graph to find the largest graph
    def distanceBetween(start: tuple = None, end: tuple = None) -> float:
        # return the distance between two points on a graph
        lat1 = start[0]
        lat2 = end[0]
        lon1 = start[1]
        lon2 = end[1]
        p = math.pi / 180
        a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(
            lat1 * p) * math.cos(lat2 * p) * (1 - math.cos(
                (lon2 - lon1) * p)) / 2
        return math.asin(math.sqrt(a))

    # nodes as lat/lon positions, weighted by the distance between each position

    all_connections_in_graph = nx.Graph()
    node_as_keys_pos_values = {}
    for start_point, end_point_list in all_points_dict.items():
        node_as_keys_pos_values[start_point] = (start_point[0], start_point[1])
        all_connections_in_graph.add_node(start_point,
                                          pos=(start_point[0], start_point[1]))
        for end_point in end_point_list:
            all_connections_in_graph.add_node(end_point,
                                              pos=(end_point[0], end_point[1]))
            node_as_keys_pos_values[end_point] = (end_point[0], end_point[1])
            all_connections_in_graph.add_edge(start_point,
                                              end_point,
                                              weight=distanceBetween(
                                                  start_point, end_point))

    components_of_subgraphs = [
        all_connections_in_graph.subgraph(c).copy()
        for c in nx.connected_components(all_connections_in_graph)
    ]
    nodes_of_largest_subgraph = []
    for idx, g in enumerate(components_of_subgraphs, start=1):
        if len(g.nodes()) > len(nodes_of_largest_subgraph):
            nodes_of_largest_subgraph = list(g.nodes())
        #print(f"Subgraph {idx}: Nodes: {len(g.nodes())}, Edges: {len(g.edges())}")

    return all_connections_in_graph, nodes_of_largest_subgraph


def networkXGraphShortestPath(nx_graph=None,
                              starting_node=None,
                              ending_node=None):
    # Find the shortest path if it exists
    if starting_node is not None:
        try:
            shortest_path = nx.shortest_path(nx_graph,
                                             source=starting_node,
                                             target=ending_node)
            logger.info("[SUCCESS] Valid centerline path found")
        except nx.NetworkXNoPath:  # no direct path found
            logger.info(
                "[FAILED]  No direct path found from starting node to ending node. To view gaps, plotCenterline(display_all_possible_paths=True). Recommended fix, rerun riverCenterline: set interpolate_data=True or (if interpolate_data=True) increase interpolate_n"
            )
            return None
        #nx.draw(nx_graph, with_labels=True, font_size=10)
        return shortest_path
    else:
        return None


def centerlinePath(river_voronoi=None,
                   river_polygon=None,
                   top_polygon_line: LineString = None,
                   bottom_polygon_line: LineString = None,
                   multiple_connections: int = 0):
    # Return the starting node, ending node, all possible paths positions, and all paths starting/end position as a dictionary
    start_end_points_dict = centerline_width.pointsFromVoronoi(
        river_voronoi,
        river_polygon)  # All possible path connections from Voronoi
    nx_graphs, largest_subgraph_nodes = generateNXGraph(start_end_points_dict)

    x_ridge_point = []  # X position on path
    y_ridge_point = []  # Y position on path
    starting_node = None  # starting position at the top of the river
    ending_node = None  # ending position at the bottom of the river
    for start_point, end_point_list in start_end_points_dict.items():
        if len(
                end_point_list
        ) > multiple_connections:  # TESTING TESTING: Show only the end points that have multiple connections (set to 0 during production)
            # Find the starting and ending node based on distance from the top and bottom of the polygon
            if starting_node is None:
                starting_node = start_point
            else:
                # Only include if starting point node is on the largest subgraph (that represents the centerline)
                if start_point in largest_subgraph_nodes:
                    # if start_point is closer to the top of the polygon than the current starting_node
                    if Point(start_point).distance(top_polygon_line) <= Point(
                            starting_node).distance(top_polygon_line):
                        starting_node = start_point
            for end_point in end_point_list:
                if ending_node is None:
                    ending_node = end_point
                # Only include if starting point node is on the largest subgraph (that represents the centerline)
                if start_point in largest_subgraph_nodes:
                    # if the end_point is closer to the top of the polygon than the current starting_node
                    if Point(end_point).distance(top_polygon_line) <= Point(
                            starting_node).distance(top_polygon_line):
                        starting_node = end_point
                    else:
                        # if start_point is closer to the bottom than current ending_node
                        if Point(start_point).distance(
                                bottom_polygon_line) <= Point(
                                    ending_node).distance(bottom_polygon_line):
                            ending_node = start_point
                        # if end_point is closer to the bottom than current ending_node
                        if Point(end_point).distance(
                                bottom_polygon_line) <= Point(
                                    ending_node).distance(bottom_polygon_line):
                            ending_node = end_point
                # Save all starting and end positions for all possible paths
                x_ridge_point.append((start_point[0], end_point[0]))
                y_ridge_point.append((start_point[1], end_point[1]))

    if starting_node is None:
        logger.critical(
            "\nCRITICAL ERROR, Polygon too short for the Voronoi diagram generated (no starting node found), unable to plot centerline. Set display_voronoi=True to view vertices. Can typically be fixed by adding more data to expand range"
        )
        shortest_path_points = None
    else:
        shortest_path_points = networkXGraphShortestPath(
            nx_graphs, starting_node, ending_node)

    return starting_node, ending_node, x_ridge_point, y_ridge_point, shortest_path_points


def equalDistanceCenterline(centerline_coordinates: list = None,
                            equal_distance: int = None,
                            ellipsoid="WGS84") -> None:
    # Interpolate centerline to space out coordinates an equal physical distance from the next (in meters)
    if centerline_coordinates is None:
        return None

    equal_distance_between_centerline_coordinates = []

    geodesic = Geod(ellps=ellipsoid)

    # Iterate through coordinates based on a set distance (distance_m)
    lon_start, lat_start = centerline_coordinates[0]
    equal_distance_between_centerline_coordinates.append(
        (lon_start, lat_start))
    for i, centerline_coord in enumerate(centerline_coordinates):
        if i + 1 < len(centerline_coordinates):
            lon_end, lat_end = centerline_coordinates[i + 1]
            # move to next point when distance between points is less than the equal distance
            move_to_next_point = False
            while (not move_to_next_point):
                # forward_bearing: direction towards the next point
                forward_bearing, reverse_bearing, distance_between_meters = geodesic.inv(
                    lon_start, lat_start, lon_end, lat_end)
                if distance_between_meters < equal_distance:
                    # if the distance to the next point is less than the equal distance, reorient to bearing to next latitude
                    move_to_next_point = True
                else:
                    start_point = geopy.Point(lat_start, lon_start)
                    distance_to_move = geopy.distance.distance(
                        kilometers=equal_distance /
                        1000)  # distance to move towards the next point
                    final_position = distance_to_move.destination(
                        start_point, bearing=forward_bearing)
                    equal_distance_between_centerline_coordinates.append(
                        (final_position.longitude, final_position.latitude))
                    # set new starting point to current newly generated destination
                    lon_start = final_position.longitude
                    lat_start = final_position.latitude

    return equal_distance_between_centerline_coordinates


def evenlySpacedCenterline(centerline_coordinates: list = None,
                           number_of_fixed_points: int = None) -> None:
    # Interpolate to evenly space points along the centerline coordinates (effectively smoothing with fewer points)
    if centerline_coordinates is None:
        return None

    centerline_line = LineString(centerline_coordinates)

    # Splitting into a fixed number of points
    distances_evenly_spaced = np.linspace(0, centerline_line.length,
                                          number_of_fixed_points)
    points_evenly_spaced = [
        centerline_line.interpolate(distance)
        for distance in distances_evenly_spaced
    ]

    # Convert Shapley Points to a List of Tuples (coordinates)
    interpolated_centerline_coordinates = []
    for point in points_evenly_spaced:
        interpolated_centerline_coordinates.append((point.x, point.y))

    return interpolated_centerline_coordinates


def smoothedCoordinates(river_object: centerline_width.riverCenterline = None,
                        centerline_coordinates: list = None,
                        interprolate_num: int = None) -> None:
    # return a list coordinates after applying b-spline (smoothing)
    if centerline_coordinates is None:
        return None

    x_coordinates = []
    y_coordinates = []

    # splitting centerline coordinaets into an x and y component
    for centerline_point in centerline_coordinates:
        x_coordinates.append(centerline_point[0])
        y_coordinates.append(centerline_point[1])

    # applying a path smoothing spline
    smoothed_coordinates = []
    tck, *rest = interpolate.splprep(
        [x_coordinates, y_coordinates],
        s=0.000001)  # spline prep, tck = knots - coefficients - degree
    u = np.linspace(
        0, 1, interprolate_num
    )  # number of steps between each point (to determine smoothness)
    x_smoothed, y_smoothed = interpolate.splev(
        u, tck)  # interpolated list of points

    x_smoothed, y_smoothed = x_smoothed.tolist(), y_smoothed.tolist(
    )  # convert array to list
    smoothed_coordinates = list(zip(x_smoothed, y_smoothed))

    # Check if smoothed centerline lies outside polygon
    points_outside_polygon = 0
    for centerline_point in smoothed_coordinates:
        if not river_object.bank_polygon.contains(Point(centerline_point)):
            points_outside_polygon += 1
    if points_outside_polygon > 2:
        logger.critical(
            f"\nWARNING: Partially invalid smoothed centerline due to sparse centerline data ({points_outside_polygon} points lie outside the polygon), fix recommendation: rerun riverCenterline to create river object with interpolate_n_centerpoints set to {round(len(centerline_coordinates)*2.5)}+\n"
        )

    return smoothed_coordinates
