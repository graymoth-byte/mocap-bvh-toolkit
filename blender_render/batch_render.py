import bpy
import os

if bpy.data.filepath:
    base_dir = os.path.dirname(bpy.data.filepath)
elif "__file__" in globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
else:
    base_dir = os.getcwd()

bvh_folder = os.path.join(base_dir, "In")
out_folder = os.path.join(base_dir, "Out")
os.makedirs(out_folder, exist_ok=True)

scene = bpy.context.scene
scene.render.image_settings.media_type = 'VIDEO'
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'

for filename in os.listdir(bvh_folder):
    if not filename.endswith('.bvh'):
        continue

    filepath = os.path.join(bvh_folder, filename)

    names_before = {obj.name for obj in bpy.data.objects}
    bpy.ops.import_anim.bvh(filepath=filepath, target='ARMATURE')
    armature = next(obj for obj in bpy.data.objects if obj.name not in names_before)
    action = armature.animation_data.action

    scene.frame_start = int(action.frame_range[0])
    scene.frame_end = int(action.frame_range[1])
    scene.render.filepath = os.path.join(out_folder, os.path.splitext(filename)[0] + ".mp4")

    bpy.ops.render.opengl(animation=True)

    # Remove current armature
    armature_data = armature.data
    bpy.data.objects.remove(armature, do_unlink=True)
    bpy.data.armatures.remove(armature_data)
    bpy.data.actions.remove(action)
