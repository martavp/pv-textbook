# -*- coding: utf-8 -*-
"""
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pandas as pd
import pvlib
import matplotlib.pyplot as plt

plt.style.use('../pv-textbook.mplstyle')

lat, lon = 43.61, -3.88  # Montpellier (France)

times = pd.date_range('2019-03-21', '2019-03-22', inclusive='left', freq='5min')

solpos = pvlib.solarposition.get_solarposition(times, lat, lon)

tracking_angles = pvlib.tracking.singleaxis(
    apparent_zenith=solpos['apparent_zenith'],
    apparent_azimuth=solpos['azimuth'],
    axis_tilt=0,
    axis_azimuth=180,
    max_angle=90,
    backtrack=False,
    gcr=0.5)

weather = pvlib.location.Location(lat, lon).get_clearsky(times)

tracking_2ax = pvlib.irradiance.get_total_irradiance(
    surface_tilt=solpos['apparent_zenith'], surface_azimuth=solpos['azimuth'], solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=weather.dni, ghi=weather.ghi, dhi=weather.dhi)

tracking_1ax = pvlib.irradiance.get_total_irradiance(
    surface_tilt=tracking_angles['surface_tilt'], surface_azimuth=tracking_angles['surface_azimuth'], solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=weather.dni, ghi=weather.ghi, dhi=weather.dhi)

fixed = pvlib.irradiance.get_total_irradiance(
    surface_tilt=30, surface_azimuth=180, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=weather.dni, ghi=weather.ghi, dhi=weather.dhi)

fixed_W = pvlib.irradiance.get_total_irradiance(
    surface_tilt=60, surface_azimuth=270, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=weather.dni, ghi=weather.ghi, dhi=weather.dhi)

fixed_E = pvlib.irradiance.get_total_irradiance(
    surface_tilt=60, surface_azimuth=90, solar_zenith=solpos['apparent_zenith'], solar_azimuth=solpos['azimuth'], dni=weather.dni, ghi=weather.ghi, dhi=weather.dhi)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8), sharey=True, squeeze=True)

tracking_1ax.poa_global.plot(label='NS horizontal\n1 axis tracking', linewidth=3)
print(f'tracking_1ax={tracking_1ax.poa_global.sum() /60 /1000:.2f} kWh')

tracking_2ax.poa_global.plot(label='2 axis tracking', linewidth=3)
print(f'tracking_2ax={tracking_2ax.poa_global.sum() /60 /1000:.2f} kWh')

fixed.poa_global.plot(label='Fixed [30°]', linewidth=3)
print(f'fixed={fixed.poa_global.sum() /60 /1000:.2f} kWh')

fixed_EW = pd.DataFrame([fixed_W.poa_global, fixed_E.poa_global]).mean()
fixed_EW.plot(label='Fixed - Delta [60°]', linewidth=3)
print(f'fixed_EW={fixed_EW.sum() /60 /1000:.2f} kWh')

ax.set_ylabel('Global Irradiance [$W·m^{-2}]$')

ax.legend()

plt.savefig('tracking_day_irradiation.png', dpi=300, bbox_inches='tight')