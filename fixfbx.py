import bpy
import os
import sys

def import_fbx(filepath):
    print(f"Fixing pivot of FBX file: '{filepath}'...")
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import FBX file
    bpy.ops.import_scene.fbx(filepath=filepath)

    # Get the imported object (assuming only one object is imported)
    imported_object = bpy.context.selected_objects[0] if bpy.context.selected_objects else None

    if imported_object and imported_object.type == 'MESH':
        # Set object origin to geometry (center)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Correct rotations
        # Rotate the object to align with the default Blender orientation (Y-up, Z-forward)
        imported_object.rotation_euler = (0, 0, 0)  # Reset rotations

        # Apply specific rotations based on the imported object's orientation
        if imported_object.rotation_mode == 'QUATERNION':
            imported_object.rotation_quaternion = (1, 0, 0, 0)  # Reset quaternion rotation
        elif imported_object.rotation_mode == 'AXIS_ANGLE':
            imported_object.rotation_axis_angle = (0, 0, 1, 0)  # Reset axis-angle rotation
        else:
            # Assume Euler rotation mode (XYZ)
            # Correct rotation for common import orientations (adjust as needed)
            imported_object.rotation_euler = (imported_object.rotation_euler.x,
                                               imported_object.rotation_euler.y,
                                               imported_object.rotation_euler.z)

        print(f"Imported object '{imported_object.name}' with pivot set to geometric center and corrected rotations.")

         # Select the imported object
        bpy.context.view_layer.objects.active = imported_object
        imported_object.select_set(True)

        # Export the modified object
        export_filepath = filepath
        bpy.ops.export_scene.fbx(filepath=export_filepath, use_selection=True)

        print(f"Exported modified object to '{export_filepath}'.")
        
    else:
        print("Error: No mesh object imported from FBX file.")


# Get the FBX file path from the command-line arguments
fbx_filepath = sys.argv[-1]

# Call the import_fbx function with the FBX file path
import_fbx(fbx_filepath)
