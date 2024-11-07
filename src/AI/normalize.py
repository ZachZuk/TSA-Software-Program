import os
import numpy as np
from PIL import Image

# function to make an image suitable for an ai
def normalize_image(image_path):
    # get the image
    img = Image.open(image_path)
    
    # resize the image
    target_size = (200, 200)
    img = img.resize(target_size)
    
    # make it an array not a png
    img_array = np.array(img)
    
    # make the pixel values between 0 and 1
    img_array = img_array / 255.0
    
    # make it an image again
    normalized_img = Image.fromarray((img_array * 255).astype(np.uint8))
    
    return normalized_img

# function to take a place full of images and normalize them
def normalize_images_in_directory(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG')):  # Check for image file types
                image_path = os.path.join(dirpath, filename)
                
                # bnormalize the image
                normalized_img = normalize_image(image_path)
                
                # Save the normalized image, replacing the original
                normalized_img.save(image_path)

root_folder = 'src/Plant-Images'
normalize_images_in_directory(root_folder)