# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.18a of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pandas as pd
import pvlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.style.use('../pv-textbook.mplstyle')

lat, lon = 43.61, -3.88  # Montpellier (France)

times = pd.date_range('2019-03-21 04:00', '2019-03-22', inclusive='left', freq='5min')

solpos = pvlib.solarposition.get_solarposition(times, lat, lon)

tracking_angles = pvlib.tracking.singleaxis(
    apparent_zenith=solpos['apparent_zenith'],
    apparent_azimuth=solpos['azimuth'],
    axis_tilt=0,
    axis_azimuth=180,
    max_angle=90,
    backtrack=False,
    gcr=0.5)

irradiance = pvlib.location.Location(lat, lon).get_clearsky(times)

tracking_2ax = pvlib.irradiance.get_total_irradiance(
    surface_tilt=solpos['apparent_zenith'], surface_azimuth=solpos['azimuth'], solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=irradiance.dni, ghi=irradiance.ghi, dhi=irradiance.dhi)

tracking_1ax = pvlib.irradiance.get_total_irradiance(
    surface_tilt=tracking_angles['surface_tilt'], surface_azimuth=tracking_angles['surface_azimuth'], solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=irradiance.dni, ghi=irradiance.ghi, dhi=irradiance.dhi)

fixed = pvlib.irradiance.get_total_irradiance(
    surface_tilt=30, surface_azimuth=180, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=irradiance.dni, ghi=irradiance.ghi, dhi=irradiance.dhi)

fixed_W = pvlib.irradiance.get_total_irradiance(
    surface_tilt=60, surface_azimuth=270, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=irradiance.dni, ghi=irradiance.ghi, dhi=irradiance.dhi)

fixed_E = pvlib.irradiance.get_total_irradiance(
    surface_tilt=60, surface_azimuth=90, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=irradiance.dni, ghi=irradiance.ghi, dhi=irradiance.dhi)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), sharey=True, squeeze=True)

tracking_1ax.poa_global.plot(ax=ax, label='NS horizontal\n1 axis tracking', linewidth=3, x_compat=True)
print(f'tracking_1ax={tracking_1ax.poa_global.sum() /60 /1000:.2f} kWh')

tracking_2ax.poa_global.plot(ax=ax, label='2 axis tracking', linewidth=3, x_compat=True)
print(f'tracking_2ax={tracking_2ax.poa_global.sum() /60 /1000:.2f} kWh')

fixed.poa_global.plot(ax=ax, label='Fixed [30°]', linewidth=3, x_compat=True)
print(f'fixed={fixed.poa_global.sum() /60 /1000:.2f} kWh')

fixed_EW = pd.DataFrame([fixed_W.poa_global, fixed_E.poa_global]).sum()
fixed_EW.plot(ax=ax, label='Fixed - Delta [60°]', linewidth=3, x_compat=True)
print(f'fixed_EW={fixed_EW.sum() /60 /1000:.2f} kWh')

ax.set_ylabel('Global Irradiance [$W·m^{-2}$]')
ax.set_ylim([0, 1100])

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Hh'))
ax.xaxis.set_tick_params(rotation=0)

ax.legend(fontsize=14, loc='upper right')

plt.savefig('Figure2.18a - tracking_day_irradiation.svg', dpi=300, bbox_inches='tight')