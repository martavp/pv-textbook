# -*- coding: utf-8 -*-
"""
Code that generates the Figure of the solution of Problem 11.05 of the chapter "11. Integrated Photovoltaics" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pvlib

plt.style.use('../pv-textbook.mplstyle')

lat, lon = 40.65, -4.69  # Ávila (Spain)

times = pd.date_range('2019-06-21', '2019-06-22', inclusive='left', freq='1H')

irradiance = pvlib.location.Location(lat, lon).get_clearsky(times)
irradiance = irradiance.rename(columns={"ghi": "G(0)", 'dni':'B', "dhi": "D(0)"})

irradiance['B(0)'] = irradiance['G(0)'] - irradiance['D(0)']

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8), sharey=True, tight_layout=True)

irradiance[['B(0)', 'D(0)']].plot(ax=ax, kind='bar', stacked=True, zorder=2)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%x%X'))
ax.set_xticklabels([x for x in range(24)])
ax.xaxis.set_tick_params(rotation=0)
ax.xaxis.set_tick_params(which='minor', bottom=False)

ax.locator_params(axis='y', nbins=10)

ax.set_ylabel('Solar Irradiance [$W·m^{-2}]$')

ax.grid(visible=True, which='minor', axis='y', color='gray', linestyle=':', linewidth=0.5)
ax.minorticks_on()
ax.grid(visible=True, which='major', axis='y', color='black', linestyle='-', linewidth=1)

plt.savefig('Figure11.16 - Problem 11.05.jpg', dpi=300, bbox_inches='tight')

print(irradiance[['G(0)', 'B(0)', 'D(0)']])

irradiation_day = irradiance['G(0)'].sum() / 1000  # kWh
print(f'G(0) Daily Irradiation={irradiation_day:.3} kWh')