#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:33:31 2024

@author: luiz
"""

import cv2
import numpy as np
import subprocess
from os import path

# fp1 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_1081.JPG'
# fp2 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_1082.JPG'
# fp3 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_1083.JPG'

# fp1 = '/media/luiz/Elements/FotosEtVideos/Canon EOS 700D (2016)/2017.03.04 - ML/IMG_1051.JPG'
# fp2 = '/media/luiz/Elements/FotosEtVideos/Canon EOS 700D (2016)/2017.03.04 - ML/IMG_1052.JPG'
# fp3 = '/media/luiz/Elements/FotosEtVideos/Canon EOS 700D (2016)/2017.03.04 - ML/IMG_1053.JPG'

# fp1 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241105/E22A3944.JPG'
# fp2 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241105/E22A3945.JPG'
# fp3 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241105/E22A3946.JPG'

# fp1 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241124/E22A4171.JPG'
# fp2 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241124/E22A4172.JPG'
# fp3 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20241124/E22A4173.JPG'

fp1 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6/E22A6750.JPG'
fp2 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6/E22A6751.JPG'
fp3 = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6/E22A6752.JPG'

# Input images (bracketed exposures)
input_images = [fp1, fp2, fp3]

# Align images using Hugin's align_image_stack
aligned_images = ['aligned_0000.tif', 'aligned_0001.tif', 'aligned_0002.tif']
align_cmd = ['align_image_stack', '-x', '-a', 'aligned_'] + input_images
subprocess.run(align_cmd)

# Read aligned images in OpenCV
aligned_imgs = [cv2.imread(img) for img in aligned_images]

# Merge exposures
merge = cv2.createMergeMertens()
hdr_image = merge.process(aligned_imgs)

# Save result
cv2.imwrite('tmp/hdr_output.jpg', hdr_image * 255)


# Convert HDR image to 16-bit (scale from 0 to 65535)
hdr_image_norm = (hdr_image - np.min(hdr_image))/(np.ptp(hdr_image))
hdr_16bit = np.clip(hdr_image_norm * 65535, 0, 65535).astype('uint16')

# Save HDR image as 16-bit TIFF
cv2.imwrite('tmp/hdr_output_16bit.tiff', hdr_16bit)

# Alternatively
# Save HDR image as OpenEXR (32-bit float)
# cv2.imwrite('tmp/hdr_output.exr', hdr_image.astype('float32'))

# Save HDR image as Radiance HDR format
# cv2.imwrite('tmp/hdr_output.hdr', hdr_image.astype('float32'))
