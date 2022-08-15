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
    

data=pd.read_csv('data/cost_rooftop.csv', index_col=0, header=0)

plt.figure(figsize=(12, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
ax1 = plt.subplot(gs1[0,0])

ax1.bar(data.index, height=data['Modules'], label='PV modules', 
        color=colors['color5'])
ax1.bar(data.index, height=data['BOS'], bottom=data['Modules'], label='BOS',
        color=colors['color1'])

ax1.legend(fancybox=False, fontsize=18, loc='best', #(1.03,-0.04), 
           facecolor='white', ncol=1, frameon=True)
ax1.set_ylim(0,100)
ax1.set_ylabel('Relative price (in % compared to 2006)')

ax1.grid(color='grey', linestyle='--', axis='y', which='both')

plt.savefig('figures/costs_rooftop.jpg', dpi=300, bbox_inches='tight')  