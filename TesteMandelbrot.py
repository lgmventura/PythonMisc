# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:20:40 2017

@author: luiz
"""

import matplotlib as plt
import numpy as np

N = 800
Nit = 30

z_r = np.linspace(-2,0.5,N)
z_i = np.linspace(-1.5,1.5,N)
#z_r = np.linspace(-1.78917,-1.78916,N)
#z_i = np.linspace(-0.00001,-0.00000,N)
z = np.zeros((N,N), dtype = complex)
for k in range(1,N):
    for kk in range(1,N):
        z[k][kk] = z_r[k] + 1j*z_i[kk]

def iterate(c, Nit):
    out = 0
    for k in range(0,Nit):
        out = out**2 + c
        if abs(out) > 2:
            out = 2
            break
    return out

z_Mandel = np.zeros((N,N))
for k in range(1,N):
    for kk in range(1,N):
        z_Mandel[k][kk] = iterate(z[k][kk], Nit)
        if abs(z_Mandel[k][kk]) > 2:
            z_Mandel[k][kk] = 0
        else:
            z_Mandel[k][kk] = abs(z_Mandel[k][kk])

plot1 = plt.pyplot.imshow(z_Mandel.transpose())
