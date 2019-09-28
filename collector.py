import requests

data = requests.get("https://download.regional.atmosphere.copernicus.eu/services/CAMS50?&token=__wdPXAXwGWld9498i_72XQfIO0BcChSq3b1EiEFiPmzO8r_lVuwlETQ__&grid=0.1&model=ENSEMBLE&package=FORECAST_O3_SURFACE&time=0H24H&referencetime=2019-09-27T00:00:00Z&format=GRIB2")

print(data.content)
