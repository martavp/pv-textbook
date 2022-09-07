# -*- coding: utf-8 -*-
"""
@author: Marta
"""
import rasterio
import numpy as np

tif_file = rasterio.open('data/population/GHS_POP_E2015_GLOBE_R2019A_4326_30ss_V1_0.tif')
ghs_data = tif_file.read()


#%%
print("Tiff Boundary", tif_file.bounds)
print("Tiff CRS", tif_file.crs)
print("Data shape", ghs_data.shape)
print("Max value", np.amax(ghs_data))
print("Min value", np.amin(ghs_data))

#%%

ghs_data[0][ghs_data[0] < 0.0] = 0.0

#%%

from matplotlib import cm
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap

ourcmap = cm.get_cmap('hot_r', 460)
newcolors = ourcmap(np.linspace(0, 1, 460))
background_colour = np.array([0.9882352941176471, 0.9647058823529412, 0.9607843137254902, 1.0])
newcolors[:1, :] = background_colour
newcmp = ListedColormap(newcolors)

#%%
import matplotlib.pyplot as plt
import matplotlib.colors as colors

fig, ax = plt.subplots(facecolor='#FCF6F5FF')
fig.set_size_inches(14, 7)
ax.imshow(ghs_data[0], norm=colors.LogNorm(), cmap=newcmp)
ax.axis('off')
plt.show()
