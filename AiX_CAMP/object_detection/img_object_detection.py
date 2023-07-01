import os
import argparse
import cv2
import numpy as np

from object_detection_functions import YOLOModel, read_classes, show_detected_objects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight_path", type=str, default="./yolov3-tiny.weights")
    parser.add_argument("--cfg_path", type=str, default="./yolov3-tiny.cfg")
    parser.add_argument("--class_path", type=str, default="./coco.names")
    parser.add_argument("--img_path", type=str, default="../dataset/objects/dog_bicycle.jpg")
    args = parser.parse_args()

    # Model 정의
    print("모델을 로딩합니다... ")
    model = YOLOModel(args.weight_path, args.cfg_path)
    print("모델 로딩이 완료되었습니다")

    classes = read_classes(args.class_path)

    # 이미지를 읽어옵니다
    img = cv2.imread(args.img_path)
    
    print("객체 검출을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")
    cv2.imshow("Original Video", img)
    outs = model.inference(img)
    while True:
        show_detected_objects(img, outs, classes, threshold=0.4)
        if cv2.waitKey(1) > 0:
            break

    print("객체 검출을 종료합니다")