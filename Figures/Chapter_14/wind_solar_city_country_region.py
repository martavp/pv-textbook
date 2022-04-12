# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

plt.figure(figsize=(12, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

colors=['orange',
        'dodgerblue',
        'black',
        ]

country='DEU' #'DNK'


CF_pv=pd.read_csv('data/pv.csv',
                  sep=';', index_col=0)
CF_pv.index=pd.to_datetime(CF_pv.index)

CF_onwind=pd.read_csv('data/onshore_wind.csv',
                      sep=';', index_col=0)
CF_onwind.index=pd.to_datetime(CF_onwind.index)

CF_EU_pv=pd.read_csv('data/pv_Europe.csv',
                  sep=';', index_col=0, header=None)
CF_EU_pv.index=pd.to_datetime(CF_EU_pv.index)

CF_EU_onwind=pd.read_csv('data/onshore_wind_Europe.csv',
                      sep=';', index_col=0, header=None)
CF_EU_onwind.index=pd.to_datetime(CF_EU_onwind.index)

plt.figure(figsize=(12, 13))
gs = gridspec.GridSpec(3, 3)
gs.update(wspace=0.05, hspace=0.05)

data_dic={'solar': CF_pv[country],
          'wind': CF_onwind[country],}

data_EU_dic={'solar': CF_EU_pv[1],
          'wind': CF_EU_onwind[1],}

title_dic={'solar': 'CF solar PV',
          'wind': 'CF wind',}

for i,data in enumerate(['solar', 'wind']):
    ax0 = plt.subplot(gs[0,i])
    ax0.plot(data_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2,
             label=country)
    ax0.plot(data_EU_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2, 
             linestyle='--',
             label='Europe')
    if i != 0:
        ax0.set_yticklabels([])
    ax0.set_ylim([0,1])
    ax0.set_xlim([0,8870])
    ax0.set_title(title_dic[data])

ax0.legend(fancybox=False, fontsize=18, loc='best',#(0.6,0.8), 
                   facecolor='white', ncol=1, frameon=True)
        
plt.savefig('figures/duration_curve_city_contry_region.png', dpi=300, bbox_inches='tight')

















