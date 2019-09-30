import subprocess
import urllib.request
import os

# format:
	# type: CO|NH3|NMVOC|NO|NO2|O3|PANS|PM10|PM25|SO2|BIRCHPOLLEN|LIVEPOLLEN|GRASSPOLLEN|RAGWEEDPOLLEN
	# year: e.g. 2019
	# month: e.g. 09 (please, use two digits always)
	# hour: e.g. 00 (please, use two digits always)
	# days_ahead: 1|2|3|4
# output: Latitude Longitude Value -- still needs to be formatted
# for more info, consult: https://www.regional.atmosphere.copernicus.eu/doc/Guide_Numerical_Data_CAMS_new.pdf

def get_data(type, year, month, day, hour, days_ahead):
	create_directories()

	# downloading the file
	data = None
	for level in ["SURFACE", "ALLLEVELS"]:
		# target definition
		target = folder + "/grib2/" + type + "-" + level + "-from=" + str(year) + "-" + str(month) + "-" + str(day) + ":" + str(hour) + ":00:00Z-days_ahead=" + str(days_ahead) + ".grib2"
		if(not os.path.exists(target)):
			try:
				url = get_url(type, year, month, day, hour, days_ahead, level)
				print("Retrieving from: " + url)
				urllib.request.urlretrieve(url, target)
				break
			except urllib.error.URLError as e:
				if(e.reason == "Not Found"):
					print("The given URL doesn't work.")
			print("Saving to: " + target)
		else:
			print("File: " + target + " already present. ")
			break

	# decoding the data
	print("Decoding data.")
	data = subprocess.check_output(["grib_get_data", target]).decode()

	outpaths = []
	for time,data_time in enumerate(data.split("Latitude, Longitude, Value")):
		outpath = folder + "/csv/" + type + "-" + level + "-from=" + str(year) + "-" + str(month) + "-" + str(day) + ":" + str(hour) + ":00:00Z-time=" + str(time) + ".csv"
		outpaths.append(outpath)
		if(not os.path.exists(outpath)):
			print("Writing data to: " + outpath)
			outfile = open(outpath, "w+")
			data_time_formatted = "Latitude,Longitude,Value\n"
			for l in data_time.splitlines():
				try:
					data_time_formatted += (l.split()[0] + "," + l.split()[1] + "," + l.split()[2] + "\n")
				except:
					print("Very very minor error.")
			outfile.write(data_time_formatted)
			outfile.close()
	
	return outpaths

def get_url(type, year, month, day, hour, days_ahead, level):
	# converting days_ahead to the appropriate url format
	if (days_ahead == 1):
		time = "0H24H"
	elif (days_ahead == 2):
		time = "25H48H"
	elif (days_ahead == 3):
		time = "49H72H"
	elif (days_ahead == 4):
		time = "73H96H"

	url = "https://download.regional.atmosphere.copernicus.eu/services/CAMS50?&token=__wdPXAXwGWld9498i_72XQfIO0BcChSq3b1EiEFiPmzO8r_lVuwlETQ__&grid=0.1&model=ENSEMBLE&package=FORECAST_" + type \
	+ "_" + level + "&time=" + time \
	+ "&referencetime=" + year \
	+ "-" + month + "-" \
	+ day \
	+ "T" \
	+ hour + ":00:00Z&format=GRIB2"
	return url

def create_directories():
	folder = "cams_cache"
	if(not os.path.exists(folder)):
		try:
		    os.mkdir(folder)
		except OSError:
		    print ("Creation of the directory" + folder + " failed")
	if(not os.path.exists(folder + "/csv")):
		try:
			os.mkdir(folder + "/csv")
		except OSError:
		    print ("Creation of the directory" + folder + "/csv failed")
	if(not os.path.exists(folder + "/grib2")):
		try:
			os.mkdir(folder + "/grib2")
		except OSError:
		    print ("Creation of the directory" + folder + "/grib2 failed")

# print(get_data("O3", "2019", "09", "27", "00", 1))
# sys.exit(0)

# example
# types="CO|NH3|NMVOC|NO|NO2|O3|PANS|PM10|PM25|SO2|BIRCHPOLLEN|LIVEPOLLEN|GRASSPOLLEN|RAGWEEDPOLLEN"
# last_values = {}
# for type in types.split("|"):
# 	data = get_data(type, "2019", "09", "27", "00", 1)
# 	if(data is not None):
# 		last_values[type] = data.splitlines()[1].split()[2]
# 		print(last_values[type])
# 	print("---")

# print(last_values)
