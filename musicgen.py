#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:33:28 2021

@author: luiz
"""
import numpy as np
from music21 import midi, note, chord, environment
from midigenlib import populate_midi_track_from_data
from datetime import datetime as dtm
from os import path

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

#mode = [0, 1, 4, 6, 7, 9, 10] # crazy septatonic mode
#mode = [0,1,4,5,7,8,10,11] # some octatonic scale
mode = [0,2,3,5,7,9,11] # minor scale
#mode = [0,2,4,5,7,9,11] # major scale
#mode = [0,3,7] # minor triad
#mode = [0,4,7] # major triad
#mode = [0] # monote

seq1 = np.random.randint(1, 24, num_beats)
seq2 = np.array(list(fib(measures * beats_per_measure)))
vel_seq = np.random.randint(40, 80, num_beats)

# note array is ordered [duration, pitch, velocity]
def algorithm1(num_beats):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = np.random.randint(1,7) * 128
        pitch = np.random.randint(36, 60)
        velocity = vel_seq[i]
    
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
        velocity = vel_seq[i]
    
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
        velocity = vel_seq[i]
    
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

seq3 = seq1[seq2%10]
seq4 = seq3[seq2%10]
def algorithm4(num_beats, modeList: list = [0,2,4,5,7,9,11]):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    ms = len(modeList)
    mode_arr = np.array(modeList)
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = (seq3[i]%6)**2 * 256
        pitch = 24 + 12*np.round(seq3[i] * 1.2)%5 + modeList[seq3[i] % ms] # octave + mode position in octave
        pitch = pitch + round(i/10) * 5 # key changes
        pitch = int(pitch)
        velocity = vel_seq[i]
    
        data.append([duration, pitch, velocity])
        
        for iT in range(nT - 1):
            durationT = (seq3[(i + iT) % num_beats]%6)**2 * 256
            pitchCtpt = pitch + np.round(seq3[i] * 1.2)%24
            pitchCtpt = pitchCtpt + mode_arr[(iT * seq3[i]) % ms]
            pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
            pitchCtpt = int(pitchCtpt)
            
            dataCtpt.append([])
            dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data, dataCtpt

def algorithm5(num_beats, modeList: list = [0,2,4,5,7,9,11]):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    ms = len(modeList)
    mode_arr = np.array(modeList)
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = (seq3[i]%2 + 1)*2 * 256
        pitch = 24 + 12*np.round(seq3[i] * 1.2)%5 + modeList[seq3[i] % ms] # octave + mode position in octave
        pitch = pitch + seq3[int(i/20)] % 8 * 5 # key changes
        pitch = int(pitch)
        velocity = vel_seq[i]
    
        data.append([duration, pitch, velocity])
        
        for iT in range(nT - 1):
            durationT = (seq3[(i + iT) % num_beats]%2 + 1)*2 * 256
            pitchCtpt = pitch + np.round(seq3[i] * 1.2)%24
            pitchCtpt = pitchCtpt + mode_arr[(4 + iT + seq3[i]) % ms]
            pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
            pitchCtpt = int(pitchCtpt)
            
            dataCtpt.append([])
            dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data, dataCtpt

def algorithm6(num_beats, modeList: list = [0,2,4,5,7,9,11]):
    # duration, pitch, velocity
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    ms = len(modeList)
    mode_arr = np.array(modeList)
    for i in range(1, num_beats):
        # pick random pitch and velocity for 8th note
        duration = (seq3[i]%5 + 1)*2 * 128
        base_octave = 24 + round(seq3[i]/12)*12
        pitch = base_octave + mode_arr[seq3[i] % ms] # octave + mode position in octave
        key_base = seq3[int(i/10)] % 5 * 5 # key changes
        pitch = pitch + key_base
        pitch = int(pitch)
        velocity = vel_seq[i]
    
        data.append((duration, pitch, velocity))
        
        for iT in range(nT - 1):
            durationT = (seq3[(i + 10 + 3*iT) % num_beats]%8 + 1)*2 * 64
            # if seq3[(i + 10 + 3*iT) % num_beats] > 20:
            #     durationT = durationT + int(256/3)
            pitchCtpt = base_octave + 24 + key_base # + np.round(seq3[i] * 1.2)%24 # counterpoint two octaves higher
            pitchCtpt = pitchCtpt + mode_arr[(4 + 2*iT + seq3[num_beats - i]) % ms]
            # pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
            pitchCtpt = int(pitchCtpt)
            
            dataCtpt.append([])
            dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data, dataCtpt

def algorithm7(nums: complex, t0, t1, num_beats):
    data = [] # one start note
    dataCtpt = [] # data counterpoint
    
    


# algorithm to use, change here:
algToUse = algorithm6

# calling algorithm (don't change here, change above)
data, dataCtpt = algToUse(num_beats, modeList=mode)
populate_midi_track_from_data(mts[0], data)
for iT in range(nT - 1):
    populate_midi_track_from_data(mts[iT + 1], dataCtpt[iT])


mf = midi.MidiFile()
for mt in mts:
    mf.tracks.append(mt)

# env = environment.Environment()
# temp_filename = env.getTempFile('.mid')
outPath = '/media/luiz/Volume/Dokumente/Musik/Projekte/Kompon/Algoritmos'
temp_filename = dtm.isoformat(dtm.now()).replace(':', '')[:17]
temp_filename = path.join(outPath, temp_filename + '.mid')
print("Saving file to: %s" % temp_filename)
mf.open(temp_filename, 'wb')
mf.write()
mf.close()

# saving state to reproduce
import inspect

with open(temp_filename + '_config_used.txt', 'w') as out_txt_file:
    out_txt_file.write('key\tvalue\n')
    for key in dir():
        if key[0] != '_' and key not in ['exit', 'environment',
                                         'export_variables', 'key', 'In',
                                         'my_shelf', 'Out', 'quit', 'shelve']:
            try:
                out_txt_file.write(key + '\t' + str(globals()[key]) + '\n')
            except:
                #
                # __builtins__, my_shelf, and imported modules can not be shelved.
                #
                print('ERROR saving: {0}'.format(key))
    lines = inspect.getsource(algToUse) # getting source code from algorithm being used
    out_txt_file.write('Code from ' + algToUse.__name__ + ':\n')
    out_txt_file.write(lines)
    # out_txt_file.write(algToUse.__name__)
    # out_txt_file.write('seq1 = ' + str(seq1))
    # out_txt_file.write('seq2 = ' + str(seq2))
    # out_txt_file.write('seq3 = ' + str(seq3))


# import shelve

# my_shelf = shelve.open(temp_filename + '.txt', 'n') # 'n' for new

# for key in dir():
#     if key[0] != '_':# and key not in ['exit', 'environment', 'export_variables', 'key', 'my_shelf', 'quit', 'shelve']:
#         try:
#             my_shelf[key] = globals()[key]
#         except:
#             #
#             # __builtins__, my_shelf, and imported modules can not be shelved.
#             #
#             print('ERROR shelving: {0}'.format(key))
# my_shelf.close()
