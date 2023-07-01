import argparse
import cv2
import pathlib
import yt_dlp

import pathlib

from style_transfer_functions import StyleTransferNet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    parser.add_argument("--style_path", default=str(pathlib.Path().absolute().parent.joinpath('style_transfer/models/mosaic_light.onnx')))
    parser.add_argument("--skip_ratio", type=int, default=10)
    args = parser.parse_args()

    # 모델을 정의합니다
    model = StyleTransferNet(args.style_path)


    SKIP_RATIO = args.skip_ratio # 추론하는 데 시간이 오래 걸리기 때문에, 프레임을 스킵하며 추론하도록 했습니다

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
            print("이미지 창에서 esc 버튼을 눌러 종료하세요. 스타일 변환을 시작합니다")

            cap = cv2.VideoCapture(str(new_path))

            print("스타일 변환을 수행합니다. esc 키를 누르면 종료합니다")
            i = 0;
            while True: 
                ret, frame = cap.read()
                if not ret:
                    print("비디오를 가져오는 중 오류가 발생했습니다")
                    break
                
                if i % SKIP_RATIO == 0:
                    output = model.inference(frame)

                i = i + 1

                # 원본 영상과 스타일 변환된 영상을 함께 출력합니다
                cv2.imshow("Input", frame)
                cv2.imshow("Output", output)

                if cv2.waitKey(1) > 0:
                    break
            
            print("스타일 변환을 종료합니다")