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


import xml.etree.ElementTree as ET
import base64
import os
from collections import defaultdict

def find_element(parent, local_name):
    """Find first child element by local tag name (ignoring namespace)."""
    if parent is None:
        return None
    for child in parent:
        tag = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
        if tag == local_name:
            return child
    return None

def findall_elements(parent, local_name):
    """Find all child elements by local tag name (ignoring namespace)."""
    elements = []
    if parent is None:
        return elements
    for child in parent:
        tag = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
        if tag == local_name:
            elements.append(child)
    return elements

def add_tempo_changes(input_file, output_file, tempo_changes):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Detect namespace from root
    namespace = root.tag.split('}', 1)[0] + '}' if '}' in root.tag else ''

    # Helper to create elements with namespace
    def make_element(tag):
        return ET.Element(f"{namespace}{tag}")

    # Find Score > Part > Staff
    score = find_element(root, 'Score')
    part = find_element(score, 'Part')
    staff = find_element(score, 'Staff')
    measures = findall_elements(staff, 'Measure')

    # Group tempo changes by measure number
    tempo_by_measure = defaultdict(list)
    for measure_num, tempo_bpm in tempo_changes:
        tempo_by_measure[measure_num].append(tempo_bpm)

    # Process each measure with tempo changes
    for measure_num, tempos in tempo_by_measure.items():
        index = measure_num - 1
        if index < 0 or index >= len(measures):
            print(f"Measure {measure_num} out of range. Skipping.")
            continue

        measure = measures[index]
        voices = findall_elements(measure, 'voice')
        voice = voices[0] if voices else None

        # Create voice if missing
        if voice is None:
            voice = make_element('voice')
            measure.insert(0, voice)  # Insert as first child

        # Add tempo changes in order
        for i, tempo_bpm in enumerate(tempos):
            # Generate unique ID
            eid = base64.urlsafe_b64encode(os.urandom(16)).decode('ascii').replace('=', '')
            
            # Build <Tempo> element
            tempo_elem = make_element('Tempo')
            
            # Sub-elements with text content
            ET.SubElement(tempo_elem, 'tempo').text = f"{tempo_bpm / 60.0:.6f}"
            ET.SubElement(tempo_elem, 'followText').text = '1'
            ET.SubElement(tempo_elem, 'eid').text = eid
            ET.SubElement(tempo_elem, 'visible').text = '0'
            
            # Construct <text> with symbol and BPM
            text_elem = ET.SubElement(tempo_elem, 'text')
            sym_elem = ET.SubElement(text_elem, 'sym')
            sym_elem.text = 'metNoteQuarterUp'
            sym_elem.tail = f' = {tempo_bpm}'  # Text after symbol

            # Insert tempo at position i in voice
            voice.insert(i, tempo_elem)

    # Format XML with indentation (Python 3.9+)
    if hasattr(ET, 'indent'):
        ET.indent(tree, space='  ')
    
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

measures = list(range(measure_offset, measure_offset + len(tempos)))
tempo_changes = list(zip(measures, tempos))

# Example usage:
add_tempo_changes('/home/luiz/Music/Transcrições/20250402 - Toque dia 27-02-2025 - 18h - Pilar - DR_0059 - rev1.mscx',
                  '/home/luiz/Music/Transcrições/20250402 - Toque dia 27-02-2025 - 18h - Pilar - DR_0059 - rev1 - sync.mscx', tempo_changes)
