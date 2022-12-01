# -*- coding: utf-8 -*-
"""
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('../pv-textbook.mplstyle')

days_year = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
dn = days_year.day_of_year

C = (dn - 80) * 360/365

def sind(degrees): return np.sin(np.deg2rad(degrees))
def cosd(degrees): return np.cos(np.deg2rad(degrees))

# eccentricity
eccentricity_effect = -7.53*cosd(C) - 1.5*sind(C)

# declination
δ = 23.45 * sind(C)
declination_effect = 9.87*sind(2*C)

ET = eccentricity_effect + declination_effect

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 6.7))

plt.subplots_adjust(hspace=0)
fig.set_tight_layout(True)

ax1.plot(days_year, ET, label='Equation Time')
ax1.plot(days_year, declination_effect,
         label='Declination (δ) effect', linestyle=':')
ax1.plot(days_year, eccentricity_effect,
         label='Eccentricity (ε) effect', linestyle='--')
ax1.axhline(y=0, linewidth=0.5, color='black', linestyle=':')
ax1.legend(fontsize=10)
ax1.set_ylabel("Equation of Time [minutes]", fontsize=14)
ax1.set_xlabel("Day of the Year", fontsize=14)

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%j\n[%b %d]'))
ax1.tick_params(axis="x", labelsize=8)
ax1.grid()

im = ax2.scatter(δ, ET, c=dn, s=5, cmap='twilight')

for d in [0, 80, 172, 262, 354]:
    ax1.scatter(days_year[d], ET[d], c='black', marker='o')
    ax2.scatter(δ[d], ET[d], c='black', marker='v')

    ax1.annotate(days_year[d].strftime('%j\n[%b %d]'), xy=(
        days_year[d], ET[d]),  xycoords='data', xytext=(0, 0), 
        textcoords='offset points', fontsize=8)
    
    xytext = (-10, -10) if d == 172 else (10, -10)
    horizontalalignment = 'right' if d == 172 else 'left'
    
    ax2.annotate(days_year[d].strftime('%j\n[%b %d]'), xy=(
        δ[d], ET[d]),  xycoords='data', xytext=xytext, 
        textcoords='offset points', fontsize=8, 
        horizontalalignment=horizontalalignment)

ax2.axhline(y=0, linewidth=0.5, color='black', linestyle=':')
ax2.axvline(x=0, linewidth=0.5, color='black', linestyle=':')
ax2.tick_params(direction='in')
ax2.set_ylabel("Equation of Time [minutes]", fontsize=14)
ax2.set_xlabel("Declination (δ) [$\degree$]", fontsize=14)

cbar = fig.colorbar(im, ax=ax2, fraction=0.05, aspect=40)
cbar.set_label(label='Day of the year', fontsize=14)
cbar.ax.yaxis.set_major_formatter(mdates.DateFormatter('%j [%b %d]'))
cbar.ax.tick_params(labelsize=8)

plt.savefig('equation_time.png', dpi=300)