# Adds a breakable rigid body constraint to selection - 20200229

import bpy

break_threshold = 0.5

for obj in bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.rigidbody.constraint_add()
    obj.rigid_body_constraint.use_breaking = True
    obj.rigid_body_constraint.breaking_threshold = break_threshold
