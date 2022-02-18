# -*- coding: utf-8 -*-
"""
@author: Marta
"""
import numpy as np
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

years=np.arange(2010,2020)
mean=[3.550, 2.971, 2.253,1.974,1.784, 1.359, 1.236, 1.068, 0.912, 0.751]
max_value = [6.000, 5.800, 4.950, 4.000, 3.900, 3.050, 2.450, 2.250, 2.100, 1.700]
min_value = [2.500, 1.950, 1.600, 1.250, 1.100, 0.900, 0.800, 0.650, 0.600, 0.500]
ax1.set_ylabel('(EURO$_{2019}$/W$_p$)')
ax1.plot(years, mean, color='black', linewidth=4,
         marker='o', markerfacecolor='white',markersize=12)
ax1.fill_between(years, max_value, min_value, color=color_1, alpha=0.5)

ax1.set_xlim(2010,2019)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)

plt.savefig('figures/cpst_PV_plants.jpg', dpi=300, bbox_inches='tight')  