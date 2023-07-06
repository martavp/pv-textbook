# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.09 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, FixedFormatter, FixedLocator
import numpy as np

plt.style.use('../pv-textbook.mplstyle')

color_dec = 'C0'
color_mar = 'C1'
color_jun = 'C2'
color_analemma = 'C6'

list_dates_plot = ['2019-03-21', '2019-06-21', '2019-12-21']

# adapted from https://pvlib-python.readthedocs.io/en/stable/gallery/solar-position/plot_sunpath_diagrams.html
def plot_cartesian(ax, location, times):
    solpos = location.get_solarposition(times)
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :] # remove nighttime
    
    # draw the analemma loops
    ax.scatter(solpos.azimuth, solpos.apparent_elevation, s=0.1, marker= '.', 
                    color=color_analemma, label=None)

    for hour in np.unique(solpos.index.hour):
        # choose label position by the largest elevation for each hour
        subset = solpos.loc[solpos.index.hour == hour, :]
        height = subset['apparent_elevation']
        pos = solpos.loc[height.idxmax(), :]
        if hour > 12:
            ha = 'right'
        else:
            ha = 'left'
        ax.text(pos['azimuth'], pos['apparent_elevation'], str(hour)+'h', size=12, horizontalalignment=ha) # hour in summer includes DST
    
    for date in pd.to_datetime(list_dates_plot):
        times_day = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=location.tz)
        solpos_day = location.get_solarposition(times_day)
        solpos_day = solpos_day.loc[solpos_day['apparent_elevation'] > 0, :]
        label = date.strftime('%Y-%m-%d')
        if date.month == 3:
            color = color_mar
        elif date.month == 6:
            color = color_jun
        elif date.month == 12:
            color = color_dec
        ax.plot(solpos_day['azimuth'], solpos_day['apparent_elevation'], color=color, label=label, linewidth=3)
    
    ax.set_ylabel('Solar Elevation [°]', fontsize=16)
    ax.set_xlabel('Solar Azimuth [°]', fontsize=16)
        
    ax.xaxis.set_major_locator(FixedLocator(np.arange(start=0, stop=361, step=45)))
    ax.xaxis.set_major_formatter(FixedFormatter([f"{azi}°" for azi in np.arange(start=-180, stop=181, step=45)]))

    ax.yaxis.set_major_formatter(EngFormatter(unit="°", sep=''))
    ax.set_xlim([0, 360])
    
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    
    ax.set_ylim([0, 91])
    ax.yaxis.set_ticks(np.arange(0, 91, 15))

    ax.grid()

    for letter, position in zip(['N', 'E', 'S', 'W', 'N'], [0, 90, 180, 270, 360]) :
        ax.annotate(letter, xy=(position, 2),  xycoords='data', fontsize=14, horizontalalignment='center', verticalalignment='center')

def plot_polar(ax, location, times):
    solpos = location.get_solarposition(times)
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :] # remove nighttime

    # draw the analemma loops
    ax.scatter(np.radians(180 + solpos['azimuth']), 90 - solpos['apparent_elevation'], s=0.1, marker= '.', 
                    color=color_analemma, label=None)

    for hour in np.unique(solpos.index.hour):
        # choose label position by the largest elevation for each hour
        subset = solpos.loc[solpos.index.hour == hour, :]
        r = 90 - subset['apparent_elevation']
        pos = solpos.loc[r.idxmin(), :]
        if hour < 12:
            ha = 'left'
        elif 12 <= hour < 16:
            ha = 'center'
        else:
            ha = 'right'
        ax.text(np.radians(180 + pos['azimuth']), 90 - pos['apparent_elevation'], str(hour)+'h', size=12, horizontalalignment=ha) # hour in summer includes DST
    
    for date in pd.to_datetime(list_dates_plot):
        times_day = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=location.tz)
        solpos_day = location.get_solarposition(times_day)
        solpos_day = solpos_day.loc[solpos_day['apparent_elevation'] > 0, :]
        label = date.strftime('%Y-%m-%d')
        if date.month == 3:
            color = color_mar
        elif date.month == 6:
            color = color_jun
        elif date.month == 12:
            color = color_dec
        ax.plot(np.radians(180 - solpos_day['azimuth']), 90 - solpos_day['apparent_elevation'], color=color, label=label, linewidth=3)
    
    # change coordinates to be like a compass
    ax.set_theta_zero_location('S')
    ax.set_theta_direction(-1)

    rtick_locs = np.arange(start=0, stop=100, step=15)
    rtick_labels = [f'{r}°' for r in reversed(rtick_locs)]
    ax.set_rgrids(radii=rtick_locs, labels=rtick_labels, fontsize=14)
    
    thetatick_locs = np.arange(start=0, stop=360, step=45)
    thetatick_labels = []
    for theta in thetatick_locs:
        if theta == 180:
            thetatick_labels.append('±180°')
        elif theta > 180:
            thetatick_labels.append(f'{theta - 360}°')
        else:
            thetatick_labels.append(f'{theta}°')
                                         
    ax.set_thetagrids(thetatick_locs, labels=thetatick_labels, fontsize=14)
    ax.tick_params(axis='both', pad=10)

    ax.set_ylabel('Solar Elevation [°]', fontsize=16, rotation=0)
    ax.yaxis.set_label_coords(0.85, 1.01)
    ax.set_rmax(90)
    ax.set_rlabel_position(200)
    
    ax.set_xlabel('Solar Azimuth [°]', fontsize=16)
        
    for letter, position in zip(['N', 'E', 'S', 'W'], [-180, -90, 0, 90]) :
        ax.annotate(letter, xy=(np.radians(position), 85),  xycoords='data', fontsize=16, horizontalalignment='center', verticalalignment='center')
    
#%%
budapest = pvlib.location.Location(latitude=47.49, longitude=19.04, altitude=151, tz='Europe/Budapest')
times_budapest = pd.date_range('2019-01-01 00:00:00', '2020-01-01', inclusive='left', freq='H', tz=budapest.tz)

fig, ax_cartesian = plt.subplots(nrows=1, ncols=1, figsize=(6, 6))
plot_cartesian(ax_cartesian, location=budapest, times=times_budapest)
plt.savefig('Figure2.09 - sunpath_budapest_cartesian.jpg', dpi=300)

fig, ax_polar = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), subplot_kw={'projection': 'polar'})
plot_polar(ax_polar, location=budapest, times=times_budapest)
plt.savefig('Figure2.09 - sunpath_budapest_polar.jpg', dpi=300)
