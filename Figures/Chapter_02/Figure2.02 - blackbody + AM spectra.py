# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.02 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import constants

plt.style.use('../pv-textbook.mplstyle')

h = constants.h # 6.626e-34 [J·s]
c = constants.speed_of_light # 3.0e+8 [m/s]
k_B = constants.Boltzmann # 1.38e-23 [J/K]
π = constants.pi # 3.141592

R_Sun = 695e6 # Sun's radius [m]
r_Sun_Earth = 149e9 # distance Earth-Sun [m]
solid_angle_Sun = (π * R_Sun**2) / r_Sun_Earth**2 # Area / distance**2

VISIBLE_RANGE = (350, 850) # [nm]
HEIGHT_VISIBLE = 0.05 # [W/m2/nm]
MAX_LEVEL = 2.2 # [W/m2/nm]
WV_INI = 100 # [nm]
WV_MAX = 3000 # [nm]

def solar_spectral_emittance(λ, T):
    planck_law_radiance = 2 * h * c**2 / (λ**5) * 1 / (np.exp(h*c/((λ)*k_B*T)) - 1)
    
    return planck_law_radiance * solid_angle_Sun * 1e-9 # [W/m2/nm]

wavelengths = np.linspace(start=WV_INI, stop=WV_MAX, num=1000)

fig, ax1 = plt.subplots(figsize=(8, 6))

#%% BLACKBODY EMITTER
ax1.plot(wavelengths, solar_spectral_emittance(λ=wavelengths*1e-9, T=4000), linewidth=1)
ax1.plot(wavelengths, solar_spectral_emittance(λ=wavelengths*1e-9, T=5000), linewidth=1)
ax1.plot(wavelengths, solar_spectral_emittance(λ=wavelengths*1e-9, T=5780), linewidth=1)

ax1.legend(['4000 K','5000 K', '5780 K'])

ax1.set_xlim([WV_INI, WV_MAX])
ax1.set_ylim([0, MAX_LEVEL])

ax1.yaxis.set_ticks(np.arange(0, MAX_LEVEL, 0.5))

ax1.set_xlabel("Wavelength ($\lambda$) [$nm$]")
ax1.set_ylabel("Spectral irradiance [$W·m^{-2}·nm^{-1}]$")

#%% ax2 - VISIBLE RANGE
y = np.linspace(start=0, stop=1, num=100)
extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))
X = np.array([wavelengths]*100)

# [x0, y0, width, height]
ax2 = ax1.inset_axes([VISIBLE_RANGE[0], 0, VISIBLE_RANGE[1]-VISIBLE_RANGE[0], HEIGHT_VISIBLE], transform=ax1.transData)
ax2.imshow(X, extent=extent, cmap='nipy_spectral', aspect='auto', alpha=0.5)
ax2.axis('off')

#%% ax3 - AM0&1.5 SPECTRA
ax3 = ax1.twinx()

def interp_df(df, new_index, limit=None):
    index_joined = df.index.join(new_index, how='outer')
    return df.reindex(index=index_joined).interpolate(limit=limit).reindex(new_index)

astmg173 = interp_df(pd.read_csv('data/spectra_astmg173.csv', skiprows=1, index_col='Wvlgth nm'), wavelengths)

am0 = astmg173['Etr W*m-2*nm-1']
am0.plot(ax=ax3, color='C3', alpha=0.8, linewidth=3)

am15g = astmg173['Global tilt  W*m-2*nm-1']
am15g.plot(ax=ax3, color='C4', alpha=0.8, linewidth=3)

ax3.set_ylim([0, MAX_LEVEL])
ax3.legend(['AM0', 'AM1.5G'], bbox_to_anchor=(1, 0.7))
ax3.axis('off')

plt.savefig('Figure2.02 - blackbody + AM spectra.jpg', dpi=300, bbox_inches='tight')