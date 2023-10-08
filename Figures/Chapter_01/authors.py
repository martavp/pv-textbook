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

plt.figure(figsize=(9, 9))
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
        'Geo Biomass Other': colors['color14'], 
        }

ax1 = plt.subplot(gs1[0,0])
filename= 'data/Statistical Review of World Energy Data.xlsx'
datafile = pd.read_excel(filename,
                              sheet_name='Solar Capacity',
                              index_col=0, header=0, squeeze=True) 
 
capacity=0.001*datafile.loc['Total World'][0:27] #MW -> GW
capacity.index=[int(x) for x in datafile.loc['Megawatts'][0:27]]


ax1.set_xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020])
ax1.tick_params(direction='out')
ax1.set_xticklabels([1990, 1995, 2000, 2005, 2010, 2015, 2020])

ax1.set_ylim(0,210)
ax1.set_xlim(2000,2023)

ax2=ax1.twinx()
ax2.plot(capacity, 
         color=colors['Solar PV'], 
         linewidth=5)
ax2.set_ylim(0,1100)
ax2.set_ylabel('Photovoltaics - Global cumulative capacity (GW)', fontsize=18)

ax1.get_yaxis().set_visible(False)
ax1.spines[['left', 'top']].set_visible(False)
ax2.spines[['left', 'top']].set_visible(False)

plt.savefig('figures/authors.jpg', dpi=300, bbox_inches='tight')  