#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 01:47:38 2021

@author: luiz
"""
import music21 as mus
import numpy as np
from io import BytesIO

fileLikeOpen = BytesIO()

mf = mus.midi.MidiFile()
mf.open(filename='/media/luiz/Volume/Dokumente/Musik/Projekte/Kompon/Gerada/test001.mid', attrib='wb')
#mf.ticksPerSecond = 1024
mf.ticksPerQuarterNote = 1024

mt0 = mus.midi.MidiTrack(index=0)
mt1 = mus.midi.MidiTrack(index=1)

# enumeration for channelVoiceMessages
cvm = mus.midi.ChannelVoiceMessages

dt = mus.midi.DeltaTime(mt0)
mt0.events = [dt]
dt = mus.midi.DeltaTime(mt1)
mt1.events = [dt]
for iP in range(20):
    t_on = iP*1024
    t_off = iP*1024 + 960
    # track mt0
    note_on = mus.midi.MidiEvent(track=mt0, type=cvm.NOTE_ON, time=t_on, channel=1)
    note_off = mus.midi.MidiEvent(track=mt0, type=cvm.NOTE_OFF, time=t_off, channel=1)
    note_on.pitch = iP+60
    note_off.pitch = iP+60
    note_on.velocity = 80
    note_off.velocity = 0
    dt = mus.midi.DeltaTime(mt0, time=1000)
    mt0.events.append(note_on)
    mt0.events.append(dt)
    mt0.events.append(note_off)
    dt = mus.midi.DeltaTime(mt0, time=24)
    mt0.events.append(dt)
    
    #track mt1
    note_on = mus.midi.MidiEvent(track=mt1, type=cvm.NOTE_ON, time=t_on, channel=1)
    note_off = mus.midi.MidiEvent(track=mt1, type=cvm.NOTE_OFF, time=t_off, channel=1)
    note_on.pitch = iP+63
    note_off.pitch = iP+63
    note_on.velocity = 80
    note_off.velocity = 0
    dt = mus.midi.DeltaTime(mt1, time=1000)
    mt1.events.append(note_on)
    mt1.events.append(dt)
    mt1.events.append(note_off)
    dt = mus.midi.DeltaTime(mt1, time=24)
    mt1.events.append(dt)

eot = mus.midi.MetaEvents.END_OF_TRACK
# mt0.events.append(eot)
# mt1.events.append(eot)

mf.tracks.append(mt0)
mf.tracks.append(mt1)

mf.write()
mf.close()