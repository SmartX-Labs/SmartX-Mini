# 사용할 라이브러리를 불러옵니다
from kafka import KafkaProducer # kafka는 pip3로 설치한 kafka-python 라이브러리입니다. Producer를 선언하기 위해 사용합니다
import sys # sys는 파이썬 인터프리터의 변수와 함수를 제어할 수 있게 해주며, 터미널 입력을 받기 위해 사용합니다
import json # json은 JSON 형식의 파일을 다룰 때 사용하고, 여기에서는 메시지를 JSON 형식으로 보내기 위해 사용합니다.
import argparse # argparse는 파이썬을 실행할 때 인자를 받고 다루기 위해 사용합니다
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default='chat') # python 실행시 topic을 인자로 받습니다. 인자를 주지 않으면 "chat"으로 기본값을 주겠습니다.
    args = parser.parse_args()

    server_ip = os.environ.get("SERVER_IP") # 환경변수에 저장된 서버 IP 주소를 가져옵니다.
    topic = args.topic

    # kafka-python 라이브러리에서 가져온 KafkaProducer를 사용해 JSON 형식의 메시지를 발행하는 Kafka producer를 정의합니다
    producer = KafkaProducer(bootstrap_servers=[f'{server_ip}:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    content = 'Python으로 메시지 보내기~'

    # 사용자가 프로그램을 ctrl + C로 종료하거나, 메시지 전송이 이뤄지지 않고 쌓여 오류가 나기 전에는 계속 터미널의 사용자 입력을 받아 발행합니다.
    k = 0
    while True:
        try:
            content = {str(k): content}
            producer.send(topic, content)
            k += 1
            content = input('메시지를 입력하세요: ')
            #producer.poll()
        except BufferError:
            print(f"로컬 producer의 큐가 가득 찼습니다. ({len(producer)}개의 메시지들이 전송 대기중입니다): 다시 시도해주세요")
            break
        except KeyboardInterrupt:
            print("메시지 전송을 종료합니다")
            break


    producer.flush()
