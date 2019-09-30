import pandas as pd
import numpy as np
import os
import gmaps
import time
import sys
from ipywidgets.embed import embed_minimal_html
import cams

def generate_map(type, year, month, day, hour, days_ahead):
	# reading data and calculating weights
	infile = cams.get_data(type, year, month, day, hour, days_ahead)[1]
	print(infile)
	satdata = pd.read_csv(infile)
	print("Files successfully read\n --------")
	# satdata = pd.read_csv('data.csv')
	locations = satdata[['Latitude', 'Longitude']]
	weights = 1 - (satdata['Value'] / satdata['Value'].max())
	# print(locations)
	# print(weights)


	# calculating rectangles to be render on the drawing layer
	loc1 = locations-0.05
	loc1 = loc1.apply(tuple, axis=1)
	loc2 = pd.concat([locations.Latitude - 0.05, locations.Longitude + 0.05], axis=1)
	loc2 = loc2.apply(tuple, axis=1)
	loc3 = locations+0.05
	loc3 = loc3.apply(tuple, axis=1)
	loc4 = pd.concat([locations.Latitude + 0.05, locations.Longitude - 0.05], axis=1)
	loc4 = loc4.apply(tuple, axis=1)
	loc = pd.concat([loc1, loc2, loc3, loc4], axis=1)

	# print(loc)
	# print(loclist)

	loclist = loc.values.tolist()

	# configuring gmaps
	gmaps.configure(api_key='AIzaSyCZjvcaXP_7Fc3hCr-TWM6-I7SYKHau6Dw')
	# new gmaps figure
	fig = gmaps.figure(center=((51.209381+48.431117)/2,(11.265527+19.04932)/2), zoom_level=7)

	# Boundaries for the Czech and Slovak Republic
	# Latitude    Longitude
	# 51.209381   11.265527
	# 48.431117   11.265527
	# 51.209381   19.04932
	# 48.431117   19.04932
	polys = []
	for x in range(0, len(loclist)):
	   if(loclist[x][0][0] < 51.209381 and loclist[x][0][0] > 48.431117 and loclist[x][1][1] < 19.04932 and loclist[x][1][1] > 11.265527):
		   r = int(0 + weights[x]*255)
		   g = int(255 - weights[x]*255)
		   col = (r,g,0)
		   polys.append(gmaps.Polygon(loclist[x],fill_color=col, fill_opacity=0.8, stroke_color=col, stroke_weight=0))
		   print(str(x) + "/" + str(len(loclist)) + " | Rendering: " + str(loclist[x]) + " with color: " + str(col))

	# layer for overlaying pollution
	drawing = gmaps.drawing_layer()
	drawing.features = polys
	fig.add_layer(drawing)

	# start = (51.209381, 11.265527)
	# end = (48.431117, 19.04932)
	# directions = gmaps.directions_layer(start, end, travel_mode='WALKING')
	# fig.add_layer(directions)

	# exporting html file with a Google Map
	if(not os.path.exists("cams_cache/html")):
		try:
		    os.mkdir("cams_cache/html")
		except OSError:
		    print ("Creation of the directory" + "cams_cache/html" + " failed")
	print("Exporting: " + infile.replace('csv','html'))
	embed_minimal_html(infile.replace('csv','html') , views=[fig])
	return None

generate_map("NO", "2019", "09", "27", "00", 1)
