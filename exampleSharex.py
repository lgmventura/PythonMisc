#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:07:30 2021

@author: luiz
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools as it
from mpl_toolkits.axes_grid1 import make_axes_locatable

# create some data
xy = list(it.product(range(16), range(16)))
df = pd.DataFrame(xy, columns=["x", "y"])
df["bubles"] = np.random.random(256)

# create figure and main axis
fig = plt.figure(figsize=(10,6))
ax = plt.gca()

# create a divider from make_axes_locatable
divider = make_axes_locatable(ax)

# append a new axis on the bottom whose size is 15% of the size of the main ax
bax = divider.append_axes("bottom", size="15%", pad=.05)

# append axis on the right for colourbar (size = 5%)
cax = divider.append_axes("right", size="5%", pad=.05)

cm = "plasma" # defining colourmap
sm = plt.cm.ScalarMappable(cmap=cm)

# plotting on main axis
p1 = df.plot(kind='scatter', x='x',  y='y', c='bubles', s=df["bubles"]*200, cmap=cm,
          ax=ax, colorbar=False)

# attaching colourbar to the axis at the right
plt.colorbar(sm, cax=cax)

# plotting on the adjascent axis (bottom)
p2 = df.groupby("x").mean().plot(kind = 'bar', y='bubles',ax=bax, legend=False)

# synchronizing plots on the x-axis
p2.sharex(p1)

# inserting some legend
bax.legend(bbox_to_anchor=(1.03,0),loc=3)

plt.show()