# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

colors=['orange',
        'dodgerblue',
        'black',]

# city='MADRID'
# country='SPAIN'
# region='EUROPE'

# city='BERLIN'
# country='GERMANY'
# region='EUROPE'

# city='PHILADELPHIA'
# country='PENNSYLVANIA'
# region='USA'

city='DENVER'
country='COLORADO'
region='USA'

CF_city=pd.read_csv('data/time-series/time-series-{}.csv'.format(city),
                  sep=',', index_col=0)

CF_country=pd.read_csv('data/time-series/time-series-{}.csv'.format(country),
                  sep=',', index_col=0)

CF_region=pd.read_csv('data/time-series/time-series-{}.csv'.format(region),
                  sep=',', index_col=0)

plt.figure(figsize=(12, 13))
gs = gridspec.GridSpec(3, 3)
gs.update(wspace=0.05, hspace=0.05)

data_city_dic={'solar': CF_city['solar'],
                'wind': CF_city['onwind'],}

data_country_dic={'solar': CF_country['solar'],
                  'wind': CF_country['onwind'],}

data_region_dic={'solar': CF_region['solar'],
                 'wind': CF_region['onwind'],}

title_dic={'solar': 'CF solar PV',
          'wind': 'CF onshore wind',}

for i,data in enumerate(['solar', 'wind']):
    ax0 = plt.subplot(gs[0,i])
    ax0.plot(data_city_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2,
             label=city)
    ax0.plot(data_country_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2,
             linestyle='--',
             label=country)
    ax0.plot(data_region_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2, 
             linestyle='dotted',
             label=region)
    if i != 0:
        ax0.set_yticklabels([])
    ax0.set_ylim([0,1])
    ax0.set_xlim([0,8870])
    ax0.set_title(title_dic[data])

ax0.legend(fancybox=False, fontsize=16, loc='best',#(0.6,0.8), 
           facecolor='white', ncol=1, frameon=True)
        
plt.savefig('figures/duration_curve_city_contry_region_{}.png'.format(city), 
            dpi=300, bbox_inches='tight')

















