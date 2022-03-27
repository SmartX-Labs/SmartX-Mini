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

### Check `rc-local.service` Setting (In NUC)

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
<!-- http://realtechtalk.com/Debian_Ubuntu_Mint_rclocal_service_startup_error_solution_rclocalservice_Failed_at_step_EXEC_spawning_etcrclocal_Exec_format_error-2242-articles -->
If you get Exec format error, Open `/etc/rc.local` and check the first line is `#!/bin/sh -e` and the last line is `exit 0`.

```bash
sudo vim /etc/rc.local
```

```bash
#!/bin/sh -e
...
exit 0
```

Reboot your NUC

```bash
sudo reboot
```

### Raspberry PI OS Installation

Before we start, your Raspberry Pi must be ready with proper OS. In this lab, we will use “HypriotOS” Linux for it. Insert a Micro SD into your SD card reader and attach the reader to your NUC.

#### Download Required Package and File(In NUC)

Issue the commands below to get “flash” script for the OS setup. Then, issue `flash` command to see if it’s installed correctly.

```bash
sudo apt update && sudo apt install -y pv curl python3-pip unzip hdparm
sudo pip3 install awscli
curl -O https://raw.githubusercontent.com/hypriot/flash/master/flash
chmod +x flash
sudo mv flash /usr/local/bin/flash
```

After install `flash`, clone repository from Github. You need to install `git-lfs` first because this repository contains large files.

```bash
cd ~
sudo apt install -y git
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install -y git-lfs
git lfs install
git clone https://github.com/SmartX-Labs/SmartX-Mini.git
cd ~/SmartX-Mini/SmartX-Mini-MOOC\ Collection/Experiment/Lab-2.\ Inter-Connect/
```

Next, you need to download HypriotOS from GitHub

```bash
wget https://github.com/hypriot/image-builder-rpi/releases/download/v1.9.0/hypriotos-rpi-v1.9.0.img.zip
ls -alh # Check all files
```

#### Edit HypriotOS setting and flash SD card.(In NUC)

Edit HypriotOS configuration file for your Raspberry Pi. Open the `hypriotos-init.yaml` file and edit its network section.

```bash
sudo vim hypriotos-init.yaml
```

```yaml
…
 # static IP configuration:
      interface eth0
      static ip_address=172.29.0.250/24 # Write your Raspberry Pi address
      static routers=172.29.0.254 # Write your Gateway address
      static domain_name_servers=8.8.8.8 8.8.4.4 # Write your given DNS server
…
```

The assigned IP address will be automatically applied, when you’re initially booting your Raspberry Pi.

To flash your OS to SD card, you need to know where your card is mounted.

```bash
sudo fdisk -l
```

![result of fdisk](./img/fdisk.png)

Then flash HypriotOS to your MicroSD Card. This takes a while, wait for a moment.

```bash
flash –u hypriotos-init.yaml -d /dev/sdc –f hypriotos-rpi-v1.9.0.img.zip
```

Insert the SD card back to your Raspberry PI and boot it up.

### Raspberry PI network Configuration

#### Check network setting(In PI)

#### Install required packages(In PI)

<!-- rdate 설치 추가할 것 -->
<!-- sudo apt install -y rdate -->

After install SSH server, you can access your PI from other computer with SSH.

```bash
ssh pirate@[PI_IP] #ID:pirate PW: hypriot
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

#### Verification for hostname preparation(In PI, NUC)

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
