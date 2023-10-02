# app.py
from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        processed_image = process_image(filename)
        return render_template('result.html', result=processed_image)

def process_image(filename):
    # Load and process the image using OpenCV
    image = cv2.imread(filename)
    # Perform image processing here (e.g., resizing, filtering, etc.)
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Example: Convert to RGB
    return processed_image

if __name__ == '__main__':
    app.run(debug=True)

