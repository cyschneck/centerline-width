# river-geometry

Python implementation of R-Code CMGO to find the centerline and width of rivers based on the latitude and longitude of a right and left bank

## Data
Data is accepted as text file that is converted to a .csv script

```
     llat       llon      rlat       rlon
30.037581 -92.868569 30.119804 -92.907933
30.037613 -92.868549 30.119772 -92.907924
30.037648 -92.868546 30.119746 -92.907917
30.037674 -92.868536 30.119721 -92.907909
30.037702 -92.868533 30.119706 -92.907905
...
```

Left and Right Bank Latitude and Longtiude:
- Header: llat, llon, rlat, rlon
- Data in degrees

## Requirements
Currently running on Python 3.7+

```
pip install -r requirments.txt
```

## Running Script

### Plot Centerline on Matplotlib

```python
python3 river_centerline_width.py 
```

Output:
![river_coords+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords.png)

### Return the Latitude/Longitude of Centerline

## Documentation and Algorithm

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


