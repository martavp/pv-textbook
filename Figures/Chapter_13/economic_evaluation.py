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

lifetime = 25 #years
capacity = 3 #kW
investment_cost = 1000 #EUR/kW
inverter_cost = 250 #EUR/kW
discount_rate = 0.04 
annual_electricity_generation = 3*1300*0.9 #kWh/a
self_consumption_ratio=0.35
electricity_price = 0.25 #EUR/kWh
data=pd.DataFrame(0, index= np.arange(0,lifetime+1), 
                  columns=['Expenses', 
                           'Revenues', 
                           'Cash flow', 
                           'Discounted cash flow', 
                           'Cumulative discounted cash flow'])

data.loc[0, 'Expenses'] = capacity*investment_cost
data.loc[10, 'Expenses'] = capacity*inverter_cost
data.loc[:, 'Revenues'] = annual_electricity_generation*self_consumption_ratio*electricity_price
data['Cash flow'] = data['Revenues'] - data['Expenses']

for i in data.index:
    data.loc[i, 'Discounted cash flow'] = data.loc[i, 'Cash flow']/(1+discount_rate)**(i+1)
    if i==0:
        data.loc[i, 'Cumulative discounted cash flow'] = data.loc[i, 'Discounted cash flow']
    else:
        data.loc[i, 'Cumulative discounted cash flow'] = (data.loc[i, 'Discounted cash flow'] 
                                                          + data.loc[i-1, 'Cumulative discounted cash flow'])

ax1 = plt.subplot(gs1[0,0])
ax1.bar(data.index, -data['Expenses'], color=colors['color2'])
ax1.bar(data.index, data['Revenues'], color=colors['color8'])

# turn off the right spine/ticks and top spine/ticks
ax1.spines['right'].set_color('none')
ax1.yaxis.tick_left()
ax1.spines['top'].set_color('none')
ax1.xaxis.tick_bottom()
ax1.spines['bottom'].set_position('zero')

ax1.annotate('Expenses \n (EUR)', [-5.5,-2000], fontsize=22, 
             color=colors['color2'], rotation=90, annotation_clip=False)
ax1.annotate('Revenues \n (EUR)', [-5.5, 0], fontsize=22, 
             color=colors['color8'], rotation=90, annotation_clip=False)
ax1.set_ylim([-3000, 500])
ax1.set_xlim([-0.5, 25.5])
ax1.set_xticks(np.arange(1,lifetime-1,2))
ax1.set_xticklabels(np.arange(2,lifetime,2))
ax2 = ax1.inset_axes([0.35, 0.15, 0.6, 0.35])
ax2.plot(data.index, data['Cumulative discounted cash flow'], color='gray', linewidth=3, alpha=0.7)
ax2.set_xticks(np.arange(1,lifetime+1,2))
ax2.set_ylabel('Net Present Value (EUR)')
ax2.set_ylim([-2500, 2500])
ax2.set_xlim([-0.5, 25.5])
ax2.spines['right'].set_color('none')
ax2.yaxis.tick_left()
ax2.spines['top'].set_color('none')
ax2.xaxis.tick_bottom()
ax2.spines['bottom'].set_position('zero')
ax2.annotate('investment \n recovered', xy=(13, 200), xytext=(9.8, 1500), fontsize=16,
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.savefig('figures/economic_evaluation.jpg', dpi=300, bbox_inches='tight')  