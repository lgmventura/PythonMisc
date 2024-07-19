#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:00:20 2023

@author: luiz
"""

import numpy as np
from scipy.io import wavfile as wf

from all_fractions import A038566 # generator of numerators

from os import path

samplerate = 44100; fs = 100

t_per_note = 0.1
t = np.linspace(0., t_per_note, int(samplerate*t_per_note))

amplitude = int(np.iinfo(np.int16).max / 10)

outpath = '/home/luiz/Music/Algoritmos/'

def genIntervals():
    wavdata = np.array([])
    for d in range(2,20):
        numerators = A038566(d)
        for j, nr in enumerate(numerators):
            basef = 40
            data_n = amplitude * np.sin(2. * np.pi * basef*nr * t)
            data_d = amplitude * np.sin(2. * np.pi * basef*d * t)
            
            idata = data_n + data_d
            wavdata = np.append(wavdata, idata)
            
    wf.write(path.join(outpath, "intervals.wav"), samplerate, wavdata.astype(np.int16))
            
genIntervals()
