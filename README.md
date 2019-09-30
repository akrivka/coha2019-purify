# Purify
## Find your healthy path

* cams.py 
	* downloads data from CAMS, converts them to csv and saves them to the cams_cache folder
* maps.py
	* calls get_data() from cams.py if the data isn't availible, then generates a Google Map with the overlay and saves it to the cams_cache folder
* cost_function.py
	* calculates the cost of a route

## Dependencies
* Python (urllib, pandas, numpy, gmaps)
* eccodes library (availible only on linux)
