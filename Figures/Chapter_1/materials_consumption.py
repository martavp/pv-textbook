# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import squarify

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.family'] = 'avenir'
plt.rcParams['axes.titlesize'] = 18

plt.figure(figsize=(13, 5))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.6, hspace=0.2)

"""
FIGURE A. GLASS-BACKSHEET MODULE
"""
ax1 = plt.subplot(gs1[0,0])

sizes=[40.416,
       7.629,
       2.951,
       0.025,
       0.133,]

labels=['Glass \n 40.4 g/W', 
        'Aluminum \n 7.6 g/W',
        'Silicon \n 2.9 g/W',
        '',
        '',]
colors=['dodgerblue',
        'firebrick',
        'yellowgreen',
        'black',
        'black',]

ax1.annotate('Backsheet 0.133 g/W \n Silver 0.025 g/W', 
             xy=(100,100), 
             xytext=(105,85),
             arrowprops=dict(arrowstyle="->"))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.6)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_title('Glass-backsheet module', fontsize=16)



"""
FIGURE B. GLASS-GLASS MODULE
"""
ax2 = plt.subplot(gs1[0,1])

sizes=[50.52,
       2.951,
       0.025]

labels=['Glass \n 40.4 g/W', 
        'Silicon \n 2.9 g/W',
        '']

colors=['dodgerblue',
        'yellowgreen',
        'black']

ax2.annotate('Silver 0.025 g/W', 
             xy=(100,100), 
             xytext=(105,85),
             arrowprops=dict(arrowstyle="->"))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.6)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title('Glass-glass module', fontsize=16)


plt.savefig('figures/materials_consumption.jpg', dpi=300, bbox_inches='tight')  