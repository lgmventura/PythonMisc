#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 10:53:01 2019

@author: luiz
"""

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6,6))



N = 12

filenames = []
for n in range(N):
    ax = fig.add_subplot(111, projection='polar')
    n = n+1
    r = np.ones(n)
    theta = np.arange(n) * np.log(1.5)/np.log(2) * 2*np.pi
    
    # to make the colour spectrum span the whole circle:
    theta = theta % (2*np.pi)
    theta.sort()
    
    area = 140
    #colors = np.linspace(0, 1, n)
    colors = theta/(2*np.pi)
    
    markerline, stemlines, baseline = ax.stem(
        theta, r, linefmt='grey', markerfmt='o', use_line_collection=True)
    markerline.set_markerfacecolor('none')
    markerline.set_markeredgecolor('none')
    c = ax.scatter(theta, r, c=colors, s=area, cmap='hsv', vmax=1, alpha=1)
    
    ax.set_theta_zero_location('N', offset=0)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.set_rlim(0,1.1)
    ax.set_xlabel('Passo: {}'.format(str(n)))
    if n == N:
        ax.xaxis.label.set_color('red') # last frame: red x-label
    
    filename = 'temp/frame_{}.png'.format(str(n))
    fig.savefig(filename)
    filenames.append(filename)
    
lastFrameRepeat = 4
for i in range(lastFrameRepeat):
    filenames.append(filename)
# Save gif file:
import imageio
with imageio.get_writer('ciclo_quintas_{}.gif'.format(str(N)), mode='I', duration=0.5) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)