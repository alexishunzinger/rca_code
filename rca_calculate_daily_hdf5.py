# Import
import numpy as np
import matplotlib.pyplot as plt
import pyart
import pandas as pd
import os
import glob
from netCDF4 import Dataset
from rca_calculate_hdf5_func import rca_calculate_hdf5_func

# Specify day of interest
yr = '2018'
mon = '11'
day = '08'
date = yr+mon+day

# Specify path for that day
filepath = '/home/hunzinger/data/ppi/'

dataset = Dataset('/home/hunzinger/data/rca_baseline_20181109.nc')
PCT_on_50 = dataset.variables['Flagged clutter grid gates'][:,:]
vPCT_on_50 = dataset.variables['Flagged clutter grid gates (V)'][:,:]
dbz95_baseline = dataset.variables['Baseline 95th reflectivity'][:]
vdbz95_baseline = dataset.variables['Baseline 95th reflectivity (V)'][:]
dataset.close()

# Create empty lists to fill using function
dt = []
dbz95 = []
vdbz95 = []

for f in glob.glob(os.path.join(filepath, 'corcsaprM1*.'+date+'.23*cor-ppi*.h5')):
    print(f)
    DateTime, DBZ95, VDBZ95 = rca_calculate_hdf5_func(f, PCT_on_50, vPCT_on_50)
    
    # Put all PPI times into a list
    dt.append(DateTime)
    dbz95.append(DBZ95)
    vdbz95.append(VDBZ95)

# Calculate mean dBZ95 using all PPI times to get daily mean (H)
# and calculate RCA using baseline dBZ95
dbz95_mean = np.nanmean(dbz95)
rca_mean = dbz95_baseline[0] - dbz95_mean

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

# Specify the path to access and write to the running CSV file
csv_output_path = '/home/hunzinger/data/'
csv_output_file = 'rca_daily_values.csv'
csv_filepath = csv_output_path+csv_output_file

with open(csv_filepath, 'a') as f:
    df_rca.to_csv(f, mode='a', header=f.tell()==0)
