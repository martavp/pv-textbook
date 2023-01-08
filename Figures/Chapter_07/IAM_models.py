# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 10:40:02 2023

@author: cesar
"""

from pvlib import iam
import numpy as np
import matplotlib.pyplot as plt

#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
aoi = np.arange(0, 91)
iam_physical= iam.physical(aoi, n=1.3, K=4.0, L=0.003)
iam_ASHRAE= iam.ashrae(aoi,b=0.05)
iam_Martin_Ruiz = iam.martin_ruiz(aoi, a_r=0.16)

plt.plot(aoi, iam_physical, '.', label='Physical model')
plt.plot(aoi, iam_ASHRAE, label='ASHRAE model')
plt.plot(aoi, iam_Martin_Ruiz, label='Martin-Ruiz model')
plt.xlabel(r'Angle of Incidence $\theta_i$')
plt.ylabel(r'Incidence Angle Modifier $F_{IAM,B}$')
plt.legend()
plt.ylim([0, 1.1])    
plt.gcf().set_layout_engine(layout='constrained')

plt.savefig('figures/IAM_models.jpg', dpi=300, bbox_inches='tight')