# -*- coding: utf-8 -*-
"""
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import requests
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pvlib

plt.style.use('../pv-textbook.mplstyle')

lat, lon = 40.41, -3.70  # Madrid (Spain)

params = {'lat': lat, 'lon': lon, 'browser': 1, 'outputformat': 'csv'}

tmy_file = Path('data/kt_kd_tmy_year.csv')
if not tmy_file.exists():
    resp_tmy = requests.get(
        'https://re.jrc.ec.europa.eu/api/v5_2/tmy', params=params)
    with open(tmy_file, 'wb') as f:
        f.write(resp_tmy.content)

# %%
tmy, m, _, _ = pvlib.iotools.read_pvgis_tmy(tmy_file, map_variables=True)
tmy = tmy.set_index(tmy.index.map(lambda t: t.replace(year=2022)))

tmy['kd'] = tmy.dhi / tmy.ghi

dn = tmy.index.day_of_year

def cosd(degrees): return np.cos(np.deg2rad(degrees))

# eccentricity
ε = 1 + 0.033*cosd(360/365 * dn)

tmy['zenith'] = pvlib.location.Location(
    latitude=40, longitude=0).get_solarposition(tmy.index).zenith

B0 = 1366 * ε * cosd(tmy.zenith)

tmy['kt'] = tmy.ghi / B0
tmy['kd'] = tmy.dhi / tmy.ghi


def f_demiguel(kt):
    # Defined as a piecewise function so it can be vectorized
    conds = [kt <= 0.21,
             (0.21 < kt) & (kt <= 0.76),
             0.76 < kt]
    kd = [lambda kt: 0.995 - 0.081*kt,
             lambda kt: 0.724 + 2.738 * kt - 8.32*kt**2 + 4.967*kt**3,
             0.177]
    return np.piecewise(kt, conds, kd)

def f_page(kt):
    kd = 1 - 1.13 * kt
    return kd


# %%
tmy_filt = tmy.query('0<kt<1')
kt_model = np.arange(start=0, step=0.1, stop=0.9)

fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(tmy_filt.kt, tmy_filt.kd, '.', label='Hourly data')
ax.plot(kt_model, f_demiguel(kt_model), '-', label='De Miguel model', linewidth=3)
ax.plot(kt_model, f_page(kt_model), '-', label='Page model', linewidth=3)

ax.legend(loc="upper right")
ax.set_xlabel('Clearness index ($k_T$)')
ax.set_ylabel('Diffuse fraction ($k_D$)')

plt.savefig('kt_kd.png', dpi=300)