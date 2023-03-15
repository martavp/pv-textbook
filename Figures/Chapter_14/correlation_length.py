# -*- coding: utf-8 -*-
"""
@author: Marta
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from netCDF4 import Dataset
import geopy.distance
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

nc = Dataset('data/cutout/europe-2013-era5.nc')

data=pd.DataFrame(data=None, 
                  index=None, 
                  columns=['lon', 
                           'lat', 
                           'distance',
                           'rho_wind', 
                           'rho_radiation'], 
                  dtype=float)


latitude = 48.86 #Paris
longitude = 2.34
index_lat = np.argmin(np.abs(nc.variables['lat'][:].data-latitude))
index_lon = np.argmin(np.abs(nc.variables['lon'][:].data-longitude))


lon_ref=nc.variables['lon'][index_lon].data
lat_ref=nc.variables['lat'][index_lat].data
wind_ref=nc.variables['wnd100m'][:,index_lat,index_lon].data
radiation_ref = nc.variables['influx_direct'][:,index_lat,index_lon].data+nc.variables['influx_diffuse'][:,index_lat,index_lon].data

i_min=max(0,index_lon-75)
i_max=min(len(nc.variables['lon'][:].data),index_lon+75)
j_min=max(0,index_lat-75)
j_max=min(len(nc.variables['lat'][:].data),index_lat+75)
k=0
for i in np.arange(i_min,i_max, 10):        
    for j in np.arange(j_min,j_max, 10):    
        k=k+1
        lon=nc.variables['lon'][i].data
        data.loc[k, 'lon'] = lon
        
        lat=nc.variables['lat'][j].data
        data.loc[k, 'lat'] = lat

        distance = geopy.distance.geodesic((lat,lon), (lat_ref,lon_ref)).km
        data.loc[k, 'distance'] = distance
        
        wind = nc.variables['wnd100m'][:,j,i]
        radiation = nc.variables['influx_direct'][:,j,i].data+nc.variables['influx_diffuse'][:,j,i].data
        data.loc[k,'rho_wind'] = np.corrcoef(wind,wind_ref)[0,1]
        data.loc[k,'rho_radiation'] = np.corrcoef(radiation,radiation_ref)[0,1]
        
#%%

data.to_csv('data_correlation.csv', sep=',')
data_s=pd.read_csv('data_correlation.csv', sep=',', index_col=0)
plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.set_title('Wind velocity')
ax0.set_ylabel(r'Correlation coefficient $\rho_{g_t^{R_i},g_t^{R_j}}$')
ax0.set_xlabel('distance (km)')
ax0.plot(data_s['distance'],data_s['rho_wind'],
         marker='.', 
         markersize=2,
         linewidth=0,
         color='dodgerblue')
ax0.set_ylim([-0.2,1])
ax0.set_xlim([0,3000])

ax1 = plt.subplot(gs[0,1])
ax1.set_title('Solar radiation')
#ax.set_ylabel('Correlation coefficient')
ax1.set_yticklabels([])
ax1.set_ylim([-0.2,1])
ax1.set_xlim([0,3000])
ax1.set_xlabel('distance (km)')
ax1.plot(data_s['distance'],data_s['rho_radiation'],
         marker='.', 
         markersize=1,
         linewidth=0,
         color='orange')

dis=np.arange(0,3000,200)
CL_wind=650
cor_theo_wind=[np.exp(-(1/CL_wind)*d) for d in dis]
ax0.plot(dis,cor_theo_wind, 'gray', linewidth=3)

CL_radiation=600*4
cor_theo_radiation=[np.exp(-(1/CL_radiation)*d) for d in dis]

plt.savefig('figures/correlation_length.png', 
            dpi=300, bbox_inches='tight')