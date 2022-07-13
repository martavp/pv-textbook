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

cost=pd.read_csv('data/cost_historical.csv', sep=',')

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
color_1=colors['color5']

ax1 = plt.subplot(gs1[0,0])
ax1.loglog(cost['volume'], cost['cost'],
           marker='o', markerfacecolor=color_1,
           linewidth=0, color='black', #color_1,
           markersize=14)
ax1.set_ylabel('Module price (EUR$_{2019}$/W$_p$)')
ax1.set_xlabel('Cumulative PV capacity (GW)')
ax1.grid(color='grey', linestyle='--', axis='both', which='both')
ax1.set_ylim(0.1,30)
ax1.set_xlim(0.0005, 10000)
ax1.set_yticks([0.1, 1, 10, 100])
ax1.set_yticklabels(['0.1', '1', '10', '100'])


ax1.annotate('1980', xy=(0.0083, 25), xytext=(0.001, 24), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='-'))

ax1.annotate('1990', xy=(0.23, 10.1), xytext=(0.6, 11), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='-'))

ax1.annotate('2000', xy=(1.26, 4.6), xytext=(3.5, 5), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='-'))

ax1.annotate('2010', xy=(40.9, 1.68), xytext=(100, 1.6), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='-'))

ax1.annotate('2020', xy=(805, 0.183), xytext=(2000, 0.15), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='-'))
plt.savefig('figures/learning_curve.jpg', dpi=300, bbox_inches='tight')