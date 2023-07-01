import argparse
import cv2
import imutils
import numpy as np

import os
from kafka import KafkaConsumer
from recognition_functions import get_known_encodings, detect_faces, recognize_faces, draw_recognition_results

if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("--known_path", default="../dataset/single_face")
    parser.add_argument("--save_path", default="../dataset/single_face/saved_encodings.pkl")
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--topic", default="pi-video")
    args = parser.parse_args()

    server_ip = os.environ.get("SERVER_IP")
    consumer = KafkaConsumer(args.topic, bootstrap_servers=f"{server_ip}:9092")

    
    # 미리 알고 있던 얼굴에 대한 정보를 불러옵니다
    known_names, known_encodings = get_known_encodings(args.known_path)
    
    print("얼굴 인식을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")
    for message in consumer:
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)
        img = imutils.resize(img, width=800)

        face_locations = detect_faces(img)
        recognized_names = recognize_faces(img, face_locations, known_encodings, known_names, args.threshold)
        draw_recognition_results(img, face_locations, recognized_names)

        if cv2.waitKey(1) > 0:
            break
    print("얼굴 인식을 종료합니다")
