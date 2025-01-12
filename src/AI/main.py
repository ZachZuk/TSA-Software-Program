import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory
from diagnose import diagnoser
from llm import generate
import os
from flask_cors import CORS
import sys

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOADS_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')

app = Flask(__name__, template_folder='../')
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "http://127.0.0.1:5500", "http://localhost:8000"], 
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "expose_headers": ["Content-Type"]
    }
})

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.debug(f"Generate request received with form data: {request.form}")
        if 'message' not in request.form:
            return jsonify({"error": "No message provided"}), 400

        message = request.form['message']
        result = generate(message)
        return jsonify({"info": result})
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An error occurred while generating a response."}), 500

@app.route('/diagnose_plant', methods=['POST'])
def diagnose_plant():    
    try:
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
        filename = os.path.basename(image_file.filename)
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
            diagnosis = diagnoser(plant_type, filepath)
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')

@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html')

@app.route('/diseases')
def diseases():
    return render_template('diseases.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/info.json')
def info_json():
    return send_from_directory('../', 'info.json')

@app.route('/app.js')
def app_js():
    return send_from_directory('../', 'app.js')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../', 'favicon.ico')

# python web server
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))