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
                face_mesh.location = (0, -7.092, 2.58)  # Replace with desired translation
                face_mesh.rotation_euler = (math.radians(82), math.radians(180), math.radians(180))  # Replace with desired rotation
                face_mesh.scale = (0.001, 0.001, 0.001)  # Replace with desired scale
                
               # Ensure body mesh is selected
                bpy.context.view_layer.objects.active = body_mesh
                
                # Add shape keys for the body mesh
                bpy.ops.object.shape_key_add(from_mix=False)
                body_mesh_shape_key = body_mesh.data.shape_keys
                body_mesh_shape_key.key_blocks[0].name = "Basis"
                bpy.ops.object.shape_key_add(from_mix=False)
                body_mesh_shape_key.key_blocks[1].name = "Face Shape"
                
                # Add a new vertex group to the body mesh
                vertex_group = body_mesh.vertex_groups.new(name="Face Vertices")

                # Select the vertices you want to include in the vertex group
                # This will depend on your specific mesh and may require manual selection
                # For example, you might select all vertices in front of a certain point on the Z axis
                for vertex in body_mesh.data.vertices:
                    if vertex.co.z >0.0000000001:  # Replace 'some_value' with the appropriate value for your mesh
                        vertex_group.add([vertex.index], 0.1, 'ADD')

                # Add Shrinkwrap modifier to body mesh
                shrinkwrap_modifier = body_mesh.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
                shrinkwrap_modifier.target = face_mesh
                shrinkwrap_modifier.wrap_method = 'PROJECT'
                shrinkwrap_modifier.use_positive_direction = True
                shrinkwrap_modifier.use_negative_direction =True
                shrinkwrap_modifier.use_project_x = False
                shrinkwrap_modifier.use_project_y = False
                shrinkwrap_modifier.use_project_z = True
                shrinkwrap_modifier.show_viewport = True
                shrinkwrap_modifier.offset = .0002

                # Set the Shrinkwrap modifier to only affect the vertices in the vertex group
                shrinkwrap_modifier.vertex_group = "Face Vertices"
                
                
            
                # Export the merged result
                bpy.ops.export_scene.fbx(filepath=output_file_path)

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
