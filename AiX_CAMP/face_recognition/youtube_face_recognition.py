import argparse
import cv2
import imutils
import numpy as np

from recognition_functions import get_known_encodings, detect_faces, recognize_faces, draw_recognition_results

import yt_dlp
import pathlib

if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("--known_path", default="../dataset/single_face")
    parser.add_argument("--save_path", default="../dataset/single_face/saved_encodings.pkl")
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    args = parser.parse_args()

    # 미리 알고 있던 얼굴에 대한 정보를 불러옵니다
    known_names, known_encodings = get_known_encodings(args.known_path)
    

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
            print("얼굴 인식을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")

            cap = cv2.VideoCapture(str(new_path))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("비디오를 가져오는 중 오류가 발생했습니다")
                    break
                img = imutils.resize(frame, width=500)

                face_locations = detect_faces(img)
                recognized_names = recognize_faces(img, face_locations, known_encodings, known_names, args.threshold)
                draw_recognition_results(img, face_locations, recognized_names)

                if cv2.waitKey(1) > 0:
                    break
            
    print("얼굴 인식을 종료합니다")