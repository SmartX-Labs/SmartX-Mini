# Links Markdown

## 복잡한 link를 쉽게 작성할 수 있도록 하기위한 markdown 입니다.

### Lab 02

1. lab02 ppt: 필요한 패키지 및 Kafka 설치 in NUC
```Bash
wget http://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
```
2. lab02 ppt: 필요한 패키지 및 Kafka 설치 in Pi
```Bash
wget http://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
```
3. lab02 ppt: Kafka Topic 생성
```Bash
sudo bin/kafka-topics.sh --create --bootstrap-server <NUC IP>:9092 --replication-factor 1 --partitions 1 --topic chat
```
`<NUC IP>`를 적절하게 수정해 주세요.  

4. lab02 ppt: Python Kafka Producer
```Bash
git clone https://github.com/SmartX-Labs/SmartX-Mini.git
```
5. lab02 ppt: Kafka Setup
```Bash
sudo bin/kafka-topics.sh --create --bootstrap-server <NUC IP>:9092 --replication-factor 1 --partitions 1 --topic pi-video
```
`<NUC IP>`를 적절하게 수정해 주세요.  

6. lab02 ppt: OpenCV Python Setup in Pi
```Bash
sudo apt install libdatrie1 libswresample3 libchromaprint1 libgsm1 libgdk-pixbuf2.0-0 libxcb-shm0 libaom0 libjbig0 libspeex1 libtwolame0 libx264-155 libcroco3 libatspi2.0-0 libmp3lame0 libopenmpt0 librsvg2-2 libgraphite2-3 libcairo2 libxkbcommon0 libatk1.0-0 libvorbisenc2 libvorbisfile3 libwayland-client0 libwavpack1 libvdpau1 libgfortran5 libatlas3-base libvpx5 libxrandr2 libzvbi0 libxfixes3 libavcodec58 libgtk-3-0 libxcursor1 libtheora0 libsnappy1v5 libthai0 libwayland-egl1 libopenjp2-7 libxdamage1 libcodec2-0.8.1 libopus0 libswscale5 libxvidcore4 libshine3 libwayland-cursor0 libsoxr0 libatk-bridge2.0-0 libwebpmux3 libbluray2 libxcb-render0 libx265-165 libharfbuzz0b libva-x11-2 libxi6 libxrender1 libcairo-gobject2 libxinerama1 libtiff5 libvorbis0a libmpg123-0 libssh-gcrypt-4 libpangoft2-1.0-0 libpango-1.0-0 libogg0 libva2 libavutil56 libwebp6 libva-drm2 libdrm2 libavformat58 libpixman-1-0 libfontconfig1 libxcomposite1 libgme0 libpangocairo-1.0-0 libepoxy0
```

### Lab 03

1. lab03 ppt: Python 패키지 설치, 모델 다운로드: dlib
```Bash
sudo apt-get install -y build-essential cmake libgtk-3-dev libboost-all-dev
```
```Bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
```
2. lab03 ppt: Python 패키지 설치, 모델 다운로드: yolo
```Bash
wget https://pjreddie.com/media/files/yolov3-tiny.weights
```

3. lab03 ppt: Python 패키지 설치, 모델 다운로드: style
```Bash
wget https://www.dropbox.com/sh/2z3hyrewinnmubf/AACUAazQxfKpiMBzjHUVXFRDa --content-disposition
```


