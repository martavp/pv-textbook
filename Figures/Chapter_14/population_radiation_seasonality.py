# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
import requests
import datetime as dt
from pathlib import Path
import pandas as pd
import rasterio
import numpy as np
import atlite
import logging
from netCDF4 import Dataset

plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])
large_font_size=24

colors_=['lightblue',
         'darkred',
         'green',
         'orange',
         'dodgerblue',
         'black',]

def read_radiation_pvgis(raddatabase,lat,lon):
    """
    Retrieve data from PVGIS. 
    More details regarding how to download data from PVGIS using an API
    https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en

    Parameters
    ----------
    raddatabase : 
    lat:
    lon:
        
    Returns
    -------
    series : 

    """
    params = {'lat': lat, 
              'lon': lon, 
              'browser': 1, 
              'outputformat': 'csv', 
              'raddatabase': raddatabase}
    
    series_file = Path(f'data/radiation/anual_series_{lat}_{lon}_{raddatabase}.csv')
    if not series_file.exists():
        resp_series = requests.get('https://re.jrc.ec.europa.eu/api/v5_2/seriescalc', params=params)
        with open(series_file, 'wb') as f:
            f.write(resp_series.content)
    
    series = pd.read_csv(series_file, 
                          skiprows=8, 
                          index_col='time', 
                          skipfooter=10, 
                          engine='python',
                          parse_dates=True, 
                          infer_datetime_format=True, 
                          date_parser=lambda x: dt.datetime.strptime(x, '%Y%m%d:%H%M')
                          )
    
    series = series.rename({'G(i)': 'GHI'}, axis='columns')
    series['hour'] = series.index.hour
    series['date'] = series.index.date
    return series


#load population density map
tif_file = rasterio.open('data/population/GHS_POP_E2015_GLOBE_R2019A_4326_30ss_V1_0.tif')
ghs_data = tif_file.read()
ghs_data[0][ghs_data[0] < 0.0] = 0.0

ghs_lat=ghs_data.sum(axis=2)[0,:] #sum population by latitude
latitudes=np.arange(-90,90-0.00833, 0.008333)*(-1)
ghs_lat=ghs_data.sum(axis=2)[0,:] #sum population by latitude

plt.figure(figsize=(22, 6))
gs = gridspec.GridSpec(3, 6)
gs.update(wspace=0.1, hspace=0.1)

"""
Plot population density map
"""
ax0 = plt.subplot(gs[0:3,0:2])
ax0.text(.01, .99, 'a)', 
         ha='left',
         va='top', 
         transform=ax0.transAxes,
         fontsize=large_font_size)

ax0.set_title('Population density', fontsize=large_font_size)
ax0.set_xlim(43200/2*np.array([0, 1]))
ax0.set_xticks(43200/2*np.array([0, 0.1666, 0.333, 0.5, 0.6666, 0.8333, 1]))
ax0.set_xticklabels(['-180', '-120', '-60', '0', '60', '120', '180'])

ax0.set_ylim(21600/2*np.array([0, 1]))
ax0.set_yticks(21600/2*np.array([0, 0.1666, 0.333, 0.5, 0.6666, 0.8333, 1]))
ax0.set_yticklabels(['90', '60', '30', '0', '-30', '-60', '-90'])
ax0.set_ylabel('Latitude', fontsize=large_font_size)
ax0.set_xlabel('Longitude', fontsize=large_font_size)
def shrink(data, rows, cols):
    return data.reshape(int(rows), int(data.shape[0]/rows), 
                        int(cols), int(data.shape[1]/cols)).sum(axis=1).sum(axis=2)
data=ghs_data[0]
data_s=shrink(data, 21600/2, 43200/2) #reduce resolution before plotting

colorm = cm.get_cmap('Greys', 460) #set colormap
newcolors = colorm(np.linspace(0, 1, 460))
background_colour = np.array([0.9882352941176471, 0.9647058823529412, 0.9607843137254902, 1.0])
newcolors[:1, :] = background_colour
newcmp = ListedColormap(newcolors)
ax0.contourf(data_s, norm=colors.LogNorm(), cmap=newcmp)
ax0.set_ylim(ax0.get_ylim()[::-1]) #reverse latitude (y axis)
lats_ref=[40, 30, 20]
for i,lat_ref in enumerate(lats_ref):
    ax0.axhline((90-lat_ref)*21600/2/180, color=colors_[i], linewidth=2)
    ax0.axhline((90+lat_ref)*21600/2/180, color=colors_[i], linewidth=2)
    
"""
Plot population sum by latitud
"""

ax1 = plt.subplot(gs[0:3,2])
ax1.text(.01, .99, 'b)', 
         ha='left',
         va='top', 
         transform=ax1.transAxes,
         fontsize=large_font_size)
ax1.set_title('Population', fontsize=large_font_size)
ax1.plot(ghs_lat/1000000, latitudes, color='black')
ax1.set_xticks([0,1,2,3])
ax1.set_xlabel('Million habitants', fontsize=large_font_size)
ax1.set_yticks([])
ax1.set_ylim([-90,90])

for i,lat_ref in enumerate(lats_ref):
    ax1.axhline(lat_ref, color=colors_[i], linewidth=2)
    ax1.axhline(-lat_ref, color=colors_[i], linewidth=2)
 
"""
Plot annual radiation vs latitude
"""

#donwload ERAV climate reanalysis slice corresponding the one meridian
logging.basicConfig(level=logging.INFO)
cutout=atlite.Cutout(
    path='data/meridian_2019_0.nc',
    module='era5',
    x=slice(0,0.4), # Longitude
    y=slice(-90,90), # Latitude
    time='2019')

cutout.prepare()

nc = Dataset('data/meridian_2019_0.nc')
latitudes=nc.variables['lat'][:]
longitudes=nc.variables['lon'][:]
influx=nc.variables['influx_direct'][:,:,:]+nc.variables['influx_diffuse'][:,:,:]
irrad_annual=influx[:,:,0].data.sum(axis=0)

    
ax2 = plt.subplot(gs[0:3,3])
ax2.text(.01, .99, 'c)', 
         ha='left',
         va='top', 
         transform=ax2.transAxes,
         fontsize=large_font_size)
ax2.set_title('Global Horizontal \n Irradiation ', fontsize=large_font_size)
ax2.plot(irrad_annual/1000, 
         latitudes,
         color='black', 
         linewidth=3,
         )
ax2.set_yticks([])
ax2.set_xlabel('kWh/year', fontsize=large_font_size)
ax2.set_xlim([0,2800])
ax2.set_ylim([-90,90])
for i,lat_ref in enumerate(lats_ref):
    ax2.axhline(lat_ref, color=colors_[i], linewidth=2)
    ax2.axhline(-lat_ref, color=colors_[i], linewidth=2)
    
"""
Plot monthly radiation vs latitude
"""

for j,lat in enumerate(lats_ref):
    lat, lon = lat, 18.1 # 
    database = read_radiation_pvgis(raddatabase='PVGIS-ERA5', lat=lat, lon=lon)
    GHI_m = database['GHI'].resample('M').sum()/1000
    
    ax3 = plt.subplot(gs[j,4:6])
    ax3.set_yticks([])
    ax3.set_xlim([0,11])
    ax3.text(0.05, 210,'200 kWh/month', color='grey', 
             fontsize=large_font_size)
    ax3.plot([0,12], [200,200], color='grey', linestyle='--')
    ax3.set_ylim([0,400])
    ax3.plot(GHI_m.groupby(GHI_m.index.month).mean().values, 
              linewidth=2,
              color=colors_[j],
              marker='.',
              markersize=10)
    ax3.text(7, 310,'Latitude '+str(lat)+'$^{\circ}$', 
             color=colors_[j], fontsize=large_font_size)
    if j==0:
        ax3.set_title('Monthly Irradiation (kWh/month)', fontsize=large_font_size)
        ax3.text(.01, .99, 'd)', 
                 ha='left',
                 va='top', 
                 transform=ax0.transAxes,
                 fontsize=large_font_size)
    if j==2:
        ax3.set_xticks([0,2,4,6,8,10])
        ax3.set_xticklabels(['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'],
                            fontsize=large_font_size)
    else:
        ax3.set_xticks([])
        
plt.savefig('figures/population_radiaton_sesonality.jpg', 
            dpi=300, bbox_inches='tight')