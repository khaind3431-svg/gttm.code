from ultralytics import YOLO
import cv2
import os

model = YOLO("model/best.pt")

def detect_and_draw(frame, output_dir="static/plates", conf=0.5):
    os.makedirs(output_dir, exist_ok=True)
    results = model(frame, conf=conf)
    boxes = results[0].boxes.xyxy
    annotated_frame = frame.copy()
    plate_images = []

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        crop = frame[y1:y2, x1:x2]
        plate_path = os.path.join(output_dir, f"plate_{i}.jpg")
        cv2.imwrite(plate_path, crop)
        plate_images.append(plate_path)
    return annotated_frame, plate_images
