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


plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
colors={'Hydro': colors['color1'],
        'Nuclear': colors['color2'],
        'Wind': colors['color3'], 
        'Solar': colors['color5'], 
        'Coal':colors['color11'], 
        'Gas':colors['color13'],
        'Oil': colors['color12'], 
        'Geo Biomass Other': colors['color14'], 
        }

h_eq={'Hydro':8000,
      'Nuclear':8000,
      'Coal':8000,
      'Oil':8000,
      'Gas':8000}

#datafile='data/bp-stats-review-2021-all-data.xlsx'
datafile= 'data/Statistical Review of World Energy Data.xlsx'
for tech in ['Coal', 'Gas', 'Hydro', 'Nuclear', 
              'Wind', 'Solar']: # 'Geo Biomass Other', 'Oil',
    if tech in ['Wind']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} Installed Capacity'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Megawatts'][0:27]
        global_generation_2019 = 1429.6 #TWh
        global_capacity_2019 = 622704 # MW
        energy=excel.loc['Total World'][0:27]*global_generation_2019/global_capacity_2019  #MW -> TWh
    if tech in ['Geo Biomass Other']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Terawatt-hours'][0:58]

        energy=excel.loc['Total World'][0:58] #TWh

    if tech in ['Nuclear', 'Hydro', 'Solar']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} Generation - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True)
        years=excel.loc['Terawatt-hours'][0:59]

        energy=excel.loc['Total World'][0:59] #TWh 

    if tech in ['Coal', 'Oil', 'Gas']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} inputs - Elec generation'.format(tech),
                              index_col=0, header=0, squeeze=True)        
        years=excel.loc['Terawatt-hours'][0:39]

        energy=excel.loc['Total World'][0:39] #TWh

    label='Solar PV' if tech=='Solar' else tech
    ax1.semilogy(years, energy, linewidth=3, linestyle='-',
                  color=colors[tech], label=label)

ax1.set_ylabel('Global electricity generation (TWh)', fontsize=18)
ax1.grid(color='grey', linestyle='--', axis='y', which='both')
ax1.set_ylim(10, 11000)
ax1.set_xlim(1968, 2025)
ax1.text(2009, 15, 'Solar PV', color=colors['Solar'], fontsize=16)
ax1.text(1990, 15, 'Wind', color=colors['Wind'], fontsize=16)
ax1.text(1975, 220, 'Nuclear', color=colors['Nuclear'], fontsize=16)
ax1.text(1990, 5000, 'Coal', color=colors['Coal'], fontsize=16)
ax1.text(1970, 1500, 'Hydro', color=colors['Hydro'], fontsize=16)
ax1.text(1990, 1400, 'Gas', color=colors['Gas'], fontsize=16)

plt.savefig('figures/historical_energy_generation_expansion.jpg', dpi=300, bbox_inches='tight')  