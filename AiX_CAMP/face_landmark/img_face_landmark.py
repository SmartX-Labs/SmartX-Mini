import argparse
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

from landmark_utils import show_raw_landmarks, show_landmark_shape


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, default="../dataset/single_face/jimin.jpg")
    parser.add_argument("--show_parts", type=bool, default=False)
    args = parser.parse_args()

    # 얼굴 탐지기(detector)와 특징점 추출기(predictor)를 선언합니다
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # 얼굴을 찾을 이미지를 읽어옵니다
    image = cv2.imread(args.img_path)
    image = imutils.resize(image, width=500)

    show_landmark_shape(image, detector, predictor, args.show_parts)
    
    print("이미지 창에서 esc 버튼을 눌러 종료하세요")
    cv2.waitKey(0)
    print("특징점 추출을 종료합니다")