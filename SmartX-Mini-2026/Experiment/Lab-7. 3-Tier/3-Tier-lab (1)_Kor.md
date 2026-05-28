# 3-Tier Lab - Week 1

# 0. Objective

이번 실습에서는 쿠버네티스(Kubernetes) 환경에서 **3 Tier Architecture**를 기반으로 한 웹 서비스를 배포하는 과정을 다룹니다.
전체 실습은 2주간 진행되며, 그 중 1주차 실습은 다음의 요소를 중점으로 다룹니다.

- PostgreSQL Database를 쿠버네티스 위에 배포
- NestJS 기반 Backend를 쿠버네티스 위에 배포하고, 데이터베이스와 연결
- NGINX를 활용해 React를 기반 웹페이지를 전달하거나, Backend에게 요청 포워딩

> [!note]
>
> 이번 Lab은 **Lab#5 (Cluster Lab)**에서 구성한 Kubernetes Cluster 위에서 진행되며, 클러스터는 다음과 같은 구성입니다.
>
> ![Kubernetes Installation](img/nuc-prep.png)
>
> 각 실습자는 각자의 PC에서 **NUC1(master node)**에 원격 접속(SSH)하여 Kubernetes namespace를 생성하고, namespace로 분리된 환경에서 실습을 진행합니다.

# 1. Concept

## 1-1. 3-Tier Architecture

**3-Tier Architecture**란, 하나의 애플리케이션을 기능별로 세 개의 계층으로 분리(물리적/논리적)하여 구성하는 아키텍텍쳐 설계 방식입니다.

이는 특히 웹 서비스과 같이 사용자와 상호작용하고, 데이터를 처리하며, 이를 저장해야 하는 시스템에서 널리 사용됩니다.

### 구성 요소

![3-Tier Architecture](img/3-Tier-Arch.png)

1. Presentation Tier (프론트엔드)
   - 사용자와 직접 상호작용하는 계층입니다.
   - 브라우저에서 실행되는 React, Vue, Angular 등의 웹 프레임워크/라이브러리가 대표적입니다.
   - 모바일 앱도 이 계층에 해당되며 네이티브로는 안드로이드, SwiftUI, 크로스플랫폼으로 Flutter나 React Native가 대표적입니다.
2. Application Tier (백엔드)
   - Presentation Tier로부터 발생한 사용자의 요청을 처리하고, 비즈니스 로직을 수행하며, 데이터베이스와 통신합니다.
   - 보통 Express, NestJS, Django, Spring 등으로 개발된 서버 애플리케이션이 위치합니다.
   - Business Logic Tier, Transaction Tier라고도 불립니다.
3. Data Tier (데이터베이스)
   - 데이터베이스와 데이터베이스에 접근하여 데이터를 읽거나 쓰는 것을 관리하는 계층입니다.
   - 애플리케이션의 데이터를 영구적으로 저장합니다.
   - PostgreSQL, MySQL, MongoDB 등 다양한 Database가 사용됩니다.

### 등장 배경

과거의 웹 애플리케이션은 하나의 서버에서 모든 역할(사용자 인터페이스, 로직 처리, 데이터 저장)을 수행하는 **모놀리식(Monolithic) 구조**로 구성되는 경우가 많았습니다.

그러나 다음과 같은 문제들이 점차 뚜렷해지며, 3-Tier Architecture가 대두되었습니다.

- 기능이 복잡해질수록 프로젝트와 코드의 규모가 거대해지고 유지보수가 어려워짐
- 사용자 수 증가에 따른 서버의 부하 집중
- 특정 기능 하나의 변경이 전체 서비스에 영향을 주는 구조적 한계
- 서비스 확장 시 전체를 스케일링해야 하므로 비효율적

이러한 문제를 해결하기 위해 각 계층을 분리하고, 계층이나 기능별로 독립 배포 및 관리가 가능하도록 하는 구조가 필요해졌고, 그것이 바로 3-Tier Architecture입니다.

### 기존 구조와의 차이점

| 항목           | Monolithic Architecture | 3-Tier Architecture            |
| -------------- | ----------------------- | ------------------------------ |
| 코드 분리      | X (기능이 섞여 있음)    | O (기능별 계층 분리)           |
| 유지보수       | 오류 원인 파악이 어려움 | 계층 단위로 관리 가능          |
| 스케일링       | 전체 확장이 필요        | 계층 단위로 독립 확장 가능     |
| 장애 영향 범위 | 전체 서비스로 전파 가능 | 단일 계층에서 일부분 격리 가능 |
| 배포 전략      | 단일 배포               | 계층별 독립 배포 가능          |

### 이점

- **독립성**: 프론트엔드, 백엔드, DB를 서로 독립적으로 개발하고 배포 가능
- **유지보수성**: 문제 발생 시 어느 계층의 문제인지 명확하게 식별 가능
- **확장성**: 부하가 많은 계층만 별도로 확장 가능 (예: DB는 그대로 두고 BE만 scale-out)
- **보안성**: DB는 외부와 직접 연결되지 않으며, Backend를 통해서만 접근 가능

### 단점

- **운영 복잡도 증가**: 계층이 나뉘면서 통신 및 배포 구조가 복잡해짐
- **네트워크 비용 증가**: 계층 간 트래픽이 발생하므로 대규모 시스템에서는 성능 고려 필요
- **개발 난이도 상승**: 계층 간 API 설계, 데이터 포맷 설계 등 인터페이스 관리가 필요

### 3-Tier Architecture를 Kubernetes 환경에서 운영하는 이유

3-Tier 구조를 쿠버네티스 환경에서 운영할 경우 **현대적인 클라우드 네이티브** 관점에서 많은 이점을 얻을 수 있으며, 다음은 그 일부에 대한 설명입니다.

1. **배포 자동화**
   - 각 계층을 별도 Deployment로 관리하여 독립적으로 롤링 업데이트 가능

2. **자가 복구(Self-healing)**
   - 특정 계층의 일부 Pod가 비정상적으로 종료되면 자동으로 복구됨

3. **수평 확장(Horizontal Scaling)**
   - 특정 계층의 부하가 증가하면 자동으로 수평 확장하여 부하 분산 가능

4. **관측 및 로깅 통합**
   - Prometheus, Grafana 등을 활용한 계층 통합 모니터링

5. **인프라 독립성**
   - 클라우드, 온프레미스 어디서든 동일한 배포 방식 사용 가능

6. **네임스페이스 기반 격리 환경**
   - 계층별/서비스별로 namespace를 분리하여 실습과 실서비스 운영이 가능

결론적으로, 3-Tier Architecture 구조는 쿠버네티스와 궁합이 매우 잘 맞으며, 현대 서비스 개발 및 운영에 있어 기본이 되는 설계 방식입니다.

## 1-2. 왜 기업들이 Kubernetes 환경에서 서비스를 운영하는가?

**Lab#5 (Cluster Lab)**에서도 여러 번 언급했지만, 많은 기업들이 Kubernetes 기반의 인프라로 전환하는 이유는 다음과 같습니다.

### 1. **서비스 가용성 극대화**

- Pod이 실패하면 자동 복구되고, 헬스체크(Health Probe)에 실패하면 자동으로 재시작됨
- 장애가 발생해도 전체 서비스가 다운되지 않고, 부분 복구 가능

### 2. **운영 자동화**

- `Deployment`, `StatefulSet` 등의 리소스를 사용해 무중단 배포(Rolling Update), 롤백(Rollback) 등 자동화된 배포 전략 사용
- CI/CD 파이프라인과 쉽게 통합 가능

### 3. **유지보수 편의성**

- YAML 기반 선언적 설정으로 인프라 변경사항을 추적, 관리 가능
- Helm, Kustomize 등 템플릿 도구로 복잡한 설정도 단순화 가능

### 4. **확장성 (Scalability)**

- 특정 서비스가 트래픽이 몰릴 경우, `Deployment`의 `replica` 수만 조정해서 손쉽게 확장 가능
- HPA (Horizontal Pod Autoscaler)와 연계하면 자동으로 확장 가능

### 5. **리소스 효율성**

- Node 단위가 아닌 Pod 단위로 스케줄링되므로, 클러스터 리소스를 효율적으로 사용
- CPU, Memory 제한 설정으로 과도한 자원 소비 방지

### 6. **환경 간 일관성 보장**

- 개발, 테스트, 운영 환경을 동일한 설정(YAML)으로 유지 가능
- 개발자가 만든 설정이 그대로 프로덕션에 반영될 수 있음

### 7. **클라우드/온프레미스 모두 지원**

- AWS, GCP, Azure 같은 퍼블릭 클라우드는 물론, 자체 서버 환경(On-prem)에서도 동일한 방식으로 운용 가능
- 벤더 종속 없이 멀티 클라우드 전략 가능

이러한 이유로 대규모 기업뿐 아니라, 스타트업, 교육기관, 정부기관 등도 점점 Kubernetes 기반 인프라로 전환하고 있으며, 현대 인프라/DevOps 환경에서 사실상 표준으로 자리잡고 있습니다.

# 2. Lab Preparation

이제 본격적으로 3-Tier Lab을 시작해봅시다.

## 2-1. Master Node에 원격 접속하기 (For NUC2, NUC3)

우선 NUC2와 NUC3에서 실습할 경우, 터미널에 아래 명령어를 입력해 Master Node에 원격 접속합니다.

```bash
ssh <username>@nuc01
# 컴시이실 실습자의 경우 username은 gist
# 해당 명령어 입력 후 password를 입력합니다.
```

## 2-2. Kubernetes Cluster 상태 확인하기 (For all NUCs)

Kubernetes Cluster의 Master node에 접속했으면, 다음의 명령어를 입력하여 Kubernetes Cluster의 node와 pod 상태를 확인하여 Kubernetes Cluster가 정상적으로 작동 중인지 확인합니다.

```bash
# Kubernetes Cluster에 속한 노드의 상태
kubectl get nodes

# Kubernetes Cluster에 띄워진 모든 namespace의 Pod들의 상태
kubectl get pods -A
```

모든 Nodes가 `Ready` 상태이며 모든 Pods가 `Running` 상태임을 확인했을 것입니다.

> [!warning]
>
> `Ready` 상태가 아닌 Node나 `Running` 상태가 아닌 Pod가 있다면 추후 실습이 정상적으로 진행되지 않을 수 있습니다.

## 2-3. Kubernetes Namespace 생성하기 (For all NUCs)

이번 실습은 모든 실습자가 각자의 NUC에서 Kubernetes Master Node에 원격 접속하여 진행되는 만큼, Kubernetes의 자원을 여러 사용자에게 논리적으로 나누는 `namespace`를 활용합니다.

> [!note]
>
> **Namespace란?**
>
> 쿠버네티스 클러스터 내에서 논리적으로 리소스를 격리할 수 있는 기능입니다. 하나의 클러스터에서 여러 사용자나 팀이 동시에 작업하더라도 각자의 작업이 서로 영향을 주지 않도록 분리된 공간을 제공합니다.
>
> 실습에서는 실습자마다 **자신만의 namespace**를 만들고, **그 안에서만 리소스를 생성/관리**하게 됩니다. 이렇게 하면 **충돌 없이 여러 명이 동시에 실습**할 수 있습니다.

다음의 명령어를 입력하여 본인의 `namespace`를 생성해주세요!

```bash
# 현재 네임스페이스 목록 확인
kubectl get namespace

# <your_namespace>에는 각자 작업 중인 PC에 따라 nuc01, nuc02, 또는 nuc03을 입력하세요
kubectl create namespace <your_namespace>

# 생성된 본인의 namespace 확인
kubectl get namespace
```

## 2-4. Kubernetes Basic Manuals 연습

이 섹션에서는 Kubernetes 클러스터를 다루는 데 필요한 기본적인 명령어들을 직접 실습하며 익힙니다. 실습 중 배포할 리소스들은 대부분 `kubectl`을 통해 조작하게 됩니다. 아래 명령어는 자주 사용되는 명령어들이며, 이후 실습의 기본이 됩니다.

### (1) 리소스 조회: `kubectl get <resource>`

Kubernetes에서 현재 상태를 확인할 때 가장 많이 사용하는 명령어입니다.

```bash
kubectl get pods          # 현재 namespace의 Pod 목록 조회
kubectl get services      # 현재 namespace의 Service 목록 조회
kubectl get deployments   # 현재 namespace의 Deployment 목록 조회
kubectl get namespaces    # 클러스터 내 네임스페이스 목록 조회
kubectl get nodes         # 클러스터 내 노드 목록 조회
```

> [!tip]
>
> 아래와 같이 **약어** 사용 가능
>
> `pods` -> `po`
>
> `services` -> `svc`
>
> `deployments` -> `deploy`
>
> `namespaces` -> `ns`

### (2) 네임스페이스 지정 옵션: `-n <namespace>`와 `-A`

- `-n <namespace>`: 특정 네임스페이스 내 리소스만 조회
- `-A` 또는 `--all-namespaces`: 클러스터 내 모든 네임스페이스에서 리소스를 조회

```bash
# 네임스페이스 nuc01에 존재하는 모든 Pod 목록 조회
kubectl get po -n nuc01

# 모든 네임스페이스에 존재하는 모든 Service 목록 조회
kubectl get svc -A
```

### (3) 추가 정보 출력: `-o wide`

`kubectl get` 명령어에 `-o wide` 옵션을 추가하면 IP, 노드 위치 등의 추가 정보를 함께 볼 수 있습니다.

```bash
# 각 Pod가 어떤 node에 띄워졌고, 어떤 Cluster IP를 가지는지 표시된다
kubectl get pods -o wide
```

### (4) 리소스 생성/적용/삭제: `create`, `apply`, `delete`

- `create`: 존재하지 않는 새 리소스를 만드는 데 사용합니다. 초기 리소스 생성에 적합하며, 기존 리소스에 대해서는 작동하지 않습니다.
- `apply`: 기존 리소스의 설정을 수정하거나 추가할 때 유용합니다. 이미 생성된 리소스에 대해서 변경 사항을 적용할 때 사용하며, 새로운 리소스를 생성할 때도 사용할 수 있습니다.
- `delete`: 기존 리소스를 삭제할 때 사용합니다.

```bash
# 아래는 예시입니다.
kubectl apply -f deployment.yaml # 배포 파일을 적용(존재하지 않는 리소스일 경우 생성)
kubectl delete -f deployment.yaml # 해당 리소스를 삭제
```

이러한 명령어들은 이후 실습의 모든 단계에서 반복적으로 사용됩니다. 완벽하게 외우진 못하더라도 익숙해지는 것이 중요합니다.

## 2-5.YAML 파일이란?

쿠버네티스에서 리소스들은 모두 **"선언형(Declarative)"** 방식으로 관리되며, 그 핵심은 **YAML 파일**입니다.

### YAML이란?

`YAML(YAML Ain't Markup Language)`은 사람이 읽기 쉬운 **데이터 직렬화 형식**으로, 들여쓰기를 기반으로 구조화된 정보를 표현할 수 있습니다. 쿠버네티스에서는 각종 리소스(Deployment, Pod, Service 등)를 정의하는 데 사용됩니다.

### 기본 구조 예시

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: nginx
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: my-backend:v1
```

위처럼 작성된 YAML은 `kubectl apply -f <file>.yaml` 명령어로 클러스터에 적용할 수 있습니다.

#### 주요 필드 설명

- apiVersion: 리소스를 정의할 때 사용하는 Kubernetes API 버전
- kind: 리소스 정류 (Pod, Service, Deployment, Secret 등)
- metadata: 이름, 네임스페이스, 라벨 등의 metadata
- spec: 실제 리소스의 세부 동작을 정의하는 핵심 필드

### 실습에서 주의할 점

- 들여쓰기는 공백 2칸 또는 4칸 기준으로 통일
- `:` 뒤에 반드시 공백이 필요함
- 잘못 작성된 YAML 파일은 `kubectl apply` 시 오류를 발생시킴

**YAML 파일을 제대로 이해하고 다룰 줄 아는 것이 Kubernetes 실습의 핵심 중 하나입니다.**

> 실습에서 사용하는 모든 `.yaml` 파일은 Git Repository에 포함되어 있으며, 이를 수정하거나 새로운 파일로 작성하게 됩니다.

## 2-6. Cloning the git Repository

### 2-6-1. 디렉토리 생성하고 Git Clone하기

우선 본인이 사용하는 PC에 맞게 아래 명령어를 입력하여 실습 디렉토리(폴더)를 생성해주세요.

```bash
cd ~
mkdir <your_directory> # nuc01, nuc02, or nuc03
cd <your_directory>
```

이번 Lab은 `Frontend`와 `Backend`에 대한 **코드 템플릿**과, 각각을 **Kubernetes Cluster**에 배포하기 위한 `yaml` 템플릿도 준비되어 있습니다.

이를 위해 본인의 실습 디렉토리 아래 명령어를 입력하여 Github Repository에 준비된 실습 템플릿을 cloning해주세요!

```bash
git clone https://github.com/SmartX-Labs/SmartX-Mini.git
cp -r SmartX-Mini/SmartX-Mini-2026/Experiment/Lab-7.\ 3-Tier/* ./

# 실습 템플릿 확인
ls
```

### 2-6-2. Directory Architecture

```bash
.
├── backend
│   ├── Dockerfile
│   ├── eslint.config.mjs
│   ├── nest-cli.json
│   ├── package-lock.json
│   ├── package.json
│   ├── prisma
│   ├── README.md
│   ├── src
│   ├── tsconfig.build.json
│   └── tsconfig.json
├── frontend
│   ├── app.conf
│   ├── deploy.sh
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   ├── README.md
│   ├── src
│   └── vite.config.js
├── kubernetes
│   ├── backend
│   ├── container
│   ├── database
│   └── frontend
```

# 3. Database & Backend Deployment on Kubernetes

## 3-1. Database Deployment on Kubernetes

### 3-1-1. Persistent Volume 생성

#### Persistent Volume이란?

> **PersistentVolume(PV)**: 쿠버네티스 클러스터의 노드에 존재하는 실제 스토리지를 나타냅니다. Pod가 사라져도 데이터는 남아있을 수 있도록, 외부 스토리지(예: 디스크)에 대한 연결 정보를 정의합니다.
>
> **PersistentVolumeClaim(PVC)**: 사용자가 특정 스토리지를 사용하겠다고 요청하는 자원입니다. Pod는 PVC를 참조하여 간접적으로 PV를 사용하게 됩니다.

즉, PV는 실제 스토리지, PVC는 사용자의 요청이며, 이 둘을 연결하여 Pod가 안전하게 외부 저장소를 사용하는 구조입니다.

**우선, 미리 정의된 Persistent Volume template file을 각자 사용하는 namespace에 맞게 수정합니다.**

```bash
cd ~/<your_directory\>/kubernetes/database
vim postgres-pv.yaml
```

```yaml
# postgres-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv-<your_namespace> # 각자 사용하는 namespace에 맞게 수정
  labels:
    volume: postgres-pv-<your_namespace> # 각자 사용하는 namespace에 맞게 수정
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  hostPath:
    path: /mnt/data/<your_namespace>/postgres # 각자 사용하는 namespace에 맞게 수정
  persistentVolumeReclaimPolicy: Retain
```

```bash
# PostgreSQL DB를 위한 Persistent Volume 배포
kubectl apply -f postgres-pv.yaml

# postgres-pv-<your_namespace> 형태로 생성된 Persistent Volume 확인
# 다른 실습자의 PV도 함께 보일 수 있습니다.
kubectl get pv
```

### 3-1-2. PostgreSQL Database 생성

이번에는 PostgreSQL Database를 배포해보겠습니다.

```bash
vim postgres.yaml
```

`postgres.yaml` 파일은 3개의 자원을 정의합니다.

1. **Secret**: database의 user, password 등을 설정하기 위해 사용합니다.
2. **Service**: PostgreSQL을 서비스로 노출시키기 위해 사용합니다.
3. **Statefulset**: 실제 PostgreSQL를 유지하는 역할을 합니다.

> [!note]
>
> **Secret**: 외부에 노출되어선 안 되는 민감한 정보(예: 비밀번호, API 키)를 저장하기 위한 리소스입니다. 여기서는 PostgreSQL의 사용자 이름과 비밀번호를 안전하게 저장하여 다른 리소스에서 참조할 수 있도록 합니다.
>
> **StatefulSet**: 상태를 가지는 어플리케이션(예: DB) 배포를 위한 리소스입니다. 일반 Deployment와 달리, 고정된 이름과 스토리지 볼륨을 보장하며, 각 인스턴스가 고유한 ID를 가지고 안정적인 스토리지 연결이 필요한 상황에 적합합니다.

```yaml
# postgres.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: <your_namespace> # You need to replace this with your own namespace
type: Opaque
stringData:
  POSTGRES_USER: myuser
  POSTGRES_PASSWORD: mypassword # Don't use this kind of password in real life. It's just for study.
  POSTGRES_DB: mydb
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: <your_namespace> # You need to replace this with your own namespace
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: <your_namespace> # You need to replace this with your own namespace
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16
          envFrom:
            - secretRef:
                name: postgres-secret
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        selector:
          matchLabels:
            volume: postgres-pv-<your_namespace> # You need to replace this with your own namespace
        resources:
          requests:
            storage: 5Gi
```

이제 다음의 명령어를 입력하여 PostgreSQL Database를 배포해주세요.

```bash
kubectl apply -f postgres.yaml

# 생성된 Secret 확인
kubectl get secret -n <your_namespace>

# 생성된 Service 확인
kubectl get svc -n <your_namespace>

# 생성된 Statefulset 확인
kubectl get statefulset -n <your_namespace>
```

이제 `3-Tier Architecture`를 구성하는 `Data Tier`인 **PostgreSQL Database**를 Kubernetes Cluster에 배포하는 작업을 마무리했습니다.

## 3-2. Backend Deployment on Kubernetes

지금부터는 `3-Tier Architecture`에서 `Application Tier`에 해당하는 **Backend Service**를 Kubernetes Cluster에 배포해보도록 하겠습니다.

### 3-2-1. Database Access를 위한 Secret 생성

방금 생성한 PostgreSQL Database에 Backend Service가 접근하기 위해서는 DB 접속 정보가 필요합니다.

DB 접속 정보에는 Database에 접근하기 위한 **URL**과 인증을 위한 **Password**가 필요하며, Backend Service가 이 정보를 사용할 수 있도록 Kubernetes의 Secret 자원을 생성합니다.

```bash
cd ~/<your_directory\>/kubernetes/backend
vim secret.yaml
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secret
  namespace: <your_namespace> # You need to replace this with your own namespace
type: Opaque
stringData:
  DATABASE_URL: "postgresql://myuser:mypassword@postgres.<your_namespace>.svc.cluster.local:5432/mydb" # You need to replace this with your own namespace
  PASSWORD_SECRET: <your_password_secret> # You need to replace this with your own secret like random string
```

다음의 명령어를 입력하여 PostgreSQL DB에 접속할 수 있는 DB 접속 정보 Secret을 생성해주세요.

```bash
kubectl apply -f secret.yaml
kubectl get secret -n <your_namespace>
```

## 3-2-2. Backend Deployment 생성

DB에 접근하기 위한 Secret 자원 생성을 마쳤다면, 이제 Backend Service를 배포할 차례입니다.

Backend 서비스는 이미 빌드된 Docker Container Image를 사용합니다.

```bash
vim deployment.yaml
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: <your_namespace> # You need to replace this with your own namespace
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
    spec:
      containers:
        - name: api
          image: cjfgml0306/backend:latest
          ports:
            - containerPort: 3000
          envFrom:
            - secretRef:
                name: backend-secret
          resources: # 다음과 같이 Container가 사용할 수 있는 리소스의 크기를 제한할 수 있습니다.
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

```bash
kubectl apply -f deployment.yaml
kubectl get deploy -n <your_namespace>
```

## 3-2-3. Backend Service 생성

`Deployment`를 생성했으면 이와 연결될 `Service`도 함께 생성해주도록 합니다.

```bash
vim service.yaml
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-svc
  namespace: <your_namespace> # You need to replace this with your own namespace
spec:
  selector:
    app: backend-api # deployment.yaml의 spec.selector.matchLabels.app와 일치
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

```bash
kubectl apply -f service.yaml
kubectl get svc -n <your_namespace>
```

지금까지 3-Tier Architecture의 Data Tier와 Application Tier에 대한 배포를 마쳤습니다.

# 4. Frontend Deployment on Kubernetes

## 4-1. Frontend Deployment 배경지식 요약

### 4-1-1. Kubernetes Object: ConfigMap

`4.2.1`에서 `ConfigMap`을 이용하여 설정 파일을 컨테이너에 삽입합니다. 그런데 여기서 사용하는 `ConfigMap`은 무엇일까요?

`ConfigMap`이란 평문으로 설정값을 저장하는 쿠버네티스 오브젝트입니다. Backend에서 활용했던 `Secret`과는 다르게, 외부에 노출되어도 괜찮은 정보들, 가령 URL이나 Port 번호, Log Level 등을 저장하여 여러 Container에서 환경 변수나 파일 형태로 가져와 활용할 수 있습니다.

`Secret`과 비슷하게, `ConfigMap`은 크게 2가지 방법으로 활용할 수 있습니다.

1. `ConfigMap`을 컨테이너의 환경 변수로 사용
2. `ConfigMap`을 컨테이너 내부에 파일로 마운트 (공식 문서 명칭으로 ConfigMap을 `Projection`(투사)한다고 말합니다.)

이번 실습의 Frontend 배포에서 Configmap은 후술할 NGINX의 설정 파일을 추가하는 데에 사용되며, 이를 파일 형태로 가져오기 위한 방법을 `kubernetes/frontend/fe-proxy.yaml` 파일에서 확인할 수 있습니다.

> [!note]
>
> 본 내용은 "시작하세요! 도커/쿠버네티스:친절한 설명으로 쉽게 이해하는 컨테이너 관리"(용찬호 저. 위키북스). pp 344~355의 내용을 일부 활용했습니다. 자세한 사항은 해당 도서를 참고해주시기 바랍니다.

### 4-1-2. React

Meta에서 개발한 Javascript 기반 Frontend 개발 라이브러리입니다. Angular와 Vue와 함께 Frontend 개발을 위해 주로 사용하는 라이브러리입니다.

단일 HTML 페이지에서 Javascript를 통해 페이지를 부분적으로 변경하여 서비스를 제공하는 SPA(Single Page Application) 방식의 웹서비스를 개발할 때 사용하며, 페이지의 구성요소를 Component라는 단위로 쪼개어 개발하고, 웹페이지를 동적으로 구성할 때 페이지 전체를 새로 구성하는 대신, 변경된 부분만을 수정합니다.

웹서비스 뿐만 아니라, 모바일 환경과 같은 네이티브 환경에서 UI를 개발할 때에 사용할 수 있습니다.

> [!note]
>
> 본 실습을 진행하기 위해 React 프로젝트의 소스코드를 이해하지 않아도 되기에 많은 내용을 기술하지는 않았습니다. 하지만 React 코드가 궁금한 경우 `frontend/README.md`에 코드를 이해하는 데에 필요한 정보를 적어두었으니 참고하시기 바랍니다.

### 4-1-3. NGINX

사용자나 브라우저에게 HTML 및 Javascript를 제공하려면, Backend 서버가 사용자 요청에 따라 파일을 전달해주거나 Proxy 서버가 대신 파일을 전달해야 합니다. 전자의 경우 NestJS 서버에 별도의 설정을 통해 HTML 파일을 전달하도록 구성하며, 후자의 경우 NGINX를 도입하여 사용자의 요청을 NGINX가 대신 받고, 요청에 따라 파일을 전달해주거나, Backend 서버에게 요청을 포워딩합니다.

![What-is-proxy](img/proxy.png)

Proxy 서버를 배치할 경우, Backend 서버는 파일을 제공하는 로직을 신경쓰지 않고 서비스에만 집중할 수 있게 되며, Proxy가 일부 요청을 대신 처리하므로 부하 감소를 얻을 수 있습니다.

NGINX는 이러한 목적을 위해 사용할 수 있는 프록시 서버로, 특정 요청에 대해 HTML과 같은 Static File을 대신 전달하거나, 요청에 알맞은 서버에게 요청을 포워딩하거나, 포워딩 과정에서 요청을 적절히 분산하여 부하를 고르게 부여하는 로드밸런싱을 수행할 수 있습니다.

본 실습에서는 React 프로젝트로 생성된 HTML 및 Javascript 파일을 사용자에게 전달하고, 요청을 Backend Server에게 포워딩하는 역할을 수행합니다. 이를 위해 사전에 빌드된 Docker 이미지를 활용할 예정입니다.

## 4-2. Frontend Deployment on Kubernetes

> [!note]
>
> 본 실습은 사전에 빌드된 이미지파일을 사용합니다.  
> 만약 웹UI를 수정하여 배포하고자 하는 경우, `./frontend` 경로에 프로젝트 원본 및 Dockerfile이 저장되어있으므로, 이를 활용하여 코드 수정 후 이미지를 새로 빌드해 활용하시기 바랍니다.

### 4-2-1. Frontend ConfigMap 생성

먼저, HTML 및 Javascript 파일을 NGINX를 통해 브라우저에게 전달할 수 있도록 설정하기 위해, ConfigMap을 생성하도록 하겠습니다.

다음의 명령어로 `fe-proxy-cm.yaml` 파일을 열도록 하겠습니다.

```bash
cd ~/<your_directory\>/kubernetes/frontend
vim fe-proxy-cm.yaml
```

`fe-proxy-cm.yaml` 파일에서 Namespace를 자신의 Namespace로 수정하고, `upstream` 부분의 URL을 Backend 서버의 URL로 수정하겠습니다. 파일 내용은 다음과 같이 구성됩니다.

```YAML
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-proxy-cm
  namespace: <your_namespace>    # EDIT THIS
data:
  app.conf: |    # EDIT THIS
    upstream backend-svc {
      server backend-svc.<your_namespace>.svc.cluster.local:80;
    }
    server {
      listen 80;

      root /usr/share/nginx/html;
      index index.html;

      location /api/ {
        rewrite           ^/api(.*)$ $1 break;
        proxy_pass        http://backend-svc;
        proxy_redirect    off;
        proxy_set_header  Host  $host;
        proxy_set_header  X-Real-IP         $remote_addr;
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Host  $server_name;
      }

      location / {
        try_files $uri /index.html;
      }
    }

```

위의 내용에서 `metadata.namespace`의 값을 자신의 Namespace로 수정하고, `data."app.conf"`의 `upstream.server`의 값을 Backend Service의 URL로 수정해주십시오. (참고: 동일 Cluster 내 Service의 FQDN: `<svc-name>.<namespace>.svc.cluster.local`)

수정 후, 다음의 명령어를 입력하여 ConfigMap을 생성합니다.

```bash
kubectl apply -f ./fe-proxy-cm.yaml
```

이후, 제대로 생성되었는지 확인하기 위해 다음의 명령어를 입력합니다.

```bash
kubectl get cm -n <your_namespace>  # 네임스페이스에 존재하는 ConfigMap 목록 확인
kubectl describe cm nginx-proxy-cm -n <your_namespace> # nginx-proxy-cm의 내용 확인
```

### 4-2-2. Frontend Deployment 생성

다음으로, HTML 파일이 포함된 NGINX Deployment를 생성하도록 하겠습니다.

하단의 명령어를 입력하여 `fe-proxy.yaml` 파일을 열도록 하겠습니다.

```bash
vim ./fe-proxy.yaml
```

`fe-proxy.yaml` 파일의 내용은 다음과 같습니다. 파일 내용에서 `metadata.namespace`의 값을 자신의 Namespace로 수정합니다.

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-proxy
  namespace: <your_namespace>    # EDIT THIS
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-proxy
  template:
    metadata:
      labels:
        app: nginx-proxy
    spec:
      volumes:
        - name: fe-serving-config
          configMap:
            name: nginx-proxy-cm
            items:
              - key: app.conf
                path: app.conf
      containers:
        - name: nginx
          image: "tori209/smartx-fe:latest"
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          volumeMounts:
            - name: fe-serving-config
              mountPath: /etc/nginx/conf.d
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

수정 후, 다음의 명령어를 입력하여 NGINX Deployment를 생성합니다.

```bash
kubectl apply -f ./fe-proxy.yaml
```

이후, 제대로 생성되었는지 확인하기 위해 다음의 명령어를 입력합니다.

```bash
kubectl get deploy -n <your_namespace>  # 네임스페이스에 존재하는 Deployment 목록 확인
kubectl describe deploy nginx-proxy -n <your_namespace> # nginx-proxy의 내용 확인
kubectl get pod -n <your_namespace> # Deployment에 의한 Pod 생성 확인
```

# 5. 배포된 웹 서비스 확인

## 5-1. 브라우저 접근

### 5-1-1. 웹서버 IP 확인

이제, 브라우저를 통해 배포된 웹 서비스에 접근하기 위해 다음을 입력하여 접근할 IP 주소를 확인하겠습니다.

```bash
# `-o wide`: 출력에 더 많은 정보(Cluster-wide IP, Node Name, ...)를 표시합니다.
kubectl get pod -n <your_namespace> -o wide
```

위의 명령을 통해 다음과 같이 출력됩니다. 이 중에서 `nginx-proxy`로 시작하는 Pod의 IP를 복사합니다.

![Deploy List](./img/deploy-complete.png)

위의 예시의 경우, 접근할 IP 주소는 `10.244.2.107`입니다.

> [!NOTE]
>
> 일반적으로 Pod의 Cluster 내부 IP를 이용하여 Pod에 접근할 수 없으나, 장비가 Cluster의 Node로 포함된 경우에 한하여 직접 접근이 가능합니다.
> 이는 각 Node에서 Pod에게 패킷을 전달하기 위해, Kernel Routing Table과 IPTables에 Pod에게 패킷을 전달할 방법을 명시하기 때문입니다.

### 5-1-2. 웹서비스 확인

브라우저의 주소창에 `http://<nginx-ip-addr>`을 입력해 접근합니다. 그러면 다음과 같은 화면이 표시됩니다.

![WebPage_Main](./img/webpage.png)

우리가 배포한 것은 익명 게시판 서비스로, 회원가입 없이 누구나 게시글을 작성하고 조회할 수 있습니다. 현재는 어떠한 게시글도 등록되지 않아 게시글이 보이지 않는 상태입니다. '게시글 작성' 버튼을 눌러 게시글을 추가해보도록 하겠습니다. 버튼을 클릭하면 다음과 같은 화면이 보입니다.

![WebPage_Write](./img/write.png)

원하는 제목과 닉네임, 패스워드, 본문 내용을 작성한 뒤, "작성" 버튼을 클릭합니다.  
그러면 다음과 같이, 자신이 작성한 글을 확인할 수 있습니다.

> [!Note]
>
> Ubuntu 설치 과정에서 한글 입력기를 별도로 추가하지 않았다면, 한글을 입력할 수 없으니 유의 바랍니다.  
> 설정 방법은 이번 실습과 무관하므로 별도로 설명하지 않지만, 인터넷에 다양한 참고 자료가 있으니 이를 활용하시기 바랍니다.

![WebPage_with_post](./img/list-with-post.png)

다음으로, 검색 기능을 확인해보겠습니다. 현 검색 기능은 제목+본문 검색을 수행하니 참고 바랍니다.

![WebPage_Search](./img/post-search.png)

확인이 끝났다면 "게시판 목록"을 클릭하여 되돌아오겠습니다.  
다음으로 자신이 작성한 글을 클릭하여 확인해보겠습니다.

![WebPage_Detail](./img/post-without-comment.png)

화면과 같이 작성했던 제목과 닉네임, 본문 내용을 볼 수 있으며, 댓글 작성칸, 댓글 목록을 확인할 수 있습니다.

이제 댓글을 추가하겠습니다. 원하는 내용을 적고 "댓글 작성" 버튼을 누르면 다음과 같이 확인할 수 있습니다.

![WebPage_WithComment](./img/post-with-comment.png)

이제 게시글을 수정해보겠습니다. "수정" 버튼을 클릭하면 다음과 같은 수정 페이지를 확인할 수 있습니다.

![WebPage_Edit](./img/edit-post.png)

원하는 문구로 수정한 뒤, 올바른 패스워드를 입력하면 수정이 완료됩니다.  
만약 패스워드 오류, 혹은 서버 오류 발생 시 오류 메세지가 출력되니 참고 바랍니다.

추가로, 패스워드도 동일한 방법으로 수정이 가능합니다.

![WebPage_Editing](./img/comment-editing.png)

수정이 완료되면 다음과 같이 확인할 수 있습니다.

![WebPage_AfterEdit](./img/post-after-edit.png)

마지막으로 Post를 삭제하겠습니다. "삭제" 버튼을 누른 뒤, 게시글 패스워드를 입력하여 삭제해주십시오.
그러면 다음과 같이 삭제된 것을 확인할 수 있습니다.

![WebPage_AfterDel](./img/webpage.png)

이것으로 익명게시판의 기능을 모두 점검해보았습니다. 추가로 다른 조원의 서비스에 접근해 확인해보는 것을 권장합니다.

## 5-2. Server 확인하기

> [!TIP]
>
> 후술할 과정으로 하나의 사용자 동작을 처리하기 위해 어떻게 요청이 전달되고 처리되는지 엿볼 수 있습니다.  
> 더 나은 체험을 위해, 직접 웹서비스를 사용해보며 실시간 동작을 확인해보는 것을 권장합니다.

### 5-2-1. NGINX 확인

앞서 언급했듯, NGINX는 요청을 대신 받아 직접 처리하거나, 다른 서버에게 요청을 넘겨주는 역할을 합니다.  
NGINX가 어떻게 요청을 처리했는지 확인하려면 이의 로그를 확인해야 합니다. 이는 다음의 명령어로 확인할 수 있습니다.

```bash
# 이름을 모를 경우 `kubectl -n <your_namespace> get po`로 확인합니다.
kubectl -n <your_namespace> logs <nginx-proxy-pod>
```

로그를 통해 어떤 요청이 다른 서버에게 포워딩되었으며, 어떤 요청을 직접 처리했는지 확인할 수 있습니다.

### 5-2-2. DB 확인

웹서버는 데이터를 저장하기 위해 DB를 사용합니다.  
여러분이 작성한 댓글이나 게시글은 DB에 저장되고, 사용자가 요청을 보낼 때마다 이를 꺼내어 전달해줍니다.

그렇기에, DB의 Table을 확인하면 여러분의 웹서비스 화면에 보여졌던 것과 동일한 내용을 확인할 수 있습니다.

먼저, PostgreSQL DB에 접근하기 위해, DB Pod에 접근하여 CLI 도구를 실행하도록 하겠습니다. 명령은 다음과 같이 입력합니다.

```bash
# 현 설정에서 PostgreSQL Pod의 이름은 postgres-0 입니다. 아닐 경우 `kubectl -n <your_namespace> get po`로 확인합니다.
# `-U`: PostgreSQL에 등록된 사용자 ID 지정
# `-d`: 접근 시 연결할 database 이름
kubectl -n <your_namespace> exec -it po/postgres-0 -- psql -U myuser -d mydb
```

> [!note]
>
> 위의 명령은 "지정한 Pod에서 다음의 명령을 실행한다"는 의미입니다. 옵션은 다음과 같습니다.
>
> | Option           | Description                                                                                                                                                                                             |
> | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
> | `-n <namespace>` | Pod가 위치한 namespace를 지정합니다.                                                                                                                                                                    |
> | `-it`            | `--stdin`(`-i`)와 `--tty`(`-t`) 옵션으로, 사용자 입력(키보드 등)을 `exec` 실행 동안 Pod에게 전달하기 위해 필요합니다.<br>(간단하게, TTY=로컬 콘솔 접근을 위한 드라이버 / PTY=원격 접속을 위한 드라이버) |
> | `-- <cmd>`       | Pod 내부에서 실행할 명령어를 지정합니다. `--`와 `<cmd>` 사이에 공백이 있으므로 주의합니다.                                                                                                              |

그러면 PostgreSQL CLI 도구가 활성화된 것을 볼 수 있습니다.
![psql_start](img/psql_img.png)

다음으로, 존재하는 Table 목록을 조회하기 위해 `\d`을 입력합니다.  
![psql_tables](./img/psql_tables.png)

> [!TIP]
>
> PostgreSQL에서 `\d`는 연결된 Database 내 Table 목록을 출력합니다.  
> 그리고 `\d <table_name>`을 입력하면 Table의 Column 정보를 출력합니다.
>
> 또한, `\d`는 기본 정보만 출력하지만, `\d+`는 여러 세부 정보를 추가로 보여줍니다.

여기서 `Post`가 작성한 게시글을 저장하는 Table이며, `Comment`가 댓글을 저장하는 Table입니다.  
내용을 보기 위해, 다음의 명령을 입력합니다.

```SQL
-- ※ SQL은 `;`으로 끝맺어야 명령 입력이 완료되었다고 인식합니다.
SELECT * FROM "Post";     -- Post 전체 조회
SELECT * FROM "Comment";  -- Comment 전체 조회
```

그러면 여러분이 입력했던 데이터가 출력될 것입니다.  
참고로 Password는 보안을 위해 Hash Function으로 평문을 알아볼 수 없게 처리하니 유의하기 바랍니다.

종료는 `\q`, 혹은 `ctrl+d`를 입력하면 됩니다.

# 6. Lab Review

이번 Lab에서는 `3-tier 구조`의 웹 서비스를 kubernetes 환경에서 배포하는 경험을 해보았습니다.

3-tier 구조는 사용자와 직접 상호작용하는 `Presentation Tier`, Presentation tier에서 발생한 요청을 처리하고 데이터베이스와 통신하는 `Application Tier`, 생성된 데이터를 영구적으로 저장 및 관리하는 `Data Tier`의 형태를 나타냅니다.

이러한 구조를 가진 서비스를 container orchestration 도구인 kubernetes를 이용하여 배포해보았습니다. 실습을 위해 적은 수의 pod가 생성되도록 했지만, 규모있는 실제 서비스를 운영하게 된다면 kubernetes 환경에서 손쉽게 scaling을 할 수 있다는 특성을 바탕으로 적은 노력을 들여 안정적인 서비스를 운영할 수 있을 것입니다.

우리는 yaml 파일을 통한 `선언형` 방식을 통해, kubernetes의 다양한 리소스를 생성할 수 있었고 Frontend, Backend, Database를 배포하여 서비스의 작동을 확인할 수 있었습니다.

또한, Frontend(Presentation Tier)와 Backend(Application Tier) 사이의 proxy server 역할을 하는 NGINX도 사용해보았습니다.

이번 실습을 응용한다면, 여러분은 각자 본인만의 Frontend, Backend 서비스를 개발하고, 이를 Database와 함께 container image로 만든 후, kubernetes 환경에서 배포할 수 있을 것입니다. 이를 통해 구조를 갖춘 하나의 서비스를 개발하는 경험을 해볼 수 있을 것입니다.
