import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout

### training images have been removed from github to save space, training was done one time and then we had the models ### 

# parameters for training
img_height, img_width = 200, 200  # sizes of images
batch_size = 16

# list of plants
plants = ['Apple', 'Cherry_(including_sour)', 'Corn_(maize)', 'Grape', 'Peach', 'Pepper,_bell', 'Potato', 'Strawberry', 'Tomato']

# creating an ai model for a plant
def trainPlant(plant_type):
    # getting the directories for the specific plant training and testing data
    train_data_dir = f'src\\Plant-Images\\{plant_type}\\train'
    test_data_dir = f'src\\Plant-Images\\{plant_type}\\test'

    # ImageDataGenerator for training
    train_datagen = ImageDataGenerator(rescale=1./255)

    # generate/format training data for cnn
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # ImageDataGenerator for testing
    test_datagen = ImageDataGenerator(rescale=1./255)

    # generate/format testing data for cnn
    test_generator = test_datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # defining the model shape
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(512, (3, 3), activation='relu'), 
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(256, activation='relu'),  
        Dropout(0.5), 
        Dense(len(train_generator.class_indices), activation='softmax') 
    ])

    # Early stopping, saving training time
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # compiling the model for cnn
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # training the model with early stopping from before
    model.fit(
        train_generator,
        epochs=50,  
        validation_data=test_generator,
        callbacks=[early_stopping]  
    )

    # printing stuff about the model
    loss, accuracy = model.evaluate(test_generator)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

    # saving the model
    model.save(f'  {plant_type}_model.keras')

# making a model for each plant
for plant in plants:
    trainPlant(plant)