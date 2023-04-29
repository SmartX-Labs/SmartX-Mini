# lab03

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
