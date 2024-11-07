import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

img_height, img_width = 100, 100

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
    model = load_model(f'{plant_type}_model.keras')

    # making the path for where the categories are
    test_directory = os.path.join('src', 'Plant-Images', plant_type, 'test')
    
    # generate class indices from folder names in the test directory
    class_indices = {folder: idx for idx, folder in enumerate(os.listdir(test_directory)) if os.path.isdir(os.path.join(test_directory, folder))}

    # predict
    predicted_label = predict_image(model, img_path, class_indices)

    print(f'Predicted Label: {predicted_label}')

#   testing
diagnose("Grape", 'src/Plant-Images/Grape/train/Grape___Esca_(Black_Measles)/Grape___Esca_(Black_Measles)_0ca3b914-f951-485e-897d-ed75dc3c423f___FAM_B.Msls 3844.JPG')