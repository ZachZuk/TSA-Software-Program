import logging
import random
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

img_height, img_width = 200, 200

# for testing
plant_types = ['Apple', 'Cherry_(including_sour)', 'Corn_(maize)', 'Grape', 'Peach', 'Pepper,_bell', 'Potato', 'Strawberry', 'Tomato']

# possible classifications because the automatic way mixed things up somehow
class_indices_mapping = {
    'Apple': {
        'Apple___Apple_scab': 0,
        'Apple___Black_rot': 1,
        'Apple___Cedar_apple_rust': 2,
        'Apple___healthy': 3,
    },
    'Cherry_(including_sour)': {
        'Cherry_(including_sour)___Powdery_mildew': 0,
        'Cherry_(including_sour)___healthy': 1,
    },
    'Corn_(maize)': {
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 0,
        'Corn_(maize)___Common_rust_': 1,
        'Corn_(maize)___Northern_Leaf_Blight': 2,
        'Corn_(maize)___healthy': 3,
    },
    'Grape': {
        'Grape___Black_rot': 0,
        'Grape___Esca_(Black_Measles)': 1,
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 2,
        'Grape___healthy': 3,
    },
    'Peach': {
        'Peach___Bacterial_spot': 0,
        'Peach___healthy': 1,
    },
    'Pepper,_bell': {
        'Pepper,_bell___Bacterial_spot': 0,
        'Pepper,_bell___healthy': 1,
    },
    'Potato': {
        'Potato___Early_blight': 0,
        'Potato___Late_blight': 1,
        'Potato___healthy': 2,
    },
    'Strawberry': {
        'Strawberry___Leaf_scorch': 0,
        'Strawberry___healthy': 1,
    },
    'Tomato': {
        'Tomato___Bacterial_spot': 0,
        'Tomato___Early_blight': 1,
        'Tomato___Late_blight': 2,
        'Tomato___Leaf_Mold': 3,
        'Tomato___Septoria_leaf_spot': 4,
        'Tomato___Spider_mites Two-spotted_spider_mite': 5,
        'Tomato___Target_Spot': 6,
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 7,
        'Tomato___Tomato_mosaic_virus': 8,
        'Tomato___healthy': 9,
    }
}

# function to make the image a thing for the cnn and not a jpg
def load_and_preprocess_image(img_path):
    # load the image
    img = image.load_img(img_path, target_size=(img_height, img_width))
    
    # convert the image to an array
    img_array = image.img_to_array(img)
    
    # reshape the array to include batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # rescale the image (same scale as during training)
    img_array /= 255.0
    
    return img_array

# function to make a prediction based on an image
def predict_image(model, img_path, class_indices):
    # load and preprocess the image
    img_array = load_and_preprocess_image(img_path)
    
    # making the prediction
    predictions = model.predict(img_array)
    
    # get the predicted class index
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    
    # stuff for choosing the option basically
    class_labels = list(class_indices.keys())
    predicted_class_label = class_labels[predicted_class_index]
    
    return predicted_class_label

# function to diagnose a plant start to finish
def diagnose(plant_type, img_path):
    try:
        # Log the diagnosis attempt
        logger.debug(f"Starting diagnosis for {plant_type}")
        logger.debug(f"Image path: {img_path}")

        # Check if model file exists
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', f'{plant_type}_model.keras'))
        print(model_path)
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model file for {plant_type} not found")

        # loading in the right model for the plant
        logger.debug(f"Loading model from {model_path}")
        model = load_model(model_path)

        # making the path for where the categories are
        test_directory = os.path.join('src', 'Plant-Images', plant_type, 'test')
        logger.debug(f"Test directory: {test_directory}")

        # get the options from the dictionary from before
        class_indices = class_indices_mapping.get(plant_type)
        if not class_indices:
            logger.error(f"No class indices found for {plant_type}")
            raise ValueError(f"No class indices found for {plant_type}")

        # predict
        logger.debug("Starting image prediction")
        prediction = predict_image(model, img_path, class_indices)
        logger.debug(f"Prediction result: {prediction}")

        return prediction

    except Exception as e:
        logger.error(f"Error in diagnosis: {str(e)}")
        raise

# Modify predict_image to add more logging
def predict_image(model, img_path, class_indices):
    try:
        logger.debug(f"Preprocessing image: {img_path}")
        # load and preprocess the image
        img_array = load_and_preprocess_image(img_path)
        
        logger.debug("Making prediction")
        # making the prediction
        predictions = model.predict(img_array)
        
        # get the predicted class index
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        
        # stuff for choosing the option basically
        class_labels = list(class_indices.keys())
        predicted_class_label = class_labels[predicted_class_index]
        
        logger.debug(f"Predicted class: {predicted_class_label}")
        logger.debug(f"Prediction probabilities: {predictions}")
        
        return predicted_class_label

    except Exception as e:
        logger.error(f"Error in image prediction: {str(e)}")
        raise

# # list of plant image urls, plant type, and the real diagnosis
# plants = []

# # for tracking accuracy
# incorrect = 0

# # getting a bunch of plants and their information for testing
# for i in range(0, 100):
#     # get a random plant type
#     plant_type = random.choice(plant_types)
#     # picking a random disease
#     plant_diagnosis = random.choice(os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plant-Images", plant_type, "train"))))
#     # getting a url for that stuff
#     img_url = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plant-Images", plant_type, "train", plant_diagnosis)), random.choice(os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "Plant-Images", plant_type, "train", plant_diagnosis)))))
#     # putting that all in the plant list
#     plants.append([plant_type, img_url, plant_diagnosis])

# # diagnosing all those plants
# for plant in plants:
#     # diagnosing
#     diagnosis = diagnose(plant[0], plant[1])
#     print('Actual diagnosis: ' + plant[2] + ' | Predicted: ' + diagnosis)
#     # for accuracy and finding issues
#     if diagnosis != plant[2]:
#         print("nope")
#         incorrect += 1

# # printing the accuracy
# print('accuracy: ' + str(100-incorrect) + ' out of 100')