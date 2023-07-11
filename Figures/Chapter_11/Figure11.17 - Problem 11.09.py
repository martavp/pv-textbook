# -*- coding: utf-8 -*-
"""
Code that generates the Figure of the solution of Problem 11.09 of the chapter "11. Integrated Photovoltaics" of the book "Fundamentals of Solar Cells and Photovoltaic Systems Engineering"
(C) 2022 Rubén Núñez - CC BY 4.0
"""

import pvmismatch as pvmm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

import pvmm_extra

plt.style.use('../pv-textbook.mplstyle')

def plot_cells_position(pvmod, pvmod_irr, interp='bilinear', colorbar=True):
    num_cols = sum(pvmod.subStrCells)
    num_rows = pvmod.numberCells // num_cols

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.axis('off')
    
    if pvmod_irr is None:
        im = ax.imshow(np.zeros([num_rows, num_cols]), cmap='Greys')
    else:
        im = ax.imshow(pvmod_irr, cmap=LinearSegmentedColormap.from_list(name='', colors=['C12', 'C3']), interpolation=interp)
        if colorbar:
            fig.colorbar(im)

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

#%%
pvmod_flat = pvmm.PVmodule(cell_pos=cell_pos_5diode)
plot_cells_position(pvmod=pvmod_flat, pvmod_irr=None)
plt.savefig('Figure11.17 - Problem 11.09 - a.jpg', dpi=300, bbox_inches='tight')

#%%
pvmod_curve_shaded1 = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_curve_shaded1.setSuns(0.1, cells=[2])
pvmod_irr = pvmod_curve_shaded1.set_curved_irradiance()
plot_cells_position(pvmod=pvmod_curve_shaded1, pvmod_irr=pvmod_irr, colorbar=False)
plt.savefig('Figure11.17 - Problem 11.09 - b1.jpg', dpi=300, bbox_inches='tight')

#%%
pvmod_curve_shaded2 = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_curve_shaded2.setSuns(0.1, cells=[1, 2, 3])
pvmod_irr = pvmod_curve_shaded2.set_curved_irradiance()
plot_cells_position(pvmod=pvmod_curve_shaded2, pvmod_irr=pvmod_irr, colorbar=False)
plt.savefig('Figure11.17 - Problem 11.09 - b2.jpg', dpi=300, bbox_inches='tight')

#%%
pvmod_curve_shaded3 = pvmm.PVmodule(cell_pos=cell_pos_5diode)
pvmod_curve_shaded3.setSuns(0.1, cells=[0, 1, 2, 3, 4, 8])
pvmod_irr = pvmod_curve_shaded3.set_curved_irradiance()
plot_cells_position(pvmod=pvmod_curve_shaded3, pvmod_irr=pvmod_irr, colorbar=False)
plt.savefig('Figure11.17 - Problem 11.09 - b3.jpg', dpi=300, bbox_inches='tight')