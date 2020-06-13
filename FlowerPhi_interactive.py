#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 14:03:29 2018

@author: Luiz Guilherme de M. Ventura

"""

import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import widgets

#%matplotlib inline

def f(x):
    x1 = np.arange(0,10)
    y1 = np.arange(0,10)*x1**(1j*x)
    plt.scatter(y1.real, y1.imag)
    plt.ylim(-10,10)
    plt.xlim(-10,10)
    
interact(f, x=(-2,2,0.005))