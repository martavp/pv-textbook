# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18

country='DNK'

#import electricity demand data, in MWh
demand=pd.read_csv('data/electricity_demand.csv', 
                   sep=';', index_col=0)/1000 #MWh -> GWh
demand.index=pd.to_datetime(demand.index)

#%%
col='black'
plt.figure(figsize=(30, 10))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.plot(demand[country], color=col)
ax0.set_ylabel('Electricity demand (GWh)')

ax1 = plt.subplot(gs[0,1])
ax1.plot(demand[country][168:336], color=col)
plt.xticks(rotation=45)
ax2 = plt.subplot(gs[0,2])
ax2.plot(demand[country].sort_values(ascending=False).values, color=col)
ax2.set_xlabel('hours')
ax2.set_title('Duration curve')
plt.savefig('figures/demand.png', dpi=300, bbox_inches='tight')

#%%
CF_onwind=pd.read_csv('data/onshore_wind.csv',
                           sep=';', index_col=0)
CF_onwind.index=pd.to_datetime(CF_onwind.index)
#%%
col='dodgerblue'
plt.figure(figsize=(30, 10))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.plot(CF_onwind[country], color=col)
ax0.set_ylabel('Capacity factor onshore wind')
ax0.set_ylim([0,1])

ax1 = plt.subplot(gs[0,1])
ax1.plot(CF_onwind[country][168:336], color=col)
plt.xticks(rotation=45)
ax1.set_ylim([0,1])

ax2 = plt.subplot(gs[0,2])
ax2.plot(CF_onwind[country].sort_values(ascending=False).values, color=col)
ax2.set_xlabel('hours')
ax2.set_title('Duration curve')
ax2.set_ylim([0,1])

plt.savefig('figures/onwind.png', dpi=300, bbox_inches='tight')

#%%
CF_offwind=pd.read_csv('data/offshore_wind.csv',
                           sep=';', index_col=0)
CF_offwind.index=pd.to_datetime(CF_offwind.index)
#%%
col='darkblue'
plt.figure(figsize=(30, 10))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.plot(CF_offwind[country], color=col)
ax0.set_ylabel('Capacity factor offshore wind')
ax0.set_ylim([0,1])

ax1 = plt.subplot(gs[0,1])
ax1.plot(CF_offwind[country][168:336], color=col)
plt.xticks(rotation=45)
ax1.set_ylim([0,1])

ax2 = plt.subplot(gs[0,2])
ax2.plot(CF_offwind[country].sort_values(ascending=False).values, color=col)
ax2.set_xlabel('hours')
ax2.set_title('Duration curve')
ax2.set_ylim([0,1])
plt.savefig('figures/offwind.png', dpi=300, bbox_inches='tight')

#%%
CF_pv=pd.read_csv('data/pv.csv',
                           sep=';', index_col=0)
CF_pv.index=pd.to_datetime(CF_pv.index)
#%%
col='orange'
plt.figure(figsize=(30, 10))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.plot(CF_pv[country], color=col)
ax0.set_ylabel('Capacity factor solar PV')
ax0.set_ylim([0,1])

ax1 = plt.subplot(gs[0,1])
ax1.plot(CF_pv[country][168:336], color=col)
plt.xticks(rotation=45)
ax1.set_ylim([0,1])

ax2 = plt.subplot(gs[0,2])
ax2.plot(CF_pv[country].sort_values(ascending=False).values, color=col)
ax2.set_xlabel('hours')
ax2.set_title('Duration curve')
ax2.set_ylim([0,1])
plt.savefig('figures/pv.png', dpi=300, bbox_inches='tight')