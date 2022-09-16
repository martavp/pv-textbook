# -*- coding: utf-8 -*-
"""
@author: Marta
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)

static=pd.read_csv('data/Timeseries_37.779_-122.420_NS_1kWp_crystSi_14_36deg_11deg_2015_2015.csv', 
                   skiprows=range(0,10), sep=',')
static_max =max([float(x) for x in static['P'][0:8760]])
static_s = sorted([float(x)/static_max for x in static['P'][0:8760]], reverse=True)

tracking=pd.read_csv('data/Timeseries_37.779_-122.420_NS_1kWp_crystSi_14_i0deg_2015_2015.csv', 
                   skiprows=range(0,10), sep=',')
tracking_max =max([float(x) for x in tracking['P'][0:8760]])
tracking_s = sorted([float(x)/tracking_max for x in static['P'][0:8760]], reverse=True)

plt.figure(figsize=(18, 8))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.2, hspace=0.2)
color_1=colors['color5']

ax0 = plt.subplot(gs1[0,0])
ax0.set_ylabel('Normalized DC PV generation', fontsize=22)

ax0.plot(static_s, color=colors['color4'], linewidth=3,
          linestyle='--', label='static')
ax0.plot(tracking_s, color=colors['color5'], linewidth=3,
          label='1-axis horizontal \n tracking')
ax0.set_xlim(0,8760)
ax0.set_ylim(0,1.05)
ax0.set_xlabel('hours throughout the year', fontsize=22,)
# ax0.fill_between(np.arange(0,1000),np.array(tracking_s[0:1000]), 
#                  0.8*np.ones(1000), color=colors['color5'], alpha=0.3)

ax0.fill_between(np.arange(0,900),np.array(static_s[0:900]), 
                 0.8*np.ones(900), color=colors['color4'], alpha=0.6)


ax0.annotate('curtailed energy', xy=(300, 0.85), xytext=(1000, 0.9), fontsize=22,
             arrowprops=dict(facecolor='black', arrowstyle='->'))

ax0.annotate('inverter AC capacity', xy=(1000, 0.8), xytext=(2000, 0.8), fontsize=22,
             arrowprops=dict(facecolor='black', arrowstyle='->'))
ax0.legend(fancybox=False, fontsize=22, loc='lower right', 
                   facecolor='white', ncol=1, frameon=True)

ax1 = plt.subplot(gs1[0,1])
years=np.arange(2010,2022)
static = [ 1.19, 1.2, 1.21, 1.21, 1.24, 1.24, 1.23, 1.23, 1.24, 1.23, 1.22, 1.28 ]
#1-axis horizontal tracking
tracking = [1.19, 1.22, 1.23, 1.24, 1.27, 1.26, 1.27, 1.26, 1.25, 1.25, 1.23, 1.26]


ax1.set_ylabel('DC to AC ratio (global average)', fontsize=22)
ax1.plot(years, static, color=colors['color4'], linewidth=3,
          linestyle='--', label='static',
          marker='o', markerfacecolor='white',markersize=12)
ax1.plot(years, tracking, color=colors['color5'], linewidth=3,
         label='1-axis horizontal \n tracking',
         marker='o', markerfacecolor='white',markersize=12)

ax1.set_xlim(2009,2022)
ax1.set_ylim(1.18,1.30)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)
ax1.yaxis.grid('--')

ax1.legend(fancybox=False, fontsize=22, loc='best', 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/DC_AC_ratio.jpg', dpi=300, bbox_inches='tight')  