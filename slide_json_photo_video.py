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

data = {'folder': ['/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6',
                   '/media/luiz/HDp1/Celular/MiNote10/20250112'],
        'datetime photo': ['exif',
                           'file name'],
        'datetime video': ['getmtime',
                           'file name'],
        'regex datetime': ['datetime',  # in this case, the exif name
                           r'_(\d+_\d+)'], # todo: find better names
        'offset': [dt.timedelta(hours=7),
                   dt.timedelta(0)]
        }

df = pd.DataFrame(data)

for idx, folder in enumerate(df['folder']):
    files = listdir(folder)
    dt_photo = df['datetime photo'][idx]
    dt_video = df['datetime video'][idx]
    re_dtime = df['regex datetime'][idx]
    for idx2, file in enumerate(files):
        fp = path.join(folder, file)
        if file.lower().endswith('.jpg'):  # photo
            if dt_photo == 'exif':
                img_exif = exif.Image(fp)
                file_dt_str = img_exif[re_dtime]
                file_dt = dt.datetime.fromisoformat(file_dt_str.replace(':', ''))
            elif dt_photo == 'file name':
                file_dt_str = re.findall(re_dtime, file)[0]
                file_dt = dt.datetime.fromisoformat(file_dt_str)
                
        elif file.lower().endswith('.mp4'):
            if dt_video == 'getmtime':
                time_stamp = path.getmtime(fp)
                file_dt = dt.datetime.fromtimestamp(time_stamp)
            elif dt_video == 'file name':
                file_dt_str = re.findall(re_dtime, file)[0]
                file_dt = dt.datetime.fromisoformat(file_dt_str)
                
        file_dt_with_offset = file_dt + df['offset'][idx]