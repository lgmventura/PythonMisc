#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 21:53:40 2025

@author: luiz
"""

from music21 import midi, note, chord
import random

sigma_start = 20.0

dur_mu = 0.88
dur_sigma = 0.05
dur_max = 0.92

rmin_vel = -20
rmax_vel = 10

min_duration = 14

min_vel = 12

# Load a MIDI file
fp = '/home/luiz/Music/Composições/Piano solo/20241006.mid'


mf = midi.MidiFile()

mf.open(fp)

mf.read()

mf2 = midi.MidiFile()
mf2.ticksPerQuarterNote = mf.ticksPerQuarterNote


for idx1, track in enumerate(mf.tracks):
    note_dict = {}  # idx: [note_on, note_off, duration]
    note_event_list = []
    # absolute_times = [0] * len(track.events)
    current_time = 0
    note_event_abs_time = []
    note_on_off = []
    indices = []
    for idx2, event in enumerate(track.events):
        if isinstance(event, midi.DeltaTime):
            current_time += event.time
        # absolute_times[i] = current_time
            
        if event.type == midi.ChannelVoiceMessages.NOTE_ON and event.velocity > 0:
            oldV = event.velocity
            newV = oldV + random.randint(rmin_vel, rmax_vel)
            event.velocity = max(min_vel, newV)
            
            event.time = event.time + int(random.normalvariate(sigma_start*2, sigma_start))
            note_event_list.append(event)
            note_event_abs_time.append(current_time)
            note_on_off.append(True)
            indices.append(idx2)
        if event.type == midi.ChannelVoiceMessages.NOTE_OFF or (event.type == midi.ChannelVoiceMessages.NOTE_ON and event.velocity == 0):
            note_event_list.append(event)
            note_event_abs_time.append(current_time)
            note_on_off.append(False)
            indices.append(idx2)
            
            # duration_jitter = random.randint(-120, -4)
            # event.time += duration_jitter
            
    # run through list again and match notes
    for idx3, current_time in enumerate(note_event_abs_time):
        if not note_on_off[idx3]:  # is note off
            idx4 = idx3
            while True:  # run from the current note off backwards
                # idx4 will search for the note on
                if note_event_list[idx4].pitch == note_event_list[idx3].pitch and note_on_off[idx4]:
                    duration = current_time - note_event_abs_time[idx4]
                    note_dict[indices[idx3]] = [note_event_list[idx4], note_event_list[idx3], duration]
                
                idx4 = idx4 - 1
                if idx4 == -1:
                    break
            
    
    for idx2, event in enumerate(track.events):
        if event.type == midi.ChannelVoiceMessages.NOTE_OFF or (event.type == midi.ChannelVoiceMessages.NOTE_ON and event.velocity == 0):
            duration = note_dict[idx2][2]
            
            duration_jitter = random.randint(-120, -4)
            duration_jitter = max(duration_jitter, - duration + min_duration)
            
            event.time += duration_jitter
                    
    mf2.tracks.append(track)
    print(idx1)

mf2.open(fp[:-4] + '_rand_mult.mid', 'wb')
mf2.write()
mf2.close()
mf.close()