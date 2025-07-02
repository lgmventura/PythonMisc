import bpy

# select every keyframe not followed by another one within th

# Settings
frame_threshold = 30  # Adjust if needed
selected_obj = bpy.context.active_object

if not selected_obj or not selected_obj.animation_data:
    raise Exception("No animated object selected!")

action = selected_obj.animation_data.action

# Deselect all keyframes first
for fcurve in action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.select_control_point = False

# Check each F-Curve
for fcurve in action.fcurves:
    keyframes = fcurve.keyframe_points
    
    for i in range(len(keyframes) - 1):
        current_frame = keyframes[i].co[0]
        next_frame = keyframes[i + 1].co[0]
        
        # If the next keyframe is beyond the threshold, select the current one
        if (next_frame - current_frame) > frame_threshold:
            keyframes[i].select_control_point = True
    
    # Also check the last keyframe (no next keyframe exists)
    keyframes[-1].select_control_point = True

print(f"Selected keyframes with no follow-up within {frame_threshold} frames")