#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:33:31 2024

@author: luiz
"""

import cv2
import numpy as np
import subprocess

fp1 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_0624.JPG'
fp2 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_0625.JPG'
fp3 = '/media/luiz/Elements/FotosEtVideos/EOS 550D/2015.07.23/IMG_0626.JPG'

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
hdr_16bit = np.clip(hdr_image * 65535, 0, 65535).astype('uint16')

# Save HDR image as 16-bit TIFF
cv2.imwrite('tmp/hdr_output_16bit.tiff', hdr_16bit)

# Alternatively
# Save HDR image as OpenEXR (32-bit float)
# cv2.imwrite('tmp/hdr_output.exr', hdr_image.astype('float32'))

# Save HDR image as Radiance HDR format
# cv2.imwrite('tmp/hdr_output.hdr', hdr_image.astype('float32'))
