#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 13:08:34 2023

@author: luiz
"""

import pandas as pd
import geopandas
import folium
import geodatasets
import matplotlib.pyplot as plt

import webbrowser

import exif
import ffmpeg
from datetime import datetime

import os

photos_dir = '/media/luiz/HDp1/Celular/MiNote10/20231010'

# world = geopandas.read_file(geodatasets.get_path("naturalearth.land"))

# fig, ax = plt.subplots(figsize=(24, 18))
# world.plot(ax=ax, alpha=0.4, color="grey")
def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    return dd

data = pd.DataFrame()

mp = folium.Map(location=[64.98, -18.61], tiles='OpenStreetMap', zoom_start=7)# tiles="CartoDB Positron", zoom_start=7)
all_coords = []

for file in sorted(os.listdir(photos_dir)):
    if file.endswith('.jpg'):
        full_path = os.path.join(photos_dir, file)
        f_exif = exif.Image(full_path)
        if f_exif.has_exif is False:
            continue
        
        if 'datetime' not in dir(f_exif):
            continue
        
        dtime_str = f_exif.datetime
        dtime_iso_str = dtime_str.replace(':', '').replace(' ', '_')
        dtime = datetime.fromisoformat(dtime_iso_str)
        
        if 'gps_latitude' in dir(f_exif):
            gps_lat_dms = f_exif.gps_latitude
            gps_lon_dms = f_exif.gps_longitude
            gps_lat_ref = f_exif.gps_latitude_ref
            gps_lon_ref = f_exif.gps_longitude_ref
            
            gps_lat_dd = dms_to_dd(*gps_lat_dms) * (1 if gps_lat_ref == 'N' else -1)
            gps_lon_dd = dms_to_dd(*gps_lon_dms) * (1 if gps_lon_ref == 'E' else -1)
            
            if dtime > datetime(2023, 9, 23, 12, 00, 00) and \
                dtime < datetime(2023, 10, 8, 8, 00, 00):
                folium.Marker(
                  location=[gps_lat_dd, gps_lon_dd],
                  popup=file + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                  ).add_to(mp)
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)
    
    if file.endswith('.mp4'):
        full_path = os.path.join(photos_dir, file)
        tags = ffmpeg.probe(full_path)['format']['tags']
        dtime_iso_str = tags['creation_time'][:-4] # offset naïve: improve this!
        dtime = datetime.fromisoformat(dtime_iso_str)
        
        if 'location' in tags.keys():
            location_str = tags['location']
            gps_lat_dd = float(location_str[:8])
            gps_lon_dd = float(location_str[8:-1])
            
            if dtime > datetime(2023, 9, 23, 12, 00, 00) and \
                dtime < datetime(2023, 10, 8, 8, 00, 00):
                folium.Marker(
                  location=[gps_lat_dd, gps_lon_dd],
                  popup=file + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                  ).add_to(mp)
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)

data = data.sort_values('datetime')


for index, row in data.iterrows():
    all_coords.append([row['gps_lat'], row['gps_lon']])

folium.PolyLine(all_coords).add_to(mp)

mp.save("map.html")

webbrowser.open_new_tab("map.html")

