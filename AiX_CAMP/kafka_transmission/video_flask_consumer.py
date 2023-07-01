import argparse
import os

from flask import Flask, Response
from kafka import KafkaConsumer


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--topic", default='pi-video')
	args = parser.parse_args()

	# Broker 서버의 IP 주소와 사용할 topic 설정을 읽어옵니다
	server_ip = os.environ.get("SERVER_IP")
	topic = args.topic

	consumer = KafkaConsumer(topic, bootstrap_servers=f'{server_ip}:9092')

	app = Flask(__name__)

	def kafkastream():
		for message in consumer:
			yield(b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')

	@app.route('/')
	def index():
		return Response(kafkastream(), mimetype='multipart/x-mixed-replace; boundary=frame')


	if __name__ == '__main__':
		app.run(host='0.0.0.0')
