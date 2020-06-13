#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:12:18 2019

@author: luiz
"""
import PlaySound # in the same folder


for k in range(20):
    PlaySound.sine_tone(128*(k+1),0.3,0.2)
    
D = set()
for k in range(48): # play inside an octave all frequencies still not played
    kk = k*256
    while kk >= 512:
        kk = kk/2
    if not kk in D:
        PlaySound.sine_tone(kk, 0.5, 0.2)
    D.add(kk)