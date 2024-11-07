import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

# parameters
img_height, img_width = 100, 100  # sizes of images
batch_size = 32

# list of plants
plants = ['Apple', 'Cherry_(including_sour)', 'Corn_(maize)', 'Grape', 'Peach', 'Pepper,_bell', 'Potato', 'Strawberry', 'Tomato']

# function to create a model for a plant
def trainPlant(plant_type):
    # directories for the data
    train_data_dir = f'src\\Plant-Images\\{plant_type}\\train'
    test_data_dir = f'src\\Plant-Images\\{plant_type}\\test'

    # ImageDataGenerator for training
    train_datagen = ImageDataGenerator(rescale=1./255)

    # generate/format training data for cnn i think
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # ImageDataGenerator for testing
    test_datagen = ImageDataGenerator(rescale=1./255)

    # generate/format testing data for cnn i think
    test_generator = test_datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # making the model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(train_generator.class_indices), activation='softmax')  # Number of classes
    ])

    # compiling the model
    model.compile(optimizer=Adam(), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])
    
    # training the model
    model.fit(
        train_generator,
        epochs=10,  # Set the number of epochs
        validation_data=test_generator  # Add validation data
    )

    # printing stuff about the model
    loss, accuracy = model.evaluate(test_generator)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

    # saving the model
    model.save(f'{plant_type}_model.keras')

# making a model for each plant
for plant in plants:
    trainPlant(plant)