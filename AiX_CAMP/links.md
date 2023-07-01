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

### Lab 03

1. lab03 ppt: Python 패키지 설치, 모델 다운로드: dlib
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


