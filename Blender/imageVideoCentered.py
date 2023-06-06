import bpy
from PIL import Image
from os import listdir
from os.path import isfile, join

mypath = "/home/luiz/Music/temp/trim/"

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

files.sort(key=natural_keys)

screen_w = 3840 # the half, because we are displaying two pages per view
screen_h = 2160

two_pages_per_view = False

if two_pages_per_view:
    screen_w = screen_w / 2

dur = 500

seq = bpy.context.scene.sequence_editor_create()

for idx, file in enumerate(files):
    im = Image.open(join(mypath, file))
    width, height = im.size

    strip = seq.sequences.new_image(filepath=join(mypath, file), name=file, frame_start=idx*dur, channel=6)

    strip.frame_final_end = (idx+1)*dur-1
    #strip.use_translation = True
    if two_pages_per_view == True:
        if idx % 2 == 0: # to put even pages on the left
            strip.transform.offset_x = -screen_w/2#screen_w/2 - width/2
        else: # and uneven pages on the right
            strip.transform.offset_x = +screen_w/2
    else:
        strip.transform.offset_x = 0
    strip.transform.offset_y = 0#screen_h/2 - height/2
    strip.blend_type = 'ALPHA_OVER'

# Also works:
#    bpy.context.scene.sequence_editor.sequences_all[file].use_translation = True
#    bpy.context.scene.sequence_editor.sequences_all[file].transform.offset_x = screen_w/2 - width/2
#    bpy.context.scene.sequence_editor.sequences_all[file].transform.offset_y = screen_h/2 - height/2


#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].use_translation = True
#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].transform.offset_y = 100
#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].transform.offset_x = 30