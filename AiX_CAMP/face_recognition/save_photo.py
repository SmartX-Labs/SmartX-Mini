import cv2
import os
import numpy as np
import argparse
from kafka import KafkaConsumer


def record_face(consumer, save_path):
    cnt = 0
    print("사진 저장을 시작합니다")
    print("이름을 입력한 뒤, 키를 누르시면 사진이 저장됩니다. 종료하시려면 사람의 이름 대신 'c'를 입력해주세요")
    name = input(f"사람의 이름을 영어로 입력해 주세요: ")
    for message in consumer:
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)
        cv2.imshow(f"{name} Photo", img)
        
        if cv2.waitKey(1) > cnt:
            cnt += 1
            cv2.imwrite(f"{save_path}/{name}.jpg", img)
            print(f"{save_path}/{name}.jpg 에 이미지가 저장되었습니다")
            name = input(f"사람의 이름을 영어로 입력해 주세요: ")
            if name == 'c': return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", default="../dataset/single_face")
    args = parser.parse_args()


    server_ip = os.environ.get("SERVER_IP")
    consumer = KafkaConsumer("pi-video", bootstrap_servers=f"{server_ip}:9092")
    os.makedirs("./known_faces", exist_ok=True)

    record_face(consumer, args.save_path)