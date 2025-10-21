import face_recognition
import cv2
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image)

        return jsonify({
            'message': f'Detected {len(face_locations)} face(s).',
            'faces': face_locations
        })
    else:
        return jsonify({"error": "Invalid file format. Only .jpg, .jpeg, and .png are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=True)