import cv2
import os

def save_plate_image(plate):
    folder = "static/plates"
    os.makedirs(folder, exist_ok=True)

    index = len(os.listdir(folder)) + 1
    filename = f"plate_{index:04d}.jpg"
    cv2.imwrite(os.path.join(folder, filename), plate)


def save_frame_image(frame):
    folder = "static/outputs"
    os.makedirs(folder, exist_ok=True)

    index = len(os.listdir(folder)) + 1
    filename = f"frame_{index:04d}.jpg"
    cv2.imwrite(os.path.join(folder, filename), frame)
