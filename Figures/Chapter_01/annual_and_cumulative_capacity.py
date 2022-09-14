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

plt.figure(figsize=(16, 8))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.4, hspace=0.2)

colors={'Hydro': colors['color1'],
        'Nuclear': colors['color2'],
        'Wind': colors['color3'], 
        'Solar': colors['color5'], 
        'Solar PV': colors['color5'], 
        'Coal':colors['color11'], 
        'Gas':colors['color13'],
        'Oil': colors['color12'], 
        'Geo Biomass Other': colors['color14'], 
        }


"""
FIGURE A) ANNUAL AND CUMULATIVE PV CAPACITY
"""

ax1 = plt.subplot(gs1[0,0])
datafile = pd.read_excel('data/bp-stats-review-2021-all-data.xlsx', 
                              sheet_name='Solar Capacity',
                              index_col=0, header=0, squeeze=True) 
 
capacity=0.001*datafile.loc['Total World'][0:24] #MW -> GW
capacity.index=[int(x) for x in datafile.loc['Megawatts'][0:24]]
capacity.loc[2020]=700 #update 2020 capacity
capacity.loc[2021]=900 #update 2020 capacity
annual_capacity=capacity.diff()[1:]


ax1.bar(annual_capacity.index, 
        annual_capacity,
              width=0.8,
              color='black')
ax1.set_ylabel('Solar PV - Annual capacity added (GW/a)')
ax1.set_xticklabels([1990, 1995, 2000, 2005, 2010, 2015, 2020],rotation=70)
ax1.set_ylim(0,210)

ax2=ax1.twinx()
ax2.plot(capacity, 
         color=colors['Solar PV'], 
         linewidth=3)
ax2.set_ylim(0,950)
ax2.spines['right'].set_color(colors['Solar PV'])
ax2.yaxis.label.set_color(colors['Solar PV'])
ax2.tick_params(axis='y', colors=colors['Solar PV'])
ax2.set_ylabel('Solar PV - Cumulative capacity (GW)', color=colors['Solar'])
ax1.grid(color='grey', linestyle='--', axis='y', which='both')

"""
FIGURE B) INSTALLED CAPACITY PER TECHNOLOGY 2009-2019
"""

ax2 = plt.subplot(gs1[0,1])

labels=['Solar PV',
        'Wind',
        'Hydro',
        #'Nuclear', #net additions 2009-2019:-7GW
        'Coal',
        #'Oil', #net additions 2009-2019:-2GW
        'Gas']

sizes = [638, 487, 283, 529, 438]

ax2.pie(sizes, 
        colors=[colors[label] for label in labels], 
        labels=labels, 
        startangle=90, 
        wedgeprops={'linewidth':0})
ax2.set_title('Power generation capacity added (2009-2019)')

plt.savefig('figures/annual_and_cumulative_capacity.jpg', dpi=300, bbox_inches='tight')  