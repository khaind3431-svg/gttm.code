import easyocr
import cv2
import os

reader = easyocr.Reader(['en'])

def read_plate_text(image_path):
    # Nếu input là đường dẫn -> đọc ảnh
    if isinstance(image_path, str):
        if not os.path.exists(image_path):
            return ""
        image = cv2.imread(image_path)
    else:
        image = image_path

    # Chuyển sang grayscale nếu ảnh là màu
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Đọc chữ bằng EasyOCR
    results = reader.readtext(image)
    text = ""
    for (bbox, text_found, prob) in results:
        text += text_found + " "

    return text.strip()
