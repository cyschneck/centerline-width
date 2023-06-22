# Centerline-Width
 <p align="center">
  <img src="https://raw.githubusercontent.com/cyschneck/centerline-width/main/assets/centerline_logo.jpg" />
</p>

![PyPi](https://img.shields.io/pypi/v/centerline-width)
![license](https://img.shields.io/github/license/cyschneck/centerline-width)
[![NSF-2141064](https://img.shields.io/badge/NSF-2141064-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2141064&HistoricalAwards=false)
[![pytests](https://github.com/cyschneck/centerline-width/actions/workflows/pytests.yml/badge.svg)](https://github.com/cyschneck/centerline-width/actions/workflows/pytests.yml)

Find the centerline and width of rivers based on the latitude and longitude positions from the right and left bank 

* **Convert raw data from Google Earth Pro to CSV**
	* extractPointsToTextFile()
	* convertColumnsToCSV()
* **Find centerline and width of river**
	* plotCenterline()
	* plotCenterlineWidth()
	* riverWidthFromCenterline()
	* saveCenterlineCSV()
	* saveCenterlineMAT()
	* centerlineVoronoi
	* centerlineEvenlySpaced
	* centerlineSmoothed
	* centerlineLength
	* rightBankLength
	* leftBankLength

| River Outlined in Google Earth Pro | Generated Centerline for the Riverbank |
| ------------- | ------------- |
| ![river_google_earth+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example_google_earth.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example.png) |

Python implementation of [R-Code CMGO](https://github.com/AntoniusGolly/cmgo) (with modification)

NOTE: This is Beta quality software that is being actively developed, use at your own risk. This project is not supported or endorsed by either JPL or NASA. The code is provided “as is”, use at your own risk.

## Install
PyPi pip install at [pypi.org/project/centerline-width/](https://pypi.org/project/centerline-width/)

```
pip install centerline-width
```

## Requirements
Currently running on Python 3.7+

```
pip install -r requirements.txt
```
Requirements will also be downloaded as part of the pip download

## Quickstart: centerline-width

The core of centerline-width works with a .csv file of the left and right bank latitude/longitudes. So, if starting from Google Earth Pro, two .kml must first be translated to a single .csv file

```python
import centerline_width
centerline_width.extractPointsToTextFile(left_kml="left_bank.kml",
					right_kml="right_bank.kml",
					text_output_name="river_coordinates_output.txt")
centerline_width.convertColumnsToCSV(text_file="river_coordinates_output.txt")
```
Then once the .csv file is created, in order to run the centerline-width functions, generate a river object from the `river_coordinates_output.csv`

```python
river_object = centerline_width.riverCenterline(csv_data="river_coordinates_output.csv")
```

To plot the centerline, run the `plotCenterline()` function from `river_object` created
```python
river_object.plotCenterline()
```
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_centerline.png)

To plot the width of the river at intervals along the bank, run `plotCenterlineWidth`

While `apply_smoothing`, `remove_intersections`, and `display_true_centerline` are optional, they are recommended to generate a minimal width diagram
```python
river.plotCenterlineWidth(apply_smoothing=True, remove_intersections=True, display_true_centerline=False)
```
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width.png)

For more details to fix unexpected behavior or error code: [Debugging, Error Handling, and Edge Cases](#debugging-error-handling-and-edge-cases)

## Preprocessing
### Convert KML files to Text File

Convert two .kml files from Google Earth Pro (for the left and right bank) and export the coordinates into a text file

```
extractPointsToTextFile(left_kml=None,
			right_kml=None,
			text_output_name=None)
```

* **[REQUIRED]** left_kml (string): File location of the kml file for left bank
* **[REQUIRED]** right_kml (string): File location of the kml file for right bank
* **[REQUIRED]** text_output_name (string): Output file name (and location)

```python
import centerline_width
centerline_width.extractPointsToTextFile(left_kml="leftbank.kml",
					right_kml="rightbank.kml",
					text_output_name="data/river_coords_output.txt")
```
Output: The text file `data/river_coords_output.txt` with the headers `llat, llon, rlat, rlon` (for the left latitude, left longitude, right latitude, and right longitude)

Example:
```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
```

### Converted Text File to CSV

Convert a text file with coordinates for a left and right bank's latitude and longitude to a csv file with columns for the left bank latitude (llat), left bank longitude (llon), right bank latitude (rlat), right bank longitude (rlon)

```
convertColumnsToCSV(text_file=None, flipBankDirection=False)
```
* **[REQUIRED]** text_file (string): File location of the text file to convert
* [OPTIONAL] flipBankDirection (boolean): If the latitude/longitude of the banks are generated in reverse order, flip the final values so left/right bank are in order

Scripts expects data as a list of point for left and right banks:
- Header: llat, llon, rlat, rlon

```python
import centerline_width
centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt",
				flipBankDirection=True)
```
Converts text file:
```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.037441 -92.867476
30.037613 -92.868549 30.037448 -92.867474
30.037648 -92.868546 30.037482 -92.867449
30.037674 -92.868536 30.037506 -92.867432
30.037702 -92.868533 30.037525 -92.867430
```
To a CSV file:
```
llat,llon,rlat,rlon
30.037581,-92.868569,30.037441,-92.867476
30.037613,-92.868549,30.037448,-92.867474
30.037648,-92.868546,30.037482,-92.867449
30.037674,-92.868536,30.037506,-92.867432
30.037702,-92.868533,30.037525,-92.867430
```
Output: A csv file `data/river_coords.csv` with the headers `llat, llon, rlat, rlon`

## Centerline and Width
### River Object
First, generate a river object to contain river data and available transformations
```
centerline_width.riverCenterline(csv_data=None,
				optional_cutoff=None,
				interpolate_data=False,
				interpolate_n=5,
				interpolate_n_centerpoints=None,
				equal_distance=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] optional_cutoff (int): Include only the first x number of the data to chart (useful for debugging)
* [OPTIONAL] interpolate_data (bool): Interpolate between existing data by adding additional points
* [OPTIONAL] interpolate_n (int): Number of additional points to add between existing data, defaults to 5 (note: larger numbers will take exponentially longer to run, recommends less than 15)
* [OPTIONAL] interpolate_n_centerpoints (int): Number of points used to interpolate the Voronoi centerline, defaults to the the length of the data frame (df_len)
* [OPTIONAL] equal_distance (int): Equal distance between points (in meters) used to interpolate the Voronoi centerline, defaults 1/10th the length fo the Voronoi centerline

**Solutions for sparse data:**

`interpolate_data` is an option that can be used to find a centerline when the existing data generates a Voronoi graph that is jagged or contains gaps due to the combination of sparse data and a narrow river (See: Debugging, Error Handling, and Edge Cases - Fix Gaps and Jagged Centerlines). By default, `interpolate_data=True` will add 5 additional points between each existing point but can be changed with the `interpolate_n` option

`interpolate_n_centerpoints` is an option that can be used to increase the resolution (number of points) of the centerline found by the Voronoi vertices. By default, will evenly space out to the size of the dataframe. Can artificially increase the amount of width lines generated by increasing the number of center points. When `interpolate_n_centerpoints` increases, the number of width lines generated will increase (and visa versa)

| interpolate_n_centerpoints=75 | interpolate_n_centerpoints=200 |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_n_centerpoints_75.png) | ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_n_centerpoints_200.png) |

**Object (class) useful attributes:**

* centerlineVoronoi (list of tuples): List of the latitude and longitude coordinates of the centerline generated by Voronoi diagrams
* centerlineEqualDistance (list of tuples): List of the latitude and longitude coordinates of the centerline generated by equal distances between coordinates from the Voronoi diagrams
* centerlineEvenlySpaced (list of tuples): List of the latitude and longitude coordinates of the centerline generated by evenly spacing out points generated by the Voronoi diagrams
* centerlineSmoothed (list of tuples): List of the latitude and longitude coordinates of the centerline generated by smoothing out the evenly spaced out points generated by the Voronoi diagrams
* centerlineLength (float): Length of the centerline of the river (in km)
* rightBankLength (float): Length of the right bank of the river (in km)
* leftBankLength (float): Length of the left bank of the river (in km)

**Object (class) additional atttributes:**

* river_name (string): name of object, set to the csv_data string
* left_bank_coordinates (list of tuples): list of coordinates of the left bank generated from the csv file (`[(x, y), (x, y)]`)
* right_bank_coordinates (list of tuples) list of coordinates of the right bank generated from the csv file (`[(x, y), (x, y)]`)
* df_len (int): Length of the data frame of the csv data (spliced by the optional_cutoff)
* equal_distance (int): Distance between points (in meters) used in centerlineEqualDistance, defaults to 1/10th the length of the centerline
* bank_polygon (Shapley Polygon): Multi-sided polygon generated to encapsulate river bank (used to define an inside and an outside of the river)
* top_bank (Shapley Linestring): Linestring that represents the top of the river/polygon
* bottom_bank (Shapley Linestring): Linestring that represents the bottom of the river/polygon
* starting_node (tuple): Tuple of the starting position (latitude and longitude) of the centerline path
* ending_node (tuple): Tuple of the end position (latitude and longitude) of the centerline path
* bank_voronoi (scipy Voronoi object): Voronoi generated by left/right banks
* x_voronoi_ridge_point (list of tuples): X positions on Voronoi ridge (starting Latitude position to ending Latitude position)
* y_voronoi_ridge_point (list of tuples): Y position on Voronoi ridge (starting Longitude position to ending Longitude position)
* interpolate_data (bool): if interpolating between existing data, defaults to False
* interpolate_n (int): specifies how many additional points will be added between points along the river bank when interpolating data, defaults to 5
* interpolate_n_centerpoints (int): specifies how many points will be used to interpolate the Voronoi centerline, defaults to the length of the data frame (df_len)


```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
```

### Return Latitude/Longitude Coordinates of Centerline
Return the latitude/longitude coordinates of the centerline based on the left and right banks

**Types of Centerlines**

There are four types of centerline coordinates formed from the riverbank data

- **Voronoi centerline**: centerline generated from where Voronoi vertices intersect within the river
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/voronoi_centerline.png)
- **Equal Distance Centerline**: centerline based on Voronoi centerline but each point is equally spaced out from the previous (in meters)
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/evenly_spaced_centerline.png)
- **Evenly Spaced Centerline**: centerline based on Voronoi centerline but evenly spaced with a fixed number of points
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/evenly_spaced_centerline.png)
- **Smoothed Centerline**: centerline generated from the evenly spaced centerline but smoothed by a b-spline
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/smoothed_centerline.png)

Centerline coordinates are formed by the Voronoi vertices
```
river_object.centerlineVoronoi
```

Centerline coordinates are formed by Equally Distanced vertices, set by `equal_distance`
```
river_object.centerlineEqualDistance
```

Centerline coordinates are formed by Evenly Spaced vertices
```
river_object.centerlineEvenlySpaced
```

Centerline coordinates are formed from Smoothed vertices
```
river_object.centerlineSmoothed
```

Example:
```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv", optional_cutoff=15)
river_centerline_coordinates = river_object.centerlineVoronoi
```
Output is a list of tuples: (example) `[(-92.86788596499872, 30.03786596717931), (-92.86789573751797, 30.037834641974108), (-92.8679141386283, 30.037789636848878), (-92.8679251193248, 30.037756853899904), (-92.86796903819089, 30.03765423778148), (-92.86797335733262, 30.037643336049054), (-92.8679920356456, 30.037592224469797), (-92.86800576063828, 30.037555441489403), (-92.86800841510367, 30.037546512833107), (-92.8680119498663, 30.03753043193875)]`

### Save Centerline Coordinates to a .CSV File
Save the centerline coordinates to a csv file with columns for latitude and longitude

```
saveCenterlineCSV(save_to_csv=None, centerline_type="Voronoi")
```
* **[REQUIRED]** save_to_csv (str): CSV filename, requires a .csv extension
* [OPTIONAL] centerline_type (str): Centerline type to save to CSV (not case-sensitive), options: ["Voronoi", "Evenly Spaced", "Smoothed"], defaults to "Voronoi"
* [OPTIONAL] latitude_header (str): Column header for latitude values, defaults to `<centerline_type> Centerline Latitude (Deg)`
* [OPTIONAL] longitude_header (str): Column header for Longitude values, defaults to `<centerline_type> Centerline Longitude (Deg)`

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.saveCenterlineCSV(save_to_csv="centerline_coordinates.csv", centerline_type="Smoothed")
```
Returns a csv with the Latitude and Longitude coordinates of the specified centerline with column headers with centerline type: `Smoothed Centerline Latitude (Deg), Smoothed Centerline Longitude (Deg)`

### Save Centerline Coordinates to a .MAT File
Save the centerline coordinates to a .mat file with columns for latitude and longitude

```
saveCenterlineMAT(save_to_mat=None, centerline_type="Voronoi")
```
* **[REQUIRED]** save_to_mat (str): MAT filename, requires a .mat extension
* [OPTIONAL] centerline_type (str): Centerline type to save to MAT (not case-sensitive), options: ["Voronoi", "Evenly Spaced", "Smoothed"], defaults to "Voronoi"
* [OPTIONAL] latitude_header (str): Column header for latitude values, defaults to `<centerline_type>_Centerline_Latitude_(Deg)` (will remove spaces and special characters and replaces with underscores)
* [OPTIONAL] longitude_header (str): Column header for Longitude values, defaults to `<centerline_type>_Centerline_Longitude_(Deg)` (will remove spaces and special characters and replaces with underscores)

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.saveCenterlineMAT(save_to_mat="centerline_coordinates.mat", centerline_type="Smoothed")
```
Returns a .mat file with the Latitude and Longitude coordinates of the specified centerline with column headers with centerline type: `Smoothed_Centerline_Latitude_(Deg), Smoothed_Centerline_Longitude_(Deg)`

### Return Length of Centerline
Return the length of the centerline found between the left and right bank generated by the Voronoi diagram
```
river_object.centerlineLength
```
Length returned in kilometers
```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv", optional_cutoff=550)
river_centerline_length = river_object.centerlineLength
```
The length of the river centerline returns `215.34700589636674` km

## Plot Centerline in Matplotlib
Plot the centerline created from a list of right and left banks with Voronoi vertices

```
plotCenterline(display_all_possible_paths=False, 
		plot_title=None, 
		save_plot_name=None, 
		display_voronoi=False)
```
* [OPTIONAL] display_all_possible_paths (boolean): Display all possible paths, not just the centerline (useful for debugging), defaults to False
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] display_voronoi (boolean): Overlay Voronoi diagram used to generate centerline, defaults to False

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.plotCenterline()
```
Output:
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_centerline.png)

## Plot Centerline Width Lines in Matplotlib
### Plot the Centerline Width Lines
Plot the width of the river based on the centerline

Display Centerline at even intervals from the Voronoi generated centerline
```
plotCenterlineWidth(plot_title=None, 
		save_plot_name=None, 
		display_true_centerline=True,
		transect_span_distance=3,
		apply_smoothing=False,
		flag_intersections=True,
		remove_intersections=False)
```
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] display_true_centerline (boolean): Display generated true centerline based on Voronoi diagrams
* [OPTIONAL] transect_span_distance (int): Sum up n number of points around a center point to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] flag_intersections (bool): Display intersecting width lines as red in graph, defaults to True
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaults to False

**apply_smoothing**

apply_smoothing applies a spline to smooth the centerline points created by the Voronoi vertices. This reduces the noise of the slopes and can create width lines that are less susceptible to small changes in the bank

| apply_smoothing=False | apply_smoothing=True |
| ------------- | ------------- |
| ![river_without_smoothing+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_without_smoothing.png) | ![river_with_smoothing+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_with_smoothing.png) |

**transect_span_distance**

Transect span describes the number of points that are averaged to generated a width line (example: transect_span_distance=3, average of three slopes)

![transect_span_distance](https://user-images.githubusercontent.com/22159116/227870492-69d105b2-0d3e-4d50-90d9-e938400a58fb.png)
| transect_span_distance=6 | transect_span_distance=30 |
| ------------- | ------------- |
| ![river_transect_6+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_transect_6.png) | ![river_transect_30+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_transect_30.png) |

**remove_intersections**

remove_intersections will remove the width lines that intersect other lines (that could be creating unrepresentative long width lines). Intersections are removed first in order from most to least (to ensure that the most width lines as possible are kept) and then, based on the longer of two intersecting lines

Intersecting lines are flagged in red by default (flag_intersections=True)

| remove_intersections=False | remove_intersections=True |
| ------------- | ------------- |
| ![river_keep+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_keep_intersections.png) | ![river_remove+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width_remove_intersections.png)|

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_object.plotCenterlineWidth(apply_smoothing=True, remove_intersections=True, display_true_centerline=False)
```
![river_coords_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_coords_width.png)

### Return Width of River

Return the width of the river at each (evenly spaced or smoothed) centerline coordinates as `(Longitude, Latitude) : width`

```
riverWidthFromCenterline(transect_span_distance=3,
			apply_smoothing=True,
			remove_intersections=False,
			units="km",
			save_to_csv=None)
```
* [OPTIONAL] transect_span_distance (int): Sum up n number of points around a center point to determine the slope (increase to decrease the impact of sudden changes), defaults to 6, must be greater than 2 (since the slope is found from the difference in position between two points), measured orthogonal to the centerline
* [OPTIONAL] apply_smoothing (bool): Apply a B-spline smoothing to centerline
* [OPTIONAL] remove_intersections (bool): Iterative remove intersecting lines, to maintain the most width lines, but return only non-intersecting width lines, defaults to True
* [OPTIONAL] units (string): Units to measure distance, options: ["km" (kilometers), "m" (meters), "mi" (miles), "nmi" (nautical miles), "ft" (feet), "in" (inches), "rad" (radians), "deg" (degrees)], defaults to "km" (kilometers)
* [OPTIONAL] save_to_csv (string): CSV filename to output width, defaults to None (no file is saved), requires a .csv extension (Column Headers: `Centerline Latitude (Deg)", "Centerline Longitude (Deg)", "Width (<units specified>)`)

Important note, when using `apply_smoothing=True`, the centerline generated is the result of evenly spaced coordinates generated from the original Voronoi coordinates, so the smoothed coordinates may not match exactly to the original centerline coordinates. When `apply_smoothing=False`, width lines are generated from the evenly spaced centerline coordinates

```python
import centerline_width
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv")
river_width_dict = river_object.riverWidthFromCenterline(transect_span_distance=3,
							apply_smoothing=True,
							units="km",
							remove_intersections=True)
```
Width dictionary = `{(-92.86792084788995, 30.037769672351182): 0.10969163557087018, (-92.86795038641004, 30.03769867854198): 0.10794219579997719}`

## Documentation and Algorithm to Determine Centerline

The centerline is defined by the greatest distance from the right and left bank, created from a Voronoi Diagram. The remaining paths within the river are filtered through Dijkstra's algorithm to find the shortest path that is the centerline

### Right and Left bank points are plotted (X-Axis for Latitude, Y-Axis for Longitude)
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example1.png)

### Generate a polygon to encapsulate the river between the right and left banks to define in and outside of river
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example2.png)

### Generate a Voronoi based on the points along the riverbanks
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example3.png)

### Display Voronoi ridge vertices that lie within the polygon (within the riverbanks)
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example4.png)

### Filter out any point pairs that only have one connection to filter out the short dead end paths and find the starting and ending node based on distance from the top and bottom of polygon
With the vertices removed, it is possible to form multiple unconnected graphs within the polygon. The largest subgraph is assumed to contain the centerline and the other subgraphs are filtered out
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example6.png)
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example7.png)

### Find the shortest path from the starting node to the ending node ([Dijkstra's Algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path))
| Points on River Bank | NetworkX Graph of Points on River Bank |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example10.png) | ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example9.png) |

### Display the centerline found by connecting the starting/ending node with the shortest path
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example8.png)

This is an attempt at a more robust algorithm working from raw data to ensure that all dead ends are removed, and no gaps exist in the centerline

Points that only have one connection are removed, but limiting the number of connections for a point to just two will create gaps. The Voronoi vertices connect to other vertex values, but some connect to more and some only connect to one other point. Removing additional values will create gaps, so this is avoided in this code by not applying additional filters.

**All vertices:**
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example4.png)

**Vertices that have at least two connections (that would create gaps):**
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/example5.png)

## Debugging, Error Handling, and Edge Cases
### Wide Start/End of River
If the data starts or ends with a large width, it is possible for the starting/ending nodes to end up in the wrong position
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_example3.png)
Currently, the starting node is determined by the closest node to the top of the bank (in green) and the ending node is determined by the closest node to the bottom of the bank (in red) that sits along the longest path

### Invalid Polygon
A polygon is formed to encapsulate the river with the given data (to determine the inside and outside of the river). The top and bottom are connected by a straight line from the start/end of the available data. As a result, it is possible for this straight line to overlap and create an invalid polygon.

A polygon is invalid if it overlaps within itself:
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_example1.png)
In this example, the polygon is invalid, but with such a small overlap it is still able to find a valid path

With limited data, the polygon will overlap more dramatically and will struggle to find a valid centerline:
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_example4.png)

### Invalid Centerline
If the data is too small, a centerline and its coordinates cannot not be found (since only a single Voronoi vertex exists within the polygon and after dead ends are filtered)

`CRITICAL ERROR, Polygon too short for the Voronoi diagram generated (no starting node found), unable to plot centerline. Set displayVoronoi=True to view vertices. Can typically be fixed by adding more data to expand range.`
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_example2.png)
Can be fixed by expanding the data until the polygon is large enough to contain at least two different vertex points

### Invalid Top and Bottom Bank Postions (flipBankDirection = True)
Error: `WARNING: Invalid Polygon Due to Flipped Banks, fix recommendation: rerun convertColumnsToCSV() and set flipBankDirection=True (or reset to default 'False' if currently set to flipBankDirection=True)`

If the data for the left and right riverbanks are generated in reverse order, they will be read in the incorrect order and the graph will find the invalid top and bottom of the bank

If the latitude/longitude of the banks are generated in reverse order, flip the final values so left/right bank are in order

This can be fixed by using the flipBankDirection optional argument `centerline_width.convertColumnsToCSV(text_file="data_example.txt", flipBankDirection=True)`
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/flipDirection_example.png)

### Invalid Smoothed Centerline
The smoothed centerline (`river_object.centerlineSmoothed`) can end up lying outside the river if the centerline data points are sparse in a narrow river. If more than two points in the smoothed centerline lie outside the river, a warning will be thrown

Example Error: `WARNING: Partially invalid smoothed centerline due to sparse centerline data (6 points lie outside the polygon), fix recommendation: rerun riverCenterline to create river object with interpolate_n_centerpoints set to 62+`

By default, `interpolate_n_centerpoints` is set to None and not additional points will be added between the existing points along the centerline. By adding additional points between the existing centerline, the smoothed centerline can be fixed to stay within the polygon. This fix is set by creating a river object, `centerline_width.riverCenterline`, with `interpolate_n_centerpoints=65` (with the recommended 62+) to fix for centerline coordinates that lie outside the polyogon

`interpolate_n_centerpoints = None` does not interpolate data points, so the size will be set to the number of fixed points when creating the evenly spaced coordinates (equal to the size of the data frame)

| interpolate_n_centerpoints = None | interpolate_n_centerpoints = 65 |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_smoothed_centerline.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_smoothed_centerline_fixed.png) |

For very narrow rivers, this problem can become extreme and pronounced
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/invalid_smoothed_centerline_extreme.png)

By increasing the interpolation between the centerline points, the smoothed centerlines will be forced within the polygon and reduce the amount of points outside of the polygon. By default, this warning will be thrown if more than 2 points are outside of polygon, so as long as more than 2 points lie outside the polygon, the warning will recommend doubling the amount of centerline points

### Fix Gaps and Jagged Centerlines
Gaps formed can cause part of the centerline to be skipped due to sparse data. As a result, the start and end of the centerline can skip parts at the beginning or end of a river
![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_false_gaps_short_path.png)
Set river object created by `centerline_width.riverCenterline` to `interpolate_data=True` to fix for jagged edges or gaps formed by the interaction of sparse data and narrow banks
```python
river_object = centerline_width.riverCenterline(csv_data="data/river_coords.csv", interpolate_data=True)
```
| interpolate_data = False | interpolate_data = True |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_false_gaps.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_true_no_gaps.png) |
| ![example+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_false_gaps_2.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/interpolate_true_no_gaps_2.png) |

The amount of additional points added by interpolating can be adjusted with `interpolate_n`, but defaults to add 5 additional points between values

## Developer Notes: Tech Debt and Bug Fixes
* Option to set the distance between centerline points (a sub version of evenly spaced) (distance seperating = 1m)
* option to turn off verbose (no logs printed)
* Fix legend overlapping on graph, replace doc_examples that have an overlapping

## Citations
Based on work written in R (Golly et al. 2017):

>Golly, A. and Turowski, J. M.: Deriving principal channel metrics from bank and long-profile geometry with the R package cmgo, Earth Surf. Dynam., 5, 557-570, https://doi.org/10.5194/esurf-5-557-2017, 2017.

[Github - CMGO](https://github.com/AntoniusGolly/cmgo)

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>

This material is based upon work supported by the National Science Foundation Graduate Fellowship under Grant No. 2141064. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.

## Bug and Feature Request

Submit a bug fix, question, or feature request as a [Github Issue](https://github.com/cyschneck/centerline-width/issues) or to ugschneck@gmail.com/cyschneck@gmail.com
