import os
import cv2  # OpenCV for image reading and writing
import random
import numpy as np
# Define paths
input_dir = 'posture_images_data'       # Directory containing the original images
output_dir = 'augmented_data'     # Directory to save augmented images

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Placeholder for your augmentation function
def augment_image(image):
    def rotate_image(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (w, h))

    def add_gaussian_noise(image, mean=0, std=1):
        noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
        return cv2.add(image, noise)
    # Randomly apply rotation
    if random.choice([True, False]):
        image = rotate_image(image, angle=random.uniform(-5, -1))
    else:
        image = rotate_image(image, angle=random.uniform(1, 5))
    # Randomly apply Gaussian noise
    #else:
    image = add_gaussian_noise(image, mean=0, std=0.3)
        
    return image
# Process each .jpg file in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.jpg'):
        # Load the image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        
        # Skip if image couldn't be loaded
        if image is None:
            print(f"Warning: Could not read {filename}. Skipping.")
            continue
        
        # Apply the augmentation function
        augmented_image = augment_image(image)
        
        # Construct new filename with the prefix "a"
        new_filename = f"a{filename}"
        output_path = os.path.join(output_dir, new_filename)
        
        # Save the augmented image to the output directory
        cv2.imwrite(output_path, augmented_image)
        output_path = os.path.join(output_dir, filename)
        
        # Save the augmented image to the output directory
        cv2.imwrite(output_path, image)
        print(f"Saved augmented image: {output_path}")
