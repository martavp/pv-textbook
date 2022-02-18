# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


cost=pd.read_csv('data/cost_historical.csv', sep=',')

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
color_1='darkorange'

ax1 = plt.subplot(gs1[0,0])
ax1.loglog(cost['volume'], cost['cost'],
           marker='o', markerfacecolor=color_1,
           linewidth=0, color='black', #color_1,
           markersize=14)
ax1.set_ylabel('Module price (USD2019/W$_p$)')
ax1.set_xlabel('Cumulative PV capacity (MW)')
ax1.grid(color='grey', linestyle='--', axis='both', which='both')
ax1.set_ylim(0.1,200)
ax1.set_xlim(0.05, 10000000)
ax1.set_yticks([0.1, 1, 10, 100])
ax1.set_yticklabels(['0.1', '1', '10', '100'])

plt.savefig('figures/learning_curve.jpg', dpi=300, bbox_inches='tight')