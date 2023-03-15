# -*- coding: utf-8 -*-
"""
@author: Marta

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


plt.figure(figsize=(12,12))
gs1 = gridspec.GridSpec(2, 1)
gs1.update(wspace=2, hspace=0.2)

#retrieve data from BP
data=pd.read_csv('data/bp-stats-review-2022-consolidated-dataset-panel-format.csv',
               index_col=-1, header=0)[['Country','Year','elect_twh','solar_twh']]
data.set_index(['Country','Year'], inplace=True)

#retrive manual data
datam=pd.read_csv('data/pv_penetration_manual.csv', index_col=0, header=0)

countries=['Total World',
           'Total Africa',
           'US',
           'China',
           'EU',
           'India',
           'Japan',
           'Germany',           
           'Australia',           
           'Spain',           
           'Chile',
           'Greece',   
           'Netherlands',
           'Israel',
           'Hawaii',
           'California',
           'South Australia',           
           'Honduras',
           'Kauai (Hawaii)',
           #'Ta u Island (American Samoa)'
           #'Yemen', #missing data
           'Vietnam',
           'Italy',
           'Hungary']

countries_BP=['Total World',
              'Total Africa',
              'US',
              'China',
              'India',
              'Japan',
              'Germany',           
              'Australia',           
              'Spain',  
              'Netherlands', 
              'Israel',
              'Chile',
              'Australia',
              'Greece',
              #'United Kingdom', 
              'Yemen',
              'Vietnam',
              'Italy',
              'Hungary'] 

countries_ins=['Germany',
               'California',
               'Spain',
               'South Australia'
               ]


ax1 = plt.subplot(gs1[1,0])
for country in countries:
    if country in countries_BP:
        e_2021 = data.loc[(country,2021),'elect_twh']
        e_2010 = data.loc[(country,2010),'elect_twh']
        r_2021 = 100*data.loc[(country,2021),'solar_twh']/data.loc[(country,2021),'elect_twh']
        r_2010 = 100*data.loc[(country,2010),'solar_twh']/data.loc[(country,2021),'elect_twh']
    else:
        e_2021 = datam.loc[country,'Annual electricity generation 2021 (TWh)']
        e_2010 = datam.loc[country,'Annual electricity generation 2010 (TWh)']
        r_2010 = datam.loc[country,'penetration 2010']
        r_2021 = datam.loc[country,'penetration 2021']
        
    ax1.scatter(e_2021,
                r_2021,
                400,
                alpha=0.6, 
                edgecolor='orange',
                facecolor='orange',
                zorder=1)    

    name=country
    
    if country=='Total World': 
        name='World'
    if country=='Total Africa': 
        name='Africa'
        
    ax1.text(e_2021, r_2021+1.3,
             name,
             ha='center',
             fontsize=14)   
    ax1.text(e_2021, r_2021,
              round(r_2021),
              ha='center',
              va='center',
              fontsize=14)

ax1.set_ylabel('Solar PV share (%)')    
ax1.set_xlabel('Annual electricity generation (TWh)') 
ax1.grid(color='grey', linestyle='--', axis='y')
ax1.set_xscale('log')
ax1.set_ylim(0, 40)

#retrive manual data
datam=pd.read_csv('data/wind_pv_penetration_manual.csv', index_col=0, header=0)
countries=['Ta u Island (American Samoa)',
           'King Island (Australia)',
           'El Hierro',
           'Kauai (Hawaii)',
           'Maui',
           'Crete',
           'Ireland',
           'ERCOT (Texas)',
           'ENTSOE'
           ]
ax0 = plt.subplot(gs1[0,0])
for country in countries:
        e_2021 = datam.loc[country,'Annual electricity generation 2021 (TWh)']
        r_2021 = datam.loc[country,'penetration 2021']
        ax0.scatter(e_2021,
                    r_2021,
                    400,
                    alpha=0.6, 
                    edgecolor='green',
                    facecolor='green',
                    zorder=1)    

        name=country
        
            
        ax0.text(e_2021, r_2021+1.3,
                 name,
                 ha='center',
                 fontsize=14)   
        ax0.text(e_2021, r_2021,
                  round(r_2021),
                  ha='center',
                  va='center',
                  fontsize=14)

ax0.set_ylabel('Wind and solar PV share (%)')    
ax0.set_xlabel('Annual electricity generation (TWh)') 
ax0.grid(color='grey', linestyle='--', axis='y')
ax0.set_xscale('log')
ax0.set_ylim(0, 102)        
plt.savefig('figures/pv_wind_share.jpg', dpi=300, bbox_inches='tight')  