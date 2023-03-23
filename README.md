# Centerline-Width
![PyPi](https://img.shields.io/pypi/v/centerline-width)
![license](https://img.shields.io/github/license/cyschneck/centerline-width)

Find the centerline and width of rivers based on the latitude and longitude from the right and left bank 

| River Outlined in ArcGIS | Generated Centerline for the River Bank |
| ------------- | ------------- |
| ![river_google_earth+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example_google_earth.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example.png) |


Python implementation of [R-Code CMGO](https://github.com/AntoniusGolly/cmgo) (with modification)

## Requirements
Currently running on Python 3.7+

```
pip install -r requirments.txt
```
Requirements will also be downloaded as part of the pip download

## Install
PyPi pip install at [pypi.org/project/centerline-width/](https://pypi.org/project/centerline-width/)

```
pip install centerline-width
```

## Running Script
### Convert KML files to Text File

Convert two .kml files from Google Earth Pro and exports the coordinates into a text file

```
extractPointsToTextFile(left_kml=None, right_kml=None, text_output_name="data/river_coords.txt")
```

* **[REQUIRED]** left_kml (string): File location of the kml file for left bank
* **[REQUIRED]** right_kml (string): File location of the kml file for right bank
* [OPTIONAL] text_output_name (string): Output file name (and location), defaults to "data/river_coords.txt"

```python
import centerline_width
centerline_width.centerline_width.extractPointsToTextFile(left_kml="leftbank.kml",
							right_kml="rightbank.kml",
							text_output_name="data/river_coords_output.txt")
```

### Converted Data Text File to CSV

Convert a text file with coordinates for a left and right bank's latitude/longitude

```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
```

Scripts expect data as a list of point for left and right banks:
- Header: llat, llon, rlat, rlon

```
convertColumnsToCSV(text_file=None, flipBankDirection=False)
```
* **[REQUIRED]** text_file (string): File location of the text file to convert
* [OPTIONAL] flipBankDirection (boolean): If the latitude/longitude of the banks are generated in reverse order, flip the final values so left/right bank are in order

```python
import centerline_width
centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt", flipBankDirection=True)
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

### Return Latitude/Longitude Coordinates of Centerline
Return a list of lists for each latitude/longtiude coordinate of the centerline
```
centerlineLatitudeLongitude(csv_data=None, optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```python
import centerline_width
centerline_coordinates = centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv", optional_cutoff=cutoff)
```
Output: `[(-92.86788596499872, 30.03786596717931), (-92.86789573751797, 30.037834641974108), (-92.8679141386283, 30.037789636848878), (-92.8679251193248, 30.037756853899904), (-92.86796903819089, 30.03765423778148), (-92.86797335733262, 30.037643336049054), (-92.8679920356456, 30.037592224469797), (-92.86800576063828, 30.037555441489403), (-92.86800841510367, 30.037546512833107), (-92.8680119498663, 30.03753043193875)]`

### Return the length of the centerline
Return the length of the centerline (in degrees)

```
centerlineLength(centerline_coordinates=None)
```
* **[REQUIRED]** centerline_coordinates (list): A list of centerline coordinates (via centerlineLatitudeLongitude())

```python
import centerline_width
centerline_coordinates = centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv")
centerline_length = centerlineLength(centerline_coordinates=centerline_coordinates)
```
Returns the length from each centerline coordiante (currently in degrees)

### Plot Centerline in Matplotlib
Plot the centerline created from a list of right and left banks with Voronoi vertices

```
plotCenterline(csv_data=None,
		display_all_possible_paths=False, 
		plot_title=None, 
		save_plot_name=None, 
		displayVoronoi=False, 
		optional_cutoff=None)
```
* **[REQUIRED]** csv_data (string): File location of the text file to convert
* [OPTIONAL] display_all_possible_paths (boolean): Display all possible paths, not just the centerline (useful for debugging)
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_plot_name (string): Save the plot with a given name and location
* [OPTIONAL] displayVoronoi (boolean): Overlay Voronoi diagram used to generate centerline
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```python
import centerline_width
centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
				save_plot_name="data/river_coords.png", 
				display_all_possible_paths=False, 
				displayVoronoi=False, 
				optional_cutoff=550)
```
Output:
![river_coords+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords.png)

## Future Work:
### Return Width of River
Return the width of the river based on the centerline
```
riverWidthFromCenterline(csv_data=None,
						centerline_coordinates=None,
						save_to_csv=None,
						optional_cutoff=None)
```

* **[REQUIRED]** csv_data (string): File location of the text file to convert
* **[REQUIRED]** centerline_coordinates (list): A list of centerline coordinates (via centerlineLatitudeLongitude())
* [OPTIONAL] plot_title (string): Change plot title, defaults to "River Coordinates: Valid Centerline = True/False, Valid Polygon = True/False"
* [OPTIONAL] save_to_csv (string): Save the csv with a given name and location
* [OPTIONAL] optional_cutoff (int): Include only the first x amount of the data to chart (useful for debugging)

```python
import centerline_width
river_width_dict = centerline_width.riverWidthFromCenterline(csv_data="data/river_coords.csv", 
							centerline_coordinates=centerline_long_lat_coordinates,
							save_to_csv="data/river_width.csv")
```

### Additional Channel Metrics

Return the length of the centerline (length of the left/right bank)

Return the slope of the river

Return the width of the river

Return the bank retreat

Return the abundances of species

Return the knickpoints (occurrences of knickpoints)

Return smoothed centerline

## Documentation and Algorithm to Determine Centerline

The centerline is defined by the greatest distance from the right and left bank, created from a Voronoi Diagram. The remaining paths within the river are filtered through Dijkstra's algorithm to find the shortest path that is the centerline

### Right and Left bank points are plotted (X-Axis for Latitude, Y-Axis for Longitude)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example1.png)

### Generate a polygon to encapsulate the river between the right and left banks to define in and outside of river
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example2.png)

### Generate a Voronoi based on the points along the river banks
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example3.png)

### Display Voronoi ridge vertices that lie within the polygon (within the river banks)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

### Filter out any point pairs that only have one connections to filter out the short dead end paths and find the starting and ending node based on distance from the top and bottom of polygon
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example6.png)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example7.png)

### Find the shortest path from the starting node to the ending node ([Dijkstra's Algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path))
| Points on River Bank | NetworkX Graph of Points on River Bank |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example10.png) | ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example9.png) |

### Display the centerline found by connecting the starting/ending node with the shortest path
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example8.png)

This is an attempt at a more robust algorithm working from raw data to ensure that all dead ends are removed and no gaps exist in the centerline

Points that only have one connection are removed, but by limiting the number of connections for a point to just two will create gaps. The Voronoi vertices connect to other vertex values, but some connect to more and some only connect to one other point. Removing additional values will create gaps, so this is avoided in this code by not applying additional filters.

**All vertices:**
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

**Vertices that have at least two connections (that would create gaps):**
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example5.png)

## Debugging, Error Handling, and Edge Cases
A polygon is invalid if it overlaps within itself:
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example1.png)
In this example, the polygon is invalid, but with such a small overlap it is still able to find a valid path

With limited data, the polygon will overlap more dramatically and will no longer be able to find a valid centerline:
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example4.png)

If the data starts with a large width, it is possible for the starting node to be invalid
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example3.png)
Currently, the starting node is determined by the closest node to the top of the bank (in green) and the ending node is determined by the closest node to the bottom of the bank (in red)

If the data is too small, a centerline and its coordinates cannot not be found (since only a single Voronoi vertex exists within the polygon and after deadends are filtered)
`CRITICAL ERROR, Voronoi diagram generated too small to find centerline (no starting node found), unable to plot centerline. Set displayVoronoi=True to view. Can typically be fixed by adding more data to expand range.`
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example2.png)
Can be fixed by expanding the data until the polygon is large enough to contain at least two different vertex points

## Citations
Based on the work in R:

>Golly, A. and Turowski, J. M.: Deriving principal channel metrics from bank and long-profile geometry with the R package cmgo, Earth Surf. Dynam., 5, 557-570, https://doi.org/10.5194/esurf-5-557-2017, 2017.

[Github - CMGO](https://github.com/AntoniusGolly/cmgo)

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>
