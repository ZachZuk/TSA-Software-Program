import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout

# parameters
img_height, img_width = 200, 200  # sizes of images
batch_size = 16

# list of plants
plants = ['Grape']

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
        Conv2D(256, (3, 3), activation='relu'),  # Added more filters
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(512, (3, 3), activation='relu'),  # Added another layer
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(256, activation='relu'),  # Increased the number of units in the dense layer
        Dropout(0.5),  # Regularization to prevent overfitting
        Dense(len(train_generator.class_indices), activation='softmax')  # Number of classes
    ])

    # Early stopping callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # training the model with early stopping
    model.fit(
        train_generator,
        epochs=50,  # You can set a higher number of epochs
        validation_data=test_generator,
        callbacks=[early_stopping]  # Add early stopping callback
    )

    # printing stuff about the model
    loss, accuracy = model.evaluate(test_generator)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

    # saving the model
    model.save(f'  {plant_type}_model.keras')

# making a model for each plant
for plant in plants:
    trainPlant(plant)