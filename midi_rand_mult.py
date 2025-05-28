#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 21:53:40 2025

@author: luiz
"""

from music21 import converter, note, chord
import random

sigma_start = 0.01

dur_mu = 0.88
dur_sigma = 0.05
dur_max = 0.92

rmin_vel = -20
rmax_vel = 10

# Load a MIDI file
fp = '/home/luiz/Music/Composições/Piano solo/20241006.mid'

midi_file = converter.parse(fp, format='midi')

# Iterate through all notes and modify them
for element in midi_file.recurse().notesAndRests:
    if isinstance(element, note.Rest):
        continue
    
    if isinstance(element, note.Note):
        # Shift all notes forward by 1 beat
        element.offset += random.normalvariate(sigma_start*2, sigma_start)
        
        # Double the duration of all notes
        element.quarterLength *= min(random.normalvariate(dur_mu, dur_sigma), dur_max)
        element.quarterLength = max(element.quarterLength, 0.01)
        
        element.volume.velocity += random.randint(rmin_vel, rmax_vel)
    
    # elif isinstance(element, chord.Chord):
    #     # For chords, you can modify the entire chord
    #     element.offset += 0.5
    #     element.quarterLength = 1.5

# Save the modified MIDI
out_fp = fp[:-4] + '_rand_mult.mid'
midi_file.write('midi', fp=out_fp, quantizePost=False)