# Lab#6. Analytics Lab

# 0. Objective

이전 Tower Lab에서는 SNMP, Flume, Kafka 등을 이용해서 라즈베리파이의 자원 상태를 InfluxDB에 저장하고, 이를 Chronograf의 대시보드를 통해 시각화 및 모니터링하는 실습을 진행했습니다.

이번 실습에서는 Headlamp를 활용하여 클러스터에서 실행 중인 Pod, Deployment, Service 등의 상태를 확인하고 직접 조작하는 방법을 학습합니다.

## kubectl과 Headlamp의 차이점

쿠버네티스 클러스터는 `kubectl` 명령어를 사용하여 직접 조작할 수 있지만, UI기반 대시보드를 활용하면 시각적인 인터페이스를 통해 클러스터의 상태를 직관적으로 파악하고 조작할 수 있는 장점이 있습니다.

특히, 다음과 같은 이유로 웹UI 기반 대시보드 사용이 유용합니다:

1. 실시간 클러스터 모니터링: 대시보드를 통해 리소스 사용량과 상태를 한눈에 확인
2. 관리 및 디버깅 용이: 명령어 입력 없이 클릭 몇 번으로 리소스를 생성, 수정, 삭제 가능
3. 비전문가 접근성 향상: kubectl 명령어에 익숙하지 않은 사용자도 쉽게 Kubernetes를 운영 가능

# 1. Concept

Headlamp는 웹 UI 기반의 쿠버네티스 사용자 인터페이스입니다.

Headlamp를 사용하면 컨테이너화된 애플리케이션을 쿠버네티스 클러스터에 배포하고, 애플리케이션을 디버깅하며, 클러스터 리소스 관리하는 과정을 보다 쉽게 수행할 수 있습니다.

예를 들어, `Deployment의 Scaling`, `Rolling update`, `Pod restart`, `새로운 애플리케이션 배포` 등을 수행할 수 있습니다.

또한, Headlamp는 클러스터 내 쿠버네티스 리소스의 상태 및 발생한 오류에 대한 정보를 제공하므로, 쿠버네티스 클러스터의 상태를 효과적으로 모니터링하고 관리할 수 있습니다.

&nbsp;

# 이번 실습은 NUC1에서 진행합니다

&nbsp;

# 2. Practice

## 2-1. 쿠버네티스 클러스터 상태 확인

```shell
kubectl get nodes
kubectl get po -n kube-system -o wide
```

위 명령어 입력 시, 아래 사진과 같이 모든 **노드**가 `Ready` 상태이며, 모든 **kube-system**의 Pod가 `Running` 상태여야 합니다.
![cluster status](img/1-cluster-status.png)

## 2-2. Headlamp 설치

아래 명령어를 입력하여 Headlamp를 설치하고,
port-forward를 통해서 Headlamp에 접근할 수 있도록 합니다.

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/headlamp/main/kubernetes-headlamp.yaml
kubectl port-forward -n kube-system service/headlamp 8080:80
```

> [!note]
>
> **`kubectl port-forward`?**
>
> **port-forward**는 로컬 머신에서 클러스터 내부의 서비스에 접근할 수 있도록 합니다.
>
> Headlamp는 기본적으로 **클러스터 내부에서 실행되므로, 외부에서 직접 접근할 수 없습니다.**
>
> kubectl port-forward를 실행하면 로컬 브라우저에서 **추가적인 네트워크 설정 없이 내부 서비스에 접근**할 수 있습니다.

kubectl port-forward 명령어 입력 후 port-forward가 실행되면, 새로운 터미널에서 작업을 이어갑니다. 새로운 터미널을 열어주세요!

> [!tip]
>
> **새로운 터미널 열기 단축키 `Ctrl + Shift + T`**

## 2-3. Headlamp 접근을 위한 토큰 발급

Headlamp에 로그인하려면 인증이 필요하며, 이를 위해 `Service Account`와 `ClusterRoleBinding`을 생성하여 **관리 권한을 부여하고, 해당 계정의 토큰**을 발급해야 합니다.

아래 명령어를 실행하여 **headlamp-admin**라는 서비스 계정을 만들고, 이를 **클러스터 관리자(admin) 역할**과 바인딩한 후, 로그인에 사용할 토큰을 생성합니다.

### Service Account

```shell
kubectl -n kube-system create serviceaccount headlamp-admin
```

### ClusterRoleBinding

admin-user 서비스 계정이 클러스터 관리자(admin) 권한을 가지도록 설정합니다.

```shell
kubectl create clusterrolebinding headlamp-admin --serviceaccount=kube-system:headlamp-admin --clusterrole=admin
```

### 로그인 토큰 발급

위에서 생성한 headlamp-admin 계정의 인증 토큰을 발급합니다. 이 토큰을 사용하여 Headlamp에 로그인할 수 있습니다.

```shell
kubectl create token headlamp-admin -n kube-system
```

토큰 발급이 성공적으로 이뤄지면, 아래 사진과 같이 터미널에 해당 토큰이 출력됩니다. 이 토큰은 Headlamp 로그인 화면에서 사용하게 됩니다.

![token](img/2-dashboard-token.png)

## 2-3. Headlamp 접근

이제 Headlamp에 접근해봅시다. 아래 주소를 브라우저에 입력해 Headlamp에 접근해보세요!

<http://localhost:8080/>

> [!warning]
>
> ⚠️ **오류 발생 시, `kubectl port-forward` 명령어가 제대로 실행됐는지 확인해주세요!**

&nbsp;

실습과정을 정상적으로 수행했을 경우, 아래와 같이 로그인 화면을 볼 수 있습니다. 방금 전 발급 받은 토큰을 입력하고 `Authenticate` 버튼을 클릭하여 로그인합니다.

![signin](img/3-dashboard-login.png)

&nbsp;

로그인 성공 시, 아래 사진과 같이 Headlamp에 접근할 수 있습니다.

![ui](img/3-dashboard-enter.png)

&nbsp;

> [!warning]
>
> ⚠️ **오류 발생 시** 아래 공식 문서 참고
>
> <https://headlamp.dev/docs/latest/installation/in-cluster/>

## 2-4. Headlamp에서 Pod 삭제

이제 대시보드에서 현재 실행 중인 Pod를 삭제하겠습니다. 아래 사진과 같이 진행 후 `새로고침`을 눌러주세요!

![pod delete](img/4-pod-delete.png)

아래 사진을 보면 알 수 있듯이, `Evict`한 Pod는 현재 `Terminating` 상태입니다.

또한 새로운 Pod가 생성된 것을 알 수 있는데요, 현재 대시보드를 통해 보고있는 Pod들은 `Deployment`에 의해 배포되었기 때문에 `replica` 수 유지를 위해 새로운 Pod가 생성된 것입니다.

### 2-4-1. Review: 쿠버네티스의 `Self-healing` 기능

![pod delete dashboard](img/4-pod-delete-result-dashboard.png)

터미널을 통해서도 똑같은 결과를 확인해볼 수 있습니다.

```shell
kubectl get pod
```

![pod delete terminal](img/4-pod-delete-result-terminal.png)

## 2-5. Headlamp에서 Deployment Scaling

이번에는 지난 Cluster Lab에서 수행한 Deployment Scaling을 해보겠습니다.

아래 사진처럼 `Deployments` 탭에 들어가서, `simple-app-deployment`를 클릭해주세요.

![deployment](img/5-deploy.png)

&nbsp;

사진과 같이 우측 상단에 `Scale resources` 버튼을 클릭해주세요.

![deployment - 1](img/5-deploy-2.png)

&nbsp;

사진과 같이 `replicas`의 수를 `10`으로 수정하고 `Scale 버튼`을 클릭해주세요. (다른 숫자로 수정해도 괜찮습니다.)

![deployment - 2](img/5-deploy-3.png)

&nbsp;

이제 Deployments가 관리하는 Pod의 수가 10개가 된 것을 확인할 수 있습니다.

![deployment - 3](img/5-deploy-4.png)

&nbsp;

대시보드의 `Pods` 탭과 터미널에서도 같은 결과를 확인할 수 있습니다.

![deployment - 4](img/5-deploy-5.png)

&nbsp;

```shell
kubectl get pod
```

![deployment - 5](img/5-deploy-6.png)

## 2-6. Headlamp에서 클러스터 이벤트 확인하기

Headlamp에서는 클러스터 내에서 발생하는 다양한 이벤트를 실시간으로 확인할 수 있습니다.

이벤트는 Pod, Deployment, Service, Node 등의 리소스에서 발생하는 상태 변화나 경고 메시지를 포함하며, 예를 들어 다음과 같은 내용을 확인할 수 있습니다:

- Pod 상태 변화: 생성(Create), 스케줄링(Scheduling), 종료(Terminated), 재시작(Restart) 등
- 컨테이너 관련 오류: CrashLoopBackOff, ImagePullBackOff, OOMKilled(메모리 초과 종료) 등
- 스케줄링 문제: 리소스 부족(Insufficient CPU/Memory), 노드 부족(No Nodes Available) 등
- 네트워크 문제: Service 연결 실패, DNS 해결 불가 등의 오류
- 스토리지 오류: PVC(PersistentVolumeClaim) 바인딩 실패, 볼륨 마운트 실패 등

이벤트 로그를 활용하면 클러스터 내에서 발생하는 문제를 신속하게 파악하고, 디버깅하는 데 큰 도움을 받을 수 있습니다.

&nbsp;

이제 `Clusters` 탭으로 이동해서 여러 페이지를 둘러봅니다.

![event - 1](img/6-events-1.png)

대시보드를 통해 오류가 발생한 이벤트도 확인할 수 있으며, 아래와 같이 오류 메시지를 확인하여 원인을 분석할 수 있습니다.

## 2-7. Headlamp에서 노드 정보 접근

이번에는 노드(Node) 정보에 접근해보겠습니다.

`Nodes 탭`에 접근하면 아래 사진과 같이 노드 정보를 볼 수 없는 상황이 발생할 수 있습니다.

![node forbidden](img/7-node-forbidden.png)

### 왜 노드 정보에 접근할 수 없는가?

쿠버네티스는 보안 강화를 위해 기본적으로 일반 사용자(ServiceAccount)에게 노드 정보 접근을 제한합니다.

화면에 표시된 오류 메시지를 보면 다음과 같은 내용이 포함되어 있습니다:

```shell
nodes is forbidden:
User "system:serviceaccount:kubernetes-dashboard:admin-user"
cannot list resource "nodes" in API group ""
at the cluster scope
```

이는 admin-user 서비스 계정이 노드 정보를 조회할 수 있는 권한이 없기 때문입니다.

#### 쿠버네티스의 보안 기능

- 노드(Node) 정보 및 관리는 클러스터의 핵심 기능 중 하나로, 임의의 사용자에게 노출될 경우 보안 문제가 발생할 수 있습니다.
- 특히, 노드의 상태, 리소스 사용량, 구성 정보 등이 외부에 노출될 경우 클러스터 전체 운영에 영향을 줄 수 있기 때문에, 기본적으로 노드 조회 권한이 제한됩니다.
- 관리자 권한이 부여된 계정만 노드 정보를 확인할 수 있도록 하는 것이 쿠버네티스의 보안 정책입니다.

따라서, 노드 정보를 확인하려면 추가적인 권한(RoleBinding 또는 ClusterRoleBinding) 설정이 필요합니다.

# 3. Review

## Lab Summary

이번 실습에서는 Headlamp를 활용하여 클러스터 내 리소스 상태를 시각적으로 모니터링하고 조작하는 방법을 학습했습니다.

특히, Pod, Deployment, Service 등의 리소스를 관리하는 방법과 함께, 대시보드를 통해 이벤트 로그를 확인하는 과정을 실습했습니다.

또한, kubectl을 이용한 명령어 기반 조작과 대시보드의 차이점을 비교하며, GUI 환경에서 쿠버네티스를 운영하는 장점을 배웠습니다.

## 컨테이너 오케스트레이션에 대시보드가 필요한가?

컨테이너 오케스트레이션 환경에서 대시보드는 **운영 효율성과 가시성**을 높이는 중요한 도구입니다.

**kubectl**과 같은 **CLI(Command Line Interface)** 명령어를 이용해 모든 작업을 수행할 수도 있지만, 대시보드를 활용하면 클러스터의 상태를 직관적으로 확인하고, 실시간으로 리소스를 관리할 수 있습니다.

대시보드가 필요한 몇 가지 이유는 다음과 같습니다:

1. **실시간 클러스터 모니터링 시각화**
   - CLI 기반 kubectl 명령어로는 텍스트 기반 출력을 확인해야 하지만, 대시보드에서는 CPU, 메모리 사용량, Pod 상태 등을 별도의 명령어 없이 한눈에 파악할 수 있습니다.
2. **관리 및 디버깅 용이성**
   - kubectl을 사용할 경우, 로그 확인이나 이벤트 분석을 위해 여러 명령어를 조합해야 하지만, 대시보드에서는 클러스터 내 오류나 이벤트를 즉시 확인하고 분석할 수 있습니다.
3. **비전문가 접근성 향상**
   - 개발자가 아닌 운영팀, DevOps 엔지니어 또는 관리자가 클러스터를 쉽게 모니터링하고 조작할 수 있도록 돕습니다.
   - 물론 비전문가의 쿠버네티스 클러스터 접근은 주의해야합니다.

결론적으로, 대시보드는 CLI만으로는 부족할 수 있는 쿠버네티스 클러스터 운영의 가시성을 보완하고, 더욱 직관적인 관리를 가능하게 하는 핵심적인 도구입니다.

## 주요 과정 요약

이번 실습에서 수행한 주요 과정은 다음과 같습니다:

1. Headlamp 설치 및 접근
   - kubectl apply를 이용해 대시보드를 설치하고, kubectl proxy를 실행하여 웹 대시보드에 접근.

2. 대시보드 로그인 및 인증 토큰 발급
   - ServiceAccount 및 ClusterRoleBinding을 생성하여 관리 권한을 부여하고, admin-user의 로그인 토큰을 발급하여 대시보드에 로그인.

3. 대시보드를 활용한 리소스 조작 실습
   - Pod 삭제: Deployment에 의해 새로운 Pod가 자동 생성되는 Self-healing 기능 확인
   - Deployment Scaling: Replica 개수를 조정하여 동적으로 리소스를 확장

4. 클러스터 이벤트 로그 확인
   - Events 탭에서 Pod, Deployment, Service 등에서 발생한 이벤트를 확인

5. 노드 정보 접근 제한 확인
   - 기본적으로 admin-user 계정이 노드 정보를 조회할 수 없도록 보안 정책이 적용됨을 확인
   - 쿠버네티스의 보안 정책을 이해하고, 필요할 경우 권한을 추가해야 함을 인식
