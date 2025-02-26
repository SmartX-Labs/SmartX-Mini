# Lab#6. Analytics Lab

## 0. Objective

As we did at Tower Lab, this time we will use the kubernetes dashboard to visualize the resource share of each pod in a cloud-native environment for efficient operation.

This lab aims to deploy the kubernetes dashboard in the form of .yaml.

## 1. Concept

Dashboard is a web-based Kubernetes user interface. You can use Dashboard to deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources. You can use Dashboard to get an overview of applications running on your cluster, as well as for creating or modifying individual Kubernetes resources (such as Deployments, Jobs, DaemonSets, etc). For example, you can scale a Deployment, initiate a rolling update, restart a pod or deploy new applications using a deploy wizard.

Dashboard also provides information on the state of Kubernetes resources in your cluster and on any errors that may have occurred.

#### Check K8s Cluster status

```shell
# From NUC1 -> check status
kubectl get nodes
kubectl get po -n kube-system -o wide
```

![nodes-status.png](img/nodes-status.png)

#### 2-1. install kubernetes Dashboard

```shell
# From NUC1
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml
kubectl proxy
```

#### 2-2. Issue Dashboard token
Cluster role binding
```shell
cat <<EOF | kubectl create -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF
```
Service account
```shell
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
EOF
```
Get token
```shell
kubectl -n kubernetes-dashboard create token admin-user
```
#### 2-3. Access Dashboard

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
![image](https://github.com/SmartX-Labs/SmartX-Mini/assets/53600533/7acd0b5f-06ce-4c32-bbfa-6b0d11aff6f8)
Paste the token you generated just before.
![nodes-status.png](img/ui-dashboard.png)

if you encounter the error please refer to offical docs or search! it's debug!
https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
