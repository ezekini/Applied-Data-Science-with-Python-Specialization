#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
#
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
#
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
#
# Each row in the assignment datafile corresponds to a single observation.
#
# The following variables are provided to you:
#
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
#
# For this assignment, you must:
#
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
#
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.


# import matplotlib.pyplot as plt
# import mplleaflet
# import pandas as pd


# def leaflet_plot_stations(binsize, hashid):

#     df = pd.read_csv('BinSize_d{}.csv'.format(binsize))

#     station_locations_by_hash = df[df['hash'] == hashid]

#     lons = station_locations_by_hash['LONGITUDE'].tolist()
#     lats = station_locations_by_hash['LATITUDE'].tolist()

#     plt.figure(figsize=(8, 8))

#     plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

#     return mplleaflet.display()


# leaflet_plot_stations(400, 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


get_ipython().run_line_magic('matplotlib', 'inline')
#%matplotlib notebook

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import matplotlib.ticker as ticker


# Default fig size para plt
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 12
fig_size[1] = 6
plt.rcParams["figure.figsize"] = fig_size


df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')


# Create useful? columns

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month_Day'] = df['Date'].dt.strftime('%m-%d')


# Drop all 29th feb

#df.drop(index=list(df[df['Month_Day'] == '02-29'].index), inplace=True)
df = df[df['Month_Day'] != '02-29']


df['Data_Value'] = df['Data_Value'] / 10


# Filter the data to the 2005-2014 range, get TMAX & TMIN, and then max/min() for each day

max_temp = df[(df['Year'] >= 2005) & (df['Year'] < 2015) & (
    df['Element'] == 'TMAX')].groupby(['Month_Day'])['Data_Value'].max()

min_temp = df[(df['Year'] >= 2005) & (df['Year'] < 2015) & (
    df['Element'] == 'TMIN')].groupby(['Month_Day'])['Data_Value'].min()

max_temp_2015 = df[(df['Year'] == 2015) & (df['Element'] == 'TMAX')].groupby(
    ['Month_Day'])['Data_Value'].max()

min_temp_2015 = df[(df['Year'] == 2015) & (df['Element'] == 'TMIN')].groupby(
    ['Month_Day'])['Data_Value'].min()


record_high = max_temp.loc[max_temp < max_temp_2015]
record_low = min_temp.loc[min_temp > min_temp_2015]


record_high = record_high.reindex_like(min_temp_2015)
record_low = record_low.reindex_like(min_temp_2015)

# 1 year day index
date_idx = np.arange('2015-01-01', '2016-01-01', dtype='datetime64[D]')


# In[320]:


plt.figure()
# Color palette generated in https://medialab.github.io/iwanthue/
# Max and min temps
plt.plot(date_idx, max_temp, color='#a0d186', linewidth=1.8)
plt.plot(date_idx, min_temp, color='#018f7f', linewidth=1.8)
# 2015 records
plt.scatter(date_idx, record_high, color='#6737e3', s=40)
plt.scatter(date_idx, record_low, color='#ff4487', s=40)

# Additional elemements
ax = plt.gca()
ax.fill_between(date_idx, max_temp, min_temp, facecolor='#f1c0b5', alpha=0.18)
ax.axis(['2015/01/01', '2015/12/31', -50, 50])


plt.title('Daily historical Max/Min temperature in Ann Arbour, Michigan (2005-2014)', fontsize=14)
# Legend and title
plt.legend(['Max temperature (2005-2014)', 'Min temperature (2005-2014)',
            '2015 days MAX temperature > 2005-2014', '2015 days MIN temperature < 2005-2014'], loc='best', frameon=False)


# Set axis names and title:
plt.xlabel('Month', fontsize=15)
plt.ylabel('° Celsius', fontsize=15)


# Location of minor and major ticks:
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))


# Ticks
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
ax.tick_params(axis='x', which='minor', labelsize=13)
ax.tick_params(axis='y', direction='inout', length=6, width=2, color='grey', labelsize=13)

# Hide the right and top spines
ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

# for tick in ax.xaxis.get_minor_ticks():
#    tick.tick1line.set_markersize(0) # Make small ticker disappear
#    tick.label1.set_horizontalalignment('center')

# plt.savefig('foo.pdf')
