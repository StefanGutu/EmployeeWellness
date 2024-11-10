import pandas as pd
import cv2
import os
import numpy as np
from image_landmark import get_pose_params
import random

#TODO: To be tested
def augment_image(image):
    def rotate_image(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (w, h))

    def add_gaussian_noise(image, mean=0, std=0.3):
        noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
        return cv2.add(image, noise)
    # Randomly apply rotation
    if random.choice([True, False]):
        image = rotate_image(image, angle=random.uniform(-5, 5))
        
    # Randomly apply Gaussian noise
    else:
        image = add_gaussian_noise(image, mean=0, std=10)
        
    return image


def get_dataset(input_path: str, output_path="posture_dataset.csv", aug=False):
    columns = []
    # Loop through all files in the directory
    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        target_label = os.path.splitext(filename)[0].split('_')[1]  # Get the part before the extension and split by '_'
        img = cv2.imread(file_path)
        if img is None:
            continue

        # sharpened_img, flipped_img = augument_image(img)

        _, img_params = get_pose_params(img)
        if img_params:
            if not columns:
                columns = list(img_params.keys()) + ['Target']
                df = pd.DataFrame(columns=columns)
                df.to_csv(output_path, index=False)
        else:
            continue
        
        # Augumentarea
        # _, shrp_params = get_pose_params(sharpened_img)
        # _, flip_params = get_pose_params(flipped_img)

        # rows.append([list(param.values()) + [int(target_label)] for param in [img_params, shrp_params, flip_params] if param])
        # df = pd.DataFrame([list(param.values()) + [int(target_label)] for param in [img_params, shrp_params, flip_params] if param], columns=columns)
        df = pd.DataFrame([list(img_params.values()) + [int(target_label)]])
        df.to_csv(output_path, mode='a', header=False, index=False)
    # df = pd.DataFrame(rows, columns=columns)
    # df.to_csv(output_path)


get_dataset("../posture_images_data")
        





