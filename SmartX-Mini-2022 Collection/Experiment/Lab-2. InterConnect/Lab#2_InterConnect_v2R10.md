# 2. InterConnenct Lab

## Objective

## Concept

### Raspberry PI

### Apache Kafka

### Net-SNMP

### Apache-Flume

### Docker

## Practice

<!-- Physical Interconnect 이미지도 넣어야 하나? 근데 iperf나 관련된 확인하는 내용은 터미널 여는 내용 말고 다 빠졌던데 -->
![overview](img/overview.png)

### Check `rc-local-service` Setting (In NUC)

```bash
sudo touch /etc/rc.local
sudo chmod +x /etc/rc.local
sudo vi /lib/systemd/system/rc-local.service
```

Add below lines in `rc-local.service`

```text
...
[Install]
WantedBy=multi-user.target
...
```

Apply setting and check `rc-local.service` status

```bash
sudo systemctl enable rc-local.service
sudo systemctl start rc-local.service
sudo systemctl status rc-local.service
```

![rc-local.service status](./img/rc-local.png)

Reboot your NUC

```bash
sudo reboot
```

### Prepare 3 terminals on NUC

<!-- 이게 왜 필요하지? iperf 내용 startmooc에만 남아있고 21년도 PPT에는 없던데-->

We need 3 terminals.(Bare metal, VM, Contariner)

Boot and Access to KVM on NUC

```bash
sudo kvm -m [memory_capacity] -name [vm_name] \
-smp cpus=[cpu],maxcpus=[max_cpu] \
-device virtio-net-pci,netdev=net0 \
-netdev tap,id=net0,ifname= [tap_name],script=no \
-boot d [img_name].img \
-daemonize
```

```bash
vncviewr localhost:5
```

Access to Container on NUC

```bash
docker start [container_name]
docker attach [container_name]
```

### Raspberry PI OS Installation

#### Download Required Package and File(In PI)

#### Edit HypriotOS setting and flash SD card.(In PI)

### Raspberry PI network Configuration

#### Check network setting(In PI)

#### Install required packages(In PI)

<!-- rdate 설치 추가할 것 -->
<!-- sudo apt install -y rdate -->
<!-- SSH 접속 가능하다 내용을 open-ssh 설치 이후로 이동 -->
```bash
ssh pirate@[PI_IP]
```

### Hostname Preparation

#### Hostname preparation for Kafka(In NUC)

Every machine which communicate with themselves must know
their own address. This information is stored in `/etc/hosts`.

```bash
sudo vim /etc/hosts
```

Add 2 lines below the file.

```text
[NUC_IP] [NUC_HOSTNAME]
[PI_IP] [PI_HOSTNAME]
```
<!-- 예시 이미지 -->

To check your hostname, you can use  `hostname` command.

```bash
hostname
```

<!-- 이 /etc/hosts도 재부팅 하면 사라지나 PI처럼? -->

#### Hostname preparation for Kafka(In PI)

Repeat the same job in Raspberry PI.

```bash
sudo vim /etc/hosts
```

Add 2 lines below the file.

```text
[NUC_IP] [NUC_HOSTNAME]
[PI_IP] [PI_HOSTNAME]
```
<!-- 예시 이미지 -->

#### Verification for hostname preparation

### Kafka Deployment(IN NUC)

#### Clone repository from GitHub

#### Check Dockerfile

#### Build docker image

#### Place docker containers

<!-- 슬라이드 28 세팅 여기로 -->

#### Zookeeper configuration

#### Broker configuration

#### Consumber topic configuration

### Flume on Raspberry PI(IN PI)

#### Install Net-SNMP installation

#### Clone repository from GitHub

#### Check Dockerfile

#### Build docker image

#### Run flume on container

### Consume message from brokers

<!-- 이미지 넣기 -->

## Review

### Lab Summary

1. How to physically inter-connect two kinds of Boxes? (NUC and Raspberry PI)
2. How to inter-connect data transfer (via Kafka messaging) between functions located in different boxes?

You need to distinguish physical Inter-connect from data Inter-connect!

> Thank You for Your Attention Any Questions? -> khs0404@smartx.kr
