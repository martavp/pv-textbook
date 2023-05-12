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
V_measured = [0.0,106.2,135.2,160.0,186.2,
              223.4,259.3,295.2,322.8,353.1,382.1,409.7,444.1,
              478.6,509.0,537.9,560.0,583.4,609.7,634.5,651.0,
              666.2,680.0, 692.4,706.2,717.2,729.7,740.7,754.5,
              764.1,772.4,780.7]

I_measured = [713.2,713.2,713.2,707.0,707.0,
              703.9,703.9,703.9,703.9,703.9,700.8,697.7,694.6,
              694.6,694.6,694.6,691.5,676.0,660.5,629.5,598.4,
              567.4,530.2,483.7,424.8,365.9,313.2,254.3,176.7,
              108.5,52.7,0]

V_extrapolated =[1.4,22.1,55.2,91.0,132.4,175.2,217.9,257.9,
                 292.4,346.2,402.8,446.9,502.1,557.2,606.9,
                 635.9,660.7,726.9,746.2,758.6,769.7,787.6,
                 802.8,819.3,829.0,838.6,846.9
]

I_extrapolated =[806.2,803.1,803.1,800.0,800.0,796.9,796.9,
                 790.7,790.7,790.7,787.6,784.5,784.5,781.4,
                 781.4,775.2,765.9,679.1,632.6,582.9,530.2,
                 446.5,341.1,235.7,145.7,55.8,-3.1]

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