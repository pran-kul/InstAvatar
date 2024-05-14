import bpy
import os
import sys
def convert_obj_to_fbx(obj_file, fbx_file):
    print(f"Converting OBJ to FBX...'{obj_file}'...")
    # Clear existing objects and data
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("Cleared existing objects and data.")

    # Import OBJ file
    print(f"Importing OBJ file: '{obj_file}'...")
    bpy.ops.wm.obj_import(filepath=obj_file)

    # Set output FBX file path
    fbx_file_dir = os.path.dirname(fbx_file)
    if not os.path.exists(fbx_file_dir):
        os.makedirs(fbx_file_dir)

    # Export imported objects to FBX
    print(f"Exporting FBX file: '{fbx_file}'...")
    bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True, embed_textures=True)

# Example usage:
obj_file_path = sys.argv[-2]
fbx_file_path = sys.argv[-1]

convert_obj_to_fbx(obj_file_path, fbx_file_path)