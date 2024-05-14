import bpy
import math

def attach_face_to_bone(body_file_path, face_file_path, output_file_path):
    # Clear all mesh data
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import body and face meshes
    bpy.ops.import_scene.fbx(filepath=body_file_path)
    bpy.ops.import_scene.fbx(filepath=face_file_path)

    # Get armature and body mesh objects
    armature_obj = bpy.data.objects.get('Armature')
    if armature_obj:
        # Find the body mesh inside the armature hierarchy
        body_mesh = None
        for obj in armature_obj.children:
            if obj.type == 'MESH':
                body_mesh = obj
                break
        
        if body_mesh:
            # Get the face object
            face_mesh = bpy.data.objects.get('defaultobject')
            if face_mesh:
                # Scale, rotate, and position the face object
                face_mesh.location = (0, -7.02, 2.58)  # Replace with desired translation
                face_mesh.rotation_euler = (math.radians(82), math.radians(180), math.radians(180))  # Replace with desired rotation
                face_mesh.scale = (0.001, 0.001, 0.001)  # Replace with desired scale
                
              

                # Add Boolean modifier to the body mesh
                boolean_modifier = body_mesh.modifiers.new(name="Boolean", type='BOOLEAN')
                boolean_modifier.operation = 'UNION'
                boolean_modifier.object = face_mesh

                # Apply the Boolean modifier
                bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)

              

        else:
            print("Body mesh not found inside the armature.")

    else:
        print("Armature object not found.")

# Specify paths and settings
body_file_path = "C://Users//natio//Documents//USC//Spring2024//CSCI_599//NextFace//output//body.fbx"
face_file_path = "C://Users//natio//Documents//USC//Spring2024//CSCI_599//NextFace//output//PranavImage.png//mesh0.fbx"
output_file_path = "C://Users//natio//Documents//USC//Spring2024//CSCI_599//NextFace//output//PranavImage.png//merged//merged.fbx"
bone_to_attach_face_to = 'mixamorig1:HeadTop_End'

# Attach face to bone
attach_face_to_bone(body_file_path, face_file_path, output_file_path)
