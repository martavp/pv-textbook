# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.06 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('../pv-textbook.mplstyle')

meteo_day = pd.read_csv('data/IES-UPM meteo - 2022_07_17.txt',
                        parse_dates=[0], index_col=0, delimiter='\t')
# filters night negative values due to pyranometer zero-offset
meteo_day = meteo_day.query('Gh > 0')

meteo_day['Bh'] = meteo_day['Gh'] - meteo_day['Dh']

irradiation_day = meteo_day.Gh.sum() / 60 / 1000  # kWh

meteo_day['hsp'] = 0

center_moment = pd.Timedelta(hours=irradiation_day/2)
meteo_day.loc[(meteo_day.index > meteo_day.index.mean() - center_moment) &
              (meteo_day.index < meteo_day.index.mean() + center_moment), 'hsp'] = 1000

print(f'G(0) Daily Irradiation={irradiation_day:.3} kWh')
print(f'PSH={(2*center_moment).components.hours}h{(2*center_moment).components.minutes}m')

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 8), sharey=True)
plt.subplots_adjust(wspace=0.05)

meteo_day[['Bn', 'Gh', 'Dh', 'Bh']].plot(ax=ax1, x_compat=True)
ax1.set_ylim([0, 1100])
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax1.xaxis.set_tick_params(rotation=0)
ax1.set_xlabel('')
ax1.set_ylabel('Solar Irradiance [$W·m^{-2}]$')
ax1.axhline(y=1000, color='black', linestyle='--')
ax1.annotate('Standard Irradiance Level',
             (meteo_day.index[0], 1010), fontsize=14)
ax1.legend(['B', 'G(0)', 'D(0)', 'B(0)'], loc=[0.37, 0.25])

ax2.fill_between(meteo_day.index, meteo_day.Gh,
                 label='Daily Global Irradiance')
ax2.fill_between(meteo_day.index, meteo_day['hsp'],
                 alpha=0.5, label='Peak Sun Hours')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax2.axhline(y=1000, color='black', linestyle='--')
ax2.annotate('', xy=(pd.Timestamp('2022-07-17 10:15'), 370),
             xytext=(pd.Timestamp('2022-07-17 11:00'), 470),
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3, rad=1"),
             fontsize=12)
ax2.annotate('Same area', xy=(pd.Timestamp(
    '2022-07-17 06:30'), 465), fontsize=14)

ax2.legend(loc=(0.3, 0.5))

plt.savefig('Figure2.06 - PSH.jpg', dpi=300, bbox_inches='tight')