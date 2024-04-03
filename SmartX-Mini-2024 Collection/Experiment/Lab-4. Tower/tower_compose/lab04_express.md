# lab04

사용법

1. sudo apt update && sudo apt install -y docker-compose-plugin sshpass
2. cd "~/SmartX-Mini/SmartX-Mini-2023 Collection/Experiment/Lab-3. Tower/tower_compose"
3. sudo docker compose up # please wait about 30 seconds after you type the command
4. chmod +x pi_flume.sh
5. ./pi_flume.sh # after you type this please wait up to 5 minutess
6. change SmartX-mini/ubuntu-kafkatodb/broker_to_influxdb.py appropriately
7. run below commands

```
sudo sysctl -w fs.file-max=100000
ulimit -S -n 2048
python3 ~/SmartX-mini/ubuntu-kafkatodb/broker_to_influxdb.py
```

8. please go to http://localhost:8888 and see the visualized result of lab02.

## 내년도 조교분들을 위한 전체적인 설명

0. lab4가 정상적으로 안된 학생분들을 위한 code입니다.
1. docker compose yaml과 pi_flume.sh은 lab2에서 kakfa와 flume가 잘 build 된 후에 사용해 주세요.
   1-1. 2023년 기준 docker image가 build가 잘못되서 lab 진행이 안될 수도 있으므로, sudo docker rmi를 통해서 지우고 다시 build하는 것도 방법입니다.
2. 또한, 기존에 container 들을 sudo docker rm -f 를 통해서 chronograf, influxdb, zookeeper, broker0, broker1, broker2, consumer을 지운 후에 docker compose yaml을 사용해 주세요
3. pi_flume.sh에 대해서 raspberry pi의 host가 재부팅 시에 초기화 된다는 고려하여 작성되었기 때문에, 다시 lab을 진행한다면 pi를 sudo reboot 해주세요.
4. kafka와 flume간에 sink가 이루에 지기까지 최대 10분 정도 기다려 주세요.
   4-1. terminal에 sink만 출력되고 pi의 SNMP 정보가 나오지 않는 경우를 말합니다.
