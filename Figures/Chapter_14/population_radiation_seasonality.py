# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

colors=['orange',
        'dodgerblue',
        'black',]

"""
Necesito:
*mapa con densidad de población
*matriz de reanalisys con datos de radiación para cada
uno de las céldas de 40x40km y con datos horarios 
para un año

"""
plt.figure(figsize=(22, 6))
gs = gridspec.GridSpec(3, 6)
gs.update(wspace=0.1, hspace=0.1)
ax0 = plt.subplot(gs[0:3,0:2])

# Pintar el mapa del mundo, señalar 3 puntos con 
# distintas latitudes 
#ax0.set_title('map')
ax0.set_xticks([])
ax0.set_yticks([])

# Pintar la población sumada por latitud
ax1 = plt.subplot(gs[0:3,2])
ax1.set_title('Population')
ax1.set_xticks([])
ax1.set_yticks([])

# Pintar la radiacón anual en función de la latitud
# (haciendo una media para las distintas longitudes)
ax2 = plt.subplot(gs[0:3,3])
ax2.set_title('Annual Solar \n Radiation')
#ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlabel('kWh/kW')
ax2.set_xlim([0,2400])
for i in range(0,3):
    ax3 = plt.subplot(gs[i,4:6])
    ax3.set_yticks([])
    ax3.set_xlim([0,12])
    ax3.plot([0,12], [1,1], color='grey', linestyle='--')
    if i==0:
        ax3.set_title('Monthly Radiation')
    if i==2:
        ax3.set_xticks([0,2,4,6,8,10])
        ax3.set_xticklabels(['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'])
    else:
        ax3.set_xticks([])
        
plt.savefig('figures/population_radiaton_sesonality.png', 
            dpi=300, bbox_inches='tight')