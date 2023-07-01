from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import time
import os
import argparse
from kafka import KafkaConsumer

from landmark_utils import show_raw_landmarks, show_landmark_shape


if __name__ == "__main__":
    # 인자로 데이터의 경로를 받습니다
    parser = argparse.ArgumentParser()
    # parser.add_argument("--show_parts", type=bool, default=False)
    parser.add_argument("--topic", type=str, default='pi-video')
    args = parser.parse_args()

    # Kakfa와 연결해 pi-video topic을 구독합니다
    server_ip = os.environ.get('SERVER_IP')
    topic = 'pi-video'
    consumer = KafkaConsumer(topic, bootstrap_servers=f"{server_ip}:9092")

    # 얼굴 탐지기(detector)와 특징점 추출기(predictor)를 선언합니다
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    print("이미지 창에서 esc 버튼을 눌러 종료하세요. 얼굴 특징점 추출을 시작합니다")
    for message in consumer:
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        image = cv2.imdecode(array, 1)
        image = imutils.resize(image, width=500) # 이미지의 크기를 줄입니다

        show_landmark_shape(image, detector, predictor)

        if cv2.waitKey(1) > 0:
            break

    print("얼굴 특징점 추출을 종료합니다")