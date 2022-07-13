# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import squarify
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
plt.figure(figsize=(13, 5))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.6, hspace=0.2)

"""
FIGURE A. GLASS-BACKSHEET MODULE
"""
ax1 = plt.subplot(gs1[0,0])

sizes=[40.416,
       7.629,
       5.0,
       2.951,
       0.025,
       0.133,]

labels=['Glass \n 40.4 g/W', 
        'Aluminum \n 7.6 g/W',
        'EVA \n 5.0 g/W',
        'Silicon \n 2.9 g/W',
        '',
        '',]

cols=[colors['color1'],
        colors['color2'],
        colors['color8'],
        colors['color5'],
        'black',
        'black',]

ax1.annotate('Backsheet 0.133 g/W \n Silver 0.025 g/W',
             fontsize=16,
             xy=(100,100), 
             xytext=(102,85),
             arrowprops=dict(arrowstyle="->"))
squarify.plot(sizes=sizes, label=labels, color=cols, alpha=0.6,
              text_kwargs={'fontsize':16})
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_title('Glass-backsheet module')



"""
FIGURE B. GLASS-GLASS MODULE
"""
ax2 = plt.subplot(gs1[0,1])

sizes=[50.52,
       5.0,
       2.951,
       0.025]

labels=['Glass \n 40.4 g/W',
        'EVA \n 5.0 g/W',
        'Silicon \n 2.9 g/W',
        '']


cols=[colors['color1'],
        colors['color8'],
        colors['color5'],
        'black']


ax2.annotate('Silver 0.025 g/W',
             fontsize=16,
             xy=(100,100),
             xytext=(105,85),
             arrowprops=dict(arrowstyle="->"))
squarify.plot(sizes=sizes, label=labels, color=cols, alpha=0.6,
              text_kwargs={'fontsize':16})
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title('Glass-glass module')


plt.savefig('figures/materials_consumption.jpg', dpi=300, bbox_inches='tight')  