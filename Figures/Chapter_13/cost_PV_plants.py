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

cost=pd.read_csv('data/cost_historical.csv', sep=',')

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
color_1=colors['color5']

ax1 = plt.subplot(gs1[0,0])

years=np.arange(2010,2021)

mean=[4.731, 4.007, 3.021, 2.647, 2.393, 1.823, 1.567, 1.432, 1.223, 1.009, 0.883]
max_value = [6.000/0.9, 5.800/0.9, 4.950/0.9, 5.400, 5.300, 4.200, 3.300, 3.000, 2.750, 2.300, 2.300]
min_value= [3.400, 2.600, 2.100, 1.7000, 1.400, 1.200, 1.100, 0.800, 0.7500, 0.700, 0.600]
ax1.set_ylabel('(USD$_{2019}$/W$_p$)')
ax1.plot(years, mean, color='black', linewidth=4,
         marker='o', markerfacecolor='white',markersize=12)

ax1.bar(years, max_value, bottom=min_value, color=color_1, alpha=0.8)

ax1.set_xlim(2009,2021)
ax1.set_ylim(0,8)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)
ax1.yaxis.grid('--')

plt.savefig('figures/cost_PV_plants.jpg', dpi=300, bbox_inches='tight')  