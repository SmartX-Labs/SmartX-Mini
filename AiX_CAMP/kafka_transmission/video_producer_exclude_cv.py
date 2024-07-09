from picamera2 import Picamera2, MappedArray
import io
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import argparse
import os

def main():
    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    while True:
        # Capture frame
        buffer = io.BytesIO()
        picam2.capture_file(buffer, format='jpeg')
        
        # transfor data
        future = producer.send(topic, buffer.getvalue())
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break
        print('.', end='', flush=True)

    # Cancel the sending task and stop the camera
    picam2.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default='pi-video')
    args = parser.parse_args()

    # Broker 서버의 IP 주소와 사용할 topic 설정을 읽어옵니다
    server_ip = os.environ.get("SERVER_IP")
    topic = args.topic

    # Kafka producer를 선언합니다
    producer = KafkaProducer(bootstrap_servers=f"{server_ip}:9092")

    main()