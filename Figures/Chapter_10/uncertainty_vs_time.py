# -*- coding: utf-8 -*-
"""
@author: Marta
"""
import numpy as np
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

# invented performance data
P50=100
E_0=0.04
E_1=0.025
P90=96.8


ax1 = plt.subplot(gs1[0,0])
ax1.set_ylabel('PV power plant production (MWh/year) ',
               fontsize=20)
ax1.set_xlabel('years in operation',
               fontsize=20)

years=np.arange(0,31)

ax1.plot(years, 
         [P50*(1-0.005)**y for y in years],
         color=colors['color6'],
         linestyle='--',
         linewidth=4,
         label=None)
ax1.text(2,96.1,'P50 generation', rotation=-25, fontsize=20, color=colors['color6'])

ax1.plot(years, 
         [P90*(1-0.0044)**y for y in years], 
         color=colors['color1'], 
         linestyle='--',
         linewidth=4,
         label=None)
ax1.text(1.5,93.7,'P90 generation', rotation=-21, fontsize=20, color=colors['color1'])
ax1.fill_between(years, 
                 [P50*((1-0.005)**y+E_0*np.exp(-0.033*y)) for y in years],
                 [P50*((1-0.005)**y-E_0*np.exp(-0.033*y)) for y in years],
                 color=colors['color5'], 
                 alpha=0.6,
                 linewidth=4,
                 label='modelling uncertainty')
ax1.fill_between(years, 
                 [P50*((1-0.005)**y+E_1*np.exp(-0.033*y)) for y in years],
                 [P50*((1-0.005)**y-E_1*np.exp(-0.033*y)) for y in years],
                 color=colors['color4'], 
                 alpha=0.6,
                 linewidth=4,
                 label='weather variability')
ax1.set_xlim(0,30)
ax1.set_ylim(80,106)

ax1.yaxis.grid('--')
ax1.legend(fancybox=False, fontsize=18, loc='best', 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/uncertainty_vs_time.jpg', dpi=300, bbox_inches='tight')  