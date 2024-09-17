from flask import Flask, render_template, request
import numpy as np
import face_recognition as fr
import os
import cv2
from ffpyplayer.player import MediaPlayer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Your existing face recognition code
path = "imgs"
known_names = []
known_name_encodings = []

images = os.listdir(path)

for _ in images:
    image = cv2.imread(f'{path}/{_}')
    encoding = fr.face_encodings(image)[0]
    known_name_encodings.append(encoding)
    known_names.append(os.path.splitext(_)[0])

@app.route('/')
def home():
    return render_template('index.html', result="")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        image = cv2.imread(filename)
        if image is None:
            return render_template('index.html', result="Failed to read uploaded image")

        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = ""
            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)
            if matches[best_match]:
                name = known_names[best_match]
                # Add your video display logic here
                # This code assumes you have a folder named 'videos' containing videos named as the recognized names
                print(f"Recognized: {name}")
            else:
                print('Sorry, we do not have data on this person right now.')

        return render_template('index.html', result="Face recognized")
    else:
        return render_template('index.html', result="No file uploaded")

if __name__ == '__main__':
    app.run(debug=True)
"""""
Sure! Here's an explanation of the code divided into sections:

Importing Required Libraries:
Flask is a web framework for building web applications in Python.
render_template is used to render HTML templates.
request is used to handle HTTP requests.
numpy provides mathematical functions to work with arrays.
face_recognition is a library for face recognition tasks.
os provides functions for interacting with the operating system.
cv2 is OpenCV, a library for computer vision tasks.
ffpyplayer is used for playing media files.
Creating Flask Application:
An instance of the Flask class is created, and the __name__ variable is passed to it.
The UPLOAD_FOLDER configuration is set to specify the folder for uploaded files.
Face Recognition Code:
The code loads images from the "imgs" directory and performs face recognition on them.
Each image is read using cv2.imread and then encoded using fr.face_encodings.
The encodings and corresponding names are stored in known_name_encodings and known_names lists.
Home Route:
The '/' route is defined to render the 'index.html' template with an empty result.
Upload Route:
The '/upload' route is defined to handle the POST request when an image is uploaded.
The uploaded file is saved to the 'uploads' folder.
The image is read using cv2.imread and face detection and encoding are performed using fr.face_locations and fr.face_encodings.
The face encodings are compared with the known encodings using fr.compare_faces and the best match is determined using np.argmin.
If a match is found, the recognized name is printed, and the video display logic can be added.
The result is rendered in the 'index.html' template.
Main Block:
The script is run only if it's the main module, using if __name__ == '__main__'.
The Flask application is run with debug mode enabled.
This code sets up a Flask web application that allows users to upload an image and performs face recognition on it. If a match is found, it prints the recognized name and you can add video display logic for the recognized person. The code assumes you have a folder named 'videos' containing videos named as the recognized names.

Please note that the video display logic is not included in the provided code snippet. You would need to add the necessary code to display videos based on the recognized names.
"""""