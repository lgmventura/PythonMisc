#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 23:00:58 2022

@author: luiz
"""

from scipy.io.wavfile import write
import sounddevice as sd

from os import path, listdir
import numpy as np

import matplotlib.pyplot as plt


def createPartials(baseFreq, harmonicAmps, harmonicsDecay, hDeviation, recursionLevel, duration_s = 5, sample_rate = 44100, _it = 0):
    assert(len(harmonicAmps) == len(harmonicsDecay))
    harmonic_base = 1 # 6/5 # 1
    t = np.linspace(0, duration_s, duration_s*sample_rate)
    wv = np.zeros(duration_s * sample_rate)
    for idxHarm, iHarm in enumerate(harmonicAmps):
        if _it < recursionLevel:
            _it = _it + 1
            i_wv = createPartials(baseFreq * (idxHarm + 1), harmonicAmps, harmonicsDecay, hDeviation, recursionLevel, duration_s, sample_rate, _it)
        else:
            #i_wv = iHarm * np.sin(t * baseFreq * (idxHarm + 1) * 2*np.pi) * np.exp(-t * 1/harmonicsDecay[idxHarm])
            #i_wv = iHarm * np.sin(t * baseFreq*(1+np.random.randn()*0.04) * (idxHarm + 1) * 2*np.pi + 2*np.pi*np.random.randn()) * np.exp(-t * 1/harmonicsDecay[idxHarm])
            i_wv = iHarm * np.sin(t * baseFreq*(1 + hDeviation[idxHarm]) * (harmonic_base)**(idxHarm + 1) * 2*np.pi + 2*np.pi*np.random.randn()) * np.exp(-t * 1/harmonicsDecay[idxHarm])
        wv = wv + i_wv
    wv = (wv - np.mean(wv))/np.ptp(wv)
    return wv

#                     1     2     3     4     5     6     7     8     9    10    11
harmonics = np.array([0.4, 0.20, 0.40, 0.10, 0.30, 0.08, 0.01, 0.01, 0.04, 0.02, 0.01])
h_decay   = np.array([  2,    3,    4,    6,    3,  0.9,  0.5,  0.3,  0.6,  0.8,  0.3])/6
h_deviation = np.random.randn(len(harmonics))/200
wv = createPartials(140, harmonics, h_decay, h_deviation, recursionLevel = 3)

data = wv
scaled = np.int16(data/np.max(np.abs(data)) * 32767 * 3/4)
write('/media/luiz/Volume/Dokumente/Musik/test.wav', 44100, scaled)

if True:
    fs = 44100
    sd.play(data, fs)
