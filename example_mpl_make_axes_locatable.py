#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:05:34 2021

@author: luiz
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd

x = np.linspace(0, 10, num=100)
y = x ** 2 + 10 * np.random.randn(100)


f, (ax1, ax2) = plt.subplots(2,1,sharex=True,figsize=(8,12))

im1 = ax1.scatter(x, y, c=y, cmap='magma')
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=.05)

plt.colorbar(im1, cax=cax)

im2 = ax2.plot(x, y,'.')

plt.show()