import random
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

img_height, img_width = 200, 200

plant_types = ['Apple', 'Cherry_(including_sour)', 'Corn_(maize)', 'Grape', 'Peach', 'Pepper,_bell', 'Potato', 'Strawberry']

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
    # loading in the right model for the plant
    model = load_model(f'models/{plant_type}_model.keras')

    # making the path for where the categories are
    test_directory = os.path.join('src', 'Plant-Images', plant_type, 'test')
    
    # generate class indices from folder names in the test directory
    class_indices = {folder: idx for idx, folder in enumerate(os.listdir(test_directory)) if os.path.isdir(os.path.join(test_directory, folder))}

    # predict
    return predict_image(model, img_path, class_indices)

plants = []

correct = 0

for i in range(0, 100):
    plant_type = random.choice(plant_types)
    plant_diagnosis = random.choice(os.listdir(os.path.join("src", "Plant-Images", plant_type, "train")))
    img_url = f'src/Plant-Images/{plant_type}/train/{plant_diagnosis}/{random.choice(os.listdir(os.path.join("src", "Plant-Images", plant_type, "train", plant_diagnosis)))}'
    plants.append([plant_type, img_url, plant_diagnosis])

for plant in plants:
    diagnosis = diagnose(plant[0], plant[1])
    print('Actual diagnosis: ' + plant[2] + ' | Predicted: ' + diagnosis)
    if diagnosis == plant[2]:
        correct += 1

print('accuracy: ' + str(correct) + ' out of 100')