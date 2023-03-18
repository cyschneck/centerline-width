from pykml import parser
import re
import pandas as pd

# Internal centerline_width reference to access functions, global variables, and error handling
import centerline_width

'''
 Code takes in a kml file from Google Earth Pro and exports the coordinates
 into a txt file. 
'''
def extractPointsToTextFile(left_kml=None, right_kml=None, text_output_name="river_coords.txt"):
	centerline_width.errorHandlingExtractPointsToTextFile(left_kml=left_kml, right_kml=right_kml, text_output_name=text_output_name)

	# extract points from kml file
	with open(left_kml) as f:
		doc = parser.parse(f)
	root = doc.getroot()
	coords = root.Document.Placemark.LineString.coordinates.text
	lon = re.findall(r'(-[0-9]{2}\.[0-9]*)',coords)
	lat = re.findall(r'[^-]([0-9]{2}\.[0-9]*)',coords)
	llon = list([float(i) for i in lon])
	llat = list([float(i) for i in lat])
	
	with open(right_kml) as f:
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
	
	with open(text_output_name, 'a') as f:
		dfAsString = df.to_string(header=True, index=False)
		f.write(dfAsString)


