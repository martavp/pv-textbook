# -*- coding: utf-8 -*-
"""
@author: Cristobal
"""

import pandas as pd
import matplotlib.pyplot as plt
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


### Define colours
color1 = '#5FA1D8' #ligthblue
color2 = '#B31F20' #darkred


# update font size (to reduce figure size)
params = {'axes.labelsize': 8,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'legend.fontsize': 6}     

plt.rcParams.update(params)




### Read data
data = pd.read_csv('data/merit_order.csv',delimiter='\t')



# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.fill_between(data.Day,data.Price_min,data.Price_max,color=color1,alpha=0.5)
ax.plot(data.Day,data.Price_mean,label='Price mean',color=color1,linewidth=2)

# set axes parameters
ax.set_xlabel("Day", fontsize = 14)
ax.set_ylabel("Electricity price (EUR/MWh)",fontsize=14,color=color1)
ax.set_xlim([1,30])
ax.set_ylim([0,100])
ax.tick_params(axis='y', colors=color1)

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(data.Day,data.Percentage,label='Load',color=color2,linewidth=2)
ax2.set_ylabel("Percentage of solar and wind (%)",fontsize=14,color=color2)
ax2.set_ylim([0,80])
ax2.tick_params(axis='y', colors=color2)


ax.grid()


plt.savefig('figures/merit_order.jpg', dpi=300, bbox_inches='tight')  


