# Low Pass filter for 2D Stabilization
# Author: Luiz Guilherme de M. Ventura
# 25.08.2017
# GPL: Free to use and distribute.

import bpy
import math
import numpy as np
from bpy.types import Panel
from bpy.props import *

filterW = 10

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "2D Stabilization Low Pass"
 
    filterW = IntProperty(name="Filter width", 
        min=2, max=100)
    filterType = EnumProperty(name="Filter type", 
        min=1, max=2)
 
    def execute(self, context):
        message = "%d, %a" % (self.filterW, self.filterType)
        self.report({'INFO'}, message)
        print(message)
        scene = bpy.context.scene
        numFrames = scene.frame_end - scene.frame_start
        frameno = scene.frame_start
        coords = np.zeros((2, numFrames))
        # for frame in range(scene.frame_start, scene.frame_end):
        for clip in bpy.data.movieclips:
            for track in clip.tracking.tracks:
                #print("New Track - ")
                #print(frameno)
                frameNewTrack = frameno
                newMarkerAtFrame = track.markers.find_frame(frameNewTrack)
                while True:
                    markerAtFrame = track.markers.find_frame(frameno)
                    if not markerAtFrame or frameno >= scene.frame_end:
                        break
                    coords[0][frameno-1], coords[1][frameno-1] = markerAtFrame.co.xy[0] - 0.3*newMarkerAtFrame.co.xy[1], markerAtFrame.co.xy[1] - newMarkerAtFrame.co.xy[1]
                    #print(markerAtFrame.co.xy)
                    clip.tracking.stabilization.keyframe_insert(data_path="target_position", frame=frameno)
                    clip.tracking.stabilization.target_position[0] = -coords[0][0] - markerAtFrame.pattern_bound_box[0][0]
                    clip.tracking.stabilization.target_position[1] = -coords[1][0] - markerAtFrame.pattern_bound_box[0][1]
                    print(-coords[0][frameno-1])
                    for k in range(1, self.filterW):
                        f = frameno - k
                        if (f < 0):
                            f = 0
                        clip.tracking.stabilization.target_position[0] = clip.tracking.stabilization.target_position[0] + coords[0][f]/self.filterW
                        clip.tracking.stabilization.target_position[1] = clip.tracking.stabilization.target_position[1] + coords[1][f]/self.filterW
                    frameno += 1

        print(coords)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        global filterW, filterType
        self.filW = filterW
        self.filT = filterType
        return context.window_manager.invoke_props_dialog(self)
 
 
bpy.utils.register_class(DialogOperator)
 

 
#bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
#
#    Panel in tools region
#
class DialogPanel(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'TOOL_PROPS'
    bl_label = 'Location compensation'
    bl_context = 'objectmode'
    bl_category = 'Tools'
 
    def draw(self, context):
        global filterW, filterType
        filterW = 10
        filterType = 1
        self.layout.operator("object.dialog_operator")
 
#
#	Registration
bpy.utils.register_module(__name__)