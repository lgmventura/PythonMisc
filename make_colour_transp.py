#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:57:50 2024

@author: luiz
"""

from PIL import Image
import os

def make_transparent(input_folder, output_folder, colour_rgb=[255, 255, 255]):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process each PNG file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            # Load image
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path)

            # Convert image to RGBA (if not already)
            img = img.convert("RGBA")

            # Create a transparent mask for the image
            datas = img.getdata()
            newData = []
            for item in datas:
                # Set pixel to transparent if it matches a specific color (e.g., white)
                if item[0] == colour_rgb[0] and item[1] == colour_rgb[1] and item[2] == colour_rgb[2]:
                    newData.append((255, 255, 255, 0))  # Transparent
                else:
                    newData.append(item)

            # Update image data with transparent mask
            img.putdata(newData)

            # Save the image with transparent background
            output_path = os.path.join(output_folder, filename)
            img.save(output_path, "PNG")

# Usage example:
input_folder = "/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/20231010/mapas - celulares LG+Louise+Pedro"
output_folder = "/media/luiz/HDp1/Câmeras de outrem/Islândia 2023/20231010/mapas - celulares LG+Louise+Pedro/proc"
make_transparent(input_folder, output_folder, colour_rgb=[170, 211, 223])