import argparse
import os
import numpy as np
import cv2

from kafka import KafkaConsumer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default='pi-video')
    args = parser.parse_args()

    # Broker 서버의 IP 주소와 사용할 topic 설정을 읽어옵니다
    server_ip = os.environ.get("SERVER_IP")
    topic = args.topic
    
    consumer = KafkaConsumer(topic, bootstrap_servers=f"{server_ip}:9092")

    for message in consumer:
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)
        cv2.imshow("Input", img)

        if cv2.waitKey(1) > 0:
            break
    print("영상 수신을 종료합니다")