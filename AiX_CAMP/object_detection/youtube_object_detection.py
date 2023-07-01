import argparse
import cv2

from object_detection_functions import YOLOModel, read_classes, show_detected_objects

import yt_dlp
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight_path", type=str, default="./yolov3-tiny.weights")
    parser.add_argument("--cfg_path", type=str, default="./yolov3-tiny.cfg")
    parser.add_argument("--class_path", type=str, default="./coco.names")
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/WriuvU1rXkc?t=22")
    args = parser.parse_args()

    # Model 정의
    print("모델을 로딩합니다... ")
    model = YOLOModel(args.weight_path, args.cfg_path)
    print("모델 로딩이 완료되었습니다")

    ydl_opts = {
        "format": "mp4/bestaudio/best",
    }
    classes = read_classes(args.class_path)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(args.youtube_url, download=False)
        ydl.download([info['webpage_url']])
        file_name=ydl.prepare_filename(info)
        new_path = pathlib.Path().absolute().joinpath(file_name)

        if not pathlib.Path(new_path).is_file():
            print("파일 다운로드에 실패하였습니다.")
        else: 
            print("객체 검출을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")
            cap = cv2.VideoCapture(str(new_path))
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("비디오를 가져오는 중 오류가 발생했습니다")
                    break
                
                cv2.imshow("Original Video", frame)

                outs = model.inference(frame)
                show_detected_objects(frame, outs, classes, threshold=0.4)

                if cv2.waitKey(1) > 0:
                    break

            print("객체 검출을 종료합니다")