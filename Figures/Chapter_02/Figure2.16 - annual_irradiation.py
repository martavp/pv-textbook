# -*- coding: utf-8 -*-
"""
Code that generates Figure 2.16 of the chapter "2. Solar Radiation" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import requests
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pvlib

plt.style.use('../pv-textbook.mplstyle')

lat, lon = 39.47, -0.37 # Valencia (Spain)

params = {'lat': lat, 'lon': lon, 'browser': 1, 'outputformat': 'csv'}

tmy_file = Path('data/Figure2.16 - annual_irradiation_tmy.csv')
if not tmy_file.exists():
    resp_tmy = requests.get('https://re.jrc.ec.europa.eu/api/v5_2/tmy', params=params)
    with open(tmy_file, 'wb') as f:
        f.write(resp_tmy.content)

tmy, _, _, _ = pvlib.iotools.read_pvgis_tmy(tmy_file, map_variables=True)

tmy = tmy.set_index(tmy.index.map(lambda t: t.replace(year=2022)))

with open(tmy_file, 'r') as f:
    while line := f.readline():
        if 'Elevation' in line:
            altitude = float(line.split()[-1])

location = pvlib.location.Location(latitude=lat, longitude=lon, altitude=altitude)
solar_position = location.get_solarposition(tmy.index)

#%%
def calculate_poa(tmy, surface_tilt, surface_orientation, solar_position):
    irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_orientation,
        dni=tmy['dni'],
        ghi=tmy['ghi'],
        dhi=tmy['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        model='isotropic')
    
    return irradiance['poa_global']

tilt_range = np.arange(start=0, stop=91, step=1)
orientation_range = np.arange(start=0, stop=361, step=1)

r_angles, theta_angles = np.meshgrid(tilt_range, np.radians(orientation_range))

poa_tmy = np.zeros(shape=r_angles.shape)
for i, orientation in enumerate(orientation_range):
    for j, tilt in enumerate(tilt_range):
        poa_tmy[i, j] = calculate_poa(tmy, surface_tilt=tilt, surface_orientation=180 - orientation, solar_position=solar_position).sum()

#%%
print(f"Annual irradiation={poa_tmy.max()/1000:.0f} kWh/m2")

fig = plt.figure(figsize=(14, 8))
spec = fig.add_gridspec(nrows=1, ncols=1, right=0.5)

ax_polar = fig.add_subplot(spec[0,0], polar=True)
im = ax_polar.contourf(theta_angles, r_angles, poa_tmy / poa_tmy.max() * 100, levels=30, cmap='jet', alpha=0.7)
ax_polar.set_theta_zero_location('S')

ax_polar.set_theta_zero_location('S')
ax_polar.set_theta_direction(-1)

# radius
rtick_locs = np.arange(start=0, stop=100, step=20)
rtick_labels = [f'{r}°' for r in rtick_locs]
ax_polar.set_rgrids(rtick_locs, labels=rtick_labels, fontsize=16)

# orientation
thetatick_locs = np.arange(start=0, stop=360, step=45)
thetatick_labels = []
for theta in thetatick_locs:
    if theta == 180:
        thetatick_labels.append('±180°')
    elif theta > 180:
        thetatick_labels.append(f'{theta - 360}°')
    else:
        thetatick_labels.append(f'{theta}°')

ax_polar.set_thetagrids(thetatick_locs, labels=thetatick_labels, fontsize=16)
ax_polar.xaxis.set_tick_params(pad=7)
ax_polar.set_xlabel('Orientation [°]', fontsize=18)

# tilt
ax_polar.set_ylabel('Tilt [°]', rotation=0)
ax_polar.yaxis.set_label_coords(0.76, 0.98)
ax_polar.set_rmax(90)
ax_polar.set_rlabel_position(200)

# [left, bottom, width, height]
cbar_ax = fig.add_axes([0.55, 0.25, 0.015, 0.55])
spec_cbar = fig.add_gridspec(nrows=1, ncols=1, left=0.55, right=0.57)
fig.colorbar(im, cax=cbar_ax, ticks=np.arange(start=0, stop=101, step=10), label='Relative level of annual irradiation [%]')
cbar_ax.yaxis.set_major_formatter(PercentFormatter())

# add cubes
imagebox_0_0 = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_0_0.png"), zoom=0.15)
imagebox_S_opt = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_S_opt.png"), zoom=0.15)
imagebox_S_90 = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_S_90.png"), zoom=0.15)
imagebox_SE_opt = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_SE_opt.png"), zoom=0.15)
imagebox_SE_90 = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_SE_90.png"), zoom=0.15)
imagebox_E_opt = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_E_opt.png"), zoom=0.15)
imagebox_E_90 = OffsetImage(plt.imread("data/Figure2.16 - annual_irradiation - cube_E_90.png"), zoom=0.15)

idx_max = np.unravel_index(np.argmax(poa_tmy, axis=None), poa_tmy.shape)

ax_polar.plot(np.radians(orientation_range[idx_max[0]]), tilt_range[idx_max[1]], marker='x', color='C1')

ax_polar.add_artist(AnnotationBbox(imagebox_0_0, xy=(np.radians(0), 5), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_S_opt, xy=(np.radians(5), tilt_range[idx_max[1]]), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_S_90, xy=(np.radians(0), 90-6), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_SE_opt, xy=(np.radians(-45), tilt_range[idx_max[1]]), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_SE_90, xy=(np.radians(-45), 90-6), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_E_opt, xy=(np.radians(-90), tilt_range[idx_max[1]]), frameon=False))
ax_polar.add_artist(AnnotationBbox(imagebox_E_90, xy=(np.radians(-90), 90-6), frameon=False))


spec_cube = fig.add_gridspec(nrows=1, ncols=1, left=0.7)
ax_cube = fig.add_subplot(spec_cube[0,0])
ax_cube.imshow(plt.imread('data/Figure2.16 - annual_irradiation - cube_main.png'))
ax_cube.axis('off')

plt.savefig('Figure2.16 - annual_irradiation.jpg', dpi=300, bbox_inches='tight')