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

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
color_1=colors['color5']

ax1 = plt.subplot(gs1[0,0])

years=np.arange(2010,2022)
#hectares per MW (IRENA power generation costs)
mean=[2.69, 2.57, 2.41, 2.45, 2.2, 2.12, 2.17, 2.05, 1.99, 1.96, 1.94, 1.94]
max_value = [5.13, 4.84, 3.97, 4.15, 3.69, 3.61, 3.58, 3.43, 3.41, 3.28, 3.32, 3.85]
min_value= [1.2, 1.22, 1.07, 1.26, 1.2, 1.1, 1.08, 0.97, 0.9, 0.88, 0.85, 0.93]


#hectares per MW to MW/km2
mean=[100/x for x in mean]
max_value=[100/x for x in max_value]
min_value=[100/x for x in min_value]

dif_value=[a-b for a,b in zip(min_value,max_value)]

ax1.set_ylabel('Utility-scale solar PV land use (W/m$^2$)')
ax1.plot(years, mean, color='black', linewidth=4,
         marker='o', markerfacecolor='white',markersize=12)

ax1.bar(years, dif_value, bottom=max_value, color=color_1, alpha=1)

ax1.set_xlim(2009,2022)
ax1.set_ylim(0,120)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)
ax1.yaxis.grid('--')

plt.savefig('figures/landuse_PV_plants.jpg', dpi=300, bbox_inches='tight')  