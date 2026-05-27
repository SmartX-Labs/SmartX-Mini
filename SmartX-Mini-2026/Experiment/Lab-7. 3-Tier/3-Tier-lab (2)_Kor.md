# 3-Tier Lab - Week 2

# 0. Objective

지난 **1주차** 실습에서는 **Development with Kubernetes**에 해당하는, 쿠버네티스 클러스터 환경에 3-Tier 웹 서비스 배포하기를 진행했습니다.

이번 **2주차** 실습에서는 **Operation with Kubernetes**로, 쿠버네티스 클러스터 운영자 관점에서 실습을 진행합니다.

이번 실습은 다음의 요소를 중점으로 다룹니다.

- **Private Container Image Registry**를 쿠버네티스 내부에 구축하고, 실제 이미지를 `push & pull`
- **Helm**을 이용해 **Kubernetes Monitoring Stack** (Prometheus + Grafana 등)을 배포
- **Grafana** 대시보드를 활용한 쿠버네티스 클러스터 모니터링 (노드, 파드 등)

> [!note]
>
> 이번 Lab은 **Lab#5 (Cluster Lab)**에서 구성한 Kubernetes Cluster 위에서 진행되며, 클러스터는 다음과 같은 구성입니다.
>
> ![Kubernetes Installation](img/nuc-prep.png)
>
> 각 실습자는 각자의 PC에서 **NUC1(master node)**에 원격 접속(SSH)하여 Kubernetes namespace를 생성하고, namespace로 분리된 환경에서 실습을 진행합니다.

# 1. Concept

## 1-1. Container Image Registry

Container image registry는 container image를 저장하고 배포하기 위한 중앙 저장소의 역할을 합니다.  
Docker, Kubernetes 환경에서 container image를 push 하고 pull 해오는 대상이라고 생각할 수 있습니다.

주요 container image registry의 예시는 다음과 같습니다.

1. Docker Hub  
   Docker에서 운영하는 공개 container image registry입니다. 지금까지 실습에서 주로 사용했습니다.
2. Amazon ECR  
   AWS에서 제공하는 container image registry입니다.
3. GitHub Container Registry (GHCR)  
   GitHub에서 제공하는 container image registry입니다.
4. Harbor  
   CNCF(Cloud Native Computing Foundation) Graduated Project로서, on-premise 환경에서 registry를 구축하기 위해 사용됩니다.
5. 자체 구축 Docker Registry  
   Docker에서 공식적으로 제공하는 registry:2 container image를 바탕으로 구축할 수 있는 registry입니다.

이번 실습에서는 registry:2 container image를 바탕으로, 지금까지 구축한 kubernetes cluster에서 private container registry를 배포합니다.

## 1-2. 쿠버네티스 클러스터 모니터링의 중요성

쿠버네티스 클러스터 모니터링 도구의 필요성은 다음과 같습니다.

1. **가용성 확보** – CPU·메모리·디스크·네트워크 지표를 미리 수집해 과부하 전 징후 감지
2. **트러블슈팅 단축** – 파드가 CrashLoop / Pending 상태일 때 근본 원인을 로그·메트릭으로 추적
3. **용량 계획(Capacity Planning)** – 역사적 데이터를 토대로 노드 수, 스토리지 크기, GPU 수요 예측
4. **알림과 대응** – Alertmanager와 연동하여 Slack·PagerDuty 등으로 실시간 알림 → SRE Runbook 실행

> [!note]
>
> 📈 **Monitoring Market**  
> CNCF Survey(2024)에 따르면 “Prometheus + Grafana Stack”은 **프로덕션 쿠버네티스 클러스터의 77 %** 가 채택 중입니다. 상용 SaaS(New Relic, Datadog, Dynatrace 등)도 Prometheus Remote-Write 프로토콜을 기본 지원하면서 사실상 표준으로 자리잡았습니다.

## 1-3. Prometheus와 Grafana의 작동 원리

### 1-3-1. Prometheus의 작동 원리

![prometheus-arch](img/prometheus-arch.png)

Prometheus는 시계열(time-series) 데이터 수집 및 저장에 특화된 모니터링 도구입니다. 주요 특징은 다음과 같습니다:

- **데이터 수집 방식**: Prometheus는 모니터링 대상(Target)으로부터 메트릭 데이터를 주기적으로 수집하는 **Pull** 방식을 사용합니다. 이를 위해 각 대상에 **Exporter**를 설치하여 메트릭을 HTTP 엔드포인트로 노출합니다.
- **데이터 저장**: 수집된 메트릭은 Prometheus의 내장 **시계열 데이터베이스**에 저장됩니다. 이 데이터는 시간 정보와 함께 저장되어 시간에 따른 변화 추이를 분석할 수 있습니다.
- **데이터 질의**: Prometheus는 자체 쿼리 언어인 `PromQL`을 제공하여 다양한 방식으로 메트릭 데이터를 조회하고 분석할 수 있습니다.
- **알림 기능**: 설정된 조건에 따라 Alertmanager와 연동하여 이메일, Slack 등으로 **알림**을 보낼 수 있습니다.

### 1-3-2. Grafana의 역할과 기능

![grafana](img/grafana.png)

Grafana는 다양한 데이터 소스로부터 데이터를 시각화하는 대시보드 도구입니다. Prometheus와 함께 사용하면 다음과 같은 이점을 제공합니다:

- **데이터 시각화**: Prometheus에 저장된 메트릭 데이터를 다양한 그래프, 차트, 게이지 등으로 시각화하여 한눈에 시스템 상태를 파악할 수 있습니다.
- **대시보드 구성**: 사용자는 원하는 메트릭을 선택하여 **커스터마이징된 대시보드**를 생성할 수 있습니다. 또한, Grafana 커뮤니티에서 공유하는 **다양한 대시보드 템플릿**을 활용할 수 있습니다.
- **알림 설정**: 특정 조건을 만족하는 경우 **Grafana 자체적으로도 알림을 설정**하여 사용자에게 통지할 수 있습니다.

### 1-3-3 Prometheus와 Grafana의 통합

두 도구의 통합은 다음과 같은 구조로 이루어집니다:

1. **메트릭 수집**: 모니터링 대상 시스템에 설치된 Exporter가 메트릭을 HTTP 엔드포인트로 노출합니다.
2. **데이터 수집 및 저장**: Prometheus는 설정된 주기에 따라 Exporter로부터 메트릭을 Pull 방식으로 수집하여 자체 데이터베이스에 저장합니다.
3. **데이터 시각화**: Grafana는 Prometheus를 데이터 소스로 설정하고, PromQL을 사용하여 필요한 메트릭을 조회하여 대시보드에 시각화합니다.
4. **알림 및 대응**: 설정된 조건에 따라 Prometheus의 Alertmanager나 Grafana의 알림 기능을 통해 사용자에게 알림을 전달합니다.

이러한 구조를 통해 시스템의 성능, 자원 사용량, 오류 상태 등을 실시간으로 모니터링하고, 문제 발생 시 신속하게 대응할 수 있습니다.

- **참고자료**
  - **Prometheus 공식 문서**: <https://prometheus.io/docs/introduction/overview/>
  - **Grafana 공식 문서**: <https://grafana.com/docs/grafana/latest/>

### 요약

1. **Exporter** (Node Exporter, cAdvisor, kube-state-metrics)가 /metrics 엔드포인트로 노출
2. **Prometheus가** 잡 간격(기본 30 s)으로 Exporter Endpoint를 **pull**
3. 수집된 시계열 데이터에 대해 **Recording Rule / Alert Rule** 평가
4. 조건을 만족하면 **Alertmanager**가 이메일, Slack 등으로 알림 전송
5. **Grafana**는 Prometheus API(PromQL) 쿼리를 통해 대시보드 시각화

# 2. Container Image Registry Deployment on Kubernetes

지금까지 생성된 대부분의 container들은 원격으로 존재하는 public container image 저장소인 Docker Hub에서 pull 해온 container image를 바탕으로 생성되었습니다.

이제부터는 Docker Hub와 같이 공개된 container image registry를 사용하지 않고, Private Container Image Registry를 직접 구축하고 해당 저장소로 container image를 push, pull 해보겠습니다.

그렇게 하기 위해서, 직접 구축한 kubernetes cluster에 Docker Hub와 같은 역할을 하는 Container Image Registry를 구축해야 합니다.

아래의 과정을 따라, 여러분만의 Private Container Image Registry를 간단하게 구축해보겠습니다.

## 2-1. Container Runtime 설정

지금까지 우리는 Docker를 주된 container runtime으로 사용했습니다.
그러나 Docker를 제외하고도 다양한 container runtime이 존재합니다.
실제로 kubernetes는 기본적으로 `Containerd`를 기본 container runtime으로 사용합니다.

실습에서는 두 단계에서 각각 다른 container runtime이 사용됩니다.

1. Host machine에 설치된 `Docker`를 통해 container image를 build하고 해당 image를 container image registry로 push하는 과정
2. Kubernetes pod 생성 시, kubernetes 기본 container runtime인 `Containerd`를 통해 private container image registry에서 container image를 조회하여 사용하는 과정

따라서 우리는 두 개의 container runtime의 설정을 해주어야 합니다.

기본적으로 Docker와 Containerd 모두 https 프로토콜을 사용하여 container image의 push와 pull을 진행하도록 구현되어 있습니다.

그러나 이번 실습에서는 private container image registry를 구축하며 https 지원을 위한 SSL/TLS 인증서까지 도입하는 과정은 다루지 않을 것입니다.

Kubernetes cluster 내부에서 hostname을 통한 http 통신만 사용할 것이기 때문에, 아래의 설정을 진행해야 합니다.

## For NUC01

> [!WARNING] > **이번 실습에서는 NUC01에서만 Docker에 대한 설정을 진행합니다.** > **NUC01 역할을 하는 실습자만 Docker 설정을 하면 됩니다.**

아래의 명령어를 입력하여 Docker에 대한 설정을 진행합니다.

```shell
sudo vim /etc/docker/daemon.json
```

파일에 존재하는 가장 바깥 중괄호 안에 "insecure-registries" 필드를 추가하고 이에 해당하는 값을 같이 적어줍니다. 이 설정을 통해 http 프로토콜을 사용하여 container image를 push, pull할 수 있게 됩니다.

> [!WARNING]
> 예시에 나와있는 `...`은 제외하고 `"insecure-registries": ["nuc01:5000", "nuc02:5000", "nuc03:5000"]`만 입력해주시기 바랍니다. 나머지 필드는 수정하지 않습니다.

```json
{
  ...
  ...
  ...
  ...
  "insecure-registries": ["nuc01:5000", "nuc02:5000", "nuc03:5000"]
}
```

파일의 수정을 완료했다면, 아래의 명령어를 입력하여 Docker를 재시작합니다.

```shell
sudo systemctl restart docker
```

## For All NUCs

> [!WARNING] > **Containerd에 대한 설정은 모든 NUC에서 진행합니다.**  
> **실습자들은 각 NUC에 ssh로 접속하여 자신의 registry 등록을 진행합니다.**

```shell
ssh gist@nuc01
# 설정 진행...
ssh gist@nuc02
# 설정 진행...
ssh gist@nuc03
# 설정 진행...
```

이제는 Containerd에 대한 설정을 진행하겠습니다.  
아래의 명령어를 입력하여 파일을 열어줍니다.

```shell
sudo vim /etc/containerd/config.toml
```

파일의 내용 중 `[plugins.'io.containerd.cri.v1.images'.registry]`라는 필드를 찾고, 다음과 같이 수정합니다.

> [!WARNING]
> 예시에 나와있는 `...`은 제외하고 내용을 입력하여 주시기 바랍니다. **들여쓰기에 주의해주시기 바랍니다.** 나머지 부분은 수정하지 않습니다.

```toml
...
...
...

[plugins.'io.containerd.cri.v1.images'.registry]
  config_path = "/etc/containerd/certs.d"

...
...
...
```

자신의 NUC의 정보를 추가하기 위해서 파일을 수정합니다

```shell
sudo mkdir -p /etc/containerd/certs.d/<your_hostname>:5000
sudo vim /etc/containerd/certs.d/<your_hostname>:5000/hosts.toml
```

```toml
server = "http://<your_hostname>:5000"
[host."http://<your_hostname>:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
  plain_http = true
```

모두 수정했다면, 아래의 명령어를 입력하여 containerd를 재시작합니다.

```shell
sudo systemctl daemon-reload
sudo systemctl restart containerd
```

## 이제부터 다시 ssh로 접속한 NUC01에서 실습을 진행합니다

## 2.2 Persistent Volume(PV) 생성

여러분이 직접 build한 container image를 container registry에 push 했을 때, 해당 image에 대한 정보가 영구적으로 파일 시스템에 남아있어야 합니다. 그래야 원할 때 해당 image를 pull 해올 수 있기 때문입니다.

이전 실습 과정에서도 살펴보았듯이, Kubernetes에서는 데이터를 실제 스토리지에 저장하기 위한 방법으로 Persistent Volume과 Persistent Volume Claim을 사용합니다.

### Persistent Volume이란?

> [!NOTE]  
> Persistent volume은 kubernetes cluster에 존재하는 실제 스토리지 영역을 나타냅니다. 우리는 kubernetes 환경에서 다양한 Pod를 생성하고 삭제하는데, Pod가 삭제되어도 보존되었으면 하는 데이터가 있는 상황에서 Persistent Volume을 사용할 수 있습니다.

아래의 명령어를 입력하여 Persistent Volume을 정의한 yaml 파일을 확인하겠습니다.  
본인이 사용중인 hostname과 namespace를 기반으로 yaml 파일의 내용을 수정해주시기 바랍니다.

```shell
cd ~/<your_namespace>/kubernetes/container
vim container-image-registry-pv.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: container-image-registry-pv-<your_namespace>
  labels:
    volume: container-image-registry-pv-<your_namespace>
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data/<your_namespace>/registry
    type: DirectoryOrCreate
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - <your_hostname>
```

이제, 수정한 파일을 적용하여 PV를 생성합니다.  
아래의 명령어를 입력하여 파일의 내용을 적용하고 PV 목록을 확인해봅니다.

```shell
kubectl apply -f container-image-registry-pv.yaml
kubectl get pv
```

## 2.3 Persistent Volume Claim(PVC) 생성

그 다음으로, Persistent volume claim도 생성합니다.

> [!NOTE]
> Persist volume claim은 사용자가 특정 조건을 만족하는 스토리지(PV)를 사용하겠다고 선언하는 역할을 합니다. 일반적으로 특정 기능을 하는 Pod가 스토리지를 요구할 때, Persistent volume claim을 통해 사전에 정의된 Persistent volume을 사용할 수 있습니다.

아래의 명령어를 입력하여 PVC에 대한 내용이 담긴 yaml 파일을 열고, 내용을 수정합니다.

```shell
vim container-image-registry-pvc.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: container-image-registry-pvc-<your_namespace>
  namespace: <your_namespace>
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  selector:
    matchLabels:
      volume: container-image-registry-pv-<your_namespace>
  resources:
    requests:
      storage: 5Gi
```

수정이 완료되었다면, 아래의 명령어를 입력하여 PVC를 생성하고 PVC가 잘 생성되었는지 확인합니다.

```shell
kubectl apply -f container-image-registry-pvc.yaml
kubectl get pvc -n <your_namespace>
```

## 2.4 Deployment 생성

지금까지는 container image가 push 되었을 때 저장될 스토리지에 대한 설정을 했다면,  
이제는 실제로 container image를 처리하는 pod를 띄우기 위한 과정을 다룹니다.  
우리는 Deployment를 정의하여 pod를 생성합니다.

아래의 명령어를 입력하여 deployment가 정의된 yaml 파일을 열고, 수정합니다.

```shell
vim container-image-registry.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: container-image-registry
  namespace: <your_namespace>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: container-image-registry
  template:
    metadata:
      labels:
        app: container-image-registry
    spec:
      nodeSelector:
        kubernetes.io/hostname: <your_hostname>
      tolerations:
        - key: "node-role.kubernetes.io/control-plane"
          operator: "Exists"
          effect: "NoSchedule"
      containers:
        - name: registry
          image: registry:2
          ports:
            - containerPort: 5000
              hostPort: 5000
          volumeMounts:
            - name: registry-storage
              mountPath: /var/lib/registry
      volumes:
        - name: registry-storage
          persistentVolumeClaim:
            claimName: container-image-registry-pvc-<your_namespace>
```

수정이 완료되었다면, 명령어를 입력하여 deployment를 생성합니다.  
그리고 해당 deployment가 잘 생성되었는지 확인합니다.

```shell
kubectl apply -f container-image-registry.yaml
kubectl get deploy -n <your_namespace>
```

## 2.5 Build & Push Container Image

이제 container image를 build하고, 구축한 private container image registry로 push할 수 있게 되었습니다.

아래의 명령어를 입력하여 container image를 build 하고 tag를 붙이고, push 해보겠습니다.  
이전에 사용한 Frontend용 container image와 Backend용 container image 모두에 대해 실행합니다.

```shell
sudo docker build -t <your_namespace>-frontend ~/<your_namespace>/frontend
sudo docker tag <your_namespace>-frontend <your_hostname>:5000/<your_namespace>-frontend
sudo docker push <your_hostname>:5000/<your_namespace>-frontend
```

Frontend를 위한 container image를 build하고 push 했다면, Backend를 위한 container image에 대해서도 동일한 과정을 진행합니다.

```shell
sudo docker build -t <your_namespace>-backend ~/<your_namespace>/backend
sudo docker tag <your_namespace>-backend <your_hostname>:5000/<your_namespace>-backend
sudo docker push <your_hostname>:5000/<your_namespace>-backend
```

이제 직접 build한 container image가 private container image registry에 push되었기 때문에, 해당 container image에 대한 실제 물리적 데이터를 파일 시스템을 통해 확인해보며 잘 저장되었는지 확인할 수 있습니다.

우리는 Persistent Volume에 대한 yaml 파일에서 각각의 PV가 실습자의 NUC에 설정되도록 만들었습니다.

따라서 **push된 container image에 대한 물리적 파일을 확인하기 위해서는 각자의 NUC에서 아래의 명령어를 입력해야 합니다.**

> [!WARNING]
> 아래의 명령어는 ssh로 접속한 터미널이 아니라, 실습자 자신의 터미널을 새로 열고 입력해야 합니다.

```shell
ls -al /mnt/data/<your_namespace>/registry/docker/registry/v2/repositories
```

지금까지의 과정에서 문제가 발생하지 않았다면, 위의 명령어를 통해 push된 container image를 확인할 수 있을 것입니다.

## 2.6 Re-Deployment of Frontend and Backend

이제는 직접 build한 container image로 저번 실습에서 생성한 Frontend, Backend를 다시 배포해보겠습니다.  
간단하게, 이전에 생성한 Deployment와 관련된 yaml 파일의 container image 필드만 수정하면 됩니다.

아래의 명령어를 입력해서 수정할 파일을 열어주시기 바랍니다.

```shell
cd ~/<your_namespace>/kubernetes/backend
vim deployment.yaml
```

그리고 containers 아래의 image 필드 값을 아래와 같은 값으로 수정합니다.

```yaml
---
spec:
  containers:
    - name: api
      image: <your_hostname>:5000/<your_namespace>-backend
      ports:
        - containerPort: 3000
```

수정을 완료했다면, 아래의 명령어를 입력하여 수정사항을 반영합니다.

```shell
kubectl apply -f deployment.yaml
```

이제는 Frontend도 변경해보겠습니다.  
아래의 명령어를 입력해주시기 바랍니다.

```shell
cd ~/<your_namespace>/kubernetes/frontend
vim fe-proxy.yaml
```

그리고 Backend와 마찬가지로, containers 아래의 image 필드 값을 수정합니다.

```yaml
containers:
  - name: nginx
    image: <your_hostname>:5000/<your_namespace>-frontend
    imagePullPolicy: Always
```

수정을 완료했다면 아래의 명령어를 입력하여 수정사항을 반영합니다.

```shell
kubectl apply -f fe-proxy.yaml
```

Backend와 Frontend를 담당하는 Pod가 모두 재생성되었는지 확인합니다.

```shell
kubectl get pod -n <your_namespace> -o wide
```

모든 Pod의 재생성이 완료되었다면 NGINX Pod의 IP 주소를 브라우저에 입력하여 실행 결과를 확인합니다.

# 3. Helm 설치 및 쿠버네티스 모니터링 툴 배포

## 3-1. Helm 설치하기

### 3-1-1. Helm이란?

Helm은 Kubernetes에서 애플리케이션을 보다 **간단하고 일관되게 배포**할 수 있도록 도와주는 패키지 매니저입니다.

**기존의 수동 배포 방식**에서는 **여러 개의 YAML 파일을 직접 관리**하고, 이를 **순서에 맞게 적용**해야 했습니다. 그러나 Helm을 사용하면 이러한 **YAML 파일들을 하나의 Chart로 묶어 배포**하고, **변수나 설정 등을 일괄적으로 관리**할 수 있습니다.

즉, Helm은 `apt`, `yum`, `brew`와 같은 Linux/Unix 패키지 매니저와 비슷하게 작동하며, 애플리케이션을 하나의 패키지로 정의해 쉽게 설치, 업그레이드, 삭제할 수 있게 도와줍니다.

> [!note]
>
> **Chart란?**
>
> 하나의 애플리케이션에 대한 모든 리소스 정의 파일을 묶은 것입니다. `values.yaml` 파일을 통해 설정값을 쉽게 커스터마이징할 수 있습니다.

또한 Helm은 **GitOps**와도 자연스럽게 연동되며, Git repository에 **선언형 구성 파일**을 두고 지속적으로 이를 동기화하는 파이프라인을 구성할 때 사용됩니다.

### 3-1-2. Helm 설치 (For NUC1)

다음 명령어를 입력하여, Helm을 설치해주세요.

```bash
cd ~
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh


# 설치 후
# 아래 명령어를 통해 정상적으로 설치되었는지 확인
helm version
```

### 3-1.3. Helm 조작법 (All NUCs)

Helm은 기본적으로 다음과 같은 명령어로 조작됩니다.

```bash
helm version                             # Helm 버전 확인
helm repo list                           # 등록된 Helm 저장소 목록 확인
helm repo add <name> <url>               # 새로운 Helm 저장소 추가
helm repo update                         # 저장소 목록 업데이트
helm install <release-name> <chart>      # Helm Chart 설치
helm upgrade <release-name> <chart>      # 기존 Helm Chart 업그레이드
helm uninstall <release-name>            # Helm Chart 삭제
helm list -A                             # 모든 네임스페이스에서 설치된 Helm 리소스 목록 확인
```

다음은 그 **예시**입니다.

```bash
# 예시
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

이러한 방식으로 복잡한 리소스를 쉽게 배포하고 관리할 수 있습니다.

## 3-2. 쿠버네티스 모니터링 툴, Prometheus와 Grafana 설치하기

### 3-2-1. Helm Repository 등록 및 업데이트 (For NUC1)

먼저 Prometheus와 Grafana를 포함한 Helm Chart 저장소를 추가하고 업데이트합니다.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo list
helm repo update
```

### 3-2-2. Kubernetes Prometheus Stack 설치하기 (For NUC1)

`kube-prometheus-stack`은 다음의 구성 요소를 한 번에 설치할 수 있도록 도와주는 Helm Chart입니다.

- **Prometheus**: 메트릭 수집
- **Alertmanager**: 알림 전송
- **Grafana**: 시각화 대시보드
- **Node Exporter**: 노드 단위 메트릭 수집
- **Kube State Metrics**: 쿠버네티스 리소스 상태 수집

일반적으로 각 기능에 맞게 namespace를 정의하고, 해당 namespace에 리소스를 배포합니다. 따라서, 이 Helm Chart는 `monitoring`이라는 이름의 namespace에 설치됩니다.

```bash
helm list -n monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace --set prometheus.prometheusSpec.maximumStartupDurationSeconds=300
helm list -n monitoring
```

설치가 완료되면 다음과 같이 배포된 리소스들을 확인해볼 수 있습니다.

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

`prometheus-grafana`라는 이름의 서비스(service)가 생성된 것을 확인할 수 있습니다. 이 IP(ClusterIP) 주소를 통해 Grafana 대시보드에 접근합니다.

# 4. Grafana 접근해서 살펴보기 (All NUCs)

## 4-1. Grafana 접속 계정 정보 확인

Grafana의 기본 로그인 정보는 Helm 설치 시 자동으로 Secret에 저장됩니다. 아래의 명령어로 비밀번호를 확인합니다.

```bash
kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

기본 ID는 `admin`, 비밀번호는 위 명령어로 출력된 값입니다.

## 4-2. Grafana 대시보드 접속

Prometheus Stack이 생성한 `prometheus-grafana` 서비스에 부여된 Cluster IP를 확인합니다.

```bash
kubectl get svc -n monitoring
```

`prometheus-grafana` 항목의 `CLUSTER-IP` 주소를 복사하여 웹 브라우저에서 접속합니다.

```bash
http://<CLUSTER-IP>:80
```

접속 후 로그인 정보를 입력하면 Grafana 대시보드가 열립니다.

![grafana_login](img/grafana_login.png)

![grafana_main](img/grafana_main.png)

- 왼쪽 메뉴의 **Dashboards** 로 이동하면 Prometheus Stack이 미리 구성해놓은 다양한 모니터링 대시보드를 확인할 수 있습니다.
- **Nodes**, **Pods**, **Kubernetes Cluster** 등 다양한 자원에 대한 실시간 메트릭을 시각적으로 확인 가능합니다.

> [!tip]
>
> 실습자별 네임스페이스에 독립적으로 Prometheus와 Grafana가 설치되었기 때문에,
>
> 본인의 서비스만 필터링하여 모니터링할 수 있습니다.

## 4-3. Missions

지금부터는 구체적인 Instructions 없이 주어진 미션에 맞게 Grafana 대시보드를 살펴봅니다. **각 Mission을 달성하면 스크린샷을 찍고**, 최종 점검 시 조교에게 보여주세요.

> [!tip]
>
> 우분투 화면 스크린샷 단축키: `Shift + Ctrl + PrtScn`

### Mission 1

자신의 namespace(nuc01, nuc02, or nuc03)에 속한 모든 Pod 목록을 Grafana에서 찾아보세요. 1주차 실습에서 배포한 backend-api, nginx-proxy, postgres 등이 해당됩니다.

### Mission 2

특정 Pod의 CPU 및 메모리 사용량을 시계열 그래프로 확인해보세요. `backend-api`나 `postgres` 등 자주 요청이 발생하는 Pod을 선택해보면 좋습니다.

### Mission 3

현재 본인이 조작하고 있는 NUC PC의 CPU/Memory 전체 사용률을 확인해보세요. `Node Exporter`에서 제공하는 대시보드를 통해 확인할 수 있습니다.

### Mission 4

Kubernetes Cluster 전체 상태를 요약해서 보여주는 대시보드를 찾아보세요. 클러스터 리소스 현황, 경고 발생 여부 등을 포함합니다.

> [!tip]
>
> 미션 수행 중 모르는 지표나 단어가 나온다면, 직접 검색하거나 조교에게 질문하세요.

# 5. Lab Summary

이번 실습에서는 지난 시간 Kubernetes 위에 웹 서비스를 직접 배포한 것에 이어, 실제 운영 환경에서도 필수적으로 요구되는 **컨테이너 이미지 관리, 패키지 관리, 모니터링 시스템**을 구성해보았습니다.

실습의 핵심 내용은 다음과 같습니다:

1. `Private Container Image Registry` 구축을 통해, 본인이 만든 컨테이너 이미지를 직접 저장하고 관리할 수 있게 되었습니다.
2. `Helm`이라는 Kubernetes 패키지 매니저를 통해 복잡한 리소스를 손쉽게 설치할 수 있는 경험을 해보았습니다.
3. Helm Chart 중 하나인 `kube-prometheus-stack`을 통해 `Prometheus`와 `Grafana`를 포함한 모니터링 스택을 손쉽게 배포하였습니다.
4. `Grafana`를 통해 실시간으로 Kubernetes 클러스터의 상태와 동작을 시각적으로 확인하였습니다.

이러한 실습은 단순한 웹 서비스 배포에서 한 발 더 나아가, **실제 서비스 운영 환경에서 필요한 DevOps 역량**을 키우는 데에 필수적인 기초가 됩니다.

이것으로, **3-Tier Architecture Lab**을 마치겠습니다.
