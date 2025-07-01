#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This aims to take labels exported from audacity marking each
beat and create a list of tempos for musescore to sync the
music or whatever rhythmic is there.

Still alpha: more functionality is going to come.

Created on Mon 30/06/2025, 22:01:14 +0200

@author: luiz
"""

import numpy as np
import pandas as pd

import re

audacity_labels_fp = '/media/luiz/HDp1/Gravações/20250330/SJDR/20250227 - 18h Pilar DR_0059 - compassos rev1.txt'


aud_labels_df = pd.read_csv(audacity_labels_fp, delimiter='\t', header=None)

def is_time_signature(text):
    if isinstance(text, str):
        if re.match('\d+/\d+', text):
            return True
        else:
            return False
    else:
        return False

def get_time_signature(text):
    if not is_time_signature(text):
        raise(ValueError("text must be in the form a/b"))
    numerator = int(re.findall('(\d+)/\d+', lab_text)[0])
    denominator = int(re.findall('\d+/(\d+)', lab_text)[0])
    return (numerator, denominator)

def calc_tempo(delta_time_s, tsig):
    tempo = tsig[0]/tsig[1] / delta_time_s * 4 * 60
    return tempo

last_lab_start = None
last_time_sig = None
tempos = []
for idx, row in aud_labels_df.iterrows():
    lab_start = row[0]
    lab_end = row[1]
    lab_text = row[2]
    
    time_sig = (4, 4)  # default if not given
    if is_time_signature(lab_text):
        time_sig = get_time_signature(lab_text)
    
    if last_lab_start is not None:
        delta_time_s = lab_start - last_lab_start
        tempo = round(calc_tempo(delta_time_s, last_time_sig), 4)
        
        tempos.append(tempo)
    
    last_lab_start = lab_start
    last_time_sig = time_sig

# score
measure_offset = 86