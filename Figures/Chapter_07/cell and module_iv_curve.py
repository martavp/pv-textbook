# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 23:26:54 2023

@author: cesar
Based on https://pvlib-python.readthedocs.io/en/stable/gallery/shading/plot_partial_module_shading_simple.html#sphx-glr-gallery-shading-plot-partial-module-shading-simple-py
"""
from pvlib import pvsystem, singlediode
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.constants import e as qe, k as kB

#import default figure format for the book
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)
    
# Thermal voltage calculation with kB in J/K, T in K, qe in C=J/V
Tc = 25 #in degC
Vth = kB * (273.15+Tc) / qe

cell_parameters = {
    'I_L_ref': 8.24 / 2,
    'I_o_ref': 2.36e-9 / 2,
    'a_ref': 1.3*Vth,
    'R_sh_ref': 1000 *2,
    'R_s': 0.00181 *2,
    'alpha_sc': 0.0042,
    'breakdown_factor': 2e-3,
    'breakdown_exp': 3,
    'breakdown_voltage': -15,
}

#Modification of cell parameters for Np strings in parallel.
#Series connections are performed with simulate_module function
Np = 2
Ns = 4

mod_cell_parameters = {
    'I_L_ref': 8.24 / 2 * Np,
    'I_o_ref': 2.36e-9 / 2 * Np,
    'a_ref': 1.3*Vth,
    'R_sh_ref': 1000 *2 / Np,
    'R_s': 0.00181 *2 / Np,
    'alpha_sc': 0.0042,
    'breakdown_factor': 2e-3,
    'breakdown_exp': 3,
    'breakdown_voltage': -15,
}

def simulate_full_curve(parameters, Geff, Tcell, ivcurve_pnts=1000):
    """
    Use De Soto and Bishop to simulate a full IV curve with both
    forward and reverse bias regions.
    """
    # adjust the reference parameters according to the operating
    # conditions using the De Soto model:
    sde_args = pvsystem.calcparams_desoto(
        Geff,
        Tcell,
        alpha_sc=parameters['alpha_sc'],
        a_ref=parameters['a_ref'],
        I_L_ref=parameters['I_L_ref'],
        I_o_ref=parameters['I_o_ref'],
        R_sh_ref=parameters['R_sh_ref'],
        R_s=parameters['R_s'],
    )
    # sde_args has values:
    # (photocurrent, saturation_current, resistance_series,
    # resistance_shunt, nNsVth)

    # Use Bishop's method to calculate points on the IV curve with V ranging
    # from the reverse breakdown voltage to open circuit
    kwargs = {
        'breakdown_factor': parameters['breakdown_factor'],
        'breakdown_exp': parameters['breakdown_exp'],
        'breakdown_voltage': parameters['breakdown_voltage'],
    }
    v_oc = singlediode.bishop88_v_from_i(
        0.0, *sde_args, **kwargs
    )
#    vd = np.linspace(0.99*kwargs['breakdown_voltage'], v_oc, ivcurve_pnts)
    vd = np.linspace(0, v_oc, ivcurve_pnts)

    ivcurve_i, ivcurve_v, _ = singlediode.bishop88(vd, *sde_args, **kwargs)
    return pd.DataFrame({
        'i': ivcurve_i,
        'v': ivcurve_v,
    })

def plot_curves(dfs, labels, title):
    """plot the forward- and reverse-bias portions of an IV curve"""
    fig, axes = plt.subplots()
    xlim = 0
    ylim = 0
    for df, label in zip(dfs, labels):
        df.plot('v', 'i', label=label, ax=axes)
        #axes.set_ylim([0, 10])
        if df['i'].max()>ylim:
            axes.set_ylim([0, df['i'].max()*1.15])
            ylim=df['i'].max()
        if df['v'].max()>xlim:
            axes.set_xlim([0, df['v'].max()*1.1])
            xlim=df['v'].max()
    axes.set_ylabel('current [A]')
    axes.set_xlabel('voltage [V]')
    #fig.suptitle(title)
    fig.tight_layout()
    return axes


cell_curve_full_sun = simulate_full_curve(cell_parameters, Geff=1000, Tcell=25)
cell_curve_shaded = simulate_full_curve(cell_parameters, Geff=200, Tcell=25)
# ax = plot_curves([cell_curve_full_sun, cell_curve_shaded],
#                  labels=['Full Sun', 'Shaded'],
#                  title='Cell-level reverse- and forward-biased IV curves')

def interpolate(df, i):
    """convenience wrapper around scipy.interpolate.interp1d"""
    f_interp = interp1d(np.flipud(df['i']), np.flipud(df['v']), kind='linear',
                        fill_value='extrapolate')
    return f_interp(i)


def combine_series(dfs):
    """
    Combine IV curves in series by aligning currents and summing voltages.
    The current range is based on the first curve's current range.
    """
    df1 = dfs[0]
    imin = df1['i'].min()
    imax = df1['i'].max()
    i = np.linspace(imin, imax, 1000)
    v = 0
    for df2 in dfs:
        v_cell = interpolate(df2, i)
        v += v_cell
    return pd.DataFrame({'i': i, 'v': v})

def simulate_module(cell_parameters, poa_direct, poa_diffuse, Tcell,
                    shaded_fraction, cells_per_string=Ns, strings=1):
    """
    Simulate the IV curve for a partially shaded module.
    The shade is assumed to be coming up from the bottom of the module when in
    portrait orientation, so it affects all substrings equally.
    For simplicity, cell temperature is assumed to be uniform across the
    module, regardless of variation in cell-level illumination.
    Substrings are assumed to be "down and back", so the number of cells per
    string is divided between two columns of cells.
    """
    # find the number of cells per column that are in full shadow
    nrow = cells_per_string // 2
    nrow_full_shade = int(shaded_fraction * nrow)
    # find the fraction of shade in the border row
    partial_shade_fraction = 1 - (shaded_fraction * nrow - nrow_full_shade)

    df_lit = simulate_full_curve(
        cell_parameters,
        poa_diffuse + poa_direct,
        Tcell)
    df_partial = simulate_full_curve(
        cell_parameters,
        poa_diffuse + partial_shade_fraction * poa_direct,
        Tcell)
    df_shaded = simulate_full_curve(
        cell_parameters,
        poa_diffuse,
        Tcell)
    # build a list of IV curves for a single column of cells (half a substring)
    include_partial_cell = (shaded_fraction < 1)
    half_substring_curves = (
        [df_lit] * (nrow - nrow_full_shade - 1)
        + ([df_partial] if include_partial_cell else [])  # noqa: W503
        + [df_shaded] * nrow_full_shade  # noqa: W503
    )
    substring_curve = combine_series(half_substring_curves)
    substring_curve['v'] *= 2  # turn half strings into whole strings
    # bypass diode:
    substring_curve['v'] = substring_curve['v'].clip(lower=-0.5)
    # no need to interpolate since we're just scaling voltage directly:
    substring_curve['v'] *= strings
    return substring_curve

kwargs = {
    'cell_parameters': mod_cell_parameters,
    'poa_direct': 800,
    'poa_diffuse': 200,
    'Tcell': 25
}
module_curve_full_sun = simulate_module(shaded_fraction=0, **kwargs)
cell_curve_full_sun = simulate_full_curve(cell_parameters, Geff=1000, Tcell=25)
#module_curve_shaded = simulate_module(shaded_fraction=0.1, **kwargs)
ax = plot_curves([module_curve_full_sun, cell_curve_full_sun],
                 labels=['module', 'single cell'],
                 title='Module-level reverse- and forward-biased IV curves')

ax.annotate(
    '$I_{SC,cell}$',
    xy=(0, 4), xycoords='data',fontsize=16,
    xytext=(5, 10), textcoords='offset points')
ax.annotate(
    '$N_{P}$·$I_{SC,cell}$',
    xy=(0, 8), xycoords='data',fontsize=16,
    xytext=(5, 12), textcoords='offset points')
ax.annotate(
    '$V_{OC,cell}$',
    xy=(0.75, 0), xycoords='data',fontsize=16,
    xytext=(0, 10), textcoords='offset points',rotation=92)
ax.annotate(
    '$N_{S}$·$V_{OC,cell}$',
    xy=(2.97, 0), xycoords='data',fontsize=16,
    xytext=(0, 10), textcoords='offset points',rotation=92)

plt.savefig('figures/cell_and_module_IV.jpg', dpi=300, bbox_inches='tight')  