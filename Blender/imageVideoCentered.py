import bpy
from PIL import Image
from os import listdir
from os.path import isfile, join

mypath = "/media/luiz/Volume/Dokumente/Musik/Projekte/Kompon/temp/trim"

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

screen_w = 960
screen_h = 1080

seq = bpy.context.scene.sequence_editor_create()

for idx, file in enumerate(files):
    im = Image.open(join(mypath, file))
    width, height = im.size

    strip = seq.sequences.new_image(filepath=join(mypath, file), name=file, frame_start=idx*500, channel=6)

    strip.frame_final_end = (idx+1)*500-1
    strip.use_translation = True
    strip.transform.offset_x = screen_w/2 - width/2
    strip.transform.offset_y = screen_h/2 - height/2
    strip.blend_type = 'ALPHA_OVER'

# Also works:
#    bpy.context.scene.sequence_editor.sequences_all[file].use_translation = True
#    bpy.context.scene.sequence_editor.sequences_all[file].transform.offset_x = screen_w/2 - width/2
#    bpy.context.scene.sequence_editor.sequences_all[file].transform.offset_y = screen_h/2 - height/2


#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].use_translation = True
#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].transform.offset_y = 100
#    bpy.context.scene.sequence_editor.sequences_all["20170816_orq-0{}.png".format(str(idx))].transform.offset_x = 30