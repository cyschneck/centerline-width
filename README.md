# Centerline-Width
![PyPi](https://img.shields.io/pypi/v/centerline-width)
![license](https://img.shields.io/github/license/cyschneck/centerline-width)

Find the centerline and width of rivers based on the latitude and longitude of the right and left bank

| Points on River Bank | Centerline of River Bank |
| ------------- | ------------- |
| ![river_google_earth+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example_google_earth.png) | ![river_centerline+png](https://raw.githubusercontent.com/cyschneck/centerline-width/main/data/doc_examples/river_example.png) |


Python implementation of [R-Code CMGO](https://github.com/AntoniusGolly/cmgo) (with modification)

## Data
Scripts can accept a text file that can be converted to a .csv file

```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
...
```

Scripts expect data as a list of point:
- Header: llat, llon, rlat, rlon

## Requirements
Currently running on Python 3.7+

```
pip install -r requirments.txt
```

## Running Script

### Converted Text File to CSV

```python
import centerline_width
centerline_width.convertColumnsToCSV(text_file="data/river_coords.txt", flipBankDirection=True)
```

### Plot Centerline in Matplotlib
```python
import centerline_width
centerline_width.plotCenterline(csv_data="data/river_coords.csv", 
				save_plot_name="data/river_coords.png", 
				display_all_possible_paths=True, 
				displayVoronoi=False, 
				optional_cutoff=cutoff)
```
Output:
![river_coords+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords.png)

### Return Latitude/Longitude Coordinates of Centerline
```python
import centerline_width
centerline_long_lat_coordinates = centerline_width.centerlineLatitudeLongitude(csv_data="data/river_coords.csv", 																optional_cutoff=cutoff)
```
Output: `[(-92.86788596499872, 30.03786596717931), (-92.86789573751797, 30.037834641974108), (-92.8679141386283, 30.037789636848878), (-92.8679251193248, 30.037756853899904), (-92.86796903819089, 30.03765423778148), (-92.86797335733262, 30.037643336049054), (-92.8679920356456, 30.037592224469797), (-92.86800576063828, 30.037555441489403), (-92.86800841510367, 30.037546512833107), (-92.8680119498663, 30.03753043193875)]`
### Return Width of River
```python
import centerline_width
river_width_dict = centerline_width.riverWidthFromCenterline(csv_data="data/river_coords.csv", 																centerline_coordinates=centerline_long_lat_coordinates,
							save_to_csv="data/river_width.csv")
```
Output: ``
## Documentation and Algorithm (Backend)

The centerline is defined by the greatest distance from the right and left bank, created from a Voronoi Diagram. The remaining paths within the river are filtered through Dijkstra's algorithm to find the shortest path that is the centerline

### Right and Left bank points are plotted (X-Axis for Latitude, Y-Axis for Longitude)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example1.png)

### Generate a polygon to encapsulate the river between the right and left banks to define in and outside of river
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example2.png)

### Generate a Voronoi based on the points along the river banks
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example3.png)

### Display Voronoi ridge vertices that lie within the polygon (within the river banks)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

### Filter out any point pairs that only have one connections to filter out the short dead end paths

###  Find the starting and ending node based on distance from the top and bottom of polygon
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example6.png)
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example7.png)

### Find the centerline: shortest path from the starting node to the ending node ([Dijkstra's Algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path))
| Points on River Bank | NetworkX Graph of Points on River Bank |
| ------------- | ------------- |
| ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example10.png) | ![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example9.png) |

![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example8.png)

This is an attempt at a more robust algorithm working from raw data to ensure that all dead ends are removed and no gaps exist in the centerline

Points that only have one connection are removed, but by limiting the number of connections for a point to just two will create gaps. The Voronoi vertices connect to other vertex values, but some connect to more and some only connect to one other point. Removing additional values will create gaps, so this is avoided in this code by not applying additional filters.

All vertices:
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example4.png)

Vertices that have at least two connections (that would create gaps):
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/example5.png)

## Edge Cases
Invalid Polygon
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example1.png)

Invalid Polygon
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example4.png)

Invalid Starting Node
![example+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/doc_examples/invalid_example3.png)

## Citations
Based on the work:

Golly, Antonius & Turowski, Jens. (2017). Deriving principle channel metrics from bank and long-profile geometry with the R-package cmgo. Earth Surface Dynamics Discussions. 5. 1-19. 10.5194/esurf-5-557-2017. 

[Github - CMGO](https://github.com/AntoniusGolly/cmgo)

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>
