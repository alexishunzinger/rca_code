#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "ERROR: Arguments are csv file path and output path for figures"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    print(csvpath, fig_outpath)


csvfile = csvpath+'rca_daily_values_abbrev.csv'
csvfile_error = csvpath+'rca_daily_values_error.csv'

df = pd.read_csv(csvfile)
# Ensure values in csv file are in chronological order
df = df.sort_values(by='DATE')

ylim = -3,3

# Plot the H polarization RCA values only
fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=0.5)
ax.plot(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=0.5)
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (H) during CACTI')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_h.png')

fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_V'],
               color='k',
               linewidth=0.5)
ax.plot(df['DATE'],df['RCA_V'],
               color='k',
               linewidth=0.5)
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (V) during CACTI')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_v.png')

fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_H'],
            color='k',
            linewidth=0.5,
            label='H')
ax.plot(df['DATE'],df['RCA_H'],
            color='k',
            linewidth=0.5,
            label='')
ax.scatter(df['DATE'],df['RCA_V'],
            color='slategrey',
            linewidth=0.5,
            label='V')
ax.plot(df['DATE'],df['RCA_V'],
            color='slategrey',
            linewidth=0.5,
            label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values during CACTI')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_hv.png')


# Plot the error values

df = pd.read_csv(csvfile_error)
# Ensure values in csv file are in chronological order
df = df.sort_values(by='DATE')

ylim = -3,3

# Plot the H polarization RCA values only
fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=0.5)
ax.plot(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=0.5)
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (H) during CACTI (+1 dBZ bias)')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_h_err.png')

fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_V'],
               color='k',
               linewidth=0.5)
ax.plot(df['DATE'],df['RCA_V'],
               color='k',
               linewidth=0.5)
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values (V) during CACTI (+1 dBZ bias)')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_v_err.png')

fig, ax = plt.subplots(figsize=[8,4])
ax.axhline(0.,linestyle='--',color='grey')
ax.scatter(df['DATE'],df['RCA_H'],
            color='k',
            linewidth=0.5,
            label='H')
ax.plot(df['DATE'],df['RCA_H'],
            color='k',
            linewidth=0.5,
            label='')
ax.scatter(df['DATE'],df['RCA_V'],
            color='slategrey',
            linewidth=0.5,
            label='V')
ax.plot(df['DATE'],df['RCA_V'],
            color='slategrey',
            linewidth=0.5,
            label='')
ax.legend()
ax.set_ylabel('RCA value')
ax.set_title('Daily RCA values during CACTI (+1 dBZ bias)')
ax.set_ylim(ylim)
ax.scatter('2018-11-08',0.0,marker='D',linewidth=1,color='b')
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'timeseries_rca_hv_err.png')