# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)

colors=[colors['color5'],
        colors['color1'],
        'black',
        colors['color2'],
        ]

country='DEU'#'DNK'

#import electricity demand data, in MWh
demand=pd.read_csv('data/electricity_demand.csv', 
                   sep=';', index_col=0)/1000 #MWh -> GWh
demand.index=pd.to_datetime(demand.index)

CF_pv=pd.read_csv('data/pv.csv',
                  sep=';', index_col=0)
CF_pv.index=pd.to_datetime(CF_pv.index)

CF_onwind=pd.read_csv('data/onshore_wind.csv',
                      sep=';', index_col=0)
CF_onwind.index=pd.to_datetime(CF_onwind.index)

plt.figure(figsize=(12, 13))
gs = gridspec.GridSpec(3, 3)
gs.update(wspace=0.05, hspace=0.05)

data_dic={'solar': CF_pv[country],
          'wind': CF_onwind[country],
          'demand': demand[country]/max(demand[country])}

ylabel_dic={'solar': 'CF solar PV',
          'wind': 'CF wind',
          'demand': 'normalized demand'}

for i,data in enumerate(['solar', 'wind', 'demand']):
    ax0 = plt.subplot(gs[i,0])
    ax0.plot(data_dic[data], 
             color=colors[i])
    ax0.set_ylabel(ylabel_dic[data])
    ax0.set_ylim([0,1])
    ax1 = plt.subplot(gs[i,1])

    ax1.plot(data_dic[data].iloc[4468:4468+168],# [4468:4636]
             color=colors[i],
             linewidth=2)
    plt.xticks(rotation=0)
    ax1.set_ylim([0,1])
    ax1.set_yticklabels([])
    ax2 = plt.subplot(gs[i,2])
    ax2.plot(data_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2)
    
    ax2.set_yticklabels([])
    ax2.set_ylim([0,1])
    ax2.set_xlim([0,8870])
    ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
    ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
    
    if i==0:
        ax0.set_title('1 year')
        ax1.set_title('1 week in June')
        ax2.set_title('Duration curve')
    
    if i==2:
        ax2.set_xlabel('hours')
        ax0.set_xticks(data_dic[data].index[np.arange(0,4)*24*121])
        ax0.set_xticklabels(['Jan', 'May', 'Sep', 'Dec'])
        ax1.set_xticks(data_dic[data].index[np.arange(0,7)*24+4468+12])
        ax1.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
    else:
        ax0.set_xticklabels([])
        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
        

plt.savefig('figures/wind_solar_demand.tif', dpi=300, bbox_inches='tight')

#%%
"""
Mismatch figure
"""

G_pv=0.5*np.mean(demand[country])/np.mean(CF_pv[country])
G_onwind=0.5*np.mean(demand[country])/np.mean(CF_onwind[country])

mismatch = G_pv*CF_pv[country]+G_onwind*CF_onwind[country] - demand[country]

plt.figure(figsize=(12, 4))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.05, hspace=0.05)
ax0 = plt.subplot(gs[0,0])
ax0.plot(mismatch, 
         color=colors[3])
ax0.set_ylabel('Mismatch')

ax1 = plt.subplot(gs[0,1])
ax1.plot(mismatch.iloc[4468:4468+168],# [4468:4636]
         color=colors[3],
         linewidth=2)
plt.xticks(rotation=0)

ax2 = plt.subplot(gs[0,2])
ax2.plot(mismatch.sort_values(ascending=False).values, 
         color=colors[3],
         linewidth=2)

ax2.set_xlim([0,8870])
ax0.set_ylim([-80,180])
ax1.set_ylim([-80,180])
ax2.set_ylim([-80,180])
ax1.set_yticklabels([])
ax2.set_yticklabels([])
ax0.axhline(y = 0.5, color = 'gray', linestyle = '--')
ax1.axhline(y = 0.5, color = 'gray', linestyle = '--')
ax2.axhline(y = 0.5, color = 'gray', linestyle = '--')
#ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
#ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1])

ax0.set_title('1 year')
ax1.set_title('1 week in June')
ax2.set_title('Duration curve')

ax2.set_xlabel('hours')
ax0.set_xticks(data_dic[data].index[np.arange(0,4)*24*121])
ax0.set_xticklabels(['Jan', 'May', 'Sep', 'Dec'])
ax1.set_xticks(mismatch.index[np.arange(0,7)*24+4468+12])
ax1.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
ax2.annotate('curtailment', (9500, 40), 
             annotation_clip=False, 
             rotation=90,
             fontsize=16,
             color='dimgray')

ax2.annotate('backup \n energy', (9500, -70), 
             annotation_clip=False, 
             rotation=90,
             fontsize=16,
             color='dimgray')


ax2.annotate('', xy=(1.05, 0.3), 
             xycoords='axes fraction', xytext=(1.05, 1),
             arrowprops=dict(arrowstyle="<->",
                             color='dimgray',
                             lw=2))
ax2.annotate('', xy=(1.05, 0.3), 
             xycoords='axes fraction', xytext=(1.05, 0),
             arrowprops=dict(arrowstyle="<->",
                             color='dimgray',
                             lw=2))
plt.savefig('figures/mismatch.tif', dpi=300) #, bbox_inches='tight')
#%%
"""
Wind and solar seasonal complementarity figure
"""

label_country={'DEU':'Germany',
               'DNK':'Denmark',
               'ESP':'Spain'}

plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 1)
gs.update(wspace=0.05, hspace=0.05)

ax0 = plt.subplot(gs[0,0])
for i,data in enumerate(['solar', 'wind', 'demand']):
    norm_data=data_dic[data]/data_dic[data].mean()
    ax0.plot(norm_data.groupby(pd.Grouper(freq='W')).mean(), 
         color=colors[i], alpha=1, linewidth=3, label=data)

#Add dotted horizontal line
ax0.set_ylim([0.2,2.2])
ax0.set_yticks([0.5, 1, 1.5, 2])
ax0.set_xlim((data_dic['demand'].index[0], data_dic['demand'].index[-1]))
ax0.set_xticks(data_dic['demand'].index[24*15+np.arange(0,6)*24*60])
ax0.set_xticklabels(['Jan', 'Mar', 'May',  'Jul', 'Sep', 'Nov'])
ax0.set_ylabel(label_country[country])

ax0.legend(fancybox=False, fontsize=18, loc='upper center',
           facecolor='white', ncol=3, frameon=True)
plt.savefig('figures/wind_solar_complementarity_{}.tif'.format(country), dpi=300, bbox_inches='tight')












