# -*- coding: utf-8 -*-
"""
@author: Cristobal
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])


# update font size (to reduce figure size)
params = {'axes.labelsize': 9,
          'xtick.labelsize': 9,
          'ytick.labelsize': 9,
          'legend.fontsize': 9}     

plt.rcParams.update(params)




### Define figure and axes size
figure_width = 12 # cm
figure_height = 7 # cm

left_margin = 1 # cm
right_margin = 3.5 #cm
top_margin = .2 # cm
bottom_margin = .8 # cm

left    = left_margin / figure_width # Percentage from height
right   = right_margin / figure_width # Percentage from height
top     = top_margin / figure_height # Percentage from height
bottom  = bottom_margin / figure_height # Percentage from height

width  = 1 - left - right
height = 1 - top - bottom

cm2inch = 1/2.54 # inch per cm

fig = plt.figure(figsize=(figure_width*cm2inch,figure_height*cm2inch))
ax = fig.add_axes((left, bottom, width, height))


### Read data
data = pd.read_csv('data/selfconsumption.csv',delimiter='\t')


### Create hours vector
x = np.arange(1, 25)


### Plot
plt.plot(x,data.load,'k-',label='Load',linewidth=2)
plt.fill_between(x,data.load,edgecolor='k',linewidth=.5,label='Imported from the grid')
plt.fill_between(x,data.PV,0,edgecolor='k',linewidth=.5,label='PV generation')
plt.fill_between(x,data.exported,edgecolor='k',linewidth=.5,label='Exported to the grid')
plt.fill_between(x,data.bat_in,edgecolor='k',linewidth=.5,label='Battery charge')
plt.fill_between(x,data.bat_out,data.load,edgecolor='k',linewidth=.5,label='Battery discharge')


### Axes
plt.xlim([0.8, 24.2])
plt.xticks(ticks=[4,8,12,16,20,24])
plt.xlabel('Hour')
plt.ylabel('kW')



### Set legend out of the box
plt.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left')



plt.rcParams['xtick.labelsize'] = 10


plt.savefig('figures/selfconsumption.jpg', dpi=300, bbox_inches='tight') 



