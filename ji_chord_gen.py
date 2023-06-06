#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 21:27:26 2023

@author: luiz
"""

import numpy as np
import music21 as mus
from midigenlib import populate_midi_track_from_data_chords
from datetime import datetime as dtm
from os import path

dims = np.array([3/2, 4/3])

root_note = mus.pitch.Pitch(60)

lattice = [[-2,-1,0,1],
           [-2,2]]

notes = []
for idxDim, dim in enumerate(dims):
    notes_dim = []
    for idxStep, step in enumerate(lattice[idxDim]):
        note = mus.pitch.Pitch()
        note.frequency = root_note.frequency * \
            np.power(dim, float(lattice[idxDim][idxStep]))
        notes_dim.append(note)
    notes.append(notes_dim)

mts = []
mts.append(mus.midi.MidiTrack(0))

data = []

pitches = []
cents = []
vels = []

for noteDim in notes:
    for note in noteDim:
        pitches.append(note.midi)
        cents.append(note.getCentShiftFromMidi())
        vels.append(80)

data.append([1, pitches, cents, vels])
data.append([1, pitches, cents, vels])

populate_midi_track_from_data_chords(mts[0], data)

mf = mus.midi.MidiFile()
for mt in mts:
    mf.tracks.append(mt)

# env = environment.Environment()
# temp_filename = env.getTempFile('.mid')
outPath = '/home/luiz/Music/Algoritmos'
temp_filename = dtm.isoformat(dtm.now()).replace(':', '')[:17]
temp_filename = path.join(outPath, temp_filename + '_chord.mid')
print("Saving file to: %s" % temp_filename)
mf.open(temp_filename, 'wb')
mf.write()
mf.close()