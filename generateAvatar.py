
import subprocess
import os

def start_generation(face_obj,face_fbx,output_file_path,gender):
    filename = os.path.basename(output_file_path)
    print(filename)
    print(f"Starting the generation process for{filename}...")
    '''
    try:
        objTofbx.convert_obj_to_fbx(face_obj,face_fbx)
    except Exception as e:
        print("An error occurred while converting OBJ to FBX:", e)

    '''
    # Replace with the actual path on your system
    blender_executable_path  = "C://Program Files//Blender Foundation//Blender 4.1//blender.exe"
    blender_script_path = "./objTofbx.py"
    subprocess.run([blender_executable_path, "--background", "--python", blender_script_path, "--",face_obj, face_fbx])
    
    # Path to the Blender script
    blender_script_path = "./fixfbx.py"
    subprocess.run([blender_executable_path, "--background", "--python", blender_script_path, "--", face_fbx])

    
    if(gender == "f"):
        print("Usng female body mesh")
        body_mesh_filepath =  os.path.dirname(os.path.dirname(output_file_path)) +"/body_female.fbx"
        blender_script_path = "./mergefbx_female.py"
        dir_path = output_file_path + f"/{gender}_merged"
        if not os.path.exists(dir_path):
            # If the directory doesn't exist, create it
            os.makedirs(dir_path)
        subprocess.run([blender_executable_path, "--background", "--python", blender_script_path, "--",dir_path + f"/{filename}_Avatar.fbx" ,body_mesh_filepath, face_fbx])
        
    else:
        print("Usng male body mesh")
        body_mesh_filepath =  os.path.dirname(os.path.dirname(output_file_path)) +"/body_male.fbx"
        blender_script_path = "./mergefbx_male.py"
        dir_path = output_file_path + f"/{gender}_merged"
        if not os.path.exists(dir_path):
            # If the directory doesn't exist, create it
            os.makedirs(dir_path)
        subprocess.run([blender_executable_path, "--background", "--python", blender_script_path, "--",dir_path + f"/{filename}_Avatar.fbx" ,body_mesh_filepath, face_fbx])
    

