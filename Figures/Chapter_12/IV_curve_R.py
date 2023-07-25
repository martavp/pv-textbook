# -*- coding: utf-8 -*-
"""
@author: Marta
"""

#import pandas as pd
import numpy as np
from pvlib import pvsystem
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
IL =0.042  #A
I0 = 10**(-13) #A
Rs = 0
Rsh = 10**(13)
nNsVth = 1*1*0.025 # =25C
IVcurve = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=100,
    method='lambertw'
)

plt.figure(figsize=(6, 6))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
ax1.plot(np.concatenate(([-0.1],IVcurve['v'],[0.675])), 
         np.concatenate(([0.042],IVcurve['i'],[-0.011])),
           linewidth=4, color=colors['color1'],)

ax1.plot([0,0.8],          
         [0,0.045],
         linewidth=3, color=colors['color2'],)

ax1.plot([0,0.8],          
         [0,0.02],
         linewidth=3, color=colors['color2'],)

ax1.plot([0,0.8],          
         [0,0.1],
         linewidth=3, color=colors['color2'],)

ax1.plot([0,0.8],          
         [0,0.45],
         linewidth=3, color=colors['color2'],)

ax1.set_ylabel('Current (A)')
ax1.set_xlabel('Voltage (V)')
ax1.set_ylim(-0.011,0.050)
ax1.set_xlim(-0.1, 0.75)


ax1.vlines(0,-0.01, 0.05, linestyles='dotted', color='black')
ax1.hlines(0,-0.1, 0.75, linestyles='dotted', color='black')
ax1.text( -0.01, 0.041, 'x', fontsize=18, weight='bold')
ax1.text( 0.01, 0.045, '$I_{sc}$', fontsize=18, weight='bold')
ax1.text( 0.655, -0.001, 'x', fontsize=18, weight='bold')
ax1.text( 0.58, 0.002, '$V_{oc}$', fontsize=18, weight='bold')
ax1.text( 0.575, 0.0395, 'x', fontsize=18, weight='bold')
ax1.text( 0.58, 0.042, '$P_{max}$', fontsize=18, weight='bold')
ax1.text( 0.06, 0.03, '$R_{1}$', fontsize=18, weight='bold', color=colors['color2'])
ax1.text( 0.24, 0.027, '$R_{2}$', fontsize=18, weight='bold', color=colors['color2'])
ax1.text( 0.47, 0.023, '$R_{3}$', fontsize=18, weight='bold', color=colors['color2'])
ax1.text( 0.55, 0.011, '$R_{4}$', fontsize=18, weight='bold', color=colors['color2'])

plt.savefig('Figures/IVcurve_R.jpg', dpi=300, bbox_inches='tight')