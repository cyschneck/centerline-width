# river-geometry

Python implementation of R-Code CMGO to find the centerline and width of rivers based on the latitude and longitude of a right and left bank

## Data
Data is accepted as txt file that is converted to a .csv script

Left and Right Bank Latitude and Longtiude:
- Header: llat, llon, rlat, rlon
- Data in degrees

## Requirements
Currently running on Python 3.7+

```
pip install -r requirments.txt
```

## Running Script

```python
python3 river_centerline_width.py 
```

Output:
![river_coords+png](https://raw.githubusercontent.com/cyschneck/river-geometry/main/data/river_coords.png)

## Citations
Based on the work:

Golly, Antonius & Turowski, Jens. (2017). Deriving principle channel metrics from bank and long-profile geometry with the R-package cmgo. Earth Surface Dynamics Discussions. 5. 1-19. 10.5194/esurf-5-557-2017. 

 <p align="center">
  <img src="https://user-images.githubusercontent.com/22159116/222872092-e0b579cc-4f84-4f49-aa53-397785fb9bf2.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872119-7c485ee2-4ffd-413a-9e4f-b043b122d2bb.png" />
  <img src="https://user-images.githubusercontent.com/22159116/222872019-12931138-9e10-4e51-aa1e-552e72d09af0.png" />
</p>


