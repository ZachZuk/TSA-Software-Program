import json
import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from diagnose import diagnose
from werkzeug.utils import secure_filename
import os
import sys

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOADS_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')

app = Flask(__name__, static_folder='../') 
CORS(app)  # Enable CORS for all routes

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

        # Check if image is present in the request
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'error': 'No image file'}), 400
        
        # Get the uploaded image file
        image_file = request.files['image']
        
        # Check if filename is empty
        if image_file.filename == '':
            logger.error("No selected file")
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

        # Diagnose the plant disease using the uploaded image
        try:
            diagnosis = diagnose(plant_type, filepath)
            logger.debug(f"Diagnosis result: {diagnosis}")
        except Exception as diagnose_error:
            logger.error("Error in diagnosis process")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': 'Diagnosis failed', 
                'details': str(diagnose_error),
                'traceback': traceback.format_exc()
            }), 500

        # Get the relevant plant information from the JSON file
        plant_info = get_plant_info(diagnosis)

        # Return the diagnosis and plant information as JSON
        return jsonify({'diagnosis': diagnosis, 'plant_info': plant_info})
    
    except Exception as e:
        # Log the full error traceback
        logger.error("Unexpected error during diagnosis")
        logger.error(traceback.format_exc())
        
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

def get_plant_info(diagnosis):
    try:
        # Log the full path to ensure we're looking in the right place
        import os
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")
        print(f"Looking for info.json in: {os.path.join(current_dir, 'src', 'info.json')}")

        # Try multiple potential paths for info.json
        possible_paths = [
            'src/info.json',
            '../src/info.json',
            'info.json',
            os.path.join(current_dir, 'src', 'info.json')
        ]

        info = None
        for path in possible_paths:
            try:
                with open(path, 'r') as f:
                    info = json.load(f)
                print(f"Successfully loaded info.json from {path}")
                break
            except FileNotFoundError:
                print(f"File not found: {path}")
            except json.JSONDecodeError:
                print(f"JSON decode error in {path}")

        if info is None:
            print("Could not find info.json in any of the expected locations")
            return {}

        # Try to get plant info with the exact diagnosis
        try:
            plant_info = info[diagnosis]
            print(info[diagnosis])
            return plant_info
        except KeyError:
            print(f"No exact match for {diagnosis}")

            # Try partial matching
            for key in info.keys():
                if diagnosis in key:
                    print(f"Found partial match: {key}")
                    return info[key]

            print(f"No match found for diagnosis: {diagnosis}")
            return {}

    except Exception as e:
        print(f"Unexpected error in get_plant_info: {e}")
        import traceback
        traceback.print_exc()
        return {}

if __name__ == '__main__':
    app.run(debug=True)