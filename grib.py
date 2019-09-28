import pygrib

grbs = pygrib.open("W_fr-meteofrance,MODEL,ENSEMBLE+FORECAST+SURFACE+O3+0H24H_C_LFPW_20190927000000.grib2")

grbs.seek(0)
for grb in grbs:
    print(grb)


grbs.select(name='Mass density')[0]
