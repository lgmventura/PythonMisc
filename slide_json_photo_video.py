#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a JSON file for doing a photo + video presentation with
slide_show_html_photo_video_narration.py.

Created on Sun Jan 26 16:44:12 2025

@author: luiz
"""

import datetime as dt
import json
import numpy as np
import pandas as pd
from os import path, listdir
import re
import exif
import ffmpeg

img_formats = ('.jpg')
vid_formats = ('.mp4')

data = {'folder': ['/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6',
                   '/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6',
                   '/media/luiz/HDp1/Celular/MiNote10/20250112'],
        'datetime photo': ['exif',
                           'exif',
                           'file name'],
        'datetime video': ['getmtime',
                           'getmtime',
                           'file name'],
        'regex datetime': ['datetime',  # in this case, the exif name
                           'datetime',
                           r'_(\d+_\d+)'], # todo: find better names
        'offset': [dt.timedelta(hours=7),
                   dt.timedelta(hours=7),
                   dt.timedelta(0)]
        }

df = pd.DataFrame(data)

all_files = []
all_paths = []
all_dtimes = []
all_dt_w_offset = []
all_categs = []
for idx, folder in enumerate(df['folder']):
    files = listdir(folder)
    dt_photo = df['datetime photo'][idx]
    dt_video = df['datetime video'][idx]
    re_dtime = df['regex datetime'][idx]
    for idx2, file in enumerate(files):
        fp = path.join(folder, file)
        if file.lower().endswith(img_formats):  # photo
            if dt_photo == 'exif':
                img_exif = exif.Image(fp)
                if not img_exif.has_exif:
                    print(f'Skipping {file} - no exif.')
                    continue
                try:
                    file_dt_str = img_exif[re_dtime]
                except AttributeError as exception:
                    print(f'Skipping {file} - no {re_dtime}.')
                    print(exception)
                    continue
                file_dt = dt.datetime.fromisoformat(file_dt_str.replace(':', ''))
            elif dt_photo == 'file name':
                file_dt_matches = re.findall(re_dtime, file)
                if len(file_dt_matches) == 0:
                    print(f'Skipping {file}. No regex match found.')
                    continue
                file_dt_str = file_dt_matches[0]
                file_dt = dt.datetime.fromisoformat(file_dt_str)
            all_categs.append('image')
            
        elif file.lower().endswith(vid_formats):
            if dt_video == 'getmtime':
                time_stamp = path.getmtime(fp)
                file_dt = dt.datetime.fromtimestamp(time_stamp)
            elif dt_video == 'file name':
                file_dt_matches = re.findall(re_dtime, file)
                if len(file_dt_matches) == 0:
                    print(f'Skipping {file}. No regex match found.')
                    continue
                file_dt_str = file_dt_matches[0]
                file_dt = dt.datetime.fromisoformat(file_dt_str)
            all_categs.append('video')
        else:
            print(f'Skipping {file} - not a selected format.')
            continue
        
        file_dt_with_offset = file_dt + df['offset'][idx]
        
        all_files.append(file)
        all_paths.append(folder)
        all_dtimes.append(file_dt)
        all_dt_w_offset.append(file_dt_with_offset)

data_all = {'path': all_paths,
            'file': all_files,
            'category': all_categs,
            'datetime': all_dtimes,
            'dt_with_offset': all_dt_w_offset}

df_all = pd.DataFrame(data_all)
