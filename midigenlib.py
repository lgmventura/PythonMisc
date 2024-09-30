#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:11:22 2021

@author: luiz et al
"""
from music21 import midi, environment

# https://github.com/cuthbertLab/music21/blob/c6fc39204c16c47d1c540b545d0c9869a9cafa8f/music21/midi/__init__.py#L1471
def populate_midi_track_from_data(mt, data, initial_delay=0):
    # notes
    t = initial_delay
    tLast = 0
    for d, p, v in data:
        dt = midi.DeltaTime(mt)
        dt.time = t - tLast
        # add to track events
        mt.events.append(dt)

        me = midi.MidiEvent(mt)
        me.type = midi.ChannelVoiceMessages.NOTE_ON
        me.channel = 1
        me.time = None  # d
        me.pitch = p
        me.velocity = v
        mt.events.append(me)

        # add note off / velocity zero message
        dt = midi.DeltaTime(mt)
        dt.time = d
        # add to track events
        mt.events.append(dt)

        me = midi.MidiEvent(mt)
        me.type = midi.ChannelVoiceMessages.NOTE_OFF
        me.channel = 1
        me.time = None  # d
        me.pitch = p
        me.velocity = 0
        mt.events.append(me)

        tLast = t + d  # have delta to note off
        t += d  # next time

    # add end of track
    dt = midi.DeltaTime(mt)
    dt.time = 0
    mt.events.append(dt)

    me = midi.MidiEvent(mt)
    me.type = midi.MetaEvents.END_OF_TRACK
    me.channel = 1
    me.data = ''  # must set data to empty string
    mt.events.append(me)

    return mt

def populate_midi_track_from_data_chords(mt, data):
    t = 0
    tLast = 0
    for d, ps, cs, vs in data: # delta, pitches, cents, velocities
        dt = midi.DeltaTime(mt)
        dt.time = t - tLast
        # add to track events
        mt.events.append(dt)

        for ip, p in enumerate(ps):
            me = midi.MidiEvent(mt)
            me.type = midi.ChannelVoiceMessages.NOTE_ON
            me.channel = 1
            me.time = None  # d
            me.pitch = p
            me.velocity = vs[ip]
            me.centShift = cs[ip]
            mt.events.append(me)

            # add note off / velocity zero message
            dt = midi.DeltaTime(mt)
            dt.time = d
            # add to track events
            mt.events.append(dt)

        for ip, p in enumerate(ps):
            me = midi.MidiEvent(mt)
            me.type = midi.ChannelVoiceMessages.NOTE_OFF
            me.channel = 1
            me.time = None  # d
            me.pitch = p
            me.velocity = 0
            me.centShift = cs[ip]
            mt.events.append(me)

        tLast = t + d  # have delta to note off
        t += d  # next time

    # add end of track
    dt = midi.DeltaTime(mt)
    dt.time = 0
    mt.events.append(dt)

    me = midi.MidiEvent(mt)
    me.type = midi.MetaEvents.END_OF_TRACK
    me.channel = 1
    me.data = ''  # must set data to empty string
    mt.events.append(me)

    return mt