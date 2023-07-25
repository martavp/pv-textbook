# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.19 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import requests
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
import pvlib
import datetime as dt

plt.style.use('../pv-textbook.mplstyle')

lat, lon = -15.42, 28.28 # Lusaka (Zambia)

params = {'lat': lat, 'lon': lon, 'browser': 1, 'outputformat': 'csv'}

series_calc_file = Path('data/Figure2.19 - tmy_generation_seriescalc.csv')
if not series_calc_file.exists():
    resp_seriescalc = requests.get('https://re.jrc.ec.europa.eu/api/v5_2/seriescalc', params=params)
    with open(series_calc_file, 'wb') as f:
        f.write(resp_seriescalc.content)

tmy_file = Path('data/Figure2.19 - tmy_generation_year.csv')
if not tmy_file.exists():
    resp_tmy = requests.get('https://re.jrc.ec.europa.eu/api/v5_2/tmy', params=params)
    with open(tmy_file, 'wb') as f:
        f.write(resp_tmy.content)

#%%
tmy, m, _,_ = pvlib.iotools.read_pvgis_tmy(tmy_file, map_variables=True)

tmy_months = {k:v for k,v in [(mes['month'], mes['year']) for mes in m]}

#%%
series_calc = pd.read_csv(series_calc_file, skiprows=8, index_col='time', skipfooter=10, 
                          parse_dates=True, infer_datetime_format=True, date_parser=lambda x: dt.datetime.strptime(x, '%Y%m%d:%H%M'))

series_calc = series_calc.rename({'G(i)': 'ghi'}, axis='columns')
series_calc['hour'] = series_calc.index.hour
series_calc['date'] = series_calc.index.date
series_calc['year'] = series_calc.index.year

#%%
unique_years = sorted(list(set(tmy_months.values())))

fig = plt.figure(figsize=(8, 6))
spec = fig.add_gridspec(nrows=2, ncols=len(unique_years)+1)

fig.subplots_adjust(hspace=2)

tmy = tmy.set_index(tmy.index.map(lambda t: t.replace(year=2022)))

tmy['hour'] = tmy.index.hour
tmy['date'] = tmy.index.date

ax_tmy = fig.add_subplot(spec[1,:])
im = ax_tmy.pcolormesh(tmy.pivot_table('ghi', 'hour', 'date', fill_value=0))
ax_tmy.axis('off')

for num_month, year_series_calc in enumerate(unique_years):
    ax_year = fig.add_subplot(spec[0, num_month+1])
    ax_year.pcolormesh(series_calc[series_calc['year'] == year_series_calc].pivot_table('ghi', 'hour', 'date', fill_value=0))
    ax_year.axis('off')
    
    label_months = ''
    for month_tmy_year in [month for month, year in tmy_months.items() if year == year_series_calc]:
        color = f'C{num_month}' # iterate list of colors using Cx notation

        ax_year.add_patch(Rectangle(xy=(30*(month_tmy_year-1), 0.5), width=25, height=23.3, facecolor='none', edgecolor=color, hatch='', linewidth=2, alpha=1))
        label_months += str(month_tmy_year)+' '
        ax_year.text(x=0.18, y=0.05, s=year_series_calc, color='white', transform=ax_year.transAxes, fontsize=14)
        
        ax_tmy.add_patch(Rectangle(xy=(30.417*(month_tmy_year-1), 0.5), width=29.7, height=23.3, facecolor='none', edgecolor=color, hatch='', linewidth=2, alpha=1))
        ax_tmy.text(x=30.417*(month_tmy_year-1)+7, y=1, s=dt.date(year=2010, month=month_tmy_year, day=1).strftime('%b'), color='white', fontsize=14)
        
        con = ConnectionPatch(xyA=(30.417*(month_tmy_year-1)+15, 0), xyB=(month_tmy_year/12-(1/24), 1), coordsA="data", coordsB="axes fraction",
                      axesA=ax_year, axesB=ax_tmy, color='gray', arrowstyle="->")
        ax_year.add_artist(con)

ax_legend = fig.add_subplot(spec[0, 0]) #fig.add_axes([0.26, 0.43, 0.07, 0.22]) # [left, bottom, width, height]
ax_legend.pcolormesh(tmy.pivot_table('ghi', 'hour', 'date', fill_value=0), cmap='Greys')
ax_legend.set_xlabel('Day of the year', fontsize=12)
ax_legend.set_ylabel('Hour of the day', fontsize=12)
ax_legend.tick_params(axis='x', labelsize=12)
ax_legend.tick_params(axis='y', labelsize=12)

cbar_ax = fig.add_axes([0.91, 0.115, 0.015, 0.765])
cb = fig.colorbar(im, cax=cbar_ax)
cb.set_label(label='Global Irradiance [$W·m^{-2}]$', size=16)
cb.ax.tick_params(labelsize=16)

plt.savefig('Figure2.19 - tmy_generation.jpg', bbox_inches='tight', dpi=300)