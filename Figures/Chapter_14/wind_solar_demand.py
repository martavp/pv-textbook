# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
import matplotlib.colors as colorss
import numpy as np
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)

colors=[colors['color5'],
        colors['color1'],
        'black',
        colors['color2'],]

country='DEU' # 'California' #'DEU'#'DNK'
if country=='California':
   CF_country=pd.read_csv('data/time-series/time-series-{}.csv'.format(country),
                     sep=',', index_col=0)
   
   CF_pv=CF_country['solar']
   CF_pv.index=pd.to_datetime(CF_pv.index)
   #datetime index is in UCT, California is in US/Pacific (UCT-7)
   CF_pv.index=CF_pv.index.tz_localize('UCT',nonexistent='shift_forward', ambiguous=True).tz_convert('US/Pacific')

   CF_wind=CF_country['onwind']
   CF_wind.index=pd.to_datetime(CF_wind.index)
   CF_wind.index=CF_wind.index.tz_localize('UCT',nonexistent='shift_forward', ambiguous=True).tz_convert('US/Pacific')


   
   # https://zenodo.org/record/5348396#.ZA9nRB_MK5c
   demand_USA=pd.read_csv('data/hourly-electricity-demand-by-state/demand.csv',
                          sep=',', index_col=0)
   demand_CA=demand_USA[demand_USA.index==6] #6 is the 2-digit FIPS state code for California
   demand_CA.set_index('utc_datetime', inplace=True)
   demand_CA.index = pd.to_datetime(demand_CA.index)
   demand_CA.index=demand_CA.index.tz_localize('UCT',nonexistent='shift_forward', ambiguous=True).tz_convert('US/Pacific')

   t_0 = pd.to_datetime('2011-01-01 00:00:00').tz_localize('UCT')
   t_f = pd.to_datetime('2011-12-31 23:00:00').tz_localize('UCT')
   demand = demand_CA.loc[t_0:t_f, 'scaled_demand_mwh']
   data_dic={'solar': CF_pv,
             'wind': CF_wind,
             'demand':demand/max(demand) }
else:
    #import electricity demand data, in MWh
    demand=pd.read_csv('data/electricity_demand.csv', 
                       sep=';', index_col=0)/1000 #MWh -> GWh
    demand.index=pd.to_datetime(demand.index)

    CF_pv=pd.read_csv('data/pv.csv',
                      sep=';', index_col=0)
    CF_pv.index=pd.to_datetime(CF_pv.index)

    CF_onwind=pd.read_csv('data/onshore_wind.csv',
                      sep=';', index_col=0)
    CF_onwind.index=pd.to_datetime(CF_onwind.index)

    data_dic={'solar': CF_pv[country],
              'wind': CF_onwind[country],
              'demand': demand[country]/max(demand[country])}

   
plt.figure(figsize=(15, 13))
gs = gridspec.GridSpec(3, 4)
gs.update(wspace=0.05, hspace=0.05)

ylabel_dic={'solar': 'CF solar PV',
          'wind': 'CF wind',
          'demand': 'normalized demand'}
letter=[['a)', 'e)', 'i)'],['b)', 'f)', 'j)'],
        ['c)', 'g)', 'k)'],['d)', 'h)', 'l)']]

for i,data in enumerate(['solar', 'wind', 'demand']):
    ax0 = plt.subplot(gs[i,0])
    ax0.text(.01, .99, letter[0][i], 
                 ha='left',
                 va='top', 
                 transform=ax0.transAxes,
                 fontsize=18)
    ax0.plot(data_dic[data], 
             color=colors[i])
    ax0.plot(data_dic[data].groupby(pd.Grouper(freq='W')).mean(), 
             color='grey', 
             linewidth=3)
    ax0.set_ylabel(ylabel_dic[data])
    ax0.set_ylim([0,1])
    ax1 = plt.subplot(gs[i,1])
    ax1.text(.01, .99, letter[1][i], 
                 ha='left',
                 va='top', 
                 transform=ax1.transAxes,
                 fontsize=18)
    
    ax1.plot(data_dic[data].iloc[4468:4468+168],# [4468:4636]
             color=colors[i],
             linewidth=2)
    plt.xticks(rotation=0)
    ax1.set_ylim([0,1])
    ax1.set_yticklabels([])
    ax2 = plt.subplot(gs[i,2])
    ax2.text(.01, .99, letter[2][i], 
                 ha='left',
                 va='top', 
                 transform=ax2.transAxes,
                 fontsize=18)
    ax2.plot(data_dic[data].sort_values(ascending=False).values, 
             color=colors[i],
             linewidth=2)
    
    ax2.set_yticklabels([])
    ax2.set_ylim([0,1])
    ax2.set_xlim([0,8870])
    ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
    ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
    ax2.set_xticks([2000, 4000, 6000, 8000])
    
    if i==0:
        ax0.set_title('1 year')
        ax1.set_title('1 week in June')
        ax2.set_title('Duration curve')
        ax2.set_xticklabels([])
    if i==2:
        ax2.set_xlabel('hours')
        ax0.set_xticks(data_dic[data].index[np.arange(0,4)*24*121])
        ax0.set_xticklabels(['Jan', 'May', 'Sep', 'Dec'])
        ax1.set_xticks(data_dic[data].index[np.arange(0,7)*24+4468+12])
        ax1.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
        #ax2.set_xticks([2000, 4000, 6000, 8000])
        
    else:
        ax0.set_xticklabels([])
        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
        
    ax3 = plt.subplot(gs[i,3])
    ax3.text(.01, .99, letter[3][i], 
                 ha='left',
                 va='top', 
                 transform=ax3.transAxes,
                 fontsize=18)
    
    cmap_list=[cm.Oranges, cm.Blues, cm.Greys]
    cmap=cmap_list[i]
    norm=colorss.Normalize(0, 1)

    if i==0:
        ax3.set_title('Heat map')
    if i==2:
        ax3.set_xticks([3, 6, 9, 12, 15, 18, 21 ])
        ax3.set_xticklabels(['03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'], rotation=90)
    else:
        ax3.set_xticks([])
    ax4=ax3.twinx()
    ax3.set_yticks([])
    ax4.set_yticks([4,361])
    ax4.set_yticks([30*1+15, 30*3+15, 30*5+15, 30*7+15, 30*9+15, 30*11+15])
    ax4.set_yticklabels(['Nov', 'Sep', 'Jul','May', 'Mar', 'Jan'])
    ax3.pcolor(np.array(data_dic[data]).reshape((365,24)), cmap=cmap, norm=norm)
    ax3.set_ylim(ax3.get_ylim()[::-1]) #reverse y axis
    # ax11 = plt.subplot(gs1[0:2,20])
    # cb1=mpl.colorbar.ColorbarBase(ax11, cmap=cmap, norm=norm, orientation='vertical')
    
plt.savefig('figures/wind_solar_demand_{}.tif'.format(country), dpi=300, bbox_inches='tight')

#%%
"""
Mismatch figure
"""
if country != 'California':
    demand=demand[country]
G_pv=0.5*np.mean(demand)/np.mean(data_dic['solar'])
G_onwind=0.5*np.mean(demand)/np.mean(data_dic['wind'])
mismatch = G_pv*data_dic['solar']+G_onwind*data_dic['wind'] - demand

plt.figure(figsize=(12, 4))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.05, hspace=0.05)
ax0 = plt.subplot(gs[0,0])
ax0.text(.01, .99, 'a)', 
             ha='left',
             va='top', 
             transform=ax0.transAxes,
             fontsize=18)
ax0.plot(mismatch, 
         color=colors[3])
ax0.set_ylabel('Mismatch (GWh)')
ax0.plot(mismatch.groupby(pd.Grouper(freq='W')).mean(), 
         color='grey', 
         linewidth=3)

ax1 = plt.subplot(gs[0,1])
ax1.text(.01, .99, 'b)', 
             ha='left',
             va='top', 
             transform=ax1.transAxes,
             fontsize=18)
ax1.plot(mismatch.iloc[4468:4468+168],
         color=colors[3],
         linewidth=2)
plt.xticks(rotation=0)

ax2 = plt.subplot(gs[0,2])
ax2.text(.01, .99, 'c)', 
             ha='left',
             va='top', 
             transform=ax2.transAxes,
             fontsize=18)
ax2.plot(mismatch.sort_values(ascending=False).values, 
         color=colors[3],
         linewidth=2)

ax2.set_xlim([0,8870])
if country=='DEU':
    ax0.set_ylim([-80,180])
    ax1.set_ylim([-80,180])
    ax2.set_ylim([-80,180])

if country=='California':
    ax0.set_ylim([-40000,80000])
    ax1.set_ylim([-40000,80000])
    ax2.set_ylim([-40000,80000])
    
ax1.set_yticklabels([])
ax2.set_yticklabels([])
ax0.axhline(y = 0.5, color = 'gray', linestyle = '--')
ax1.axhline(y = 0.5, color = 'gray', linestyle = '--')
ax2.axhline(y = 0.5, color = 'gray', linestyle = '--')
# ax0.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
# ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1])

ax0.set_title('1 year')
ax1.set_title('1 week in June')
ax2.set_title('Duration curve')

ax2.set_xlabel('hours')
ax0.set_xticks(data_dic[data].index[np.arange(0,4)*24*121])
ax0.set_xticklabels(['Jan', 'May', 'Sep', 'Dec'])
ax1.set_xticks(mismatch.index[np.arange(0,7)*24+4468+12])
ax1.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
ax2.annotate('curtailment', (9500, 40), 
             annotation_clip=False, 
             rotation=90,
             fontsize=16,
             color='dimgray')

ax2.annotate('backup \n energy', (9500, -70), 
             annotation_clip=False, 
             rotation=90,
             fontsize=16,
             color='dimgray')


ax2.annotate('', xy=(1.05, 0.3), 
             xycoords='axes fraction', xytext=(1.05, 1),
             arrowprops=dict(arrowstyle="<->",
                             color='dimgray',
                             lw=2))
ax2.annotate('', xy=(1.05, 0.3), 
             xycoords='axes fraction', xytext=(1.05, 0),
             arrowprops=dict(arrowstyle="<->",
                             color='dimgray',
                             lw=2))
plt.savefig('figures/mismatch_{}.tif'.format(country), dpi=300) #, bbox_inches='tight')
#%%
"""
Wind and solar seasonal complementarity figure
"""

label_country={'DEU':'Germany',
               'DNK':'Denmark',
               'ESP':'Spain',
               'California':'California'}

plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 1)
gs.update(wspace=0.05, hspace=0.05)

ax0 = plt.subplot(gs[0,0])
for i,data in enumerate(['solar', 'wind', 'demand']):
    norm_data=data_dic[data]/data_dic[data].mean()
    ax0.plot(norm_data.groupby(pd.Grouper(freq='W')).mean(), 
         color=colors[i], alpha=1, linewidth=3, label=data)

#Add dotted horizontal line
ax0.set_ylim([0.2,2.2])
ax0.set_yticks([0.5, 1, 1.5, 2])
ax0.set_xlim((data_dic['demand'].index[0], data_dic['demand'].index[-1]))
ax0.set_xticks(data_dic['demand'].index[24*15+np.arange(0,6)*24*60])
ax0.set_xticklabels(['Jan', 'Mar', 'May',  'Jul', 'Sep', 'Nov'])
#ax0.set_ylabel(label_country[country])

ax0.legend(fancybox=False, fontsize=18, loc='upper center',
           facecolor='white', ncol=3, frameon=True)
plt.savefig('figures/wind_solar_complementarity_{}.tif'.format(country), dpi=300, bbox_inches='tight')












