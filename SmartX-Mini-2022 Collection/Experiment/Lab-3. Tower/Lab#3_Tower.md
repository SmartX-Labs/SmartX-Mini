# Lab#3. Tower Lab

## 0. Objective

<img width="450" alt="overall objective" src="https://user-images.githubusercontent.com/82452337/160807997-9caadb51-b363-4e82-bbb2-e1f5888b08b3.png">

This lab objective is to build a tower to monitor the system and visualize the information being monitored.

In this lecture, We will monitor the Kafka broker cluster built the last time.

### 0-1. TSDB (Time Series Database)

<img width="225" alt="time series" src="https://user-images.githubusercontent.com/82452337/160809181-421f35de-c9fa-4fe1-a123-ff456443bef6.png">

Time series data is arrays of numbers indexed by time.

#### 0-2. InfluxDB

<img width="225" alt="influxdb logo" src="https://user-images.githubusercontent.com/82452337/160809855-4ed43c06-9d4e-4712-a349-c08616aeef94.png">

InfluxDB is an open-source time-series database (TSDB) developed by the company InfluxData.
It is written in the Go programming language for storage and retrieval of time series data in fields such as operations monitoring, application metrics, Internet of Things sensor data, and real-time analytics.

#### 0-3. Chronograf

<img width="225" alt="chronograf" src="https://user-images.githubusercontent.com/82452337/160810806-d3ec5cad-cae6-4a47-a067-395312523ff2.png">

![chronograf comoponents](./img/chronograf.png)

Chronograf is the user interface and administrative component of the InfluxDB `1.x` platform.
Chronograf allows you to quickly see the data that you have stored in InfluxDB so you can build robust queries and alerts.
It is simple to use and includes templates and libraries to allow you to rapidly build dashboards with real-time visualizations of your data.

## 1. Practice

### 1-1. Make and Run InfluxDB Container ( in NUC )

```bash
sudo docker run -d --name=influxdb --net=host influxdb:1.7
```

### 1-2. Make and run Chronograf container ( in NUC )

```bash
sudo docker run -p 8888:8888 --net=host chronograf --influxdb-url=http://<NUC IP>:8086
```

### 1-3. Install python-pip ( in NUC )

```bash
sudo apt-get install -y libcurl4 openssl curl python3-pip
```

### 1-4. Install python packages ( in NUC )

```bash
sudo pip install requests kafka-python influxdb msgpack
```

### 1-5. Modify `broker_to_influxdb.py` code ( in NUC )

```bash
vi ~/SmartX-mini/ubuntu-kafkatodb/broker_to_influxdb.py
```

In this file, change `<NUC_IP>` into your actual NUC IP.

> ex) '203.237.53.100:9091'

<img width="450" alt="broker_to_influxdb python file" src="https://user-images.githubusercontent.com/82452337/160814546-da543a58-e6b6-49cb-bdb1-19aa2de9c1fb.png">

### 1-6. Run `broker_to_influxdb.py` python code

Before this, you need to check the following,

#### 1-6-1. Kafka zookeeper and brokers in NUC are running
- Start zookeeper,brokers container (excute below command in NUC terminal.)
```bash
sudo docker start zookeeper broker0 broker1 broker2
```
- Run zookeeper (excute below command in zookeeper container.)  
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```
- Run brokers (excute below command in each broker container.)
```bash
bin/kafka-server-start.sh config/server.properties
```
#### 1-6-2. Flume container in PI is running
When pi is rebooted, the information in /etc/hosts disappears.
So, you need to rewrite "IP and hostname info" in /etc/hosts.
```bash
sudo vim /etc/hosts
```
Add 2 lines below the file.

[NUC_IP] [NUC_HOSTNAME]
[PI_IP] [PI_HOSTNAME]

- Start flume container (excute below command in PI terminal.)
```bash
sudo docker start flume
sudo docker attach flume
```
- Run flume (excute below command in flume container.)
```bash
bin/flume-ng agent --conf conf --conf-file conf/flume-conf.properties --name agent -Dflume.root.logger=INFO,console
```

#### 1-6-3. Run `broker_to_influxdb.py`. (excute below commands in NUC terminal.)
````bash
sudo sysctl -w fs.file-max=100000
ulimit -S -n 2048
python3 ~/SmartX-mini/ubuntu-kafkatodb/broker_to_influxdb.py
````

### 1-7. Open your web browser and connect to Chronograf Dashboard ( in NUC )

> ( http:// "YOUR NUC IP" :8888 )

<img width="450" alt="First Dashboard page" src="https://user-images.githubusercontent.com/82452337/160814749-895dc5bf-1076-413f-bca8-3fbbaf72f0b9.png">

### 1-8. Create Dashboard

<img width="450" alt="create Dashborad" src="https://user-images.githubusercontent.com/82452337/160812878-66f82327-dbb5-4a39-ba1d-a48d4b16c8cb.png">

### 1-9. Add data

<img width="450" alt="Add data" src="https://user-images.githubusercontent.com/82452337/160812911-63a7fe0f-4ab3-4ce8-a4ef-54bef3cbdab8.png">

### 1-10. Submit query

```sql
SELECT "memory" FROM "Labs"."autogen"."labs" WHERE time > :dashboardTime:
```

<img width="450" alt="submit graph" src="https://user-images.githubusercontent.com/82452337/160812933-9b8d688b-0b16-474c-ac7c-88530a24131a.png">

### 1-11. We can see the changes in values from influxDB.

<img width="450" alt="graph" src="https://user-images.githubusercontent.com/82452337/160812960-9810fa2c-733e-4cbf-8e1c-a627323aff65.png">

## 2. Lab Summary

With Tower Lab, you have experimented role of Monitor Tower.

Visibility Center function to enable ‘distributed monitoring’ over remote Boxes and to store ‘monitoring information’ to TSDB(Time Series Database).
