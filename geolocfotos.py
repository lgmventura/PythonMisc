#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 13:08:34 2023

@author: luiz
"""

import pandas as pd
import numpy as np
# import geopandas
# import geodatasets
import matplotlib.pyplot as plt

import os

import time

import exif
import ffmpeg
from datetime import datetime

from PIL import Image
from make_colour_transp import make_transparent

# method 1
import folium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import webbrowser

# for cartopy (method 2)
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import cartopy.geodesic as cgeo
import io
from urllib.request import urlopen, Request

import cartopy.io.img_tiles as cimgt
# import shapely

# croácia 2013 (infelizmente, quase nenhum dado de GPS)
#photos_dir = '/media/luiz/Elements/FotosEtVideos/Nexus4/2013-10-22/Camera'

# islândia 2023
photos_dir1 = '/media/luiz/HDp1/Celular/MiNote10/20231010'
photos_dir2 = '/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/Louise'
photos_dir3 = '/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/Pedro'

photos_dirs = [photos_dir1,
               photos_dir2,
               photos_dir3]

loc_centre = [64.98, -18.61]
# world = geopandas.read_file(geodatasets.get_path("naturalearth.land"))

# os dados de GPS vêm em grau, minuto e segundo no EXIF, mas precisamos em grau vírgula flutuante
def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    return dd

data = pd.DataFrame()

# selecionando data inicial e data final para filtrar as fotos e os vídeos
# croácia 2013
# dtime_min = datetime(2013, 10, 1, 16, 00, 00)
# dtime_max = datetime(2013, 10, 7, 15, 00, 00)

# islândia 2023
# dtime_min = datetime(2023, 9, 23, 12, 00, 00)
# dtime_max = datetime(2023, 9, 24, 12, 00, 00)#(2023, 10, 8, 8, 00, 00)
dtime_min = datetime(2023, 9, 23, 12, 00, 00)
dtime_max = datetime(2023, 10, 8, 4, 00, 00)


files = []
file_paths = []
# rodar por diretório
for photo_dir in photos_dirs:
    fs = os.listdir(photo_dir)
    files = files + fs
    fps = [os.path.join(photo_dir, f) for f in fs] # fps here is file paths
    file_paths = file_paths + fps
arg_sort = np.argsort(files)  # ordenar (nem sei se é mais necessário, já que agora eu ordeno depois de novo, já que depois incluí vídeos e diferenciei o pino final dos demais)
files_sorted = np.array(files)[arg_sort]
file_paths_sorted = np.array(file_paths)[arg_sort]

# caminhar pelos arquivos ordenados
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
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)
    
    # vídeos (se houver mais formatos, adicionar aqui)
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
                
                iData = {'file': file[:-4],
                         'extension': file[-4:],
                         'datetime': dtime,
                         'gps_lat': gps_lat_dd,
                         'gps_lon': gps_lon_dd}
                data = pd.concat([data, pd.DataFrame(iData, index=[0])], ignore_index=True)

# ordenar por data e hora
data = data.sort_values('datetime')

data = data.reset_index()

# url = "https://leafletjs.com/examples/custom-icons/{}".format
# icon_image = url("leaf-red.png")
# shadow_image = url("leaf-shadow.png")

# ícones
icon_red = '/home/luiz/Pictures/Icons/Pino localidade 2 - vermelho.png'
icon_grey = '/home/luiz/Pictures/Icons/Pino localidade 2 - cinza.png'
icon_shadow = '/home/luiz/Pictures/Icons/Pino localidade 2 - sombra 2.png'



#%% method 1 - Folium

'''
Advantages:
    - Beautiful maps from OpenStreetmap or others
    - Native support for icons and markers
Disadvantages:
    - Generates a HTML. Nice for being interactive, but for generating an image,
    it takes a few seconds and needs post-processing (automated here)
    - Images must be screenshot from browser (automated here, but resolution 
                                              limited)
    - Animations are virtually impossible.
    
'''
mp = folium.Map(location=loc_centre, tiles='OpenStreetMap', zoom_start=7.2)# tiles="CartoDB Positron", zoom_start=7)
all_coords = []


# adicionar no mapa
nRows = data.shape[0]
for idxRow, iRow in data.iterrows():
    # icons must be initialized everz time: https://stackoverflow.com/questions/74200088/using-custom-icons-for-multiple-locations-with-folium-and-pandas
    icon_past = folium.CustomIcon(
        icon_grey,
        icon_size=(28, 50),
        icon_anchor=(14, 49),
        shadow_image=icon_shadow,
        shadow_size=(28, 50),
        shadow_anchor=(14, 49),
        popup_anchor=(-3, -76),
    )

    icon_current = folium.CustomIcon(
        icon_red,
        icon_size=(36, 64),
        icon_anchor=(18, 63),
        shadow_image=icon_shadow,
        shadow_size=(50, 64),
        shadow_anchor=(20, 63),
        popup_anchor=(-3, -76),
    )
    
    gps_lat_dd = iRow.gps_lat
    gps_lon_dd = iRow.gps_lon
    dtime = iRow.datetime
    file = iRow.file
    if idxRow < nRows - 1:
        folium.Marker(
                      location=[gps_lat_dd, gps_lon_dd],
                      popup=file + '\n' + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                      icon=icon_past,
                      # icon=folium.Icon(color='gray', icon='ok'),
                      ).add_to(mp)
    elif idxRow == nRows - 1:
        folium.map.CustomPane("current", z_index=600).add_to(mp)
        folium.Marker(
                      location=[gps_lat_dd, gps_lon_dd],
                      popup=file + '\n' + dtime.strftime("%Y-%m-%d %H:%M:%S"),
                      # color='red',
                      icon=icon_current,
                      pane='current',
                      # icon=folium.Icon(color='gray', icon='ok'),
                      ).add_to(mp)


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

# cropping borders (unwanted logos and leaf)
width, height = image.size
left = 54
top = 0
right = width - 100
bottom = height - 20

image = image.crop((left, top, right, bottom))

# make water transparent (you might want this or not)
image = make_transparent(image, colour_rgb=[170, 211, 223])

dt1 = dtime_min.strftime('%Y%m%d_%H%M%S')
dt2 = dtime_max.strftime('%Y%m%d_%H%M%S')

out_file = f'map_{dt1}_-_{dt2}.png'
image.save(out_file)

print("Screenshot saved successfully.")


#%% method 2 - cartopy plot
'''
Advantages:
    - plots into matplotlib
    - can be used for animations
Disadvantages:
    - doesn't work (actually is halting on downloading the openstreetmap. The higher the
    radius - lower zoom - the more frequent it hangs)
'''
# [1]: https://www.theurbanist.com.au/2021/03/plotting-openstreetmap-images-with-cartopy/


# def calc_extent(lon,lat,dist):
#     '''This function calculates extent of map
#     Inputs:
#         lat,lon: location in degrees
#         dist: dist to edge from centre
#     '''

#     dist_cnr = np.sqrt(2*dist**2)
#     top_left = cgeo.Geodesic().direct(points=(lon,lat),azimuths=-45,distances=dist_cnr)[:,0:2][0]
#     bot_right = cgeo.Geodesic().direct(points=(lon,lat),azimuths=135,distances=dist_cnr)[:,0:2][0]

#     extent = [top_left[0], bot_right[0], bot_right[1], top_left[1]]

#     return extent

# def image_spoof(self, tile):
#     '''this function reformats web requests from OSM for cartopy
#     Heavily based on code by Joshua Hrisko at:
#         https://makersportal.com/blog/2020/4/24/geographic-visualizations-in-python-with-cartopy'''

#     url = self._image_url(tile)                # get the url of the street map API
#     req = Request(url)                         # start request
#     req.add_header('User-agent','Anaconda 3')  # add user agent to request
#     fh = urlopen(req) 
#     im_data = io.BytesIO(fh.read())            # get image
#     fh.close()                                 # close url
#     img = Image.open(im_data)                  # open image with PIL
#     img = img.convert(self.desired_tile_form)  # set image format
#     return img, self.tileextent(tile), 'lower' # reformat for cartopy

# # Load the custom PNG marker
# marker_image_red = plt.imread(icon_red)
# marker_image_grey = plt.imread(icon_grey)

# num_markers = data.shape[0]

# # Define the number of frames and interval for marker appearance
# num_frames = 3 + num_markers
# n = 1  # Markers appear every n frames

# radius = 230000

# # proj = ccrs.PlateCarree()  # ccrs.PlateCarree()
# # transf = ccrs.PlateCarree()

# style = 'map'
# if style=='map':
#     ## MAP STYLE
#     cimgt.OSM.get_image = image_spoof # reformat web request for street map spoofing
#     img = cimgt.OSM() # spoofed, downloaded street map
# elif style =='satellite':
#     # SATELLITE STYLE
#     cimgt.QuadtreeTiles.get_image = image_spoof # reformat web request for street map spoofing
#     img = cimgt.QuadtreeTiles() # spoofed, downloaded street map


# extent = calc_extent(loc_centre[1], loc_centre[0], radius*1.1)

# # auto-calculate scale
# scale = int(120/np.log(radius))
# scale = (scale<20) and scale or 19

# data_crs = ccrs.PlateCarree()

# fig = plt.figure(figsize=(16, 10))
# ax = fig.add_subplot(1, 1, 1, projection=img.crs)

# ax.set_extent(extent)
# ax.add_image(img, int(scale)) # add OSM with zoom specification
    
# # Generate frames
# for i in range(num_frames):
    
#     # ax.stock_img()
    
#     # Add map features
#     # ax.add_feature(cfeature.COASTLINE)
#     # ax.add_feature(cfeature.BORDERS)
#     # ax.add_feature(cfeature.LAND)
#     # ax.add_feature(cfeature.LAKES)
#     # ax.add_feature(cfeature.RIVERS)
    

#     # Determine which markers should be visible at this frame
#     for index, row in data.iterrows():
#         gps_lat = row['gps_lat']
#         gps_lon = row['gps_lon']

#         # Create an OffsetImage object with the custom marker
#         if index < num_markers - 1:
#             imagebox = OffsetImage(marker_image_grey, zoom=0.1)  # Adjust zoom to scale marker size
#         elif index == num_markers - 1:
#             imagebox = OffsetImage(marker_image_red, zoom=0.1)  # Adjust zoom to scale marker size

#         # Create an AnnotationBbox object with the image, positioned at the coordinates
#         ab = AnnotationBbox(imagebox, (gps_lon, gps_lat), frameon=False, xycoords='data', transform=data_crs)

#         # Add the custom marker to the plot
#         ax.add_artist(ab)

#     # Save the frame
#     plt.savefig(f'tmp/frame_{i:03d}.png')
#     plt.close()

# # Create an animated GIF or video
# # frames = [Image.open(f'tmp/frame_{i:03d}.png') for i in range(num_frames)]
# # frames[0].save('marker_animation.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)


#%% Method 3 - a method 2 that should work!

import contextily as ctx
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pyproj import Transformer
from PIL import Image
import numpy as np

plt.rcParams["figure.dpi"] = 150 # lower image size

# fig, ax = plt.subplots(figsize=(16, 9))

# if the current point is too close to the last one, we can skip
lat_lon_tolerance_skip = 0.001

# Step 1: Create the map
place = ctx.Place("Iceland", zoom=7)
ax = place.plot()

# Step 2: Convert latitude and longitude to Web Mercator coordinates
# lat, lon = 64.1355, -21.8954  # Example coordinates for Reykjavík

width_meters = place.bbox_map[1] - place.bbox_map[0]
height_meters = place.bbox_map[3] - place.bbox_map[2]

# Step 3: Plot the PNG image at the specified location
img_grey = Image.open(icon_grey)
img_red = Image.open(icon_red)

image_width, image_height = img_red.size

offset_x = 0
offset_y = 1/2 * height_meters

zoom_factor_red = 0.035  # Adjust this to match the zoom used in OffsetImage
zoom_factor_grey = 0.03

# Ensure the image is in RGBA mode to handle transparency correctly
if img_grey.mode != 'RGBA':
    img_grey = img_grey.convert('RGBA')
    
if img_red.mode != 'RGBA':
    img_red = img_red.convert('RGBA')
    
xbounds = ax.get_xbound()
ybounds = ax.get_ybound()

pos_text = (0.1, 0.86)  # relativa

# absoluta:
text_x = xbounds[0] + pos_text[0]*(xbounds[1] - xbounds[0])
text_y = ybounds[0] + pos_text[1]*(ybounds[1] - ybounds[0])

annot = ax.annotate('', (text_x, text_y), fontsize=26)

iframe = 0
for index, row in data.iterrows():
    lat = row['gps_lat']
    lon = row['gps_lon']
    dtime = row['datetime']
    
    delta_days = (dtime - dtime_min).days
    annot.set_text(f'Dia {delta_days}')
    
    # skip if the current lat and lon are too close to the last
    if index >= 1:
        lat_prev = data.loc[index - 1]['gps_lat']
        lon_prev = data.loc[index - 1]['gps_lon']
        if abs(lat - lat_prev) < lat_lon_tolerance_skip and abs(lon - lon_prev) < lat_lon_tolerance_skip \
            and index < data.shape[0] - 1:
            continue
    
    # Define the transformer for converting lat/lon to Web Mercator
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)
    
    # Create an OffsetImage to display on the plot
    if index < data.shape[0] - 1:
        imagebox = OffsetImage(img_grey, zoom=zoom_factor_grey)  # Adjust the zoom to control the size of the image
        x += offset_x * zoom_factor_grey
        y += offset_y * zoom_factor_grey
    else:
        imagebox = OffsetImage(img_red, zoom=zoom_factor_red)
        x += offset_x * zoom_factor_red
        y += offset_y * zoom_factor_red
    
    # imagebox.set_offset([offset_x, offset_y])

    ab = AnnotationBbox(imagebox, (x, y), frameon=False, xycoords='data')
    
    
    # Add the image to the map
    ax.add_artist(ab)
    
    # Save the frame
    fname = f'tmp/frame_{iframe:03d}.png'
    plt.savefig(fname)
    #     plt.close()
    
    # cropping borders (unwanted logos and leaf)
    image = Image.open(fname)
    
    width, height = image.size
    left = 240
    top = 380
    right = width - 240
    bottom = height - 360

    image = image.crop((left, top, right, bottom))
    
    image.save(fname)
    
    iframe += 1
    


# Create an animated GIF or video
# frames = [Image.open(f'tmp/frame_{i:03d}.png') for i in range(data.shape[0])]
# frames[0].save('marker_animation.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)

os.system("ffmpeg -r 10 -f image2 -s 1920x1080 -i tmp/frame_%03d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p map_animation.mp4")

# Optional: Adjust the limits and show the plot
# ax.set_xlim(x - 100000, x + 100000)
# ax.set_ylim(y - 100000, y + 100000)

# plt.show()


