# -*- coding: utf-8 -*-
"""
Code that generates the Figure of the solution of Problem 2.8 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MultipleLocator

plt.style.use('../pv-textbook.mplstyle')

color_dec = 'C0'
color_mar = 'C1'
color_jun = 'C2'

list_dates_plot = ['2019-06-21', '2019-03-21', '2019-12-21']

location = pvlib.location.Location(
    latitude=25.04, longitude=121, tz='Asia/Taipei')
times = pd.date_range('2019-01-01 00:00:00', '2020-01-01',
                      inclusive='left', freq='H')

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

for date in pd.to_datetime(list_dates_plot):
    times_day = pd.date_range(
        date, date+pd.Timedelta('24h'), freq='1min', tz=location.tz)
    solpos_day = location.get_solarposition(times_day)
    solpos_day = solpos_day.loc[solpos_day['apparent_elevation'] > 0, :]
    label = date.strftime('%Y-%m-%d')
    if date.month == 3:
        color = color_mar
    elif date.month == 6:
        color = color_jun
    elif date.month == 12:
        color = color_dec
    ax.plot(180 - solpos_day.azimuth, solpos_day.apparent_elevation, color=color,
            label=label, marker='.', linewidth=0)  # linewidth=0 to avoid joining last dots

ax.xaxis.set_major_locator(MultipleLocator(90))
ax.xaxis.set_major_formatter(EngFormatter(unit="°", sep=''))
ax.yaxis.set_major_formatter(EngFormatter(unit="°", sep=''))
ax.set_ylim([0, 90])
ax.set_xlim([-180, 180])

ax.set_ylabel('Solar Elevation [°]', fontsize=18)
ax.set_xlabel('Solar Azimuth [°]', fontsize=18, labelpad=9)

for letter, position in zip(['N', 'E', 'S', 'W', 'N'], [-180, -90, 0, 90, 180]):
    ax.annotate(letter, xy=(position, -5),  xycoords='data', fontsize=14,
                horizontalalignment='center', verticalalignment='center', annotation_clip=False)

azimuth_1deg = np.linspace(start=-180, stop=180, num=1441)

solpos_jun = location.get_solarposition(pd.date_range(list_dates_plot[0], pd.to_datetime(
    list_dates_plot[0])+pd.Timedelta('24h'), freq='1min', tz=location.tz))
solpos_jun = solpos_jun[solpos_jun.apparent_elevation > 0]

elevation_jun = np.interp(
    x=azimuth_1deg, xp=solpos_jun.azimuth, fp=solpos_jun.apparent_elevation)

solpos_dec = location.get_solarposition(pd.date_range(list_dates_plot[2], pd.to_datetime(
    list_dates_plot[2])+pd.Timedelta('24h'), freq='1min', tz=location.tz))
solpos_dec = solpos_dec[solpos_dec.apparent_elevation > 0]

elevation_dec = np.interp(
    x=azimuth_1deg, xp=solpos_dec.azimuth, fp=solpos_dec.apparent_elevation)

ax.fill_between(x=180-azimuth_1deg, y1=elevation_jun,
                y2=elevation_dec, alpha=0.5, color='C3')
ax.fill_between(x=azimuth_1deg-180, y1=elevation_jun,
                y2=elevation_dec, alpha=0.5, color='C3')

# pole
pole_height = 2  # m
distance = 2.5  # m
array_width = 5  # m

pole_elevation_center = np.degrees(np.arctan(pole_height / distance))
pole_azimuth_center = 0
ax.plot([pole_azimuth_center, pole_azimuth_center], [
        0, pole_elevation_center], '-', color='black', linewidth=3)

d1 = np.sqrt((array_width / 2)**2 + distance**2)
pole_elevation_corner = np.degrees(np.arctan(pole_height / d1))
pole_azimuth_corner = np.degrees(np.arctan((array_width / 2) / distance))
# ax.plot([-pole_azimuth_corner, -pole_azimuth_corner], [0, pole_elevation_corner], '-', color='black', linewidth=3)
ax.plot([pole_azimuth_corner, pole_azimuth_corner], [
        0, pole_elevation_corner], '-', color='black', linewidth=3)

ax.plot(pole_azimuth_corner, pole_elevation_corner, 'x', color='C1')
ax.annotate('$(\Psi_{pole}, \gamma_{pole})$', xy=(pole_azimuth_corner, pole_elevation_corner+2),  xycoords='data',
            fontsize=16, horizontalalignment='center', verticalalignment='center', color='C1')

plt.savefig('Figure2.20 - Problem 2.08 - solution_sunpath.svg', dpi=300)
