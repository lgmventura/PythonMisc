#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 19:45:09 2023

@author: luiz
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import os
from shutil import copyfile

folder = '/home/luiz/Videos/Grussaí - reescalado'
folder2 = '/home/luiz/Videos/Grussaí - reescalado nonrep'

for root, dirs, files in os.walk(folder):
    for idxF, file in enumerate(sorted(files)):
        if file.endswith('.png'):
            current_img = cv2.imread(os.path.join(root, file))
            if idxF > 0:
                img_diff = (last_img - current_img)**2
                # fig, ax = plt.subplots()
                # im1 = ax.imshow(img_diff)
                
                # ax1_divider = make_axes_locatable(ax)
                # # Add an Axes to the right of the main Axes.
                # cax1 = ax1_divider.append_axes("right", size="7%", pad="2%")
                # cb1 = fig.colorbar(im1, cax=cax1)
                mean = np.mean(img_diff)
                print(file + ' - mean: {:.4f}'.format(mean))
                
                if mean > 3:
                    copyfile(os.path.join(root, file), os.path.join(folder2, file))
                
                # plt.pause(1)
            last_img = current_img