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
    
plt.figure(figsize=(12, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

colors={'Hydro': colors['color1'],
        'Nuclear': colors['color2'],
        'Wind': colors['color3'], 
        'CSP-Central tower': colors['color4'],
        'Solar PV-rooftop': colors['color5'], 
        'Solar PV-utility scale': colors['color5'], 
        'Coal':colors['color11'], 
        'Gas':colors['color13'],
        'Oil': colors['color12'], 
        'Biomass': colors['color14'], 
        'Geothermal': colors['color15'] }

techs=[
       'Coal',
       # 'Oil',
       'Gas',
       # 'Biomass',
       'Nuclear',
       # 'Hydro',
       'Geothermal',
       'Wind',
       'CSP-Central tower',
       'Solar PV-utility scale',
       'Solar PV-rooftop']

LCOE={'Solar PV-rooftop':(147,221), 
      'Solar PV-utility scale':(28,41), 
      'CSP-Central tower':(126,156),
      'Wind': (26,50),
      #'Biomass':,
      'Geothermal':(56,93),
      #'Hydro':,
      'Nuclear':(131,204),
      'Gas':(151,196),
      #'Oil':,
      'Coal':(65,152)}

ax1 = plt.subplot(gs1[0,0])
for i,tech in enumerate(techs):
    ax1.barh(i,LCOE[tech][1]-LCOE[tech][0],
             left=LCOE[tech][0],
             height=0.5,
             color=colors[tech])
    ax1.text(LCOE[tech][1]+1, i-0.15, LCOE[tech][1], fontsize=16)
    ax1.text(LCOE[tech][0]-10, i-0.15, LCOE[tech][0], fontsize=16)
ax1.set_xlim(0,250)
ax1.set_xlabel('Levelized Cost of Electricity, LCOE (USD/MWh)')
ax1.set_yticks(range(0,len(techs)))
ax1.set_yticklabels(techs)
ax1.grid(color='grey', linestyle='--', axis='x', which='both')

plt.savefig('figures/LCOE_technologies.jpg', dpi=300, bbox_inches='tight')  