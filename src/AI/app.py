import json
import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory
from diagnose import diagnose
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import sys

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOADS_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')

app = Flask(__name__, static_folder='../')
CORS(app, resources={
    r"/diagnose": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "http://127.0.0.1:5500"], 
        "methods": ["POST"],
        "allow_headers": ["Content-Type", "Accept"],
        "expose_headers": ["Content-Type"]
    }
})

# Add detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/diagnose', methods=['POST'])
def diagnose_plant():    
    try:
        # Extensive logging of request details
        logger.debug("Diagnosis request received")
        logger.debug(f"Form data: {request.form}")
        logger.debug(f"Files data: {request.files}")
        
        print("Diagnosis request received")
        print(f"Form data: {request.form}")
        print(f"Files data: {request.files}")

        # Check if image is present in the request
        if 'image' not in request.files:
            logger.error("No image file in request")
            print("No image file in request")
            return jsonify({'error': 'No image file'}), 400
        
        # Get the uploaded image file
        image_file = request.files['image']
        
        # Check if filename is empty
        if image_file.filename == '':
            logger.error("No selected file")
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        # Save the image file to the uploads directory
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(UPLOADS_FOLDER, filename)
        
        # Ensure uploads directory exists
        os.makedirs(UPLOADS_FOLDER, exist_ok=True)
        image_file.save(filepath)

        # Get the plant type from the request form data
        plant_type = request.form['plant_type']

        logger.debug(f"Diagnosing {plant_type} with image: {filepath}")
        print(f"Diagnosing {plant_type} with image: {filepath}")

        # Diagnose the plant disease using the uploaded image
        try:
            diagnosis = diagnose(plant_type, filepath)
            logger.debug(f"Diagnosis result: {diagnosis}")
            print(f"Diagnosis result: {diagnosis}")
        except Exception as diagnose_error:
            logger.error("Error in diagnosis process")
            logger.error(traceback.format_exc())
            print("Error in diagnosis process")
            print(traceback.format_exc())
            return jsonify({
                'error': 'Diagnosis failed', 
                'details': str(diagnose_error),
                'traceback': traceback.format_exc()
            }), 500

        response = jsonify({'diagnosis': diagnosis})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        # Log the full error traceback
        logger.error("Unexpected error during diagnosis")
        logger.error(traceback.format_exc())
        print("Unexpected error during diagnosis")
        print(traceback.format_exc())
        
        # Return a more detailed error response
        return jsonify({
            'error': 'Diagnosis failed', 
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500
    finally:
        # Optional: Remove the uploaded file after processing
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
