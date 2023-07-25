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


V_measured = [0.00, 144.67, 332.24, 525.33, 577.72, 612.16, 660.31, 693.25, 
              723.36, 746.59, 779.31]

I_measured = [710.77,707.69, 698.46, 692.31, 680.00, 652.31, 581.54, 483.08, 
              350.77, 221.54, 0.00]

V_extrapolated = [1.38, 96.54, 246.88,406.87, 601.34, 667.51, 707.43, 730.81, 
                  756.88, 777.40, 800.63, 819.70, 833.26, 845.52]

I_extrapolated = [800.00, 793.85, 790.77, 784.62, 775.38, 756.92, 710.77, 
                  667.69, 590.77, 492.31, 366.15, 227.69, 92.31, 0.00]

plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.4, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
ax1.plot(V_measured, I_measured, label='measured',
           linewidth=3, color=colors['color1'],)
ax1.plot(V_extrapolated, I_extrapolated, label='extrapolated to STC (IEC-60691)',
           linewidth=3, color=colors['color2'],)
ax1.set_ylabel('Current (A)')
ax1.set_xlabel('Voltage (V)')
ax1.set_ylim(0, 900)
ax1.set_xlim(0, 900)
ax1.grid()

ax1.legend(fancybox=False, fontsize=18, loc='best', 
                   facecolor='white', ncol=1, frameon=True)
plt.savefig('Figures/IVcurve_extrapolated.jpg', dpi=300, bbox_inches='tight')