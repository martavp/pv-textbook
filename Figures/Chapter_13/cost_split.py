# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


cost_split=pd.read_csv('data/cost_split.csv', sep=',', header=0, index_col=0)
cost_split.drop(index='Customer acquisition', inplace=True)
cost_split.drop(index='Incentive application',inplace=True)
cost_split['cost']=100*cost_split['cost']/cost_split.loc['Modules', 'cost']

plt.figure(figsize=(16, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
bot=0
for i,component in enumerate(cost_split.index):
    ax1.barh([0], 
             cost_split.loc[component,'cost']-bot, 
             left=bot, 

             color=cost_split.loc[component,'color'],
             alpha=cost_split.loc[component,'alpha'],
             label=component)
    
    bot=cost_split.loc[component,'cost']
ax1.set_yticks([])
ax1.set_xlim([0,100])
ax1.set_ylim([-0.4,0.4])
ax1.set_xticks(np.arange(0,110,10))
ax1.set_xticklabels(np.arange(0,110,10), fontsize=22)
ax1.set_xlabel('Cost distribution (%)', fontsize=22)
#ax1.legend(fancybox=False, fontsize=18, loc=(0.1,1.05),
#                   facecolor='white', ncol=3, frameon=True)
ax1.legend(fancybox=False, fontsize=18, loc=(1.01,0.02), 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/cost_split.jpg', dpi=300, bbox_inches='tight')  