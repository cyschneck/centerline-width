import matplotlib.pyplot as plt
import numpy as np
import os
import time
from datetime import timedelta
from pykml import parser
import re
import contextily as cx
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import math
import pandas as pd

'''
 Code takes in a kml file from google earth pro and exports the coordinates
 into a txt file. 
'''
def main():

	if __name__ != '__main__':
		raise RuntimeError("Calling function in a context other than __main__ is not supported.")

	start_time = time.monotonic()

	# extract points from kml file
	with open('leftbank.kml') as f:
		doc = parser.parse(f)
	root = doc.getroot()
	coords = root.Document.Placemark.LineString.coordinates.text
	lon = re.findall(r'(-[0-9]{2}\.[0-9]*)',coords)
	lat = re.findall(r'[^-]([0-9]{2}\.[0-9]*)',coords)
	llon = list([float(i) for i in lon])
	llat = list([float(i) for i in lat])
	
	with open('rightbank.kml') as f:
		doc = parser.parse(f)
	root = doc.getroot()
	coords = root.Document.Placemark.LineString.coordinates.text
	lon = re.findall(r'(-[0-9]{2}\.[0-9]*)',coords)
	lat = re.findall(r'[^-]([0-9]{2}\.[0-9]*)',coords)
	rlon = list([float(i) for i in lon])
	rlat = list([float(i) for i in lat])

	df = pd.DataFrame({'llat':llat,'llon':llon})
	df_rb = pd.DataFrame({'rlat':rlat,'rlon':rlon})
	df = pd.concat([df,df_rb],axis=1)
	
	with open('river_coords.txt', 'a') as f:
		dfAsString = df.to_string(header=True, index=False)
		f.write(dfAsString)

	end_time = time.monotonic()
	
	
	print("Time to run get_coordinates_kml.py: {0} seconds".format(timedelta(seconds=end_time - start_time)))


if __name__ == '__main__':
	main()


