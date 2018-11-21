import numpy as np
import matplotlib.pyplot as plt
import pyart
import os
import glob
from netCDF4 import Dataset
from rca_calculate_baseline_UN_netcdf import rca_create_baseline_UN_netcdf

dataset = Dataset('/home/hunzinger/data/rca_cluttermap_20181109.nc')
PCT_on_50 = dataset.variables['Flagged clutter grid gates'][:,:]
vPCT_on_50 = dataset.variables['Flagged clutter grid gates (V)'][:,:]
uhPCT_on_50 = dataset.variables['Flagged clutter grid gates (UZh)'][:,:]
uvPCT_on_50 = dataset.variables['Flagged clutter grid gates (UZv)'][:,:]
dataset.close()

dt = []
n = []
bins = []
p = []
dbz95 = []
vn = []
vbins = []
vp = []
dbz95_v = []
uhn = []
uhbins = []
uhp = []
dbz95_uh = []
uvn = []
uvbins = []
uvp = []
dbz95_uv = []

for f in glob.glob(os.path.join('/home/hunzinger/data/ppi_cf/', 'corcsapr2cfrppi*.20181109.*.nc')):
    print(f)
    DateTime, UHN, UHBins, UHP, DBZ95UH, UVN, UVBins, UVP, DBZ95UV = rca_create_baseline_UN_netcdf(f, PCT_on_50, vPCT_on_50, uhPCT_on_50, uvPCT_on_50)
    
    # Put all PPI times into a list
    dt.append(DateTime)
    uhn.append(UHN)
    uhbins.append(UHBins)
    uhp.append(UHP)
    dbz95_uh.append(DBZ95UH)
    uvn.append(UVN)
    uvbins.append(UVBins)
    uvp.append(UVP)
    dbz95_uv.append(DBZ95UV)

dataset = Dataset('/home/hunzinger/data/rca_baseline_20181109.nc')
n_baseline = dataset.variables['PDF counts'][:,:]
bins_baseline = dataset.variables['PDF bins'][:,:]
p_baseline = dataset.variables['CDF values'][:,:]
dbz95_baseline = dataset.variables['Baseline 95th refletivity'][:]
vn_baseline = dataset.variables['PDF counts (V)'][:,:]
vbins_baseline = dataset.variables['PDF bins (V)'][:,:]
vp_baseline = dataset.variables['CDF values (V)'][:,:]
vdbz95_baseline = dataset.variables['Baseline 95th refletivity (V)'][:]
dataset.close()

dbz95_baseline = np.nanmean(dbz95)
print(dbz95_baseline)
n = np.asarray(n)
bins = np.asarray(bins)
p = np.asarray(p)
n_baseline = np.nanmean(n,axis=0)
bins_baseline = bins[0,:]
p_baseline = np.nanmean(p,axis=0)

vdbz95_baseline = np.nanmean(dbz95_v)
print(vdbz95_baseline)
vn = np.asarray(vn)
vbins = np.asarray(vbins)
vp = np.asarray(vp)
vn_baseline = np.nanmean(vn,axis=0)
vbins_baseline = vbins[0,:]
vp_baseline = np.nanmean(vp,axis=0)

uhdbz95_baseline = np.nanmean(dbz95_uh)
print(uhdbz95_baseline, dbz95_baseline)
uhn = np.asarray(uhn)
uhbins = np.asarray(uhbins)
uhp = np.asarray(uhp)
uhn_baseline = np.nanmean(uhn,axis=0)
uhbins_baseline = uhbins[0,:]
uhp_baseline = np.nanmean(uhp,axis=0)

uvdbz95_baseline = np.nanmean(dbz95_uv)
print(uvdbz95_baseline, vdbz95_baseline)
uvn = np.asarray(uvn)
uvbins = np.asarray(uvbins)
uvp = np.asarray(uvp)
uvn_baseline = np.nanmean(uvn,axis=0)
uvbins_baseline = uvbins[0,:]
uvp_baseline = np.nanmean(uvp,axis=0)

# H and UZh
fig, ax1 = plt.subplots(figsize=[8,6])
ax1.plot(bins_baseline[1:],n_baseline*10,color='darkgrey',linestyle='--')
ax1.plot(bins_baseline[1:],p_baseline,color='darkgrey',linestyle='--',label='Corrected H polarization ::: dBZ95 = ')
ax1.plot(uhbins_baseline[1:],uhn_baseline*10,color='k')
ax1.plot(uhbins_baseline[1:],uhp_baseline,color='k',label='Uncorrected H polarization ::: dBZ95 = ')
ax1.axhline(95.,color='grey',linestyle='--')

ax1.set_ylabel('PDF*10 and CDF')
ax1.set_xlabel('Reflectivity (dBZ)')
ax1.set_title('Baseline case \n 2018-11-09')
ax1.legend()

# V and UZv
fig, ax1 = plt.subplots(figsize=[8,6])
ax1.plot(vbins_baseline[1:],vn_baseline*10,color='darkgrey',linestyle='--')
ax1.plot(vbins_baseline[1:],vp_baseline,color='darkgrey',linestyle='--',label='Corrected V polarization ::: dBZ95 = ')
ax1.plot(uvbins_baseline[1:],uvn_baseline*10,color='k')
ax1.plot(uvbins_baseline[1:],uvp_baseline,color='k',label='Uncorrected V polarization ::: dBZ95 = ')
ax1.axhline(95.,color='grey',linestyle='--')

ax1.set_ylabel('PDF*10 and CDF')
ax1.set_xlabel('Reflectivity (dBZ)')
ax1.set_title('Baseline case \n 2018-11-09')
ax1.legend()

dataset = Dataset('/home/hunzinger/data/rca_baseline_20181109.nc',
                  'r+',format='NETCDF4_CLASSIC')

azi = dataset.createDimension('azi', 360)
rang = dataset.createDimension('rang', 11)
value = dataset.createDimension('value',1)
n = dataset.createDimension('nbins',525)
bins = dataset.createDimension('bins',526)

UHPCT_ON_50 = dataset.createVariable('Flagged clutter grid gates (UZh)', np.float64, ('azi','rang'))
UHDBZ95_BASE = dataset.createVariable('Baseline 95th reflectivity (UZh)', np.float64, ('value',))
UHN_BASE = dataset.createVariable('PDF counts (UZh)', np.float64, ('nbins',))
UHBINS = dataset.createVariable('PDF bins (UZh)', np.float64, ('bins',))
UHP_BASE = dataset.createVariable('CDF values (UZh)', np.float64, ('nbins',))
UVPCT_ON_50 = dataset.createVariable('Flagged clutter grid gates (UZv)', np.float64, ('azi','rang'))
UVDBZ95_BASE = dataset.createVariable('Baseline 95th reflectivity (UZv)', np.float64, ('value',))
UVN_BASE = dataset.createVariable('PDF counts (UZv)', np.float64, ('nbins',))
UVBINS = dataset.createVariable('PDF bins (UZv)', np.float64, ('bins',))
UVP_BASE = dataset.createVariable('CDF values (UZv)', np.float64, ('nbins',))

UHPCT_ON_50[:,:] = uhPCT_on_50[0]
UHDBZ95_BASE[:] = uhdbz95_baseline
UHN_BASE[:] = uhn_baseline
UHBINS[:] = uhbins_baseline
UHP_BASE[:] = uhp_baseline
UVPCT_ON_50[:,:] = uvPCT_on_50[0]
UVDBZ95_BASE[:] = uvdbz95_baseline
UVN_BASE[:] = uvn_baseline
UVBINS[:] = uvbins_baseline
UVP_BASE[:] = uvp_baseline

dataset.close()