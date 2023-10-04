import os
import cv2
from flask import Flask, render_template, request, redirect, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Define the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Route to serve processed images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to handle image uploads and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == 'download.jpg':
        return redirect(request.url)

    if file:
        # Save the uploaded file to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Define the output path for the processed image
        processed_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_image.jpg')

        # Process the uploaded image using the process_image function
        process_image(filename, processed_filename)

        # Render the HTML template and provide the processed_filename
        return render_template('index.html', processed_filename=processed_filename)

def process_image(input_path, output_path, target_size=(800, 600)):
    try:
        # Read the input image using OpenCV
        image = cv2.imread(input_path)

        # Resize the image to the target size
        resized_image = cv2.resize(image, target_size)

        # Save the processed image
        cv2.imwrite(output_path, resized_image)

        return output_path  # Return the path to the processed image
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
