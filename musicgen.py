#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:33:28 2021

@author: luiz
"""
import numpy as np
from music21 import stream, meter, midi, note, tempo
from datetime import datetime as dtm
from os import path

from fractal_segments import koch, draw_angle_path
from math_extra import is_prime, divisors

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

nT = 3  # number of tracks (polyphony)
num_measures = 20  #
time_signature = (4, 4)  # time signature, for now, only one for the whole piece

#mode = [0, 1, 4, 6, 7, 9, 10] # crazy septatonic mode
#mode = [0,1,4,5,7,8,10,11] # some octatonic scale
mode = [0,2,3,5,7,9,11] # minor scale
#mode = [0,2,4,5,7,9,11] # major scale
#mode = [0,3,7] # minor triad
#mode = [0,4,7] # major triad
#mode = [0] # monote

# seq1 = np.random.randint(1, 24, num_measures)
# seq2 = np.array(list(fib(measures * beats_per_measure)))
# vel_seq = np.random.randint(40, 80, num_measures)

# note array is ordered [duration, pitch, velocity]
# def algorithm1(num_measures):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = np.random.randint(1,7) * 128
#         pitch = np.random.randint(36, 60)
#         velocity = vel_seq[i]
    
#         data.append([duration, pitch, velocity])
        
#         for iT in range(nT - 1):
#             r = np.random.rand()
#             if r < 0.15:
#                 pitchCtpt = pitch + 3
#             elif r < 0.3:
#                 pitchCtpt = pitch + 4
#             elif r < 0.45:
#                 pitchCtpt = pitch + 5
#             elif r < 0.6:
#                 pitchCtpt = pitch + 6
#             elif r < 0.7:
#                 pitchCtpt = pitch + 7
#             else:
#                 pitchCtpt = pitch + np.random.randint(1, 24)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([duration, pitchCtpt, velocity])
            
#     return data, dataCtpt

# def algorithm2(num_measures, modeList: list = [0,2,4,5,7,9,11]):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     ms = len(modeList)
#     mode_arr = np.array(modeList)
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = np.random.randint(1,7)**2 * 128
#         pitch = 24 + 12*np.random.randint(0, 4) + modeList[np.random.randint(0, ms)]
#         velocity = vel_seq[i]
    
#         data.append([duration, pitch, velocity])
        
#         for iT in range(nT - 1):
#             # r = np.random.rand()
#             # if r < 0.02:
#             #     pitchCtpt = pitch + 3
#             # elif r < 0.03:
#             #     pitchCtpt = pitch + 4
#             # elif r < 0.045:
#             #     pitchCtpt = pitch + 5
#             # elif r < 0.06:
#             #     pitchCtpt = pitch + 6
#             # elif r < 0.07:
#             #     pitchCtpt = pitch + 7
#             # else:
#             #     pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
#             #pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
#             durationT = np.random.randint(1,7)**2 * 128
#             pitchCtpt = pitch + np.random.randint(1, 24)
#             pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
#             pitchCtpt = int(pitchCtpt)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
#     return data, dataCtpt

# def algorithm3(num_measures, modeList: list = [0,2,4,5,7,9,11]):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     ms = len(modeList)
#     mode_arr = np.array(modeList)
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = (seq2[i]%7)**2 * 128
#         pitch = 24 + 12*np.round(seq2[i] * 1.2)%4 + modeList[np.random.randint(0, ms)]
#         velocity = vel_seq[i]
    
#         data.append([duration, pitch, velocity])
        
#         for iT in range(nT - 1):
#             # r = np.random.rand()
#             # if r < 0.02:
#             #     pitchCtpt = pitch + 3
#             # elif r < 0.03:
#             #     pitchCtpt = pitch + 4
#             # elif r < 0.045:
#             #     pitchCtpt = pitch + 5
#             # elif r < 0.06:
#             #     pitchCtpt = pitch + 6
#             # elif r < 0.07:
#             #     pitchCtpt = pitch + 7
#             # else:
#             #     pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
#             #pitchCtpt = pitch + modeList[np.random.randint(0, ms)]
#             durationT = np.random.randint(1,7)**2 * 128
#             pitchCtpt = pitch + np.round(seq2[i + 30] * 1.2)%24
#             pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
#             pitchCtpt = int(pitchCtpt)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
#     return data, dataCtpt

# seq3 = seq1[seq2%10]
# seq4 = seq3[seq2%10]
# def algorithm4(num_measures, modeList: list = [0,2,4,5,7,9,11]):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     ms = len(modeList)
#     mode_arr = np.array(modeList)
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = (seq3[i]%6)**2 * 256
#         pitch = 24 + 12*np.round(seq3[i] * 1.2)%5 + modeList[seq3[i] % ms] # octave + mode position in octave
#         pitch = pitch + round(i/10) * 5 # key changes
#         pitch = int(pitch)
#         velocity = vel_seq[i]
    
#         data.append([duration, pitch, velocity])
        
#         for iT in range(nT - 1):
#             durationT = (seq3[(i + iT) % num_measures]%6)**2 * 256
#             pitchCtpt = pitch + np.round(seq3[i] * 1.2)%24
#             pitchCtpt = pitchCtpt + mode_arr[(iT * seq3[i]) % ms]
#             pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
#             pitchCtpt = int(pitchCtpt)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
#     return data, dataCtpt

# def algorithm5(num_measures, modeList: list = [0,2,4,5,7,9,11]):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     ms = len(modeList)
#     mode_arr = np.array(modeList)
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = (seq3[i]%2 + 1)*2 * 256
#         pitch = 24 + 12*np.round(seq3[i] * 1.2)%5 + modeList[seq3[i] % ms] # octave + mode position in octave
#         pitch = pitch + seq3[int(i/20)] % 8 * 5 # key changes
#         pitch = int(pitch)
#         velocity = vel_seq[i]
    
#         data.append([duration, pitch, velocity])
        
#         for iT in range(nT - 1):
#             durationT = (seq3[(i + iT) % num_measures]%2 + 1)*2 * 256
#             pitchCtpt = pitch + np.round(seq3[i] * 1.2)%24
#             pitchCtpt = pitchCtpt + mode_arr[(4 + iT + seq3[i]) % ms]
#             pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
#             pitchCtpt = int(pitchCtpt)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
#     return data, dataCtpt

# def algorithm6(num_measures, modeList: list = [0,2,4,5,7,9,11]):
#     # duration, pitch, velocity
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
#     ms = len(modeList)
#     mode_arr = np.array(modeList)
#     for i in range(1, num_measures):
#         # pick random pitch and velocity for 8th note
#         duration = (seq3[i]%5 + 1)*2 * 128
#         base_octave = 24 + round(seq3[i]/12)*12
#         pitch = base_octave + mode_arr[seq3[i] % ms] # octave + mode position in octave
#         key_base = seq3[int(i/10)] % 5 * 5 # key changes
#         pitch = pitch + key_base
#         pitch = int(pitch)
#         velocity = vel_seq[i]
    
#         data.append((duration, pitch, velocity))
        
#         for iT in range(nT - 1):
#             durationT = (seq3[(i + 10 + 3*iT) % num_measures]%8 + 1)*2 * 64
#             # if seq3[(i + 10 + 3*iT) % num_measures] > 20:
#             #     durationT = durationT + int(256/3)
#             pitchCtpt = base_octave + 24 + key_base # + np.round(seq3[i] * 1.2)%24 # counterpoint two octaves higher
#             pitchCtpt = pitchCtpt + mode_arr[(4 + 2*iT + seq3[num_measures - i]) % ms]
#             # pitchCtpt = int(pitchCtpt/12)*12 + mode_arr[np.argsort(abs(np.mod(pitchCtpt, 12) - mode_arr))[0]] # forcing the pitchCtpt to be n*12 + any(mode)
#             pitchCtpt = int(pitchCtpt)
            
#             dataCtpt.append([])
#             dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
#     return data, dataCtpt

# def algorithm7(nums: complex, t0, t1, num_measures):
#     data = [] # one start note
#     dataCtpt = [] # data counterpoint
    
# using linear fractal (e.g. Koch)
def algorithm8(fractal_array_angles):
    # duration, pitch, velocity
    data = [] # one start note
    for iT in range(nT):
        voice_data = []
        for idx, iang in enumerate(fractal_array_angles):
            ang_rad = iang * np.pi/180
            jang = iang * iT
            jang_rad = jang * np.pi/180
            # pick random pitch and velocity for 8th note
            duration = 1 + int(4 * np.cos(ang_rad * iT))/8
            pitch = 72 + 12*iang/360 * len(divisors(abs(iang) + iT)) - iT*12
            pitch = pitch + is_prime(iang)*12
            pitch = int(pitch)
            if pitch < 20 or pitch > 112:
                pitch = 0  # will be a rest
            
            velocity = 80 + np.random.randint(0, 20)
        
            voice_data.append({'duration': duration,
                         'pitch': pitch,
                         'velocity': velocity})
        data.append(voice_data)
        # # new counterpoint tracks
        # for iT in range(nT - 1):
        #     jval = fractal_array_angles[max(0, idx - nT*12)]
        #     ang_rad_j = jval * np.pi/180
            
        #     durationT = 2*(2 + int(4 * np.cos(ang_rad_j)))/4
        #     pitchCtpt = pitch - np.round(len(divisors(abs(ival)*iT)))%24 - iT*12
        #     pitchCtpt = int(pitchCtpt)
            
        #     dataCtpt.append([])
        #     dataCtpt[iT].append([durationT, pitchCtpt, velocity])
            
    return data

# def equalize_durations(data):
#     voice_durations = np.array([])
#     for voice in data:
#         voice_duration = 0
#         for nt in voice:
#             voice_duration = voice_duration + nt['duration']
#             if nt['duration'] <= 0:
#                 raise(ValueError('Duration must be positive'))
#         voice_durations = np.append(voice_durations, voice_duration)
#     total_duration = np.max(voice_durations)
#     print(total_duration)
#     print(voice_durations)
    
#     return data
    
# algorithm to use, change here:
algToUse = algorithm8

# calling algorithm (don't change here, change above)
# data = algToUse(num_measures, modeList=mode)
arr = koch(3, 42, -42)
arr2 = np.tile(arr, (20, 1))//13
arr2 = arr2.T.flatten()
arr2 = arr2[:arr.size]
arr = arr + arr2

data = algorithm8(arr)

outPath = '/home/luiz/Music/Algoritmos/'
out_filename = dtm.isoformat(dtm.now()).replace(':', '')[:17]
out_filename = path.join(outPath, out_filename)

# Create a Part and Measure
part = stream.Part()
part.append(meter.TimeSignature(f"{time_signature[0]}/{time_signature[1]}"))

# Voices
voices = []
# data = equalize_durations(data)
for idx_voice, voice_data in enumerate(data):
    notes = []
    for idx_note, note_data in enumerate(voice_data):
        if note_data['pitch'] == 0:
            nt = note.Rest(quarterLength=note_data['duration'])
        else:
            nt = note.Note(note_data['pitch'],
                             quarterLength=note_data['duration'],
                             velocity=note_data['velocity'])
        notes.append(nt)
    voice = stream.Voice(notes)
    voice.id = f"voice{idx_voice}"
    voices.append(voice)

# Insert all voices at offset 0 in the measure
measure = stream.Measure()
for idx, voice in enumerate(voices):
    measure.insert(0, voice)  # Start at 0.0
part.append(measure)

# Export MusicXML (works in MuseScore)
try:
    part.write('musicxml', fp=f'{out_filename}.xml')
except Exception as err:
    print(err)

# Export MIDI (flatten to merge voices)
midi_stream = part.flatten()  # Combine voices into a single track
mf = midi.translate.streamToMidiFile(midi_stream)
mf.open(f'{out_filename}.mid', 'wb')  # 'wb' = write binary
mf.write()
mf.close()
# saving state to reproduce
import inspect

with open(out_filename + '_config_used.txt', 'w') as out_txt_file:
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
    #lines = inspect.getsource(algToUse) # getting source code from algorithm being used
    with open(__file__, 'r') as self_file:
        lines = self_file.read()
        
    out_txt_file.write('Code from ' + algToUse.__name__ + ':\n')
    out_txt_file.write(lines)
    # out_txt_file.write(algToUse.__name__)
    # out_txt_file.write('seq1 = ' + str(seq1))
    # out_txt_file.write('seq2 = ' + str(seq2))
    # out_txt_file.write('seq3 = ' + str(seq3))

