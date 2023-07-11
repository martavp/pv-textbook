# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 22:44:58 2023

@author: Ruben
"""
import math

import pvmismatch as pvmm
import numpy as np

def row_col2cel_idx(self, row_pos, col_pos):
    num_cols = sum(self.subStrCells)
    num_rows = self.numberCells // num_cols

    # ignores bypass diode connection -> flattens list
    list_cp = np.array(self.cell_pos).reshape(num_cols, num_rows)
    c = []
    for idx_col, col_val in enumerate(list_cp):
        cells_col = [cell['idx'] for cell in col_val]
        c.append(cells_col)
    pos = np.transpose(c)
    return pos[row_pos, col_pos]

def cel_idx2row_col(self, cel_idx):
    num_cols = sum(self.subStrCells)
    num_rows = self.numberCells // num_cols
    
    col_cel = cel_idx // num_rows
    row_cel = cel_idx % num_rows if not col_cel % 2 else num_rows - \
        (cel_idx % num_rows) - 1
    return row_cel, col_cel

def get_irr_cell_curved(self, row_pos, col_pos, cell_side, mod_radius_row, mod_radius_col):
    num_cols = sum(self.subStrCells)
    num_rows = self.numberCells // num_cols

    mid_row = num_rows / 2
    mid_col = num_cols / 2

    def get_aoi_projection(side, radius):
        aoi = side / (2 * math.pi * radius) * 360
        aoi_projection = math.cos(math.radians(aoi))
        return aoi_projection

    aoi_proj_row = get_aoi_projection(
        side=(row_pos + 0.5 - mid_row) * cell_side, radius=mod_radius_row)
    aoi_proj_col = get_aoi_projection(
        side=(col_pos + 0.5 - mid_col) * cell_side, radius=mod_radius_col)

    return aoi_proj_row * aoi_proj_col


def set_curved_irradiance(self, cell_side=156, mod_radius_row=1e10, mod_radius_col=1000):
    num_cols = sum(self.subStrCells)
    num_rows = self.numberCells // num_cols
    pvmod_irr = np.empty([num_rows, num_cols])
    
    for cel_idx in range(self.numberCells):
        row, col = self.cel_idx2row_col(cel_idx=cel_idx)
        cel_irr = self.Ee[cel_idx] * self.get_irr_cell_curved(row, col, cell_side, mod_radius_row, mod_radius_col)
        pvmod_irr[row, col] = cel_irr
        self.setSuns(cel_irr, cells=[cel_idx])

    return pvmod_irr


pvmm.pvmismatch_lib.pvmodule.PVmodule.row_col2cel_idx = row_col2cel_idx
pvmm.pvmismatch_lib.pvmodule.PVmodule.cel_idx2row_col = cel_idx2row_col
pvmm.pvmismatch_lib.pvmodule.PVmodule.get_irr_cell_curved = get_irr_cell_curved
pvmm.pvmismatch_lib.pvmodule.PVmodule.set_curved_irradiance = set_curved_irradiance