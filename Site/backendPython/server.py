from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from PIL import Image
import codigoArthur 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/process', methods=['POST'])
def process_image():
    # Check if the file is in the request
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the uploaded file
        file.save(uploaded_file_path)
        print(f"File uploaded: {uploaded_file_path}")

        # Process the image (without saving it to the processed folder)
        try:
            with Image.open(uploaded_file_path) as img:
                img.convert('RGB')
            print(f"Image processed successfully")
        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({"error": "Error processing the image"}), 500

        # Retrieve JSON data from codigoArthur.py
        try:
            json_data = codigoArthur.jsonback()
            print(f"Generated JSON data: {json_data}")
        except Exception as e:
            print(f"Error generating JSON data: {e}")
            return jsonify({"error": "Error generating JSON data"}), 500
        
        # Delete all images inside the uploads folder
        for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        # Return the JSON data to the front-end
        return jsonify(json_data), 200

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
