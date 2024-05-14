from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import subprocess
import shutil

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    print(request.files['file'])
    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part in the request.', 400

    file = request.files['file']
    gender = request.form.get('gender')
    print(f"Request recieved for {secure_filename(file.filename)} Gender {gender}")
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file.', 400

    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join('C:/Users/natio/Documents/USC/Spring2024/CSCI_599/NextFace/input', filename)
        file.save(input_path)

        # After processing, send the FBX and image files
        zip_path = os.path.join('C:/Users/natio/Documents/USC/Spring2024/CSCI_599/NextFace/output', filename)
        
        if not os.path.exists(os.path.join(zip_path,f'{gender}_merged')):
            # If the zip path does not exist, run the optimizer
            subprocess.run(['python', 'optimizer.py', '--input', input_path, '--output', 'C:/Users/natio/Documents/USC/Spring2024/CSCI_599/NextFace/output','--gender',gender])
            
            if os.path.exists(os.path.join(zip_path,f'{gender}_merged')):
                print("Avatar data is ready to be downloaded")
                shutil.make_archive(os.path.join(zip_path,os.path.splitext(filename)[0]), 'zip', os.path.join(zip_path,f'{gender}_merged'))
                return send_file(os.path.join(zip_path,os.path.splitext(filename)[0])+'.zip', mimetype='application/zip')
            else:
                print("Error in processing the image.")
                return 'Error in processing the image.', 500
        else:
            
                print("Avatar data is ready to be downloaded")
                shutil.make_archive(os.path.join(zip_path,os.path.splitext(filename)[0]), 'zip', os.path.join(zip_path,f'{gender}_merged'))
                return send_file(os.path.join(zip_path,os.path.splitext(filename)[0])+'.zip', mimetype='application/zip')
          
                

if __name__ == '__main__':
    app.run(debug=True)