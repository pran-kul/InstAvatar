import bpy
import math
import sys
import numpy as np
from collections import Counter
import os
import shutil

def get_average_texture_color(texture_path):
    # Load the image
    img = bpy.data.images.load(texture_path)

    # Define the pixel coordinates
    x1, y1 = 256, 41
    x2, y2 = 256, 61

    # Adjust the y coordinates for Blender's coordinate system
    y1 = img.size[1] - 1 - y1
    y2 = img.size[1] - 1 - y2

    # Get the colors at the specified pixels
    color1 = img.pixels[(y1 * img.size[0] + x1) * 4 : (y1 * img.size[0] + x1) * 4 + 4]
    color2 = img.pixels[(y2 * img.size[0] + x2) * 4 : (y2 * img.size[0] + x2) * 4 + 4]

    # Calculate the average color
    avg_color = [(c1 + c2) / 2 for c1, c2 in zip(color1, color2)]
    print(f"Average color: {avg_color}")
    return avg_color

def attach_face_to_body(body_file_path, face_file_path, bone_name, output_file_path):
    print(f"Attaching face to body... '{body_file_path}', '{face_file_path}', '{bone_name}', '{output_file_path}'...")
    
    diffusedtexture_image = os.path.dirname(face_file_path) + "/diffuseMap_0.png"
    print(diffusedtexture_image)
    # Clear all mesh data
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import body and face meshes
    bpy.ops.import_scene.fbx(filepath=body_file_path)
    bpy.ops.import_scene.fbx(filepath=face_file_path)

    # Get body and face objects by name
    body_obj = bpy.data.objects.get('Armature')
    face_obj = bpy.data.objects.get('mesh0')
    body_mesh = None
    hair_mesh = None
    pants_mesh = None
    shirt_mesh = None
    

    for obj in body_obj.children:
        if obj.name == 'Ch31_Body':
            body_mesh = obj
        elif obj.name == 'Ch31_Hair':
            hair_mesh = obj
        elif obj.name == 'Ch31_Pants':
            pants_mesh = obj
        elif obj.name == 'Ch31_Sweater':
            shirt_mesh = obj
            
    if body_obj and face_obj:
        # Check if the body object has an armature modifier
        armature = body_obj

        # Get the bone by name
        bone = armature.data.bones.get(bone_name)
        if bone:
            # Set face object's parent to the specific bone of the body object
            face_obj.parent = armature
            face_obj.parent_type = 'BONE'
            face_obj.parent_bone = bone_name
            face_obj.location = (0, -39.5, 5)  
            face_obj.rotation_euler = (math.radians(173), math.radians(0), math.radians(0))  # Replace with desired rotation angles in radians
            face_obj.scale = (0.1, 0.1, 0.1) 
             
           
            
            #Body material            
            avg_color = get_average_texture_color(diffusedtexture_image)
            mat = bpy.data.materials.new(name="BodyMaterial")
            r, g, b, _ = avg_color
            darkness_factor = 0.7
            r *= 1.5
            g *= 1.3
            b *=1.0
            # Apply darkness factor
            r *= darkness_factor
            g *= darkness_factor
            b *= darkness_factor
            
            mat.diffuse_color = (r, g, b, 1)
            
           
            # Assign the material to the body mesh
            if body_mesh.data.materials:
                body_mesh.data.materials[0] = mat
            else:
                body_mesh.data.materials.append(mat)
            
            
            # Hair material
            mat1 = bpy.data.materials.new(name="HairMaterial")
            mat1.diffuse_color = (0.2, 0.15, 0.1, 1)
            if hair_mesh.data.materials:
                hair_mesh.data.materials[0] = mat1
            else:
                hair_mesh.data.materials.append(mat1)
                
                
            # Pant material
            mat2 = bpy.data.materials.new(name="PantMaterial")
            mat2.diffuse_color = ( 0, 0,0.1, 1)
            if  pants_mesh.data.materials:
              pants_mesh.data.materials[0] = mat2
            else:
                pants_mesh.data.materials.append(mat2)
                
                
                
            # Shirt material
            mat3 = bpy.data.materials.new(name="shirtMaterial")
            mat3.diffuse_color = (0.4,0,0, 1) 
            if shirt_mesh.data.materials:
                shirt_mesh.data.materials[0] = mat3
            else:
                shirt_mesh.data.materials.append(mat3)
                
             
            # Prepare ShrinkWrap
            bpy.context.view_layer.objects.active = body_mesh
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.vertex_group_add()
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.vertex_group_assign()
            bpy.ops.object.mode_set(mode='OBJECT')
            vg = body_mesh.vertex_groups.new(name="ShrinkwrapGroup")
            
            # Add the vertices of the body mesh that are near the face mesh to the vertex group
            for vertex in body_mesh.data.vertices:
                vertex_global = body_mesh.matrix_world @ vertex.co
                distance_x = abs(face_obj.matrix_world.translation.x - vertex_global.x)
                distance_y = abs(face_obj.matrix_world.translation.y - vertex_global.y)
                distance_z = abs(face_obj.matrix_world.translation.z - vertex_global.z)

                # Check if the distances along each axis are within the specified limits
                x_limit = 0.1  # Adjust as needed
                y_limit = 0.05  # Adjust as needed
                z_limit = 0.1  # Adjust as needed
                if distance_x < x_limit and distance_y < y_limit and distance_z < z_limit:
                    vg.add([vertex.index], 1.0, 'ADD')
            
            # Apply Shrinkwrap 
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = body_mesh
            shrinkwrap_modifier = body_mesh.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
            shrinkwrap_modifier.target = face_obj
            shrinkwrap_modifier.vertex_group = "ShrinkwrapGroup" 
            shrinkwrap_modifier.offset = 0.5
            bpy.ops.object.modifier_apply(modifier=shrinkwrap_modifier.name)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_set_active(group="ShrinkwrapGroup")
            bpy.ops.object.vertex_group_select()
            bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=5)  # Adjust the factor and repeat values as needed
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            
       
            bpy.ops.export_scene.fbx(filepath=output_file_path,  
                         add_leaf_bones=False, bake_anim=False, 
                         bake_anim_use_all_actions=False, 
                         embed_textures=True)
                         
            shutil.copy(diffusedtexture_image , os.path.dirname(output_file_path))
            print(f"Exported merged FBX file to '{output_file_path}'.")
            print(f"Done")

        else:
            print(f"Bone '{bone_name}' not found in armature of body object.")
    else:
        print("Body or face object not found.")
        
output_file_path =  sys.argv[-3]
body_mesh_filepath = sys.argv[-2]
face_mesh_filepath = sys.argv[-1]
bone_to_attach_To = 'mixamorig9:HeadTop_End'
 

attach_face_to_body(body_mesh_filepath , face_mesh_filepath, bone_to_attach_To, output_file_path)