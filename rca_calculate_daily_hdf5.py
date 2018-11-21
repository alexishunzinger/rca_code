#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyart
import pandas as pd
import os
import glob
from netCDF4 import Dataset
from rca_calculate_hdf5_func import rca_calculate_hdf5_func

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('ERROR: Arguments are PPI path, date (YYYYMMDD), baseline netCDF path, csv file path, choose use of UZ or Z')
        sys.exit(0)
    print(sys.argv)
    #print(sys.argv[2])
    datadir = sys.argv[1]
    date = sys.argv[2]
    baselinedir = sys.argv[3]
    csvdir = sys.argv[4]
    defaultZ = sys.argv[5]
    print(datadir, date, baselinedir, csvdir, defaultZ)

    # Specify path for that day (datadir)
    # datadir should be input upon running script (sys.argv[1])
    #filepath = '/home/hunzinger/data/ppi/'

    # Specify date of interest (date)
    # date ('YYYYMMDD') should be input upon running script (sys.argv[2])
    yr = date[0:4]
    mon = date[4:6]
    day = date[6:]

    # Specify directory where the baseline netCDF is located (baselinedir)
    # baselinedir should be input upon running script (sys.argv[3])

    # Specify the path to access and write to the running CSV file (csvdir)
    # csvdir should be input upon running script (sys.argv[4])
    #csv_output_path = '/home/hunzinger/data/'
    csv_filepath = csvdir+'rca_daily_values.csv'

    # Specify the use of UZ or Z in the RCA calculation
    # defaultZ should be input upon running script (sys.argv[5])
    if defaultZ == 'UZ':
        uncorrectedZ=True
        dataset = Dataset(baselinedir+'rca_baseline_20181108.nc')
        hPCT_on_50 = dataset.variables['Flagged clutter grid gates (UZh)'][:,:]
        vPCT_on_50 = dataset.variables['Flagged clutter grid gates (UZv)'][:,:]    
        hdbz95_baseline = dataset.variables['Baseline 95th reflectivity (UZh)'][:]
        vdbz95_baseline = dataset.variables['Baseline 95th reflectivity (UZv)'][:]
        dataset.close()
    elif defaultZ == 'Z':
        uncorrectedZ=False
        dataset = Dataset(baselinedir+'rca_baseline_20181108.nc')
        hPCT_on_50 = dataset.variables['Flagged clutter grid gates'][:,:]
        vPCT_on_50 = dataset.variables['Flagged clutter grid gates (V)'][:,:]
        hdbz95_baseline = dataset.variables['Baseline 95th reflectivity'][:]
        vdbz95_baseline = dataset.variables['Baseline 95th reflectivity (V)'][:]
        dataset.close()
    else:
        print('ERROR: Must specify the use of UZ or Z in the RCA calculation')

    # Create empty lists to fill using function
    dt = []
    dbz95 = []
    vdbz95 = []

    for f in glob.glob(os.path.join(datadir, 'corcsaprM1.*.cor-ppi*_'+date+'*.h5')):
        print(f)
        DateTime, DBZ95, VDBZ95 = rca_calculate_hdf5_func(f, hPCT_on_50, vPCT_on_50, uncorrectedZ=uncorrectedZ)
        
        # Put all PPI times into a list
        dt.append(DateTime)
        dbz95.append(DBZ95)
        vdbz95.append(VDBZ95)

    # Calculate mean dBZ95 using all PPI times to get daily mean (H)
    # and calculate RCA using baseline dBZ95
    dbz95_mean = np.nanmean(dbz95)
    rca_mean = hdbz95_baseline[0] - dbz95_mean

    # Calculate mean dBZ95 using all PPI times to get daily mean (V)
    # and calculate RCA using baseline dBZ95
    vdbz95_mean = np.nanmean(vdbz95)
    vrca_mean = vdbz95_baseline[0] - vdbz95_mean

    # Write daily RCA to CSV file

    base = 0 #set to 0 for daily RCA, set to 1 when calculating for baseline
    date = yr+'-'+mon+'-'+day

    # Create dictionary and dataframe
    rca_dict = {'DATE':[date],'RCA_H':[rca_mean],'RCA_V':[vrca_mean],'BASELINE':[base]}
    df_rca = pd.DataFrame(data=rca_dict)

    with open(csv_filepath, 'a') as f:
        df_rca.to_csv(f, mode='a', header=f.tell()==0)
