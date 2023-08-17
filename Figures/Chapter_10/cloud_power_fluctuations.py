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

plt.figure(figsize=(10, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)

data = pd.read_csv('data/irradiance.csv')

ax1 = plt.subplot(gs1[0,0])
ax1.plot(data['minute'], data['global horizontal irradiance'], 
         linewidth=3,
         color=colors['color5'],
         label='irradiance')
ax1.set_xlabel('minutes', fontsize=20)
ax1.set_ylabel('Global Horizontal Irradiance (W/m$^2$) ',
               fontsize=20)
# ax1.spines["right"].set_edgecolor(colors['color5'])
# ax1.tick_params(axis='y', colors=colors['color5'])

data = pd.read_csv('data/power.csv')
ax2 = ax1.twinx()
ax2.plot(data['minute'], data['normalized power'], 
         linewidth=4,
         linestyle='--',
         color=colors['color1'],
         label='normalized power output')

ax2.set_ylabel('Normalized power output ',
               fontsize=20)
# ax2.spines["right"].set_edgecolor(colors['color1'])
# ax2.tick_params(axis='y', colors=colors['color1'])

ax1.set_xlim(0,12)
ax1.set_ylim(0,1200)
ax2.set_ylim(0,1.2)

ax1.yaxis.grid('--')
ax1.legend(fancybox=False, fontsize=18, loc='lower left', 
                    facecolor='white', ncol=1, frameon=True)
ax2.legend(fancybox=False, fontsize=18, loc='lower right', 
                    facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/cloud_power_fluctuation.jpg', dpi=300, bbox_inches='tight')  