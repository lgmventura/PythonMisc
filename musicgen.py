#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:33:28 2021

@author: luiz
"""
import numpy as np
from music21 import midi, note, chord, environment
from midigenlib import populate_midi_track_from_data

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

nT = 5
mts = []
for iT in range(nT):
    mts.append(midi.MidiTrack(iT))



beats_per_measure = 4
measures = 16
num_beats = measures * beats_per_measure

mode = [0, 1, 4, 6, 7, 9, 10]
seq1 = np.random.randint(1, 24, measures * beats_per_measure)
seq2 = np.array(list(fib(measures * beats_per_measure)))

# note array is ordered [duration, pitch, velocity]
def algorithm1(num_beats):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = np.random.randint(1,7) * 128
        pitch = np.random.randint(36, 60)
        velocity = np.random.randint(60, 80)
    
        data.append([duration, pitch, velocity])
        
        for iT in range(nT - 1):
            r = np.random.rand()
            if r < 0.15:
                pitchCtpt = pitch + 3
            elif r < 0.3:
                pitchCtpt = pitch + 4
            elif r < 0.45:
                pitchCtpt = pitch + 5
            elif r < 0.6:
                pitchCtpt = pitch + 6
            elif r < 0.7:
                pitchCtpt = pitch + 7
            else:
                pitchCtpt = pitch + np.random.randint(1, 24)
            
            dataCtpt.append([])
            dataCtpt[iT].append([duration, pitchCtpt, velocity])
            
    return data, dataCtpt

def algorithm2(num_beats, modeList: list = [0,2,4,5,7,9,11]):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    ms = len(modeList)
    mode_arr = np.array(modeList)
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = np.random.randint(1,7)**2 * 128
        pitch = 24 + 12*np.random.randint(0, 4) + modeList[np.random.randint(0, ms)]
        velocity = np.random.randint(60, 80)
    
        data.append([duration, pitch, velocity])
        
        for iT in range(nT - 1):
            # r = np.random.rand()
            # if r < 0.02:
            #     pitchCtpt = pitch + 3
            # elif r < 0.03:
            #     pitchCtpt = pitch + 4
            # elif r < 0.045:
            #     pitchCtpt = pitch + 5
            # elif r < 0.06:
            #     pitchCtpt = pitch + 6
            # elif r < 0.07:
            #     pitchCtpt = pitch + 7
            # else:
            #     pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
            #pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
            durationT = np.random.randint(1,7)**2 * 128
            pitchCtpt = pitch + np.random.randint(1, 24)
            pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
            pitchCtpt = int(pitchCtpt)
            
            dataCtpt.append([])
            dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data, dataCtpt

def algorithm3(num_beats, modeList: list = [0,2,4,5,7,9,11]):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    ms = len(modeList)
    mode_arr = np.array(modeList)
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = (seq2[i]%7)**2 * 128
        pitch = 24 + 12*np.round(seq2[i] * 1.2)%4 + modeList[np.random.randint(0, ms)]
        velocity = np.random.randint(60, 80)
    
        data.append([duration, pitch, velocity])
        
        for iT in range(nT - 1):
            # r = np.random.rand()
            # if r < 0.02:
            #     pitchCtpt = pitch + 3
            # elif r < 0.03:
            #     pitchCtpt = pitch + 4
            # elif r < 0.045:
            #     pitchCtpt = pitch + 5
            # elif r < 0.06:
            #     pitchCtpt = pitch + 6
            # elif r < 0.07:
            #     pitchCtpt = pitch + 7
            # else:
            #     pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
            #pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
            durationT = np.random.randint(1,7)**2 * 128
            pitchCtpt = pitch + np.round(seq2[i + 30] * 1.2)%24
            pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
            pitchCtpt = int(pitchCtpt)
            
            dataCtpt.append([])
            dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data, dataCtpt

data, dataCtpt = algorithm2(num_beats, modeList=[0,1,4,5,7,8,10,11])
populate_midi_track_from_data(mts[0], data)
for iT in range(nT - 1):
    populate_midi_track_from_data(mts[iT + 1], dataCtpt[iT])


mf = midi.MidiFile()
for mt in mts:
    mf.tracks.append(mt)

env = environment.Environment()
temp_filename = env.getTempFile('.mid')
print("Saving file to: %s" % temp_filename)
mf.open(temp_filename, 'wb')
mf.write()
mf.close()