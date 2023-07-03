# -*- coding: utf-8 -*-
"""
Code that generates Figure 11.11 of the chapter "11. Integrated Photovoltaics" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, cm, colors

plt.style.use('../pv-textbook.mplstyle')

ev_dict = {
    'Cev': {0: 24.0, 1: 21.5, 2: 16.0, 3: 13.8, 4: 23.5, 5: 20.0, 6: 16.0, 7: 14.0, 8: 13.1, 9: 17.7},
    'A': {0: 2.3, 1: 2.2, 2: 2.0, 3: 2.2, 4: 2.1, 5: 1.8, 6: 2.5, 7: 1.9, 8: 1.9, 9: 1.7},
    'power': {0: 690.0, 1: 660.0, 2: 600.0, 3: 660.0, 4: 630.0, 5: 540.0, 6: 750.0, 7: 570.0, 8: 570.0, 9: 510.0},
    'km_day': {0: 10.695, 1: 11.419, 2: 13.950, 3: 17.791, 4: 9.972, 5: 10.044, 6: 17.437, 7: 15.145, 8: 16.186, 9: 10.718},
    'eff': {0: 30, 1: 30, 2: 30, 3: 30, 4: 30, 5: 30, 6: 30, 7: 30, 8: 30, 9: 30}
}

ev_df = pd.DataFrame(ev_dict)

G = 4.65  # kWh/m2/day = 1700 kWh/m2/year
EFF = 30  # %
PR = 0.80
CAR_ROOF = 1.8  # m2

AREA_MIN = 1
AREA_MAX = 4
CEV_MIN = 10
CEV_MAX = 30
POWER_MAX = 600
POWER_MIN = 200
EFF_MIN = 10
EFF_MAX = 50
KM_DAY_MAX = 25
KM_DAY_MIN = 5


def f_km_day(A, Cev):
    return G * (EFF / 100) * A / (Cev / 100) * PR


def f_power(A, eff):
    return 1000 * (eff / 100) * A


ev_df['power'] = f_power(ev_df['A'], EFF)
ev_df['km_day'] = ev_df.apply(
    lambda x: f_km_day(x['A'], x['Cev']), axis='columns')
ev_df['eff'] = EFF

fig, (ax_sr, ax_cap) = plt.subplots(nrows=1, ncols=2,
                                    sharey=True, tight_layout=True, figsize=(12, 8))

# SOLAR RANGE

# scatter
cmap_orange = colors.LinearSegmentedColormap.from_list("mycmap", cm.Oranges(np.linspace(0.3, 1, 256)))

g = ax_sr.scatter(x=ev_df['Cev'], y=ev_df['A'], c=ev_df['km_day'], s=ev_df['km_day']*80,
                  marker='o', cmap=cmap_orange, vmax=KM_DAY_MAX, vmin=KM_DAY_MIN)

# cb = fig.colorbar(g)
# cb.set_label('km/day')

ax_sr.set_xscale("log")
ax_sr.xaxis.set_minor_formatter(ticker.ScalarFormatter())
ax_sr.xaxis.set_major_formatter(ticker.ScalarFormatter())

# contour
X, Y = np.meshgrid(np.linspace(AREA_MIN, AREA_MAX, num=50),
                   np.linspace(CEV_MIN, CEV_MAX, num=50))

cs = ax_sr.contour(Y, X, f_km_day(X, Y), levels=5, cmap=cmap_orange, vmax=KM_DAY_MAX,
                   vmin=KM_DAY_MIN, linestyles='--')
ax_sr.clabel(cs, cs.levels, fontsize=24, fmt="%d km/day", colors='gray')

ax_sr.axhline(y=CAR_ROOF, linestyle=':', color='black')
ax_sr.text(x=CEV_MIN+1, y=CAR_ROOF-0.15,
           s='Roof only', color='black', fontsize=24)

ax_sr.set_xlabel('$C_{EV}$ Consumption $[kWh/100km]$', fontsize=24)
ax_sr.set_xlim([CEV_MIN, CEV_MAX])
ax_sr.set_ylabel('PV area $[m^{2}]$', fontsize=24)
ax_sr.set_ylim([AREA_MIN, AREA_MAX])

ax_sr.tick_params(axis='both', labelsize=20)

# INSTALLED CAPACITY

# scatter
cmap_blues = colors.LinearSegmentedColormap.from_list("mycmap", cm.Blues(np.linspace(0.3, 1, 256)))

g = ax_cap.scatter(x=ev_df['eff'], y=ev_df['A'], c=ev_df['power'], s=ev_df['power'],
                   marker='o', cmap=cmap_blues, vmax=POWER_MAX, vmin=POWER_MIN)

# contour
X, Y = np.meshgrid(np.linspace(AREA_MIN, AREA_MAX, num=50),
                   np.linspace(EFF_MIN, EFF_MAX, num=50))
cs = ax_cap.contour(Y, X, f_power(X, Y), levels=7, cmap=cmap_blues, vmax=POWER_MAX,
                    vmin=POWER_MIN, linestyles='--', size=15)

ax_cap.clabel(cs, cs.levels, fontsize=24, fmt="%d W", colors='gray')

ax_cap.axhline(y=CAR_ROOF, linestyle=':', color='black')
# ax_cap.text(x=EFF_MIN+33, y=CAR_ROOF-0.15, s='Roof only', color='black', fontsize=24)

ax_cap.set_xlabel('Module efficiency $[\%]$', fontsize=24)
ax_cap.set_xlim([EFF_MIN, EFF_MAX])
# ax_cap.set_ylabel('PV area $[m^{2}]$', fontsize=24)
# ax_cap.set_ylim([AREA_MIN, AREA_MAX])

ax_cap.tick_params(axis='both', labelsize=20)

plt.savefig('Figure11.11 - solar_range_inst_capacity.jpg',
            dpi=300, bbox_inches='tight')
