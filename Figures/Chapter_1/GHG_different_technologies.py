# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.family'] = 'avenir'
plt.rcParams['axes.titlesize'] = 18

plt.figure(figsize=(16, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

colors={'Solar': 'darkorange',
        'Solar PV': 'darkorange',
        'Wind': 'yellowgreen',
        'Biomass': 'peru',
        'Geothermal': 'coral',
        'Hydro':'dodgerblue',
        'Nuclear': 'firebrick',
        'Coal':'black',
        'Oil': 'gray',
        'Gas':'silver'}

techs=['Solar PV', 
       'Wind',
       'Geothermal',
       'Hydro',
       'Nuclear',
       'Biomass',
       'Gas',
       'Oil',
       'Coal']

GHG={'Solar PV':20, #43
     'Wind': 13,
     'Biomass':52,
     'Geothermal':27,
     'Hydro':21,
     'Nuclear':13,
     'Gas':486,
     'Oil':840,
     'Coal':1001}

ax1 = plt.subplot(gs1[0,0])
for i,tech in enumerate(techs):
    ax1.bar(i,GHG[tech], 
            width=0.5,
            color=colors[tech])
    
#ax1.set_ylim(0,210)
ax1.set_ylabel('Lifecycle Greenhouse Gas Emissions (gr CO$_2$/kWh)')
ax1.set_xticks(range(0,len(techs)))
ax1.set_xticklabels(techs)
ax1.grid(color='grey', linestyle='--', axis='y', which='both')

plt.savefig('figures/GHG_technologies.jpg', dpi=300, bbox_inches='tight')  