from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import pathlib
import argparse

from landmark_utils import show_raw_landmarks, show_landmark_shape

import yt_dlp

if __name__ == "__main__":
    # 인자로 데이터의 경로를 받습니다
    parser = argparse.ArgumentParser()
    # parser.add_argument("--show_parts", type=bool, default=False)
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    args = parser.parse_args()

    # 얼굴 탐지기(detector)와 특징점 추출기(predictor)를 선언합니다
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    # 유튜브 동영상을 다운로드합니다

    ydl_opts = {
        "format": "mp4/bestaudio/best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(args.youtube_url, download=False)
        ydl.download([info['webpage_url']])
        file_name=ydl.prepare_filename(info)
        new_path = pathlib.Path().absolute().joinpath(file_name)

        if not pathlib.Path(new_path).is_file():
            print("파일 다운로드에 실패하였습니다.")
        else: 
            print("이미지 창에서 esc 버튼을 눌러 종료하세요. 얼굴 특징점 추출을 시작합니다")

            cap = cv2.VideoCapture(str(new_path))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("비디오를 가져오는 중 오류가 발생했습니다")
                    break

                image = imutils.resize(frame, width=500)
                show_landmark_shape(image, detector, predictor) # 동영상 내 사람 얼굴을 탐지하고 보여줍니다

                if cv2.waitKey(1) > 0:
                    break

            print("얼굴 특징점 추출을 종료합니다")

