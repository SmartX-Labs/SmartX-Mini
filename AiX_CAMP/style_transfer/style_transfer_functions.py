import imutils
import cv2
import os
import numpy as np


class StyleTransferNet:
    def __init__(self, model_path):
        self.net = self.load_model(model_path)

    def load_model(self, model_name):
        print("사전학습된 모델을 로딩합니다..")
        net = cv2.dnn.readNet(model_name)
        print("모델 로딩이 완료되었습니다.")
        return net

    def inference(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
        
        self.net.setInput(blob)
        output = self.net.forward()
        output = output.reshape((3, output.shape[2], output.shape[3]))
        output[0] += 103.939
        output[1] += 116.779
        output[2] += 123.680
        output /= 255.0
        output = output.transpose(1, 2, 0)

        return output


if __name__ == '__main__':
    # MODEL_PATH = './pretrained_winter_game.onnx'
    MODEL_PATH = './models/wave150.onnx'
    print("사전학습된 모델을 로딩합니다..")
    net = cv2.dnn.readNet(MODEL_PATH)
    print("모델 로딩이 완료되었습니다.")

    server_ip = os.environ.get("SERVER_IP")
    consumer = KafkaConsumer("pi-video", bootstrap_servers=f"{server_ip}:9092")

    SKIP_RATIO = 10 # 추론하는 데 시간이 오래 걸리기 때문에, 가능한 최근 영상에서 추론하도록 했습니다
    for i, msg in enumerate(consumer):
        array = np.frombuffer(msg.value, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)

        frame = imutils.resize(img, width=600)
        
        # 10 번의 동영상 이미지 전송이 있을 때마다, 스타일 변환을 시행합니다
        if i % SKIP_RATIO == 0:
            orig = frame.copy()
            (h, w) = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
        
            net.setInput(blob)
            output = net.forward()
            output = output.reshape((3, output.shape[2], output.shape[3]))
            output[0] += 103.939
            output[1] += 116.779
            output[2] += 123.680
            output /= 255.0
            output = output.transpose(1, 2, 0)

        # 원본 영상과 스타일 변환된 영상을 함께 출력합니다
        cv2.imshow("입력 영상", frame)
        cv2.imshow("스타일 변환 영상", output)

        if cv2.waitKey(1) > 0:
            break
        