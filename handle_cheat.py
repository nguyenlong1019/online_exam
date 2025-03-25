import cv2
import numpy as np
import sys
import os
import django
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exam_monitoring.settings")
django.setup()

from quiz.models.quiz import Monitor, Result



# Load model và cấu trúc mạng
model_file = "deploy.prototxt.txt"
config_file = "res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(model_file, config_file)


def process_video(monitor_id):
    count = 0
    reason = ""

    # Lấy đối tượng Monitor
    monitor = Monitor.objects.get(id=monitor_id)
    video_path = monitor.video.path

    # Mở video
    camera = cv2.VideoCapture(video_path)
    is_cheat = False

    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 360)) 

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        face_count = 0
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Ngưỡng phát hiện
                face_count += 1
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x1, y1, x2, y2) = box.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if face_count == 0:
            count += 1
            reason = "Gian lận: Không có người trong khung hình"
            print("Không có người trong khung hình, có thể là gian lận")
        elif face_count > 1:
            count += 1
            reason = "Gian lận: Có nhiều người trong khung hình"
            print("Có nhiều người trong khung hình, có thể là gian lận")

        if count > 6:
            is_cheat = True 
            break 
        

    camera.release()

    # Cập nhật trạng thái gian lận trong cơ sở dữ liệu
    monitor.is_cheat = is_cheat
    monitor.reason = reason
    monitor.save()

    print(monitor.exam)
    print(monitor.user)

    result = Result.objects.filter(exam=monitor.exam, user=monitor.user).order_by('-created_at').first()
    result.is_cheat = is_cheat
    result.reason = reason
    result.is_done = True
    result.save()


if __name__ == "__main__":
    monitor_id = int(sys.argv[1])
    process_video(monitor_id)
