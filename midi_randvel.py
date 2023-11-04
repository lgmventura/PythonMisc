#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 22:47:44 2023

@author: luiz
"""

from music21 import midi
import random

fp = '/home/luiz/Music/Composições/Piano solo/20230727 - em 7÷8.mid'

mf = midi.MidiFile()

mf.open(fp)

mf.read()

rmin = -10
rmax = 10


mf2 = midi.MidiFile()
mf2.ticksPerQuarterNote = mf.ticksPerQuarterNote

for idx, track in enumerate(mf.tracks):
    for event in track.events:
        if event.isNoteOn():
            oldV = event.velocity
            newV = oldV + random.randint(rmin, rmax)
            event.velocity = newV
    mf2.tracks.append(track)
    print(idx)

mf2.open(fp[:-4] + '_rand.mid', 'wb')
mf2.write()
mf2.close()
mf.close()
