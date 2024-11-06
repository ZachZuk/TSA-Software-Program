import os
from PIL import Image

def load_dataset(data_dir):
    images = []
    labels = []
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        if os.path.isdir(label_dir):
            for img_file in os.listdir(label_dir):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(label_dir, img_file)
                    
                    # Load image
                    image = Image.open(img_path)
                    images.append(image)
                    
                    # Append label
                    labels.append(label)
    
    return images, labels

# Example usage
train_images, train_labels = load_dataset('PlantDoc/train')
test_images, test_labels = load_dataset('PlantDoc/test')
