import time
import sys
import argparse
import cv2
import os

from kafka import KafkaProducer
from kafka.errors import KafkaError

# 카메라 영상을 스트리밍합니다
def produce_videostream(device_path):
    print("비디오 전송을 시작합니다")
    video = cv2.VideoCapture(device_path)

    # 비디오를 읽어옵니다
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("비디오를 읽는 과정에서 오류가 발생했습니다")
            break
        
        # 이미지 파일을 전송하기 위해 byte로 인코딩합니다
        data = cv2.imencode('.jpeg', frame)[1].tobytes()

        # 이미지 데이터를 전송합니다
        future = producer.send(topic, data)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break
        print('.', end='', flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default='pi-video')
    args = parser.parse_args()

    # Broker 서버의 IP 주소와 사용할 topic 설정을 읽어옵니다
    server_ip = os.environ.get("SERVER_IP")
    topic = args.topic

    # Kafka producer를 선언합니다
    producer = KafkaProducer(bootstrap_servers=f"{server_ip}:9092")

    # 0번째 카메라 장치를 사용해 비디오를 스트리밍합니다
    produce_videostream(0)



