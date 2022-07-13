# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
plt.figure(figsize=(12, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

colors={'Hydro': colors['color1'],
        'Nuclear': colors['color2'],
        'Wind': colors['color3'], 
        'Solar': colors['color5'], 
        'Solar PV': colors['color5'], 
        'Coal':colors['color11'], 
        'Gas':colors['color13'],
        'Oil': colors['color12'], 
        'Biomass': colors['color14'], 
        'Geothermal': colors['color15'] }

techs=['Coal',
       'Oil',
       'Gas',
       'Biomass',
       'Nuclear',
       'Hydro',
       'Geothermal',
       'Wind',
       'Solar PV']

GHG={'Solar PV':43, 
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
    ax1.barh(i,GHG[tech], 
             height=0.5,
            color=colors[tech])
    ax1.text(GHG[tech], i-0.15, GHG[tech], fontsize=16)
ax1.set_xlim(0,1070)
ax1.set_xlabel('Lifecycle Greenhouse Gas Emissions (gr CO$_2$/kWh)')
ax1.set_yticks(range(0,len(techs)))
ax1.set_yticklabels(techs)
ax1.grid(color='grey', linestyle='--', axis='x', which='both')

plt.savefig('figures/GHG_technologies.jpg', dpi=300, bbox_inches='tight')  