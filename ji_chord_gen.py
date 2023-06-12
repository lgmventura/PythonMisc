#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 21:27:26 2023

@author: luiz
"""

import numpy as np
import music21 as mus
from midigenlib import populate_midi_track_from_data_chords
from scipy.io import wavfile as wf
from datetime import datetime as dtm
from os import path

output = 'wav'

dims = np.array([3/2, 4/3])

root_note = mus.pitch.Pitch(60)

lattice = [[0, 3],
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


outPath = '/home/luiz/Music/Algoritmos'

if output == 'mid':
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
    temp_filename = dtm.isoformat(dtm.now()).replace(':', '')[:17]
    temp_filename = path.join(outPath, temp_filename + '_chord.mid')
    print("Saving file to: %s" % temp_filename)
    mf.open(temp_filename, 'wb')
    mf.write()
    mf.close()

elif output == 'wav':
    samplerate = 44100; fs = 100

    t_per_note = 1
    t = np.linspace(0., t_per_note, int(samplerate*t_per_note))

    amplitude = int(np.iinfo(np.int16).max / 10)


    wavdata = np.array([])
    for idx, noteDim in enumerate(notes):
        for jdx, note in enumerate(noteDim):
            data_n = amplitude * np.sin(2. * np.pi * note.frequency * t)
            if idx == 0 and jdx == 0:
                wavdata = np.copy(data_n)
            else:
                wavdata = wavdata + data_n
        
            
    wf.write(path.join(outPath, "ji_chord.wav"), samplerate, wavdata.astype(np.int16))