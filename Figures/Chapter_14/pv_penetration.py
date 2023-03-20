# -*- coding: utf-8 -*-
"""
@author: Marta

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


plt.figure(figsize=(16,6))
gs1 = gridspec.GridSpec(1, 2)
gs1.update(wspace=0.15, hspace=0.2)

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
           #'Netherlands',
           'Israel',
           'Hawaii',
           'California',
           'South Australia',           
           'Honduras',
           'Kauai (Hawaii)',
           #'Ta u Island (American Samoa)'
           #'Yemen', #missing data
           'Vietnam',
           #'Italy',
           #'Hungary'
           ]

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
dic_pos={'Total World':[0,0.5],
           'Total Africa':[-550,-1.5],
           'US':[0,-4.5],
           'China':[400,0.5],
           'EU':[0,0.5],
           'India':[-1000,-1.5],
           'Japan':[1300,0],
           'Germany':[0,-4],           
           'Australia':[0,0.5],          
           'Spain':[-60,-4],           
           'Chile':[-45,0.5],
           'Greece':[-38,-2],   
           'Netherlands':[0,0],
           'Israel':[0,-4.5],
           'Hawaii':[-5.5,-1.5],
           'California':[500,-1.5],
           'South Australia':[0,0.5],           
           'Honduras':[-7,-1.5],
           'Kauai (Hawaii)':[0.7,1],
           #'Ta u Island (American Samoa)'
           #'Yemen', #missing data
           'Vietnam':[600,-0.5],
           'Italy':[0,0],
           'Hungary':[0,0],
           }

ax1 = plt.subplot(gs1[0,1])
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
                600,
                alpha=0.6, 
                edgecolor='orange',
                facecolor='orange',
                zorder=1)    

    name=country
    
    if country=='Total World': 
        name='World'
    if country=='Total Africa': 
        name='Africa'
        
    ax1.text(e_2021+dic_pos[country][0], 
             r_2021+1.3+dic_pos[country][1], 
             name,
             ha='center',
             fontsize=14)   
    ax1.text(e_2021, r_2021,
              round(r_2021),
              ha='center',
              va='center',
              fontsize=14)

ax1.set_ylabel('Solar PV share (%)', fontsize=20)    
ax1.set_xlabel('Annual electricity generation (TWh)', fontsize=20)     
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
           'ERCOT(Texas)',
           'ENTSOE'
           ]
dic_pos={'Ta u Island (American Samoa)':[0.3,-5],
           'King Island (Australia)':[0.7,-2],
           'El Hierro':[0,4],
           'Kauai (Hawaii)':[-0.41,1],
           'Maui':[2.5,1],
           'Crete':[0,3.5],
           'Ireland':[10,3],
           'ERCOT(Texas)':[530,0],
           'ENTSOE':[-1500,-11],}
           
ax0 = plt.subplot(gs1[0,0])
for country in countries:
        e_2021 = datam.loc[country,'Annual electricity generation 2021 (TWh)']
        r_2021 = datam.loc[country,'penetration 2021']
        ax0.scatter(e_2021,
                    r_2021,
                    600,
                    alpha=0.6, 
                    edgecolor='green',
                    facecolor='green',
                    zorder=1)    

        name=country
        
            
        ax0.text(e_2021+dic_pos[country][0], 
                 r_2021+1.3+dic_pos[country][1],
                 name,
                 ha='center',
                 fontsize=18)   
        ax0.text(e_2021, r_2021,
                  round(r_2021),
                  ha='center',
                  va='center',
                  fontsize=18)

ax0.set_ylabel('Wind and solar PV share (%)', fontsize=20)    
ax0.set_xlabel('Annual electricity generation (TWh)', fontsize=20) 
ax0.grid(color='grey', linestyle='--', axis='y')
ax0.set_xscale('log')
ax0.set_ylim(0, 102)        
plt.savefig('figures/pv_wind_share.jpg', dpi=300, bbox_inches='tight')  