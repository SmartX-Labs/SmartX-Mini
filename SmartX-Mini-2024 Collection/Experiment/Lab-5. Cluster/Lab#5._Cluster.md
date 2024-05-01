# Lab#5. Cluster Lab

## 0. Objective

- In Lab1 Box Lab, we deployed virtual machine and docker container for deploy isolated applications in specific enviornment
- Kubernetes can automate deployment, scaling and management applications that containerized by docker. It is called container orchestrator.
- In this section, we combine 3 NUC machine with Kubernetes.
  - 1 Master -> NUC1
  - 2 Worker -> NUC2, NUC3
- On this cluster, we will install distributed storage system called ceph.
  - With similar concept with docker - kubernetes, Rook is open source cloud-native Ceph strogae orchestrator for K8S.

## 1. Concept

### 1-1. Docker Containers

![Docker Containers](img/1.png)

- **Docker** is an open platform for building, shipping and running distributed applications. It gives programmers, development teams and operations engineers the common toolbox they need to take advantage of the distributed and networked nature of modern applications.

### 1-2. Container Orchestration

![Container Orchestration](img/2.png)

- **Container orchestration** refers to the process of organizing the work of individual components and application layers.
- **Container orchestration engines** all allow users to control when containers start and stop, group them into clusters, and coordinate all of the processes that compose an application. Container orchestration tools allow users to guide container deployment and automate updates, health monitoring, and failover procedures.

### 1-3. Kubernetes

![](img/3.png)

- **Kubernetes** is an open-source system for automating deployment, scaling, and management of containerized applications.

#### 1-3-1. **Kubernetes** **Features**

- **Horizontal scaling**: Scale your application up and down with a simple command, with a UI, or automatically based on CPU usage.
- **Self-healing:** Restarts containers that fail, replaces and reschedules containers when nodes die, kills containers that don't respond to your user-defined health check, and doesn't advertise them to clients until they are ready to serve.
- **Service discovery and load balancing:** No need to modify your application to use an unfamiliar service discovery mechanism. Kubernetes gives containers their own IP addresses and a single DNS name for a set of containers, and can load-balance across them.
- **Storage Orchestration:** Automatically mount the storage system of your choice, whether from local storage, a public cloud provider

## 2. Lab Preparation

![Lab Preparation](img/7.png)

#### 2-1-2. From All NUCs

```shell
# From NUC 1 :
sudo hostname nuc01
# From NUC 2 :
sudo hostname nuc02
# From NUC 3 :
sudo hostname nuc03
```

From All NUCs

```shell
sudo vi /etc/hosts
```

From All NUCs change hostname in /etc/hostname

remove all insert nuc01 or nuc02 or nuc03 on each right NUC.

```shell
sudo vi /etc/hostname
```

```shell
sudo reboot
```

Append the following context into /etc/hosts :

```text
 127.0.0.1 localhost
 <IP Address of NUC 1>  nuc01
 <IP Address of NUC 2>  nuc02
 <IP Address of NUC 3>  nuc03
```

#### 2-1-2. Check Connectivity

```shell
# From NUC 1
ping nuc02
ping nuc03

# From NUC 2
ping nuc01
ping nuc03

# From NUC 3
ping nuc01
ping nuc02
```

#### 2-1-3. From NUC1

예시)  
<img width="116" alt="스크린샷 2022-05-24 오후 1 12 53" src="https://user-images.githubusercontent.com/65757344/169947428-3d028493-cf5e-4463-a9ea-d04f3bd56b99.png">  
**username은 netcs**이고  
hostname은 nuc01입니다!!!

**username is netcs**  
and hostname is nuc01!!!

```shell
# In new terminal
ssh <nuc2 username>@nuc02

# In another new terminal
ssh <nuc3 username>@nuc03
```

#### 2-1-4. Setting containerd

```bash
# For All NUCs
sudo apt-get update
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
```

#### 2-1-5. Reboot All NUC

```shell
# From All NUCs
sudo reboot
```

# 지금부터 NUC1 학생 자리에서 모든 작업을 시작합니다. NUC2, NUC3 학생은 NUC1자리로 가서 작업을 시작합니다.

# From now on, every thing goes with NUC1 student's seat. Students in NUC2, NUC3 should start work at NUC1 student's seat.

### 2-2. Preparations for Clustering

#### 2-2-1. Docker Version Check : Prerequisite for Kubernetes

- Check Docker Version : 19.03.11

```shell
# From All NUCs
docker version
```

# From NUC1

```shell
ssh <NUC2 username>@nuc02
ssh <NUC3 username>@nuc03
```

### 2-3. Kubernets Installation(For All NUCs)

![Kubernets Installation](img/8.png)

- NUC 1 : Master
- NUC 2 : Worker 1
- NUC 3 : Worker 2

#### 2-3-1. Swapoff

```shell
# From All NUCs
sudo swapoff -a
```

#### 2-3-2. Install Kubernetes

```shell
# From All NUCs
sudo apt-get update && sudo apt-get install -y apt-transport-https curl ipvsadm wget

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update

sudo apt install -y kubeadm=1.28.1-1.1 kubelet=1.28.1-1.1 kubectl=1.28.1-1.1
```

### 2-4. Kubernetes Configuration

#### 2-4-1. Kubernetes Master Setting(For NUC1)

지금부터 sudo su 로 root에서 실행합니다

```shell
# From NUC1
kubeadm init --pod-network-cidr=10.244.0.0/16

```

```shell
# From NUC1
# Cleanup Rook Configuration
 sudo rm -rf /var/lib/rook
 sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=all # 계속 실패한다면 이 명령어를 사용해 보세요
```

- kubeadm을 실행하면 아래와 같이 Kubernetes Cluster에 참여할 수 있는 토큰값이 발급됩니다.
- **토큰 정보를** 지금 입력하지 말고, 2-4-3 파트에서 사용하기 위해 **저장해둡니다.**
- You can get token value that can join Kubernetes Cluster like below when you execute kubeadm.
- Please don't enter **token information** right now, but **save** it to use at part 2-4-3.
- if you failed here. please check port-port forwarding refer to https://kubernetes.io/docs/reference/networking/ports-and-protocols/ (ubuntu uses ufw as the default firewall.)
  ![commnad](img/9.png)

```shell
# From NUC1
## make kubectl work for your non-root user.
rm -r $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl taint nodes --all node-role.kubernetes.io/master- # taint에서 포드를 스케쥴링 할 수 없는 경우 사용합니다
```

#### 2-4-2. Kubernetes Worker Setting(For NUC2, NUC3) [최초 진행 시에는 사용하지 않아도 됩니다!]

```shell
# From NUC2, NUC3
# sudo kubeadm reset -f
# sudo rm -r /etc/cni/net.d
# sudo ipvsadm --clear

```

#### 2-4-3. Worker Join

- 2-4-1 파트에서 발급받은 토큰 정보를 가져옵니다.
- Bring your token information you got at part 2-4-1.
- Master에서 발급받은 토큰을 NUC2, NUC3에 입력해줍니다. 커맨드는 아래와 같이 구성되어 있습니다.
- Enter token from Master to NUC2, NUC3. Command is consists of like following.
  1. sudo
  2. kubeadm join <NUC1 IP>:6443 --token <YOUR TOKEN> --discovery-token-ca-cert-hash <YOUR HASH>
  3. --ignore-preflight-errors=all

![commnad](img/9.png)

```shell
## NUC1에 NUC2, NUC3를 추가하여 클러스터를 구성합니다.
## Consist cluster by adding NUC2, NUC3 to NUC1.
## 빨간 칸 안에 있는 명령어를 복사하고, 앞에 sudo를 붙여 sudo 권한으로 실행하며, --ignore-preflight-errors=all을 붙여서 실행시킵니다.
## Copy command in red rectangle, prefix 'sudo' to run with sudo previlege and run command with option '--ignore-preflight-errors=all'.
sudo kubeadm join <NUC1 IP>:6443 --token <YOUR TOKEN> --discovery-token-ca-cert-hash <YOUR HASH> --ignore-preflight-errors=all # 계속 실패할 경우 --ignore-preflight-errors=all 옵션을 붙여 시도합니다!
```

#### 2-4-4. Check Nodes at NUC1

```shell
# From NUC1
kubectl get node
```

### 2-5. Kubenetes Network Plugin Installation

```shell
# From NUC1
# flannel을 사용합니다 https://github.com/flannel-io/flannel
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

```shell
# From NUC1 -> Check Weave works
kubectl get nodes
kubectl get po -n kube-system -o wide
```

![Kubenetes Network Plugin Installation](img/10.png)

### 2-6. Nginx Deploy

make nginx.yaml on your directory

```shell
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
spec:
  containers:
  - name: my-nginx-container
    image: nginx:latest
    ports:
    - containerPort: 80
      protocol: TCP

  - name: ubuntu-sidecar-container
    image: alicek106/rr-test:curl
    command: ["tail"]
    args: ["-f", "/dev/null"] # 포드가 종료되지 않도록 유지합니다
```

#### 2-7-1. Deploy Nginx on the Cluster

```shell
# From NUC1
kubectl apply -f nginx.yaml

# From NUC1
## Check WordPress Container
watch kubectl get pods --all-namespaces
```

#### 2-7-2. Access Nginx

```shell
# From NUC1
kubectl get svc
```

- Enter following address in web browser

  `http://<your NUC1 IP>:<Exposed port>`

## K3S installation

설치하기 전, docke, openssh-server, ssh, vim, tet-tools가 설치되어 있어야합니다.

### 1. To set firewall using ufw

![commnad](img/k3s1.png)

모든 눅에 위 테이블 속 All nodes 에 해당하는 포트를 개방합니다.
Agents : 워커 노드가 될 눅
Servers : 마스터 노드가 될 눅

#### 1-1. port-forwarding

```shell
# How to use ufw
sudo ufw enable # ufw가 켜져 있는지 아닌지 확인 할 수 있습니다.
sudo ufw status # ufw의 상태가 inactivate 상태라면 해당 명령어를 통해 활성화 시켜줍니다.
sudo ufw allow {start}:{end}/tcp # to open tcp port method if, need to open 2379~2380 ports, ufw allow 2379:2380/tcp
sudo ufw allow 2380/udp # to open udp port method
# 위 방법으로 모두 세팅한 후, 다시 ufw status 를 통해 열려있는지 확인합니다.
```

#### 1-2. Master Node port-forwarding

```shell
# from Master mode(NUC1)
sudo ufw allow 2379:2380/tcp
```

#### 1-3. Worker Node port-forwarding

```shell
# from Master mode(NUC2, 3)
sudo ufw allow 6443/tcp
```

### 2. Install K3s (NUC1)

마스터 노드(NUC01)에서 실행하여 실질적인 마스터 노드로 만들어 줍니다.

```shell
# from Master mode(NUC1)
curl -sfL https://get.k3s.io | sh -
```

### 3. Join Worker Node.

#### 3-1. 마스터 노드에서 token 조회하기

```shell
# from Master mode(NUC1)
cat /var/lib/rancher/k3s/server/node-token
```

위 명령어로 얻은 토큰을 활용하여 NUC2, NUC3를 worker node로 join 합니다.

#### 3-2. 워커노드 조인

NUC2, NUC3에서 진행합니다.

```shell
# from Worker mode(NUC2.3)
curl -sfL https://get.k3s.io | K3S_URL=https://{nuc01_IP}:6443 K3S_TOKEN={token} sh -
```

#### 3-3. 노드 상태 확인 및 포드 확인

```shell
# from Master mode(NUC1)
kubectl get nodes
kubectl get pods --all-namespaces
```
