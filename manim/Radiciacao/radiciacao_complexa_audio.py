#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 17:57:50 2024

@author: luiz
"""

import numpy as np
# import music21 as mus
# from midigenlib import populate_midi_track_from_data_chords
from scipy.io import wavfile as wf
from datetime import datetime as dtm
from os import path

from radiciacao_complexa import calc_raízes

output = 'wav'

índ = 3
radic = 8

raízes = calc_raízes(radic, índ)

run_time = 1.04
wait_time = 1.04

samplerate = 44100#; fs = 100
amplitude = int(np.iinfo(np.int16).max / 10)

real_mult = 100
imag_mult = 100

wavdata = np.array([])

def crossfade(x1, x2, crossfade_length, sample_rate):
    """
    Crossfade two signals with a given crossfade length.
    
    Parameters:
    x1 (np.array): First input signal
    x2 (np.array): Second input signal
    crossfade_length (float): Crossfade length in seconds
    sample_rate (int): Sample rate in Hz
    
    Returns:
    np.array: Crossfaded output signal
    """
    # Convert crossfade length from seconds to samples
    crossfade_samples = int(crossfade_length * sample_rate)
    
    # Create crossfade window
    fade_out = np.linspace(1, 0, crossfade_samples)
    fade_in = np.linspace(0, 1, crossfade_samples)
    
    # Ensure the signals are at least as long as the crossfade length
    if len(x1) < crossfade_samples or len(x2) < crossfade_samples:
        raise ValueError("Input signals must be at least as long as the crossfade length.")
    
    # Separate parts of the signals
    x1_fade_out = x1[-crossfade_samples:]
    x2_fade_in = x2[:crossfade_samples]
    
    # Apply crossfade
    x1_fade_out = x1_fade_out * fade_out
    x2_fade_in = x2_fade_in * fade_in
    
    # Combine signals
    output = np.concatenate((x1[:-crossfade_samples], x1_fade_out + x2_fade_in, x2[crossfade_samples:]))
    
    return output

rtime = run_time
for idx, raiz in enumerate(raízes):
    for jdx in range(1, índ + 1):
        if jdx == 1:
            wtime = 2*wait_time
        else:
            wtime = wait_time
        # parte em que a raiz aparece estática
        t = np.linspace(0., wtime, int(samplerate*wtime))
        
        r_pot = raiz**jdx
        
        # data_n = amplitude * np.sin(2. * np.pi * r_pot.real*real_mult * np.cos(r_pot.imag)*imag_mult * t)
        data_n = amplitude * (np.sin(2. * np.pi * (r_pot).real*real_mult * t) + np.cos(2. * np.pi * (r_pot).imag*imag_mult * t))
        if idx == 0 and jdx == 1:
            wavdata = np.copy(data_n)
        else:
            # wavdata = np.append(wavdata, data_n)
            wavdata = crossfade(wavdata, data_n, 0.04, sample_rate=samplerate)
    
        # seqüência de elevação (potência)
        if jdx == índ:  # neste caso, só faz a parte estática
            break
        
        t = np.linspace(0., rtime, int(samplerate*rtime))
        t2 = np.linspace(jdx, jdx + 1, int(samplerate*rtime))
        
        #data_n = amplitude * np.sin(2. * np.pi * (r_pot**t2).real*real_mult * np.cos(t2*r_pot.imag)*imag_mult * t)
        # data_n = amplitude * (np.sin(2. * np.pi * (raiz**t2).real*real_mult * t) + np.cos(2. * np.pi * (raiz**t2).imag*imag_mult * t))
        phase_real = np.cumsum(real_mult * (raiz**t2).real) / samplerate * 2 * np.pi
        phase_imag = np.cumsum(imag_mult * (raiz**t2).imag) / samplerate * 2 * np.pi
        data_n = amplitude * (np.sin(phase_real) + np.cos(phase_imag))
        # wavdata = np.append(wavdata, data_n)
        wavdata = crossfade(wavdata, data_n, 0.04, sample_rate=samplerate)

outPath = '/home/luiz/Documents/workspace/PythonMisc/manim/Radiciacao'
wf.write(path.join(outPath, f"rad_ind{índ}_radic{radic}.wav"), samplerate, wavdata.astype(np.int16))