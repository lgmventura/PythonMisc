#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 23:01:57 2025

@author: luiz
"""

import matplotlib.pyplot as plt
import numpy as np

def koch(n, ang0=60, ang1=-60, modulo360=True):
    if n > 4:
        raise(ValueError('n too large for memory'))
    # retrieve the angles
    if n == 0:
        angles = np.array([])
    elif n == 1:
        angles = np.array([0, ang0, ang1, 0])
    else:
        angles = koch(n - 1, ang0, ang1)
        for angle in angles:
            angles = np.concatenate((angles[1:], angle + koch(n - 1, ang0, ang1)))
    
    return angles

# to visualize results:
def draw_angle_path(angles, segment_length=1.0, margin=0.1):
    """
    Draw a path based on a sequence of angles, with each segment having the specified length.
    Then zoom to fit the drawing with a small margin.
    
    Parameters:
    - angles: array of angles in degrees
    - segment_length: length of each segment (default 1.0)
    - margin: margin around the drawing when zooming (default 0.1)
    """
    # Convert angles to radians
    angles_rad = np.deg2rad(angles)
    
    # Initialize starting point
    x, y = [0], [0]
    
    # Calculate each subsequent point
    current_x, current_y = 0, 0
    for angle in angles_rad:
        current_x += segment_length * np.cos(angle)
        current_y += segment_length * np.sin(angle)
        x.append(current_x)
        y.append(current_y)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x, y, '-o', markersize=4, linewidth=2)
    ax.set_title("Path following given angles")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='datalim')
    
    # Calculate bounds with margin
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    
    x_margin = max((x_max - x_min) * margin, segment_length * margin)
    y_margin = max((y_max - y_min) * margin, segment_length * margin)
    
    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    
    plt.show()

# Example usage:
if __name__ == '__main__':
    angles = [0, 90, 135, 45, -45, -90, -135]
    draw_angle_path(angles, segment_length=1.0, margin=0.2)
    