# Lab#2. InterConnect Lab

# 0. Objective

The main part of interConnect Lab is to connect one box with another box which connects computer systems in 2 ways. (Physical interconnect, Data interconnect)

- Physical Interconnect: Connection between boxes via the network.
- Data Interconnect: By using physical Interconnect, connect data between various functions.

# 1. Concept

## 1-1. Raspberry Pi

![Raspberry Pi 4 Model B](./img/pi4-labelled.png)

The Raspberry Pi (hereinafter referred to as Pi) is a small embedded computer designed by the Raspberry Pi Foundation. Compared to general-purpose computers, Pi is relatively inexpensive but has simplified hardware configurations and properties.

For example, the RTC (Real-Time Clock) is removed by default, requiring the time to be manually set after each boot. (Typically, `ntp` or `rdate` is used to synchronize the time.) Therefore, in this lab, we will configure the Pi to automatically set the time using rdate and crontab after booting.

In this lab, we will use the [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/). This model is powered via USB Type-C and can connect to a display using Micro-HDMI. Data storage is handled via a Micro SD card, meaning that the OS is installed by downloading it onto the SD card. The Pi supports both WiFi and Gigabit Ethernet for networking, but we will use Ethernet for this lab.

## 1-2. Apache Kafka

![Why We use Kafka](./img/Apache_Kafka.png)

Apache Kafka, or Kafka is an open-source distributed event streaming platform capable of handling large-scale streaming data processing.

Streaming data refers to continuous and ongoing data generated from a data source. For example, a factory's temperature sensor continuously measures and transmits temperature data at regular intervals, while a CCTV system continuously sends captured video data. Such data is called streaming data.

Various systems continuously generate events, and multiple systems process these events. The process of extracting, transforming, processing, and delivering data from the source to its destination is defined as a data pipeline. Without a unified transmission method, diagnosing problems in a data pipeline requires checking all pipeline components, which increases the time needed for troubleshooting and system complexity. Additionally, different systems may use different data formats, making integration and expansion difficult.

Kafka was developed to address these issues by providing a unified transmission method that connects data sources and processing endpoints. Both data sources and processing systems only need to interact with Kafka, while administrators can centrally manage event and data flows through Kafka. This decouples data producers and consumers, allowing for easier expansion and increased reliability.

![Kafka Overview](./img/kafka.png)

Kafka follows the publish-subscribe (Pub/Sub) pattern, which can be likened to the relationship between YouTubers and subscribers. Consumers subscribe to specific topics they are interested in, while producers publish messages to these topics. The Kafka broker then enables consumers to retrieve messages from the topics they have subscribed to.

Below table is summary of the key members of Apache Kafka.

| Name       | Description                                                                                             |
| ---------- | :------------------------------------------------------------------------------------------------------ |
| `Producer` | A component that creates events and sends them to Kafka.                                                |
| `Consumer` | A component that subscribes to topics and fetches events from Kafka for processing.                     |
| `Topics`   | The unit of event subscription. Similar to folders in a file system, it is used to store/manage events. |
| `Broker`   | A component that stores and manages events. It distributes and replicates events stored in topics.      |

Apache Kafka is commonly used as a Messaging System, but unlike traditional messaging queues, Events do not disappear immediately when a Consumer reads them, and it can be read as many times as needed. Instead, Kafka manages events by defining the event's lifetime for each Topic.

Topics are managed by being divided into multiple partitions. If a single topic were stored in one location, a large number of producers and consumers would simultaneously access that single point in a short period in large-scale environments. This could lead to system failures and, ultimately, service outages. Therefore, topics are distributed and stored across multiple brokers' "buckets" (storage spaces) for efficient management.

In some cases, topic partitions are replicated across multiple brokers for high availability and fault tolerance. A leader is elected for each partition to handle requests related to that partition.

However, operating Kafka as a distributed system introduces various challenges, such as broker management, data synchronization between nodes, failure detection and handling, metadata and configuration management, and leader election. This is where `Apache Zookeeper` plays a key role.

Zookeeper continuously communicates with brokers to monitor their status. It manages Kafka's state information (such as the number of topics, partitions, and replications) and metadata (such as broker locations and leader information). Zookeeper determines the leader for each partition, detects broker failures, and facilitates data recovery and leader re-election when a failure occurs. These functionalities enable Kafka to function as a large-scale distributed system.

In this Lab, we will see that data-interconnects can be achieved by confirming that Apache Kafka delivers Pi events to NUC's Consumer.

> [!tip]
> If you want to know more about Apache Kafka, Please refer to [Apache Kafka Docs](https://kafka.apache.org/documentation/#intro_concepts_and_terms).

## 1-3. Net-SNMP

[Net-SNMP](http://www.net-snmp.org/) is a suite of applications that allows for monitoring network devices, computers, and small devices using the SNMP protocol on Linux operating systems.

Simple Network Management Protocol (SNMP) is an L7 protocol used to manage and monitor devices connected to IP networks, such as routers, switches, and load balancers, from a central management system.

![SNMP](./img/SNMP.png)

SNMP consists of the following key components:
![SNMP Enumeration](./img/snmp_enumeration.jpg)

| Component                        | Description                                                                                                                                                                                                                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SNMP Manager                     | Central system that monitors the network. Also known as the Network Management Station (NMS). SNMP Client in Host works as SNMP Manager.                                                                                                                                                                         |
| SNMP Agent                       | Collects, stores, and modifies system information in response to commands from the SNMP Manager. SNMP Server in Network device works as SNMP Agent.                                                                                                                                                              |
| Managed Device                   | A device with an SNMP agent installed that can be centrally managed via SNMP.                                                                                                                                                                                                                                    |
| MIB(Management Information Base) | stores network status information and settings of managed devices. consists of a total of eight categories (system, interface, address translation, IP, UDP, TCP, EGP, and ICMP). each MIB Object has unique OID(Object ID) (e.g. `1.3.6.1.2.1.2.2.1.16.2`: size of received bytes at the 2nd network interface) |

Net-SNMP is a suite of applications that allows for monitoring network devices, computers, and small devices using the SNMP protocol on Linux operating systems.

Net-SNMP includes tools that enable both SNMP Manager and SNMP Agent roles on Linux systems. It provides several CLI tools (`snmpget`, `snmptable`, ...) to send SNMP requests to agents, daemon applications (e.g., `snmpd`, ...) to act as SNMP agents, and additional libraries for further SNMP-related operations.

![Net-SNMP](./img/NetSNMP.png)

In this lab, we will install `snmpd` on the Pi and use Apache Flume to collect the Pi's network interface status and system information (such as available RAM, CPU load, and available disk space). In this setup, the Pi acts as the Managed Device, `snmpd` acts as the SNMP Agent, and Flume functions as the SNMP Manager.

> [!note]
> The system information to be collected is defined in the `flume-conf.properties` file under `agent.sources.sources1.oidN` during the Flume deployment.

<!-- -->

> [!tip]  
> For more details on SNMP, refer to [GeeksForGeeks](https://www.geeksforgeeks.org/simple-network-management-protocol-snmp/).

## 1-4. Fluentd

Fluentd is an open-source data collection tool that collects, converts, and transmits log and event data from a variety of sources. Written in Ruby, it features a lightweight and plug-in-based flexible structure. It is a graduation project from the Cloud Native Computing Foundation (CNCF), widely used in cloud native environments.

Fluent's Data Flow Model is shown in the figure below and consists of three main elements.

![Fluentd](./img/fluentd.png)

| Component      | Description                                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Input / Filter | Collect, Convert, and Filter Data from external systems or command execution results. It supports various methods such as file, HTTP, and command execution ('exec') etc.   |
| Output         | Transmit the processed Data to an external system (Kafka, Elasticsearch, S3, etc.).       |
| Buffer         | Buffer data safely with stage (chunk load) and queue structures. Reliable data delivery is guaranteed by transmitting it in chunks. |

Fluentd is used to periodically collect the status information from 'snmpd' and deliver it to Kafka. The 'snmpget' command collects the status information with SNMP, processes it in JSON format, and sends it to Kafka Topic.

> [!tip]
>If you would like to know more about Fluentd, please refer to [Fluentd Docs] (https://docs.fluentd.org/) .

# 2. Practice

![overview](img/overview.png)

> [!note]
>
> If you encounter internet connectivity issues on the box despite a working gateway connection, update the DNS settings in /etc/resolv.conf as follows:
>
> ```bash
> sudo vim /etc/resolv.conf
> ```
>
> ```text
> ...
> # operation for /etc/resolv.conf
> nameserver 203.237.32.100
> ```
>
> After every boot, the content of `/etc/resolv.conf` is gone, you should do the above steps again.

## 2-1. Raspberry PI OS Installation

> [!warning]
>
> To prevent IP conflict, if VM and Docker Container are running, please turn off both.
>
> ```bash
> sudo docker stop <container_name>
> sudo killall -9 qemu-system-x86_64  # if can not kill it, use sudo killall -9 kvm
> ```

Now we will install HypriotOS on the Raspberry Pi. HypriotOS is a Debian-based operating system optimized for running Docker on Raspberry Pi. The OS is pre-configured with Docker and is optimized from the kernel to filesystem levels, for Docker. (For more details, please refer to [Hypriot Blog](https://blog.hypriot.com/about/#hypriotos:6083a88ee3411b0d17ce02d738f69d47).)

To install HypriotOS, insert the Micro SD card into a reader, and insert into the NUC.

> [!caution]
>
> **Please ensure that the Pi is <ins>completely powered off</ins>** before removing the SD card.
>
> Raspberry Pi uses SD card as a storage device.  
> If you remove it before power-off, Potential Data Corruption can occur, which causes critical, fatal error on operation.
>
> Therefore, please check whether Pi is completely powered off, and remove SD card safely.
>
> ```bash
> sudo poweroff
> ```
>
> 📰️️ Note: `sudo` is used to execute command as a `root`(admin). Only `root` can execute `poweroff`.

### 2-1-1. (NUC) Download Required Package and File

[`flash`](https://github.com/hypriot/flash) is a script that flash SD Card. We will use `flash` to install HypriotOS on SD Card. Please install `flash` following the guidance below.

```bash
cd ~
sudo apt update && sudo apt install -y pv curl python3-pip unzip hdparm python3.12-venv
python3 -m venv ~/.venv
source .venv/bin/activate
pip3 install awscli
curl -O https://raw.githubusercontent.com/hypriot/flash/master/flash
chmod +x flash
sudo mv flash /usr/local/bin/flash
```

<details>
<summary> 📰️ Note: Dependency of `flash` </summary>

For more information, please refer to <https://github.com/hypriot/flash>.

> |     Tool      | Description                               |
> | :-----------: | :---------------------------------------- |
> |     `pv`      | Showing progress bar.                     |
> |   `awscli`    | download image from AWS S3 Bucket         |
> | `python3-pip` | to install/execute `awscli`               |
> |    `curl`     | download image from web server, using URL |
> |    `unzip`    | unzip compressed image.                   |
> |   `hdparm`    | use to flash SD Card images               |

</details>

<details>
<summary> Package Version (Refer this when dependency error occurs) (Expand)</summary>

#### NUC flash dependencies

|   Package   |      Version       |
| :---------: | :----------------: |
|     pv      |      1.6.6-1       |
|    curl     | 7.68.0-1ubuntu2.15 |
| python3-pip | 20.0.2-5ubuntu1.7  |
|    unzip    |  6.0-25ubuntu1.1   |
|   hdparm    |     9.58+ds-4      |

#### Python flash dependencies

| Package | Version |
| :-----: | :-----: |
| awscli  | 1.27.59 |

</details>

`flash` delivers configuration files to `cloud-init`, to configure Network, create user account, and SSH, etc. To download pre-configured files, We will clone Github Repository.

Since there are some large files, first we will add `git-lfs`, then clone repository, at last move to next working directory. Please follow guidance below.

```bash
cd ~
sudo apt install -y git
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install -y git-lfs
git lfs install
git clone --depth=1 https://github.com/SmartX-Labs/SmartX-Mini.git
cd ~/SmartX-Mini/SmartX-Mini-2026/Experiment/Lab-2.\ InterConnect/deploy/hypriotos
```

<details>
<summary>Package Versions (Expand)</summary>

#### NUC git-lfs package versions

| Package |       Version       |
| :-----: | :-----------------: |
|   git   | 1:2.25.1-1ubuntu3.8 |
| git-lfs |        3.3.0        |

</details>

Next, download HypriotOS(v1.12.3) image file.

```bash
wget https://github.com/hypriot/image-builder-rpi/releases/download/v1.12.3/hypriotos-rpi-v1.12.3.img.zip
ls -alh # Check all files
```

### 2-1-2. (NUC) Edit Configuration of HypriotOS

`network-config` file is used to configure network setting. Now we will open and edit this file to configure.

> [!caution]
>
> **<ins>Do not change the name</ins> of `network-config` file.**  
> `network-config` is the pre-defined file name, which is used by `cloud-init` to configure network setting during booting. (HypriotOS is managed by `cloud-init`)  
> So, `cloud-init` always try to find `network-config` file at the root directory of local file system mainly. (You can figure out where is root directory, by executing `lsblk` or something.)
>
> `flash` will copy it to `/boot`(actually boot partition) of SD Card, but file name does not be changed.
>
> If you change the name of `network-config`, then `cloud-init` cannot find that file, which results in failure of network configuration. (i.e. default network setting will be applied.) In that case, you should re-install OS or manually configure network setting.
>
> So, warning again, <ins>**Do not change the file name.**</ins>
>
> REF: <https://cloudinit.readthedocs.io/en/stable/reference/datasources/nocloud.html#source-files>

<!-- -->

> [!note]
>
> Topic: What is `cloud-init`, and How it initializes the OS
>
> `cloud-init` is a tool used to initialize cloud instances. It is widely utilized by public cloud providers such as AWS and Google Cloud, as well as for provisioning private cloud infrastructure and installing bare-metal systems.
>
> During the boot sequence, `cloud-init` performs initialization in two main phases: Early-boot and Late-boot.
>
> In the **Early-boot** phase, it identifies the data source and applies configuration settings, including network configuration. First, it identifies the data source required for instance initialization based on system defaults. (The data source is the location containing the configuration information needed for instance initialization.) For public cloud providers, this data source is usually provided by an external server. For bare-metal systems (referred to as `NoCloud`), cloud-init searches for configuration files within the root directories of the local file system, such as `/` or `/boot` (these directories can be identified using the `lsblk` command).
>
> After identifying the data source, cloud-init retrieves multiple configuration files from it. It uses `meta-data` to identify instance-specific information such as the Instance ID and platform details. Through `user-data` (or `vendor-data` for public clouds), it applies configuration settings, including hardware optimizations, hostname assignments, the management of various configuration files, default user account setup, and user-defined script execution. Additionally, the `network-config` file provides the network interface settings.
>
> In the **Late-boot** phase, `cloud-init` handles tasks that are less critical for the initial boot. This phase typically uses values defined in the `user-data` or `vendor-data` files.
>
> During this phase, tools like `Ansible` or `Chef` can be used to perform fine-grained system configurations. It may also download essential software for system operation, create and configure user accounts, and execute various scripts as specified in `user-data` or `vendor-data`.
>
> Once these processes are complete, the system is fully initialized and ready for user access.
>
> REF1: <https://cloudinit.readthedocs.io/en/latest/explanation/introduction.html>  
> REF2: <https://cloudinit.readthedocs.io/en/stable/reference/datasources/nocloud.html>

```bash
pwd # check working directory is "SmartX-Mini/SmartX-Mini-2026/Experiment/Lab-2. InterConnect/deploy/hypriotos"
vim network-config
```

In the `network-config` file, `ethernet.eth0` represents the configuration for the Pi's `eth0` interface. This section specifies the IP address, DNS address, and gateway address for the Pi.

We will modify the `ethernet.eth0.addresses` field to assign an IP address to the Pi and adjust `ethernet.eth0.nameservers.addresses` to specify the DNS server. (The `ethernet.eth0.gateway4` field defines the IPv4 gateway, which should remain unchanged unless explicitly instructed.)

```yaml
…
    addresses:
      - 172.29.0.xxx/24 # change xxx to your pi address!
    gateway4: 172.29.0.254
    nameservers:
      addresses: [203.237.32.100, 203.237.32.101] # write your DNS servers
…
```

These network settings will be automatically applied during the Pi's boot process through `cloud-init`.

### 2-1-3. (NUC) Flash SD Card for HypriotOS Install

To install HypriotOS onto the SD card, we first need to identify where the SD card is mounted. We will use the `fdisk` command to locate a partition that matches the SD card's size.

SD cards are typically mounted under paths starting with `/dev/sd`. For a 32GB SD card, the size will be displayed as approximately 29.8 GiB, while a 16GB card will appear as approximately 14.6 GiB. Identify the corresponding device path based on these values. (In the image below, the SD card is mounted at `/dev/sdc`.)

```bash
sudo fdisk -l
```

![result of fdisk](./img/fdisk.png)

Once identified, use the following command to install HypriotOS onto the SD card. Wait until the process is complete and verify that the "Finished" message is displayed. If the process terminates prematurely or this message does not appear, the installation may not have been successfully applied.

```bash
flash -u hypriotos-init.yaml -F network-config -d <Your SD Card Directory> hypriotos-rpi-v1.12.3.img.zip
```

> [!tip]
>
> Table below describes options for `flash`. Details are shown by `flash --help`.
>
> | Options                          | Description                                                  |
> | :------------------------------- | :----------------------------------------------------------- |
> | `-u <file>`, `--userdata <file>` | select file which will be copied to `/boot/user-data` of OS. |
> | `-F <file>`, `--file <file>`     | select file which will be copied to `/boot` of OS.           |
> | `-d <path>`, `--device`          | Path of Device which where OS be installed.                  |
> | `~.img`, `~.img.zip`             | Raspberry OS Image File                                      |

<!-- -->

> [!note]
>
> Topic: How to resolve `BLKRRPART failed: Device or resource busy` error
>
> If this error occurs, the OS is installed successfully, but the `hypriotos-init.yaml` and `network-config` files are not copied to the SD card.
>
> Try the following steps one by one to resolve the error:
> **<ins>If you do not encounter this error, Do not apply those steps.</ins>**
>
> 1. If the SD card is mounted at `/dev/sda`, manually copy `hypriotos-init.yaml` as `user-data` to `/dev/sda1` and also copy `network-config` to the same location. Perform the following commands to do this:
>
>    ```bash
>    # Open terminal in NUC
>    sudo mkdir /mnt/sdcard
>    sudo mount /dev/sda1 /mnt/sdcard
>    sudo cp hypriotos-init.yaml /mnt/sdcard/user-data
>    sudo cp network-config /mnt/sdcard/network-config
>    sudo umount /mnt/sdcard
>    sudo eject /dev/sda
>    # remove SD card from NUC
>    ```
>
>    Then, eject the SD card from the NUC, insert it into the Pi, and power on the Pi. Verify that the network and hostname settings are correctly applied, by following `2-2-1`. if configuration is not applied, then move to step 2.
>
> 2. Run the `flash -u hypriotos-init.yaml -F network-config -d <Your SD Card Directory> hypriotos-rpi-v1.12.3.img.zip` command again to reinstall HypriotOS. Sometimes temporary error can be occurred.
> 3. Delete all partitions on the SD card and try the `flash -u hypriotos-init.yaml -F network-config -d <Your SD Card Directory> hypriotos-rpi-v1.12.3.img.zip` again. You can delete the partitions using the following commands:
>
>    ```bash
>    sudo umount <sd_card_path>
>    sudo fdisk <sd_card_path>
>    d   # enter this repetitively unless every partitions are removed.
>    w   # save changes
>    ```

<!-- -->

> [!note]
>
> Topic: About the `hypriotos-init.yaml` file
>
> The `hypriotos-init.yaml` file is used as the `/boot/user-data` file on HypriotOS.  
> The `/boot/user-data` file provides user-defined configurations to the instance during initialization. It defines user creation, hostname settings, and whether to automatically initialize `/etc/hosts`.  
> This file also contains the initial user credentials, so if you forget the ID/PW, refer to this file.
>
> REF: <https://cloudinit.readthedocs.io/en/stable/explanation/format.html>

## 2-2. Raspberry PI Environment Setup

### 2-2-1. (PI) Check Network Configuration

Now, eject the SD card, insert it into the Pi, and power it on. 

HypriotOS has SSH server enabled by default, so from now on, you can access Pi from the NUC's terminal via SSH. From the NUC's terminal, enter the following command to access Pi. The default login credentials are (ID: `pi`, Password: `1234`).

```bash
ssh pi@<PI_IP>
```

First, verify that the network interface is configured correctly by entering the following command in the shell:

```bash
ifconfig
```

Next, check the routing table using the following command:

```bash
netstat -rn
```

### 2-2-2. (PI) Install Package

To proceed with the lab, install the following packages on the Pi:

```bash
sudo apt update
sudo apt install -y git vim rdate openssh-server
```

|     Package      | Description                                                   |
| :--------------: | ------------------------------------------------------------- |
|      `git`       | Git CLI tool                                                  |
|      `vim`       | Text editor                                                   |
|     `rdate`      | Tool to synchronize system time with an external time server. |
| `openssh-server` | Package to enable SSH server functionality on the Pi.         |

<!-- TODO: mismatch with korean version -->

Once the package installation is complete, <ins>**return to the NUC**</ins>. Ensure that the <ins>**Pi remains powered on**</ins>, as you will access it via SSH from the NUC.

> [!note]
>
> Topic: Resolving `Certificate verification failed: The certificate is NOT Trusted` error
>
> If you encounter certificate verification errors while installing packages due to a repository issue, you need to switch to another APT repository.
>
> To modify the APT repository, open the /etc/apt/sources.list file using an editor (e.g., nano or vi):
>
> ```bash
> sudo nano /etc/apt/sources.list
> ```
>
> Replace the URL in the first line (e.g., <http://ftp.lanet.kr/raspbian/>) with an alternative mirror, such as <http://ftp.kaist.ac.kr/raspbian/raspbian/>.
>
> Save the changes and retry the package installation process.

<details>
<summary>Package Versions (Expand)</summary>

#### PI initial dependencies

|    Package     |         Version         |
| :------------: | :---------------------: |
|      git       |   1:2.20.1-2+deb10u7    |
|      vim       |  2:8.1.0875-5+deb10u4   |
|     rdate      |         1:1.2-6         |
| openssh-server | 1:7.9p1-10+deb10u2+rpt1 |

</details>

### 2-2-3. (PI) Configuring `crontab` for Time Synchronization

Since the Raspberry Pi lacks an RTC (Real-Time Clock), it can only maintain system time for about 17 minutes after being powered off.  
To synchronize the system time after booting, we will configure `crontab` to execute the `rdate` command 1 minute after the boot process is complete.

First, modify the `crontab` settings using the following command:

```bash
sudo crontab -e
```

If this is your first time editing crontab, you will be prompted to select a text editor.  
Choose your preferred editor and add the following line to the bottom of the configuration file (excluding comments):

![crontab editor](./img/crontab_editor_selection.png)

```bash
# Run `rdate' to synchronize the time 60 seconds after boot
@reboot sleep 60 && rdate -s time.bora.net
```

<!-- 시각이 맞춰지는데 60초 정도 걸리기 때문에 별로 쓰고 싶지는 않았는데, 부팅 마지막에 실행되는 `rc.local` 의 경우, After=network-online.target(네트워크가 다 켜진 다음 rc.local 실행)을 지정해도 DNS 에러가 뜨고(부팅 후에 같은 커맨드 쓰면 안 뜸), crontab 같은 경우에도 저 60초 정도 기다리지 않으면 DNS 에러가 발생했습니다. 60초는 짧긴 하지만 그래도 이 사이에 시계가 정확해야 하는 일 실행해서 오류가 난다면 아래 수동으로 시간 맞추는 커맨드를 입력하라 합시다.-->

Save the changes and restart the Pi using the following command:

```bash
sudo reboot
```

### 2-2-4. (NUC) Check Pi Setup

Since `openssh-server` has been installed on the Pi, you can now access the Pi via SSH from external devices.  
(From now on, there's no need to repetitively unplug and plug in the monitor, and keyboard. You can access the Pi via SSH from the NUC.)

To verify this, I will access the Pi via SSH from the terminal on the NUC.  
Return to the NUC and enter the following command:

```bash
ssh pi@<PI_IP>  # Simple Format: ssh <ID>@<destination IP or Hostname>
```

> [!note]
>
> Topic: SSH - Fingerprint Error
>
> ![ssh key error](./img/ssh_duplicated.png)
>
> This error occurs when the SSH key associated with the target IP address differs from the key of the SSH server you are trying to access. (e.g. re-install `openssh-server`)
>
> Each SSH server has a unique SSH key.  
> When an SSH client connects to a server, the server's key is shared with the client, which then stores the key and IP address in the `~/.ssh/known_hosts` file.  
> (The image below illustrates this process.)
>
> ![ssh initial access](./img/ssh_initial_access.png)
>
> When the client try to reconnects to the server, it uses the stored key in `~/.ssh/known_hosts` to verify that the server is the same one previously accessed. This mechanism helps prevent man-in-the-middle attacks.  
> If the SSH key of the server has changed, verification will be failed and `ssh` will produce an error and terminate the connection.
>
> To resolve this error, remove the previous fingerprint using the following command and then try reconnecting via SSH:
>
> ```bash
> ssh-keygen -f "/home/$(whoami)/.ssh/known_hosts" -R "<PI_IP_ADDRESS>"
> ```

Next, please check the system time by entering a commend below:

```bash
date
```

If the system time is still incorrect after rebooting, you can manually synchronize it using the command below:

```bash
sudo rdate -s time.bora.net
```

## 2-3. Hostname Configuration

Every device connected to a network is identified and communicates using a unique IP address.

However, remembering IP addresses is impractical, especially in environments where IPs change dynamically due to DHCP, cloud infrastructure, or Kubernetes pods and services. This makes direct communication using IP addresses inconvenient and inefficient.

To address this, devices are typically assigned "hostnames"—user-friendly names for easier communication. Similar to how a URL is resolved to an IP address through DNS, the `/etc/hosts` file on the Pi allows the OS to map hostnames to IP addresses.

For example, if the Pi tries to access NUC using hostname `nuc`, the OS will reference the `/etc/hosts` file and translate `nuc` to the actual IP address of the NUC. This allows the Pi to interact with the NUC using the hostname instead of the IP address.

In short, the `/etc/hosts` file links hostnames to actual IP addresses. Even if a service's IP address changes, updating the corresponding entry in `/etc/hosts` ensures uninterrupted communication.

Subsequent steps in the lab will also use hostnames rather than IP addresses for interaction.

### 2-3-1. (NUC) Hostname preparation for Kafka

First, check the hostname of the NUC using the following command:

```bash
hostname
```

Next, open the `/etc/hosts` file using a text editor.

```bash
sudo vim /etc/hosts
```

Add the following line(Pi IP Address & Hostname) at the bottom of the file:

<!--
  Modify to write Pi IP only.
  REF: Issue #98
-->

```text
172.29.0.XX        <PI_HOSTNAME>
```

> [!Caution]
>
> The hostnames of the Pi and NUC entered in `/etc/hosts` <ins>**must match their actual hostnames.**</ins>
>
> If they do not match, issues may arise during the upcoming Kafka practice sessions.

<!-- -->

> [!note]
>
> Topic: How to change Hostname (⚠️Warning⚠️: Applying this during lab is <ins>**not recommended.**</ins>)
>
> You can change the NUC's hostname using the following commands:
>
> **Temporary change (reverts after reboot):**
>
> ```bash
> sudo hostname <new_name>
> ```
>
> **Permanent change:**
>
> ```bash
> # Change Permanently
> sudo hostnamectl set-hostname <new_name>
> ```
>
> After changing the hostname, ensure you update the NUC's hostname entry in the `/etc/hosts` file.
>
> On the Pi, additional steps are required for permanent changes due to `cloud-init`  
> For more details, refer to: <https://repost.aws/ko/knowledge-center/linux-static-hostname-rhel7-centos7>

### 2-3-2. (PI) Hostname preparation for Kafka

Perform the same steps on the Pi that were done on the NUC in section 2-3-1. Open the `/etc/hosts` file and add the following line(NUC IP Address & Hostname).

```bash
sudo vim /etc/hosts
```

<!--
  Modify to write NUC IP only.
  REF: Issue #98
-->

```text
172.29.0.XX        <NUC_HOSTNAME>
```

> [!warning]
>
> The `/etc/hosts` file on the Pi is reset during boot due to cloud-init.  
> If you want to preserve these settings after reboot, follow the guidelines below.

<!-- -->

> [!tip]
>
> Topic: How to Preserve `/etc/hosts` on the Pi
>
> cloud-init regenerates the /etc/hosts file during boot using a predefined hosts template.  
> Any manual modifications will be overwritten.
>
> To make permanent changes, you can use one of the following three methods:
>
> 1. Modify the `manage_etc_hosts` value to `false` in the `hypriotos-init.yaml` file used during OS installation and reinstall the OS.
> 2. Edit the `/etc/cloud/templates/hosts.debian.tmpl` file on the Pi with the same modifications made to `/etc/hosts`.
> 3. Comment out the `update_etc_hosts` module in `/etc/cloud/cloud.cfg`. This module is responsible for regenerating `/etc/hosts`.

<!-- 2025.02.27: 이유는 모르겠지만 HypriotOS 내부에서 /boot/user-data를 직접 수정해도 Data가 날아감. 아마 cloud-init을 제대로 이해하지 못했기 때문이라고 생각한다. 추후에 근본 원인을 찾아낸다면 수정을 부탁한다. -->

### 2-3-3. (PI, NUC) Verifying Hostname-based Communication

From the NUC, verify that hostname-based communication is working correctly:

```bash
sudo ping <Your NUC hostname>
sudo ping <Your Raspberry PI hostname>
```

From the Pi, perform the same verification:

```bash
sudo ping <Your NUC hostname>
sudo ping <Your Raspberry PI hostname>
```

Successful communication should display ICMP packet responses. If you encounter errors like "Non-Reachable," check the network configuration and `/etc/hosts` entries on both devices. Similar output should be visible on both the Pi and the NUC.

![ping from pi](./img/ping_from_pi.png)

## 2-4. (NUC) Kafka Deployment

Now that NUC and Pi can communicate normally using Hostname, we will deploy Apache Kafka through Docker to configure an environment where NUC and Pi can exchange messages. (Of the two interconnects, they are Data Interconnects.)

In this exercise, Apache Kafka 4.2.0 is placed in KRaft mode. In KRaft mode, without the traditional Zookeeper, the controller is directly responsible for managing the cluster metadata. Three Controllers and three Brokers are placed in the NUC as Docker Compose, which all share the Host network.

| Container Name |    Role    | Node ID | Listening Port |
| :------------: | :--------: | :-----: | :------------: |
|  controller0   | Controller |    0    |     19090      |
|  controller1   | Controller |    1    |     19091      |
|  controller2   | Controller |    2    |     19092      |
|    broker0     |   Broker   |    3    |      9090      |
|    broker1     |   Broker   |    4    |      9091      |
|    broker2     |   Broker   |    5    |      9092      |

### 2-4-1. (NUC) Directory Movement and Check Dockerfile 

First, move to the directory that you want to use for the Kafka placement.

```bash
cd ~/SmartX-Mini/SmartX-Mini-2026/Experiment/'Lab-2. InterConnect'/deploy/kafka
```

Check that the 'Dockerfile' in the directory is the same as the bottom.

```dockerfile
FROM ubuntu:24.04

RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list.d/ubuntu.sources

RUN apt-get update && apt-get install -y wget openjdk-21-jdk-headless && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q https://downloads.apache.org/kafka/4.2.0/kafka_2.13-4.2.0.tgz -O - | tar -zxv && \
    mv kafka_2.13-4.2.0 /kafka

WORKDIR /kafka

COPY start-kafka.sh /kafka/start-kafka.sh
RUN chmod +x /kafka/start-kafka.sh
```

> [!tip]
>
> Note: Change APT Repository (Optional)
>
> It takes a lot of time to download the package through 'apt' during the image file build process.
>
> The closer you are locally, the higher the download speed is generally, but the default repository is usually overseas and slow. Therefore, we use mirror servers in local locations to improve the speed.
>
> This setting is done through 'sed' at the bottom of the Dockerfile command. For now, you can modify it to point to Kakao's mirror server, but if you want to use another server, you can modify the address of 'mirror.kakao.com ' to another value (Lanet, KAIST mirror server, etc.).
>
> ```dockerfile
> …
>
> RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list
> #Update & Install wget
> RUN sudo apt-get update
> RUN sudo apt-get install -y wget vim iputils-ping net-tools iproute2 dnsutils openjdk-7-jdk
>
> RUN sed -i 's@archive.ubuntu.com@mirror.kakao.com@g' /etc/apt/sources.list.d/ubuntu.sources
> RUN apt-get update && apt-get install -y wget openjdk-21-jdk-headless
> …
> ```

### 2-4-2. (NUC) Build Docker Image 

Build the 'ubuntu-kafka' image by entering the following command.

```bash
sudo docker build -t ubuntu-kafka .
```

> [!tip]
>
> Note: Basic Docker CLI Commands
>
> The following are common Docker CLI commands that you can use to manage containers:
>
> For more information, Please refer to [Docker Official Document](https://docs.docker.com/engine/reference/commandline/cli/).
>
> | Command                             | Description                                                 |
> | ----------------------------------- | ----------------------------------------------------------- |
> | `sudo docker --help`                | Displays available Docker CLI commands and options.         |
> | `sudo docker ps`                    | Lists running containers. Use `-a` to include stopped ones. |
> | `sudo docker rm <container_id>`     | Removes a Docker container.                                 |
> | `sudo docker start <container_id>`  | Starts a stopped Docker container.                          |
> | `sudo docker stop <container_id>`   | Stops a running Docker container.                           |
> | `sudo docker attach <container_id>` | Attaches to a running Docker container.                     |
> | `sudo docker run <options> <image>` | Creates and starts a container from the specified image.    |
>
> You can use the first 4 characters of the container ID shown by `docker ps` as `<container id>`, as long as they are unique.

### 2-4-3. (NUC) Create environment variable file ('.env')

Before running Docker Compose, write the environment variables required to set up the cluster in the `.env` file.

First, create a `CLUSTER_ID` that identifies the entire cluster.

```bash
sudo docker run --rm ubuntu-kafka bin/kafka-storage.sh random-uuid
# Output Example: MkU3OEVBNTcwNTJENDM2Qg
```

Next, create three Voter UUIDs that identify each Controller.

```bash
sudo docker run --rm ubuntu-kafka bin/kafka-storage.sh random-uuid  # CONTROLLER0_UUID
sudo docker run --rm ubuntu-kafka bin/kafka-storage.sh random-uuid  # CONTROLLER1_UUID
sudo docker run --rm ubuntu-kafka bin/kafka-storage.sh random-uuid  # CONTROLLER2_UUID
```

> [!note]
>
>`CLUSTER_ID` is the value that identifies the entire cluster, and Voter UUID is the value that identifies each Controller node. Both must be unique and cannot be changed after being formatted.

Create a `.env` file using the value you created. You can write it by referring to the `.env.example` file.

```bash
cp .env.example .env
vim .env
```

```text
CLUSTER_ID=<CLUSTER_ID generated above>
CONTROLLER0_UUID=<CONTROLLER0_UUID generated above>
CONTROLLER1_UUID=<CONTROLLER1_UUID generated above>
CONTROLLER2_UUID=<CONTROLLER2_UUID generated above>
HOST_HOSTNAME=<hostname of NUC>
```

You can check `<hostname of nuc>` by the following command.

```bash
hostname
```

### 2-4-4. (NUC) Run the cluster with Docker Compose

Run the Kafka cluster by the following command.

```bash
sudo docker compose up -d
```

Verify that all containers are running normally.

```bash
sudo docker ps
```

> [!note]
>
> **Role of `start-kafka.sh`**
>
> Inject the environment variable settings written in `docker-compose.yml` into the container, automatically create a setting file for each node's role (controller/broker), and start Kafka.

<!-- -->

> [!tip]
>
> If you restart the practice, you must delete the remaining log directory from the previous run before it is reformatted normally.
>
> ```bash
> sudo rm -rf /tmp/kraft-controller*-logs /tmp/kraft-broker*-logs
> sudo docker compose up -d
> ```

### 2-4-5. (NUC) Generate & Check Topic

After the Kafka cluster runs normally, a Topic called `resource` is created. Topic creation is done through the running `broker0` container.

```bash
sudo docker exec broker0 /kafka/bin/kafka-topics.sh --create \
  --bootstrap-server localhost:9090 \
  --replication-factor 3 \
  --partitions 3 \
  --topic resource
```

Check that Topic has been created successfully.

```bash
sudo docker exec broker0 /kafka/bin/kafka-topics.sh --list \
  --bootstrap-server localhost:9090
```

## 2-5. (PI) Fluentd on Raspberry PI

### 2-5-1. (PI) Install Net-SNMP 

Now return to Pi and install the 'Net-SNMP' package by following command.

```bash
sudo apt update
sudo apt install -y snmp snmpd snmp-mibs-downloader
```

<details>
<summary>Package Versions (Expand)</summary>

#### PI snmp dependencies

|       Package        |       Version        |
| :------------------: | :------------------: |
|         snmp         | 5.7.3+dfsg-5+deb10u4 |
|        snmpd         | 5.7.3+dfsg-5+deb10u4 |
| snmp-mibs-downloader |         1.2          |

</details>

To modify the settings file, Open the file with the editor to find '#rocommunity public localhost' and remove '#'.

```bash
sudo vim /etc/snmp/snmpd.conf
```

Restart 'snmpd.service' by the following command to reflect the configuration file.

```bash
sudo systemctl restart snmpd.service
```

### 2-5-2. (NUC) Cross-build Fluent image 

Because Fluentd images are large and time consuming to build, they are cross-built in NUC and sent to Pi instead of building directly in Pi.

Pi (ARMv7) and NUC (x86_64) have different architectures, so install QEMU first to run ARM binaries in NUC. (Do it only once for the first time.)

```bash
sudo apt-get install -y qemu-user-static
sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

Next, Move to the Fluentd directory and modify the hostname of the NUC in `fluent.conf`.

```bash
cd ~/SmartX-Mini/SmartX-Mini-2026/Experiment/'Lab-2. InterConnect'/deploy/fluentd
vim fluent.conf
```

Modify `<YOUR_NUC_HOSTNAME>` in the file to the NUC Hostname recorded in Pi's `/etc/hosts`.

```text
...
brokers <Your NUC hostname>:9090,<Your NUC hostname>:9091,<Your NUC hostname>:9092
...
```

Build an image for arm/v7 by `buildx`.

```bash
sudo docker buildx build \
  --platform linux/arm/v7 \
  --tag pi-fluentd \
  --output type=docker \
  .
```

Save the built image as a tar file and send it to Pi.

```bash
sudo docker save pi-fluentd | gzip > pi-fluentd.tar.gz
scp pi-fluentd.tar.gz pi@<PI_IP>:~/
```

### 2-5-3. (PI) Load images and run Fluentd

Load the image received in Pi.

```bash
sudo docker load < ~/pi-fluentd.tar.gz
```

Run the Fluentd container by following command.

```bash
sudo docker run -it --rm \
  --net=host \
  --security-opt seccomp=unconfined \
  --name fluentd \
  pi-fluentd
```

> [!note]
>
> The `--security-opt seccomp=unconfirmed` option is required to bypass the issue of the seccomp policy blocking some system calls in HypriotOS kernel (4.19).

<!-- -->

> [!note]
>
> If errors occur, verify that the following three values are consistent:
>
> 1. The NUC hostname in the Pi's `/etc/hosts` file.
> 2. The broker hostname in `conf/flume-conf.properties` on the Pi.
> 3. The hostname of NUC (check with the `hostname` command).

## 2-6. (NUC - `consumer` Container) Consume message from brokers

Run the following script to check whether the Consumer container can receive messages sent by the Producer.

```bash
sudo docker run -it --rm \
  --network host \
  --name consumer \
  ubuntu-kafka \
  /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9090 \
    --topic resource \
    --from-beginning
```

If everything is configured correctly, you should see the message displayed in the `consumer` container.

![consumer result](./img/consumer%20result.png)

# 3. Review

## 3-1. Lab Summary

In this lab, we experienced interconnecting computer systems in two different ways.

Through steps `2-1` to `2-3`, you prepared for the physical interconnection of two computer systems and ultimately verified their ability to communicate with each other using `ping`. Through this process, we explored and experienced the concept of <ins>**Physical Interconnect**</ins>.

Afterward, multiple containers were deployed on the Box using Docker. In summary, from steps `2-4` to `2-6`, we confirmed that the SNMP data extracted by `Apache Flume` was transmitted through `Apache Kafka` and delivered to the Consumer. Through this, we verified that two functions (Producer ↔ Consumer) could interact and exchange data via Apache Kafka, allowing us to experience <ins>**Data Interconnect**</ins>.

## 3-2. Finale

Through this lab, we have answered the following two key questions:

1. How can heterogeneous devices (e.g., NUC and Pi) be physically interconnected?
2. How can we establish data transfer between two functions located on different devices (in this case, using Kafka messaging)?

By addressing these questions, you should now have a clear understanding of the difference between Physical Interconnect and Data Interconnect.

> [!important]
> Thank you for your effort and participation in this lab.  
> We appreciate your dedication!
