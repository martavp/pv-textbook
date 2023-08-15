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

plt.figure(figsize=(18, 8))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.2, hspace=0.2)

# invented performance data
P50=100
E_0=0.05
E_1=0.04
P90=96

ax0 = plt.subplot(gs1[0,0])

import scipy.stats as stats
import math

mu = P50
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
ax0.fill_between(stats.norm.pdf(x, mu, sigma),
                 x,
                 color=colors['color5'], 
                 alpha=0.6,
                 linewidth=4,)
ax0.set_ylim([90,110])
ax0.fill_between(0.5*stats.norm.pdf(x, mu, sigma*0.5),
                 x,
                 color=colors['color4'], 
                 alpha=0.6,
                 linewidth=4,)

ax1 = plt.subplot(gs1[0,1])
ax1.set_ylabel('PV power plant production (MWh/year) ',
               fontsize=20)
ax1.set_xlabel('years in operation',
               fontsize=20)

years=np.arange(0,31)

ax1.plot(years, P50*np.ones(len(years)), 
         color=colors['color6'],
         linestyle='--',
         linewidth=4,
         label=None)
ax1.text(20,100.5,'P50 generation', fontsize=20, color=colors['color6'])
ax1.plot(years, P90*np.ones(len(years)), 
         color=colors['color1'], 
         linestyle='--',
         linewidth=4,
         label=None)
ax1.text(20,96.3,'P90 generation', fontsize=20, color=colors['color1'])
ax1.fill_between(years, 
                 [P50*(1+E_0*np.exp(-0.033*y)) for y in years],
                 [P50*(1-E_0*np.exp(-0.033*y)) for y in years],
                 color=colors['color5'], 
                 alpha=0.6,
                 linewidth=4,
                 label='modelling uncertainty')
ax1.fill_between(years, 
                 [P50*(1+E_1*np.exp(-0.033*y)) for y in years],
                 [P50*(1-E_1*np.exp(-0.033*y)) for y in years],
                 color=colors['color4'], 
                 alpha=0.6,
                 linewidth=4,
                 label='weather variability')
ax1.set_xlim(0,30)
ax1.set_ylim(90,110)

ax1.yaxis.grid('--')
ax1.legend(fancybox=False, fontsize=18, loc='best', 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/uncertainty_vs_time.jpg', dpi=300, bbox_inches='tight')  