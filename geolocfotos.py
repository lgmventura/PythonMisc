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

import numpy as np

import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from PIL import Image

# croácia 2013 (infelizmente, quase nenhum dado de GPS)
#photos_dir = '/media/luiz/Elements/FotosEtVideos/Nexus4/2013-10-22/Camera'

# islândia 2023
photos_dir1 = '/media/luiz/HDp1/Celular/MiNote10/20231010'
photos_dir2 = '/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/Louise'
photos_dir3 = '/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/Pedro'

photos_dirs = [photos_dir1,
               photos_dir2,
               photos_dir3]

# world = geopandas.read_file(geodatasets.get_path("naturalearth.land"))

# fig, ax = plt.subplots(figsize=(24, 18))
# world.plot(ax=ax, alpha=0.4, color="grey")
def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    return dd

data = pd.DataFrame()

mp = folium.Map(location=[64.98, -18.61], tiles='OpenStreetMap', zoom_start=7.2)# tiles="CartoDB Positron", zoom_start=7)
all_coords = []

# croácia 2013
# dtime_min = datetime(2013, 10, 1, 16, 00, 00)
# dtime_max = datetime(2013, 10, 7, 15, 00, 00)

# islândia 2023
# dtime_min = datetime(2023, 9, 23, 12, 00, 00)
# dtime_max = datetime(2023, 9, 24, 12, 00, 00)#(2023, 10, 8, 8, 00, 00)
dtime_min = datetime(2023, 9, 23, 12, 00, 00)
dtime_max = datetime(2023, 9, 24, 4, 00, 00)

files = []
file_paths = []
for photo_dir in photos_dirs:
    fs = os.listdir(photo_dir)
    files = files + fs
    fps = [os.path.join(photo_dir, f) for f in fs]
    file_paths = file_paths + fps
arg_sort = np.argsort(files)
files_sorted = np.array(files)[arg_sort]
file_paths_sorted = np.array(file_paths)[arg_sort]

for idxFile, file in enumerate(files_sorted):
    if file.endswith('.jpg'):
        full_path = file_paths_sorted[idxFile] # os.path.join(photos_dir, file)
        full_path = str(full_path)
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
            
            if dtime > dtime_min and \
                dtime < dtime_max:
                folium.Marker(
                  location=[gps_lat_dd, gps_lon_dd],
                  popup=file + '\n' + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                  # icon=folium.Icon(color='gray', icon='ok'),
                  ).add_to(mp)
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)
    
    if file.endswith('.mp4'):
        full_path = file_paths_sorted[idxFile] # os.path.join(photos_dir, file)
        full_path = str(full_path)
        tags = ffmpeg.probe(full_path)['format']['tags']
        dtime_iso_str = tags['creation_time'][:-4] # offset naïve: improve this!
        dtime = datetime.fromisoformat(dtime_iso_str)
        
        if 'location' in tags.keys():
            location_str = tags['location']
            gps_lat_dd = float(location_str[:8])
            gps_lon_dd = float(location_str[8:-1])
            
            if dtime > dtime_min and \
                dtime < dtime_max:
                folium.Marker(
                  location=[gps_lat_dd, gps_lon_dd],
                  popup=file + '\n' + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                  ).add_to(mp)
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)

data = data.sort_values('datetime')


for index, row in data.iterrows():
    gps_lat = row['gps_lat']
    gps_lon = row['gps_lon']
    dtime = row['datetime']
    all_coords.append([gps_lat, gps_lon])

folium.PolyLine(all_coords).add_to(mp)

mp.save("map.html")

webbrowser.open_new_tab("map.html")

# Save image

# Set up selenium options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Ensure GUI is off

# Set up the path to the geckodriver executable
# Note: Ensure geckodriver is installed and its path is set correctly
service = Service('/snap/bin/geckodriver')  # Update this path

# Set up the driver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Load the HTML file
driver.get("file:///home/luiz/Documents/workspace/PythonMisc/map.html")  # Update this path

# Give it some time to load
time.sleep(1)  # Adjust time if necessary

# Set the window size or make it full screen
driver.set_window_size(1280, 920)  # Adjust dimensions as needed
# driver.maximize_window()

# Take screenshot
screenshot_path = "map_screenshot.png"
driver.save_screenshot(screenshot_path)

# Close the browser
driver.quit()

# Open the image and save it using Pillow for further processing if needed
image = Image.open(screenshot_path)
image.save('final_map_screenshot.png')

print("Screenshot saved successfully.")