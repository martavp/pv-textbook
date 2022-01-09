# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
colors={'Solar': 'darkorange',
        'Wind': 'yellowgreen',
        'Geo Biomass Other': 'peru',
        'Hydro':'dodgerblue',
        'Nuclear': 'firebrick',
        'Coal':'black',
        'Oil': 'dimgray',
        'Gas':'gray'}
h_eq={'Hydro':8000,
      'Nuclear':8000,
      'Coal':8000,
      'Oil':8000,
      'Gas':8000}
datafile='data/bp-stats-review-2021-all-data.xlsx'
for tech in ['Coal', 'Gas', 'Hydro', 'Nuclear', 
              'Wind', 'Solar']: # 'Geo Biomass Other', 'Oil',
    if tech in ['Wind']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} Capacity'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Megawatts'][0:25]
        global_generation_2019 = 1429.6 #TWh
        global_capacity_2019 = 622704 # MW
        energy=excel.loc['Total World'][0:25]*global_generation_2019/global_capacity_2019  #MW -> TWh

    if tech in ['Geo Biomass Other']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Terawatt-hours'][0:56]
        energy=excel.loc['Total World'][0:56] #TWh

    if tech in ['Nuclear', 'Hydro', 'Solar']:
        excel = pd.read_excel(datafile, 
                              sheet_name='{} Generation - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True)
        years=excel.loc['Terawatt-hours'][0:56]
        energy=excel.loc['Total World'][0:56] #TWh 

    if tech in ['Coal', 'Oil', 'Gas']:
        excel = pd.read_excel(datafile, 
                              sheet_name='Elec Gen from {}'.format(tech),
                              index_col=0, header=0, squeeze=True)
        years=excel.loc['Terawatt-hours'][0:36]
        energy=excel.loc['Total World'][0:36] #TWh

    label='Solar PV' if tech=='Solar' else tech
    ax1.semilogy(years, energy, linewidth=3, linestyle='-',
                  color=colors[tech], label=label)

ax1.set_ylabel('Global electricity generation (TWh)', fontsize=18)
ax1.grid(color='grey', linestyle='--', axis='y', which='both')
ax1.set_ylim(10, 11000)
ax1.set_xlim(1968, 2022)
ax1.text(2009, 15, 'Solar PV', color=colors['Solar'], fontsize=16)
ax1.text(1990, 15, 'Wind', color=colors['Wind'], fontsize=16)
ax1.text(1975, 220, 'Nuclear', color=colors['Nuclear'], fontsize=16)
ax1.text(1990, 5000, 'Coal', color=colors['Coal'], fontsize=16)
ax1.text(1970, 1500, 'Hydro', color=colors['Hydro'], fontsize=16)
ax1.text(1990, 1400, 'Gas', color=colors['Gas'], fontsize=16)

plt.savefig('figures/historical_energy_generation_expansion.jpg', dpi=300, bbox_inches='tight')  