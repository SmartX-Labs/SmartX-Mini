# Lab#6. Analytics Lab

## 0. Objective

As we did at Tower Lab, this time we will use the kubernetes dashboard to visualize the resource share of each pod in a cloud-native environment for efficient operation.

This lab aims to deploy the kubernetes dashboard in the form of .yaml.

## 1. Concept

Dashboard is a web-based Kubernetes user interface. You can use Dashboard to deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources. You can use Dashboard to get an overview of applications running on your cluster, as well as for creating or modifying individual Kubernetes resources (such as Deployments, Jobs, DaemonSets, etc). For example, you can scale a Deployment, initiate a rolling update, restart a pod or deploy new applications using a deploy wizard.

Dashboard also provides information on the state of Kubernetes resources in your cluster and on any errors that may have occurred.

### 2-1. K8s 클러스터 재설정 작업 진행(re-config K8s cluster)

#### hostname 설정(hostname config)

```shell
# From NUC 1 :
sudo hostname nuc01
# From NUC 2 :
sudo hostname nuc02
# From NUC 3 :
sudo hostname nuc03
```

#### swapoff

```shell
# From All NUCs
sudo swapoff -a
sudo sed -e '/\/swapfile/s/^/#/g' -i /etc/fstab
sudo sed -e '/\/swap\.img/s/^/#/g' -i /etc/fstab
```

#### Kubernetes Master Setting(For NUC1)

```shell
# From NUC1
sudo kubeadm reset -f
sudo rm -rf /etc/cni/net.d
sudo ipvsadm --clear
```

```shell
# From NUC1
## Cleanup Rook Configuration
sudo rm -rf /var/lib/rook
sudo kubeadm init --ignore-preflight-errors=all
```

```shell
# From NUC1
## make kubectl work for your non-root user.
rm -r $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl taint nodes --all node-role.kubernetes.io/master-
```

#### Kubernetes Worker Setting(For NUC2, NUC3)

```shell
# From NUC2, NUC3
sudo kubeadm reset -f
sudo rm -r /etc/cni/net.d
sudo ipvsadm --clear

## Cleanup Rook Configuration
sudo rm -rf /var/lib/rook
```

![commnad](img/9.png)

```shell
# From NUC2, NUC3
## NUC1의 명령어를 sudo 권한으로 실행(sudo 권한 필수!)
## execute NUC1's command with sudo previlege(sudo previlege required!)
sudo kubeadm join <NUC1 IP>:6443 --token <YOUR TOKEN> --discovery-token-ca-cert-hash <YOUR HASH>
```

```shell
# From NUC1
kubectl apply -f "https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s-1.11.yaml"
```

#### Check K8s Cluster status

```shell
# From NUC1 -> check status
kubectl get nodes
kubectl get po -n kube-system -o wide
```

![nodes-status.png](img/nodes-status.png)

#### 2-2. install kubernetes Dashboard

```shell
# From NUC1
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml
kubectl proxy
```

![nodes-status.png](img/ui-dashboard.png)

if you encounter the error please refer to offical docs or search! it's debug!
https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
