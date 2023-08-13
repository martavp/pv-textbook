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

plt.figure(figsize=(10, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)
color_1=colors['color5']

ax1 = plt.subplot(gs1[0,0])

hours=np.arange(0,24)
# https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html#HR
static = [0, 0, 0, 0, 0, 4.99, 36.82, 198.27, 385.42, 531.1, 636.27, 706.06,
          728.24, 702.72, 637.47, 520.59, 370.3, 182.34, 37.49, 11.9, 0, 0, 0, 0, ]
#1-axis horizontal tracking
tracking = [0, 0, 0, 0, 0, 1.22, 501.45, 647.53, 699.57, 713.06, 716.38, 719.62,
            718.03,716.98, 723.59, 712.44, 700.44, 613.9, 482.97, 226.61, 0, 0, 0, 0]
#https://www.esios.ree.es
demand =[23811, 22272, 21340, 20727, 20638, 20977, 22707, 24672, 26679, 28774, 
         30035, 30701, 31639, 32359, 31973, 30850, 30635, 30530, 30359, 30083, 
         29758, 29394, 28878, 26876, ]

ax1.set_ylabel('normalized PV generation and \n normalized electricity demand ',
               fontsize=22)

ax1.plot(hours, tracking/np.max(static), 
         color=colors['color5'], 
         linewidth=4,
         label='HSAT')

ax1.fill_between(hours, tracking/np.max(static), 
                 color=colors['color5'], 
                 alpha=0.6,
                 linewidth=4,
                 label=None)

ax1.plot(hours, static/np.max(static), 
         color=colors['color4'], 
         linewidth=4,
         linestyle='--', 
         label='fixed structure')

ax1.fill_between(hours, static/np.max(static), 
         color=colors['color4'], 
         alpha=0.6,
         linewidth=4,
         linestyle='--', 
         label=None)

ax1.plot(hours, demand/np.max(demand), color='black', linewidth=4,
         label='electricity demand')

ax1.set_xlim(2,22)
ax1.set_ylim(0,1)
ax1.set_xticks(np.arange(2,24,2))
ax1.set_xticklabels(['02:00', '04:00', '06:00', '08:00', '10:00', 
                     '12:00', '14:00', '16:00', '18:00', '20:00', '22:00',], 
                    rotation=45)
ax1.yaxis.grid('--')

ax1.legend(fancybox=False, fontsize=18, loc='best', 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('figures/static_tracking_demand.jpg', dpi=300, bbox_inches='tight')  