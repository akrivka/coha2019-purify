import cfgrib

import xarray as xr

ds = xr.open_dataset('W_fr-meteofrance,MODEL,ENSEMBLE+FORECAST+SURFACE+O3+0H24H_C_LFPW_20190927000000.grib2', engine='cfgrib')
print(ds)
