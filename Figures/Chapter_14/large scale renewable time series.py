# -*- coding: utf-8 -*-
"""
Modified from: https://atlite.readthedocs.io/en/latest/examples/plotting_with_atlite.html 

"""

import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
plt.style.use(['seaborn-ticks','../pv-textbook.mplstyle'])
import geopandas as gpd
import pandas as pd
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

import cartopy.crs as ccrs
from cartopy.crs import PlateCarree as plate
import cartopy.io.shapereader as shpreader

import xarray as xr
import atlite

import logging
import warnings

warnings.simplefilter("ignore")
logging.captureWarnings(False)
logging.basicConfig(level=logging.INFO)

#import default color scheme for the book
import yaml
with open('../colors.yaml') as file:
    colors = yaml.load(file, Loader=yaml.FullLoader)

#%%
#Define countries and shapes
shpfilename = shpreader.natural_earth(
    resolution="10m", category="cultural", name="admin_0_countries")

reader = shpreader.Reader(shpfilename)


country='Spain'
Iberia = gpd.GeoSeries({r.attributes["NAME_EN"]: r.geometry for r in reader.records()},
    crs={"init": "epsg:4326"},).reindex(["Spain", "Portugal"]) #, "Portugal"])


Spain=Iberia["Spain"][2]
#%%

# Define and download cutout
cutout = atlite.Cutout(
    path="Spain-2020-06", module="era5", bounds=Spain.bounds, #bounds=Iberia.unary_union.bounds, 
    time="2020-06")
cutout.prepare()

#%%
projection = ccrs.Orthographic(-10, 35)
#%%
cells = cutout.grid
df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
country_bound = gpd.GeoSeries(cells.unary_union)

projection = ccrs.Orthographic(-10, 35)
fig, ax = plt.subplots(subplot_kw={"projection": projection}, figsize=(6, 6))
df.plot(ax=ax, transform=plate())
country_bound.plot(ax=ax, edgecolor="firebrick", facecolor="None", transform=plate())
fig.tight_layout()
plt.savefig('figures/global_view_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')
#%%
fig = plt.figure(figsize=(12, 7))
gs = GridSpec(3, 3, figure=fig)

ax = fig.add_subplot(gs[:, 0:2], projection=projection)
plot_grid_dict = dict(
    alpha=0.1,
    edgecolor="k",
    zorder=4,
    aspect="equal",
    facecolor="None",
    transform=plate(),
)
Iberia.plot(ax=ax, zorder=1, transform=plate())
cells.plot(ax=ax, **plot_grid_dict)
country_bound.plot(ax=ax, edgecolor="firebrick", facecolor="None", transform=plate())
ax.outline_patch.set_edgecolor("white")

ax1 = fig.add_subplot(gs[1, 2])
cutout.data.wnd100m.mean(["x", "y"]).plot(ax=ax1, color=colors['color3'])
ax1.set_frame_on(False)
ax1.xaxis.set_visible(False)
ax1.set_ylabel("Wind velocity \n 100 m (m/s)")

ax2 = fig.add_subplot(gs[0, 2], sharex=ax1)
cutout.data.influx_direct.mean(["x", "y"]).plot(ax=ax2, color=colors['color5'])
ax2.set_frame_on(False)
ax2.xaxis.set_visible(False)
ax2.set_ylabel("Solar irradiation \n (W/m2)")

ax3 = fig.add_subplot(gs[2, 2], sharex=ax1)
cutout.data.runoff.mean(["x", "y"]).plot(ax=ax3, color=colors['color1'])
times=cutout.data.runoff.mean(["x", "y"])["time"]
ax3.set_frame_on(False)
ax3.set_xlabel(None)
ax3.set_ylabel("Runoff")
ax3.set_xticks([times.values[0],
                times.values[250],
                times.values[500],
                times.values[719],])
fig.tight_layout()

plt.savefig('figures/cutout_time_series_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')

#%%
#annual capacity factors for wind and solar PV
cap_factors = cutout.wind(turbine="Vestas_V112_3MW", capacity_factor=True)

fig, ax = plt.subplots(subplot_kw={"projection": projection}, figsize=(11, 4))
cap_factors.name = "Capacity Factor Wind"
cap_factors.plot(ax=ax, transform=plate(), alpha=0.8, cmap='winter_r')

cells.plot(ax=ax, **plot_grid_dict)
ax.outline_patch.set_edgecolor("white")
fig.tight_layout();

plt.savefig('figures/capacity_factor_wind_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')

#%%
cap_factors = cutout.pv(panel="CSi", orientation={"slope": 30.0, "azimuth": 180.0},
                        capacity_factor=True)

fig, ax = plt.subplots(subplot_kw={"projection": projection}, figsize=(11, 4))
cap_factors.name = "Capacity Factor Solar PV"

cap_factors.plot(ax=ax, transform=plate(), alpha=0.7, cmap='autumn')
cells.plot(ax=ax, **plot_grid_dict)
ax.outline_patch.set_edgecolor("white")
fig.tight_layout();

plt.savefig('figures/capacity_factor_solar_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')
#%%
sites = gpd.GeoDataFrame(
        [["Grid cell a", -3.703, 40.416, 1000], #Madrid
        ["Grid cell b", -6, 37.39, 700], #Sevilla
       ["Grid cell c", -0.89, 41.65, 500], #Zaragoza
       ],
       columns=["name", "x", "y", "capacity"],).set_index("name")

nearest = cutout.data.sel({"x": sites.x.values, "y": sites.y.values}, "nearest").coords
sites["x"] = nearest.get("x").values
sites["y"] = nearest.get("y").values
cells_generation = sites.merge(cells, how="inner").rename(pd.Series(sites.index))

layout = (xr.DataArray(cells_generation.set_index(["y", "x"]).capacity.unstack())
    .reindex_like(cap_factors)
    .rename("Installed Capacity [MW]"))

fig, ax = plt.subplots(subplot_kw={"projection": projection}, figsize=(6, 3))


Iberia.plot(ax=ax, zorder=1, transform=plate(), alpha=0.3)
cells.plot(ax=ax, **plot_grid_dict)
layout.plot(ax=ax, transform=plate(), cmap="Reds", vmin=0, label="Installed Capacity [MW]")
ax.outline_patch.set_edgecolor("white")
fig.tight_layout()
plt.savefig('figures/capacity_layout_solar_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')

#%%
fig, axes = plt.subplots(len(sites)+1, sharex=True, figsize=(6, 8))

power_generation=cutout.pv(panel="CSi", orientation={"slope": 30.0, "azimuth": 180.0},
                        shapes=cells_generation.geometry)

power_generation.to_pandas().plot(subplots=True, ax=[axes[0], axes[1], axes[2]], legend=False, 
                                  color=[colors['color2'], colors['color4'],colors['color5'],])

fig.tight_layout()
axes[0].set_ylim([0,1])
axes[1].set_ylim([0,1])
axes[2].set_ylim([0,1])
axes[0].set_title("Capacity Factor")
axes[0].set_ylabel("grid cell a")
axes[1].set_ylabel("grid cell b")
axes[2].set_ylabel("grid cell c")

power_generation = (1/3)*(cutout.pv(panel="CSi", orientation={"slope": 30.0, "azimuth": 180.0},
                             layout=layout.fillna(0), shapes=Iberia) #shapes=UkIr)
                             .to_pandas()
                             .rename_axis(index="", columns="shapes",
                                          ))    

power_generation["Spain"].plot.area(ax=axes[3], title="Spain", color=colors['color5'])
axes[3].set_title=('')
axes[3].set_ylabel("aggregated")
axes[3].set_ylim([0,1])

fig.tight_layout()
plt.savefig('figures/grid_cell_agregated_timeseries_solar_{}.jpg'.format(country), 
            dpi=300, bbox_inches='tight')


