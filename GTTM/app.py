import cv2
import os
from utils.detector import detect_and_draw
from utils.ocr_reader import read_plate_text
from utils.file_utils import save_plate_image, save_frame_image


def process_input(input_path):
    # KHÔNG xoá thư mục — giữ toàn bộ ảnh cũ
    if input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        process_video(input_path)
    else:
        process_image(input_path)


def process_image(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        print("❌ Không thể đọc ảnh.")
        return

    frame, plates = detect_and_draw(frame)

    # ✅ Lưu từng biển số và đọc chữ
    for plate in plates:
        save_plate_image(plate)
        text = read_plate_text(plate)
        print(f"🔹 Biển số: {text}")

    save_frame_image(frame)  # ✅ Lưu frame kết quả

    # ✅ Hiển thị ảnh
    cv2.imshow("Kết quả nhận diện", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Không thể mở video.")
        return

    # ✅ Video Output
    out = cv2.VideoWriter(
        'static/outputs/output_video.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        20.0,
        (int(cap.get(3)), int(cap.get(4)))
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, plates = detect_and_draw(frame)

        # ✅ Lưu và đọc từng biển số xuất hiện
        for plate in plates:
            save_plate_image(plate)
            text = read_plate_text(plate)
            if text:
                cv2.putText(frame, text, (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255), 2)

        save_frame_image(frame)  # ✅ Lưu từng frame xử lý
        out.write(frame)

        # ✅ Hiển thị video trực tiếp
        cv2.imshow("Video - Nhận diện biển số", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("✅ Video đã lưu tại: static/outputs/output_video.mp4")


if __name__ == "__main__":
    path = input("Nhập đường dẫn ảnh hoặc video: ").strip()
    process_input(path)
