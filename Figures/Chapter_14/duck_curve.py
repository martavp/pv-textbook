# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
#retrieve solar capacity factors
CF_country=pd.read_csv('data/time-series/time-series-CALIFORNIA.csv',
                       sep=',', index_col=0)   
CF_pv = CF_country['solar']
CF_pv.index = pd.to_datetime(CF_pv.index)
#datetime index is in UCT, California is in US/Pacific (UCT-7)
CF_pv.index=CF_pv.index.tz_localize('UCT',nonexistent='shift_forward', ambiguous=True).tz_convert('US/Pacific')

t_0 = pd.to_datetime('2011-03-28 00:00:00').tz_localize('US/Pacific')
t_f = pd.to_datetime('2011-03-28 23:00:00').tz_localize('US/Pacific')

CF = CF_pv.loc[t_0:t_f]

#%%
# https://zenodo.org/record/5348396#.ZA9nRB_MK5c
demand_USA=pd.read_csv('data/hourly-electricity-demand-by-state/demand.csv',
                        sep=',', index_col=0)
demand_CA=demand_USA[demand_USA.index==6] #6 is the 2-digit FIPS state code for California
demand_CA.set_index('utc_datetime', inplace=True)
demand_CA.index = pd.to_datetime(demand_CA.index)
demand_CA.index=demand_CA.index.tz_localize('UCT',nonexistent='shift_forward', ambiguous=True).tz_convert('US/Pacific')

demand=0.001*demand_CA.loc[t_0:t_f,'scaled_demand_mwh'] #MWh->GWh

#%%
plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(1, 1)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.set_title('Residual load = Demand - Solar PV generation')
ax0.set_ylabel('GWh')
ax0.set_xlabel('March 28')
ax0.set_xticks(demand.index[np.arange(3,24,6)])
ax0.set_xticklabels(['03:00', '9:00', '15:00', '21:00'])
ax0.text(.77, .4, 'backup \n ramp', 
             ha='left',
             va='top', 
             transform=ax0.transAxes,
             fontsize=18,
             color='black')
ax0.arrow(.7, .2, 0.13, 0.5,
          transform=ax0.transAxes,
          color='black',
          capstyle='projecting',
          head_width=0.015,
          linewidth=2)
# ax0.annotate("", xy=(0.7, 0.2), xytext=(0.83, 7),
#             arrowprops=dict(arrowstyle="->"),
#             transform=ax0.transAxes,)
ax0.plot(demand, 
         linewidth=2,
         color='black', 
         label='demand')
#https://en.wikipedia.org/wiki/Solar_power_in_California
dic_label={1:'1 GW (2010)', 
           2.6 :'2.6 GW (2012)',
           10:'10 GW (2014)',
           18.3: '18.3 GW (2016)',
           24: '24 GW (2018)',
           31:'31 GW (2020)'}

for i,C in enumerate([1, 2.6, 10, 18.3, 24, 31]):
    mismatch=C*CF-demand
    ax0.plot(-mismatch, label=dic_label[C], 
             linewidth=2, color=colors['color'+str(i+1)])
ax0.set_ylim([0,35])
ax0.set_xlim([t_0,t_f])
ax0.legend(fancybox=False, fontsize=18, loc=(1.03, 0), 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/duck_curve.png', 
            dpi=300, bbox_inches='tight')