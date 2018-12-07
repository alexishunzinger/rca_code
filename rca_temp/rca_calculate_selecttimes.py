#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
from netCDF4 import Dataset
from rca_calculate_hdf5_func import rca_calculate_hdf5_func

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments are PPI path, date (YYYYMMDD), baseline netCDF path, csv file path, choose use of UZ or Z, choose time period"
        )
        sys.exit(0)

    datadir = sys.argv[1]
    date = sys.argv[2]
    baselinedir = sys.argv[3]
    csvdir = sys.argv[4]
    defaultZ = sys.argv[5]
    timeperiod = sys.argv[6]
    print(datadir, date, baselinedir, csvdir, defaultZ, timeperiod)

    # Specify path for that day (datadir)
    # datadir should be input upon running script (sys.argv[1])
    # filepath = '/home/hunzinger/data/ppi/'

    # Specify date of interest (date)
    # date ('YYYYMMDD') should be input upon running script (sys.argv[2])
    yr = date[0:4]
    mon = date[4:6]
    day = date[6:]

    # Specify directory where the baseline netCDF is located (baselinedir)
    # baselinedir should be input upon running script (sys.argv[3])

    # Specify the path to access and write to the running CSV file (csvdir)
    # csvdir should be input upon running script (sys.argv[4])
    # csv_output_path = '/home/hunzinger/data/'
    csv_filepath = csvdir + "rca_test_values.csv"

    # Specify the use of UZ or Z in the RCA calculation
    # defaultZ should be input upon running script (sys.argv[5])
    if defaultZ == "UZ":
        uncorrectedZ = True
        dataset = Dataset(baselinedir + "rca_baseline_20181108.nc")
        hPCT_on_50 = dataset.variables["clutter_gate_values_uzh"][:, :]
        vPCT_on_50 = dataset.variables["clutter_gate_values_uzv"][:, :]
        hdbz95_baseline = dataset.variables["baseline_dbz95_uzh"][:]
        vdbz95_baseline = dataset.variables["baseline_dbz95_uzv"][:]
        dataset.close()
    elif defaultZ == "Z":
        uncorrectedZ = False
        dataset = Dataset(baselinedir + "rca_baseline_20181108.nc")
        hPCT_on_50 = dataset.variables["clutter_gate_values_zh"][:, :]
        vPCT_on_50 = dataset.variables["clutter_gate_values_zv"][:, :]
        hdbz95_baseline = dataset.variables["baseline_dbz95_zh"][:]
        vdbz95_baseline = dataset.variables["baseline_dbz95_zv"][:]
        dataset.close()
    else:
        print("ERROR: Must specify the use of UZ or Z in the RCA calculation")


    # Specify time of interest (timeperiod)
    # time (00-11 or 12-23) should be selected upon running script (sys.argv[6])
    if timeperiod == "00-06":
        time = ['00','01','02','03','04','05','06']#,'07','08','09','10','11']
    elif timeperiod == "12-00":
        time = ['18','19','20','21','22','23'] #'07','08','09','10','11','12','13','14','15','16','17'
    else:
        print("ERROR: Must specify the time period for this day - 00-06 or 12-00")

    # Create empty lists to fill using function
    dt = []
    hdbz95 = []
    vdbz95 = []

    
    for t in time:
        for f in glob.glob(os.path.join(datadir, "corcsaprM1*.cor-ppi*" + date + t + "*.h5")):
            print(f)
            try:
                DateTime, HDBZ95, VDBZ95 = rca_calculate_hdf5_func(
                f, hPCT_on_50, vPCT_on_50, uncorrectedZ=uncorrectedZ
                )
            except OSError:
                pass

            # Put all PPI times into a list
            dt.append(DateTime)
            hdbz95.append(HDBZ95)
            vdbz95.append(VDBZ95)

    # Calculate mean dBZ95 using all PPI times to get daily mean (H)
    # and calculate RCA using baseline dBZ95
    hdbz95_mean = np.nanmean(hdbz95)
    hrca_mean = hdbz95_baseline[0] - hdbz95_mean

    hrca = hdbz95_baseline[0] - hdbz95

    # Calculate mean dBZ95 using all PPI times to get daily mean (V)
    # and calculate RCA using baseline dBZ95
    vdbz95_mean = np.nanmean(vdbz95)
    vrca_mean = vdbz95_baseline[0] - vdbz95_mean

    vrca = vdbz95_baseline[0] - vdbz95

    # Write daily RCA to CSV file

    base = 0  # set to 0 for daily RCA, set to 1 when calculating for baseline
    date = yr + "-" + mon + "-" + day


    for scan in range(0,len(dt)):
        # Create dictionary and dataframe
        csv_frame = pd.read_csv(csv_filepath)
        #import pdb; pdb.set_trace()

        rca_dict = {
            "DATE": dt[scan], "RCA_H": hrca[scan], "RCA_V": vrca[scan], "BASELINE": base
            }
        #rca_dict = {
        #    "DATE": date, "TIME":timeperiod+" Z", "RCA_H": hrca_mean, "RCA_V": vrca_mean, "BASELINE": base
        #}
        csv_frame = csv_frame.append(rca_dict, ignore_index=True)
        csv_frame.set_index('DATE')


        csv_frame.to_csv(csv_filepath , index=False)