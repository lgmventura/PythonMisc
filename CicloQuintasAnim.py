#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 10:53:01 2019

@author: luiz
"""

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()

ax = fig.add_subplot(111, projection='polar')

N = 12
r = np.ones(N)
theta = np.arange(N) * np.log(1.5)/np.log(2) * 2*np.pi
area = 100
colors = theta

c = ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
ax.set_theta_zero_location('N', offset=0)
ax.set_theta_direction(-1)
ax.set_yticklabels([])