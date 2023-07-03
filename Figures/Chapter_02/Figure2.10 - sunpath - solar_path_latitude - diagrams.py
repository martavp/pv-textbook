# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.10 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pvlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MultipleLocator

plt.style.use('../pv-textbook.mplstyle')

color_dec = 'C0'
color_mar = 'C1'
color_jun = 'C2'

list_dates_plot = ['2019-06-21', '2019-03-21', '2019-12-21']

fig = plt.figure(figsize=(8, 8), constrained_layout=True)
spec = fig.add_gridspec(nrows=3, ncols=1)

ax_tropic = fig.add_subplot(spec[0, 0])
ax_midlat = fig.add_subplot(spec[1, 0])
ax_higlat = fig.add_subplot(spec[2, 0])

def plot_cartesian_simple(ax, location, times, title):
    for date in pd.to_datetime(list_dates_plot):
        times_day = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min')
        solpos_day = location.get_solarposition(times_day)
        solpos_day = solpos_day.loc[solpos_day['apparent_elevation'] > 0, :]
        label = date.strftime('%Y-%m-%d')
        if date.month == 3:
            color = color_mar
        elif date.month == 6:
            color = color_jun
        elif date.month == 12:
            color = color_dec
        ax.plot(180 - solpos_day.azimuth, solpos_day.apparent_elevation, color=color, label=label, marker='.', linewidth=0) # linewidth=0 to avoid joining last dots
        
    ax.xaxis.set_major_locator(MultipleLocator(90))
    ax.xaxis.set_major_formatter(EngFormatter(unit="°", sep=''))
    ax.yaxis.set_major_formatter(EngFormatter(unit="°", sep=''))
    ax.set_ylim([0, 90])
    ax.set_xlim([-180, 180])
    ax.set_title(title)

    for letter, position in zip(['N', 'E', 'S', 'W', 'N'], [-180, -90, 0, 90, 180]) :
        ax.annotate(letter, xy=(position, 4),  xycoords='data', fontsize=14, horizontalalignment='center', verticalalignment='center')
       
#%%
tropics = pvlib.location.Location(latitude=15, longitude=0)
mid = pvlib.location.Location(latitude=45, longitude=0)
high = pvlib.location.Location(latitude=80, longitude=0)
times_sunpath = pd.date_range('2019-01-01 00:00:00', '2020-01-01', inclusive='left', freq='H')

plot_cartesian_simple(ax_tropic, tropics, times_sunpath, 'Tropics')
plot_cartesian_simple(ax_midlat, mid, times_sunpath, 'Midlatitudes')
plot_cartesian_simple(ax_higlat, high, times_sunpath, 'High latitudes')

ax_midlat.annotate('Summer solstice', (85, 75), color='C2', fontsize=18)
ax_midlat.annotate('Equinoxes', (85, 63), color='C1', fontsize=18)
ax_midlat.annotate('Winter solstice', (85, 51), color='C0', fontsize=18)

plt.savefig('Figure2.10 - sunpath - solar_path_latitude - diagrams.svg', dpi=300)