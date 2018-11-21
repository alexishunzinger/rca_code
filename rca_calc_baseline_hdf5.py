#!/usr/bin/env python
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pyart
from rca_calc_baseline_hdf5_func import rca_create_baseline

from netCDF4 import Dataset
dataset = Dataset('/home/hunzinger/data/rca_cluttermap_20181108.nc')
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

#/home/hunzinger/data/ppi/

for f in glob.glob(os.path.join('/run/media/hunzinger/WININSTALL/csapr2-data/', 'corcsapr*.20181108.*cor-ppi*.h5')):
    print(f)
    DateTime, N, Bins, P, DBZ95, VN, VBins, VP, DBZ95V, UHN, UHBins, UHP, DBZ95UH, UVN, UVBins, UVP, DBZ95UV = rca_create_baseline(f, PCT_on_50, vPCT_on_50, uhPCT_on_50, uvPCT_on_50)
    
    # Put all PPI times into a list
    dt.append(DateTime)
    n.append(N)
    bins.append(Bins)
    p.append(P)
    dbz95.append(DBZ95)
    vn.append(VN)
    vbins.append(VBins)
    vp.append(VP)
    dbz95_v.append(DBZ95V)
    uhn.append(UHN)
    uhbins.append(UHBins)
    uhp.append(UHP)
    dbz95_uh.append(DBZ95UH)
    uvn.append(UVN)
    uvbins.append(UVBins)
    uvp.append(UVP)
    dbz95_uv.append(DBZ95UV)

dbz95_baseline = np.nanmean(dbz95)
print(dbz95_baseline)
n = np.asarray(n)
bins = np.asarray(bins)
p = np.asarray(p)
n_baseline = np.nanmean(n,axis=0)
bins_baseline = bins[0,:]
p_baseline = np.nanmean(p,axis=0)

#plt.plot(bins_baseline[1:],n_baseline*10)
#plt.plot(bins_baseline[1:],p_baseline)
#plt.plot(x,p_baseline)
#plt.show()

vdbz95_baseline = np.nanmean(dbz95_v)
print(vdbz95_baseline)
vn = np.asarray(vn)
vbins = np.asarray(vbins)
vp = np.asarray(vp)
vn_baseline = np.nanmean(vn,axis=0)
vbins_baseline = vbins[0,:]
vp_baseline = np.nanmean(vp,axis=0)
#plt.plot(vbins_baseline[1:],vn_baseline*10)
#plt.plot(vbins_baseline[1:],vp_baseline)
#plt.show()
#plt.plot(x,p_baseline)

uhdbz95_baseline = np.nanmean(dbz95_uh)
print('UZh:',uhdbz95_baseline, 'Zh:',dbz95_baseline)
uhn = np.asarray(uhn)
uhbins = np.asarray(uhbins)
uhp = np.asarray(uhp)
uhn_baseline = np.nanmean(uhn,axis=0)
uhbins_baseline = uhbins[0,:]
uhp_baseline = np.nanmean(uhp,axis=0)

uvdbz95_baseline = np.nanmean(dbz95_uv)
print('UZv:',uvdbz95_baseline, 'Zv:',vdbz95_baseline)
uvn = np.asarray(uvn)
uvbins = np.asarray(uvbins)
uvp = np.asarray(uvp)
uvn_baseline = np.nanmean(uvn,axis=0)
uvbins_baseline = uvbins[0,:]
uvp_baseline = np.nanmean(uvp,axis=0)

# H and UZh
#fig, ax1 = plt.subplots(figsize=[8,6])
#ax1.plot(bins_baseline[1:],n_baseline,color='darkslategrey')#,linestyle='--')
#ax1.plot(bins_baseline[1:],p_baseline,color='darkslategrey',label='Corr. H polarization :: dBZ95=49.50')
#ax1.plot(uhbins_baseline[1:],uhn_baseline,color='k')
#ax1.plot(uhbins_baseline[1:],uhp_baseline,color='k',label='Uncorr. H polarization :: dBZ95=58.87')
#ax1.axhline(95.,color='grey',linestyle='--')

#ax1.set_ylabel('PDF*10 and CDF')
#ax1.set_xlabel('Reflectivity (dBZ)')
#ax1.set_title('H baseline case \n 2018-11-08')
#ax1.legend(loc='center left')

# V and UZv
#fig, ax1 = plt.subplots(figsize=[8,6])
#ax1.plot(vbins_baseline[1:],vn_baseline,color='darkslategrey')#,linestyle='--')
#ax1.plot(vbins_baseline[1:],vp_baseline,color='darkslategrey',label='Corr. V polarization :: dBZ95=49.93')
#ax1.plot(uvbins_baseline[1:],uvn_baseline,color='k')
#ax1.plot(uvbins_baseline[1:],uvp_baseline,color='k',label='Uncorr. V polarization :: dBZ95=59.59')
#ax1.axhline(95.,color='grey',linestyle='--')

#ax1.set_ylabel('PDF and CDF')
#ax1.set_xlabel('Reflectivity (dBZ)')
#ax1.set_title('V baseline case \n 2018-11-08')
#ax1.legend(loc='center left')

#print(PCT_on_50.shape)
#print(uhPCT_on_50.shape)

d = Dataset('/home/hunzinger/data/RCA_baseline_20181108.nc',
                  'w',format='NETCDF4_CLASSIC')

azi = d.createDimension('azi', 360)
rang = d.createDimension('rang', 11)
value = d.createDimension('value',1)
nbins = d.createDimension('nbins',525)
binsdim = d.createDimension('binsdim',526)

PCT_ON_50 = d.createVariable('Flagged clutter grid gates', np.float64, ('azi','rang'))
DBZ95_BASE = d.createVariable('Baseline 95th reflectivity', np.float64, ('value',))
N_BASE = d.createVariable('PDF counts', np.float64, ('nbins',))
BINS = d.createVariable('PDF bins', np.float64, ('binsdim',))
P_BASE = d.createVariable('CDF values', np.float64, ('nbins',))
VPCT_ON_50 = d.createVariable('Flagged clutter grid gates (V)', np.float64, ('azi','rang'))
VDBZ95_BASE = d.createVariable('Baseline 95th reflectivity (V)', np.float64, ('value',))
VN_BASE = d.createVariable('PDF counts (V)', np.float64, ('nbins',))
VBINS = d.createVariable('PDF bins (V)', np.float64, ('binsdim',))
VP_BASE = d.createVariable('CDF values (V)', np.float64, ('nbins',))
UHPCT_ON_50 = d.createVariable('Flagged clutter grid gates (UZh)', np.float64, ('azi','rang'))
UHDBZ95_BASE = d.createVariable('Baseline 95th reflectivity (UZh)', np.float64, ('value',))
UHN_BASE = d.createVariable('PDF counts (UZh)', np.float64, ('nbins',))
UHBINS = d.createVariable('PDF bins (UZh)', np.float64, ('binsdim',))
UHP_BASE = d.createVariable('CDF values (UZh)', np.float64, ('nbins',))
UVPCT_ON_50 = d.createVariable('Flagged clutter grid gates (UZv)', np.float64, ('azi','rang'))
UVDBZ95_BASE = d.createVariable('Baseline 95th reflectivity (UZv)', np.float64, ('value',))
UVN_BASE = d.createVariable('PDF counts (UZv)', np.float64, ('nbins',))
UVBINS = d.createVariable('PDF bins (UZv)', np.float64, ('binsdim',))
UVP_BASE = d.createVariable('CDF values (UZv)', np.float64, ('nbins',))

PCT_ON_50[:,:] = PCT_on_50
DBZ95_BASE[:] = dbz95_baseline
N_BASE[:] = n_baseline
BINS[:] = bins_baseline
P_BASE[:] = p_baseline
VPCT_ON_50[:,:] = vPCT_on_50
VDBZ95_BASE[:] = vdbz95_baseline
VN_BASE[:] = vn_baseline
VBINS[:] = vbins_baseline
VP_BASE[:] = vp_baseline
UHPCT_ON_50[:,:] = uhPCT_on_50
UHDBZ95_BASE[:] = uhdbz95_baseline
UHN_BASE[:] = uhn_baseline
UHBINS[:] = uhbins_baseline
UHP_BASE[:] = uhp_baseline
UVPCT_ON_50[:,:] = uvPCT_on_50
UVDBZ95_BASE[:] = uvdbz95_baseline
UVN_BASE[:] = uvn_baseline
UVBINS[:] = uvbins_baseline
UVP_BASE[:] = uvp_baseline

d.close()