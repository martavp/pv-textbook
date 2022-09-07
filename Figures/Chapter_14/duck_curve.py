# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

colors=['orange',
        'dodgerblue',
        'black',]



plt.figure(figsize=(6, 6))
gs = gridspec.GridSpec(1, 1)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0,0])
ax0.set_title('Residual load = Demand - Solar')
ax0.set_ylabel('GW')
ax0.set_xlabel('hour')
ax0.set_xticks(np.arange(0,24,2))
#ax0.set_xticklabels(['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'])

plt.savefig('figures/duck_curve.png', 
            dpi=300, bbox_inches='tight')