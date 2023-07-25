# -*- coding: utf-8 -*-
"""
Code that generates Figure 11.10 of the chapter "11. Integrated Photovoltaics" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pvmismatch as pvmm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

import pvmm_extra

plt.style.use('../pv-textbook.mplstyle')


def plot_cells_position(fig, ax, pvmod, pvmod_irr, interp='bilinear', colorbar=True):
    num_cols = sum(pvmod.subStrCells)
    num_rows = pvmod.numberCells // num_cols

    plt.axis('off')
    
    if pvmod_irr is None:
        im = ax.imshow(np.zeros([num_rows, num_cols]), cmap='Greys')
    else:
        im = ax.imshow(pvmod_irr, cmap=LinearSegmentedColormap.from_list(name='', colors=['C12', 'C3']), interpolation=interp)
        if colorbar:
            clb = fig.colorbar(im)
            clb.set_label('Normalized irradiance')

    for cel_idx in range(pvmod.numberCells):
        row, col = pvmod.cel_idx2row_col(cel_idx=cel_idx)
        row_next, col_next = pvmod.cel_idx2row_col(cel_idx=cel_idx+1)

        ax.plot(col, row, marker='o', color='black', markersize=28)
        ax.text(col, row, s=pvmod.row_col2cel_idx(row_pos=row, col_pos=col),
                color='white', horizontalalignment='center', verticalalignment='center', fontsize=24)
        if cel_idx < num_rows * num_cols - 1:
            ax.plot([col, col_next],
                    [row, row_next], color='black')
            
#%%
cell_pos_5diode = pvmm.pvmodule.standard_cellpos_pat(
    nrows=3, ncols_per_substr=5*[1])

cell_pos_1diode = pvmm.pvmodule.standard_cellpos_pat(
    nrows=3, ncols_per_substr=[5])

shaded_cells = [0, 1, 2, 3, 4, 8]

pvmod_flat = pvmm.PVmodule(cell_pos=cell_pos_5diode)

pvmod_curve = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_irr = pvmod_curve.set_curved_irradiance()

#%%
pvmod_curve_shaded_1diode = pvmm.PVmodule(cell_pos=cell_pos_1diode)
pvmod_curve_shaded_1diode.setSuns(0.1, cells=shaded_cells)
pvmod_irr = pvmod_curve_shaded_1diode.set_curved_irradiance()

#%%
pvmod_curve_shaded_5diode = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_curve_shaded_5diode.setSuns(0.1, cells=shaded_cells)
pvmod_irr = pvmod_curve_shaded_5diode.set_curved_irradiance()
    
#%%
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

list_mods = [pvmod_flat, pvmod_curve, pvmod_curve_shaded_5diode, pvmod_curve_shaded_1diode]
label_mods = ['flat module (UI, 5 BD)', 'curved module (UI, 5 BD)', 'curved module (Non-UI, 5 BD)', 'curved module (Non-UI, 1 BD)']

for mod, label in zip(list_mods, label_mods):
    pvsys = pvmm.PVsystem(pvmods=mod, numberStrs=1, numberMods=1)

    ax1.plot(mod.Vmod, mod.Imod, linewidth=3, label=label)
    ax1.scatter(pvsys.Vmp, pvsys.Imp, marker='o', s=300)

ax1.set_xlim(0, pvmod_curve_shaded_1diode.numberCells * 0.7)
ax1.set_ylim(0, 7)

ax1.set_xlabel('Voltage [V]')
ax1.set_ylabel('Current [A]')

ax1.legend(loc='center right')

##
pvmod_curve_shaded = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_curve_shaded.setSuns(0.1, cells=[0, 1, 2, 3, 4, 8])
pvmod_irr = pvmod_curve_shaded.set_curved_irradiance()
plot_cells_position(fig=fig, ax=ax2, pvmod=pvmod_curve_shaded, pvmod_irr=pvmod_irr)

plt.savefig('Figure11.10 - vipv iv curves.jpg', dpi=300, bbox_inches='tight')
