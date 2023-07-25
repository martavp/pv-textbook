# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 23:26:54 2023

@author: cesar
"""
from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
# use pvlib python to retrieve CEC module parameters from the SAM libraries
moduleDB = pvsystem.retrieve_sam(name='CECMod')
parameters = moduleDB['Jinko_Solar_Co___Ltd_JKM390M_72HL_V']

# list of translation conditions
cases = [
    (1000, 25),
    (800, 25),
    (600, 25),
    (400,25),
    (200,25)
]

conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])

# adjust the reference parameters according to the operating
# conditions using the De Soto model:
IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
    conditions['Geff'],
    conditions['Tcell'],
    alpha_sc=parameters['alpha_sc'],
    a_ref=parameters['a_ref'],
    I_L_ref=parameters['I_L_ref'],
    I_o_ref=parameters['I_o_ref'],
    R_sh_ref=parameters['R_sh_ref'],
    R_s=parameters['R_s'],
    EgRef=1.121,
    dEgdT=-0.0002677
)

# plug the parameters into the SDE and solve for IV curves:
curve_info = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=100,
    method='lambertw'
)

# plot the calculated curves:
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
for i, case in conditions.iterrows():
    label = (
        "$G_{ef}$ " + f"{case['Geff']} $W/m^2$"
    )
    plt.plot(curve_info['v'][i], curve_info['i'][i], label=label)
    v_mp = curve_info['v_mp'][i]
    i_mp = curve_info['i_mp'][i]
    # mark the MPP
    filled_marker_style = dict(marker='o', markersize=7,
                           color='darkgrey',
                           markerfacecolor='none',
                           markeredgecolor='black')
    plt.plot([v_mp], [i_mp], ls='', **filled_marker_style)
    plt.annotate('$P_{max}$', xy=(40, 10), xycoords='data',fontsize=14)
    ax.text(1.12, 0.48, '$T_{c}$ 25 °C',fontsize=16, transform=ax.transAxes)

plt.legend(loc=(1,0))
plt.xlabel('Module voltage [V]')
plt.ylabel('Module current [A]')
plt.gcf().set_tight_layout(True)

plt.savefig('figures/IV_variation_Gef.jpg', dpi=300, bbox_inches='tight')

# list of translation conditions
temp_cases = [
    (1000, 15),
    (1000, 25),
    (1000, 50),
    (1000,75),
]

conditions = pd.DataFrame(temp_cases, columns=['Geff', 'Tcell'])

# adjust the reference parameters according to the operating
# conditions using the De Soto model:
IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
    conditions['Geff'],
    conditions['Tcell'],
    alpha_sc=parameters['alpha_sc'],
    a_ref=parameters['a_ref'],
    I_L_ref=parameters['I_L_ref'],
    I_o_ref=parameters['I_o_ref'],
    R_sh_ref=parameters['R_sh_ref'],
    R_s=parameters['R_s'],
    EgRef=1.121,
    dEgdT=-0.0002677
)

# plug the parameters into the SDE and solve for IV curves:
curve_info = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=100,
    method='lambertw'
)

# plot the calculated curves:
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
for i, case in conditions.iterrows():
    label = (
        "$T_{c}$ " + f"{case['Tcell']} °C"
    )
    plt.plot(curve_info['v'][i], curve_info['i'][i], label=label)
    v_mp = curve_info['v_mp'][i]
    i_mp = curve_info['i_mp'][i]
    # mark the MPP
    filled_marker_style = dict(marker='o', markersize=7,
                           color='darkgrey',
                           markerfacecolor='none',
                           markeredgecolor='black')
    plt.plot([v_mp], [i_mp], ls='', **filled_marker_style)
    plt.annotate('$P_{max}$', xy=(40, 10), xycoords='data',fontsize=14)
    plt.annotate('$G_{ef}$ 1000 $W/m^2$', xy=(5, 4), xycoords='data',fontsize=16)

plt.legend()
plt.xlabel('Module voltage [V]')
plt.ylabel('Module current [A]')
plt.gcf().set_tight_layout(True) 

plt.savefig('figures/IV_variation_Tc.jpg', dpi=300, bbox_inches='tight')