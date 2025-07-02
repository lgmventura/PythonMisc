import bpy

# Get the active object and its animation data
obj = bpy.context.active_object
if not obj or not obj.animation_data:
    raise Exception("No animated object selected!")

action = obj.animation_data.action

# Loop through all F-Curves (location, rotation, scale, etc.)
for fcurve in action.fcurves:
    # Deselect all keyframes first
    for kp in fcurve.keyframe_points:
        kp.select_control_point = False
    
    # Select every 4th keyframe (indexes 0, 3, 7, etc.)
    for i in range(0, len(fcurve.keyframe_points), 4):
        fcurve.keyframe_points[i+2].select_control_point = True

print(f"Selected every 4th keyframe for {obj.name}")