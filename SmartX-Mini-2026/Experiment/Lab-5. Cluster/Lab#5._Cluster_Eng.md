# Lab#5. Cluster Lab

# 0. Objective

Kubernetes is a container orchestration tool that automates the deployment, scaling, and management of containerized applications.

In this Lab#5 Cluster, we will build a Kubernetes cluster using 3 NUC machines, deploy a simple application, and learn the concept of container orchestration.

The 3 NUC machines will play the following roles in the Kubernetes cluster:

- 1 Master Node (Control Plane) → NUC1
- 2 Worker Nodes → NUC2, NUC3

## What is the Master-Worker Architecture?

![master-worker pattern](img/master-worker.png)

The Master-Worker pattern is a software architecture pattern where one master manages the entire system, and multiple workers perform individual tasks. This pattern maximizes performance through parallel processing and supports excellent scalability by allowing dynamic addition or removal of worker nodes.

In Kubernetes, the master-worker structure is applied to cluster management. The Master (Control Plane) manages the cluster's state and schedules workloads to ensure applications run smoothly on the worker nodes. Worker nodes run the actual applications and deploy/manage Pods (containers). If a worker node goes down or fails, Kubernetes detects it and uses the scheduler to deploy a new Pod on another worker, ensuring uninterrupted service.

Thanks to these characteristics, the master-worker architecture is widely used in cluster management with Kubernetes, distributed data processing with Hadoop and Spark, parallel computing with Ray, and multithreaded applications.

# 1. Concept

## 1-1. Docker Containers

![docker icon](img/docker.png)

**Docker** is an open-source platform that uses container technology to simplify the development, deployment, and execution of applications. Docker packages applications with their dependencies and runtime into a single unit (container), enabling deployment independent of the operating system environment.

### Differences Between Docker Containers and Virtual Machines (VMs)

Compared to Virtual Machines, Docker containers offer a lighter and faster runtime environment and more efficient resource usage.

![docker diagram](img/docker-diagram.png)

### Left Side of the Image

- **Virtual Machines (VMs)**: Use a hypervisor to run multiple guest OS instances. Each OS consumes separate resources, making VMs heavier and slower to boot.
- **Docker Containers**: Share a single OS kernel while running in isolated environments. Containers are lightweight as they include only the necessary application and libraries, enabling fast and flexible deployment.

### Right Side of the Image

Docker operates based on a client-server architecture and consists of the following components:

1. Developer(docker client) runs Docker commands:
   - Uses commands like `docker build`, `docker pull`, and `docker run`.

2. Docker Daemon(Server) handles the operations:
   - Creates and manages containers and Docker images.
   - Actually executes the commands issued by the developer.

3. Image Registry:
   - Container images for applications are stored in remote registries like `Docker Hub`.
   - Cloud-based registries like AWS ECR or private registries can also be used.

## 1-2. Container Orchestration

As container technology became widely used, there arose a need for a system that could automatically deploy, manage, and scale large numbers of containers. Container orchestration emerged to solve this problem.

### Why Is Container Orchestration Necessary?

1. **Increased Number of Containers to Manage**
   - Managing a few containers on a single server is simple, but in large-scale applications involving **hundreds or thousands of containers**, it becomes challenging.

2. **Automation and Management Efficiency**
   - Functions like automated deployment, network configuration, load balancing, monitoring, and self-healing upon failure are essential.

3. **High Availability & Scalability**
   - When a container crashes, it should restart automatically; when traffic surges, the number of containers should scale up dynamically.

Key features include:

1. **Automated Deployment and Updates**
   - Automatically deploy containers and perform gradual updates (Rolling Update) when a new version is released.

2. **Load Balancing & Service Discovery**
   - Distributes traffic across multiple containers and automatically sets up communication between containers.

3. **Self-healing**
   - Detects and replaces failed containers to prevent service disruption.

4. **Cluster Resource Optimization**
   - Efficient scheduling of containers to utilize CPU, memory, and other cluster resources.

![container orchestration tool](img/container-orch.png)

The image above shows popular container orchestration tools. **Kubernetes(K8s)** is currently the most widely adopted.

It’s also known as K8s, where the 'K' is the first letter, 's' is the last, and '8' stands for the number of letters in between.

## 1-3. Kubernetes

![k8s arch](img/k8s-arch.png)

[**Kubernetes**](https://kubernetes.io/) is an **open-source orchestration system** that automates the deployment, scaling, and management of containerized applications.

### 1-3-1. **Key Features of Kubernetes**

- **Horizontal Scaling**: Scale applications easily via command-line, UI, or CPU-based auto-scaling mechanisms.
- **Self-healing**: Automatically restarts failed containers, reallocates containers from failed nodes, and kills containers that fail health checks. Faulty nodes or containers remain invisible to clients until resolved.
- **Service Discovery & Load Balancing**: Assigns each container a unique IP and enables DNS-based service discovery. Also provides load balancing to distribute traffic.
- **Storage Orchestration**: Easily mounts local or cloud storage (NFS, Ceph, AWS EBS, GCP Persistent Disk, etc.) to containers.

Kubernetes is the most widely used container orchestration tool in both **cloud environments (AWS, GCP, Azure) and on-premises environments**.

# 2. Lab Preparation

![Lab Preparation](img/network.png)

## 2-1. Perform the Following Steps on All NUCs

### 2-1-1. Set Hostname

The command `sudo hostname <name>` temporarily sets the hostname of the current node (machine) to `<name>`. However, this setting only applies to the current login session, so once you open a new terminal or reboot the node, it will revert to the previous hostname. For convenience in building the Kubernetes cluster during this lab, we will change the hostname for each NUC.

\*Ask your TA for the assigned role of nuc01, nuc02, and nuc03.

#### Temporarily Change Hostname

```shell
# At NUC 1 :
sudo hostname nuc01
# At NUC 2 :
sudo hostname nuc02
# At NUC 3 :
sudo hostname nuc03
```

#### Check the Temporarily Changed Hostname

```shell
# The output should be nuc01, nuc02, or nuc03 depending on the role.
hostname
```

The file `/etc/hostname` stores the hostname that will be used during system boot. Using `echo <hostname>` to write the new hostname into `/etc/hostname` ensures that the hostname change persists after reboot. However, editing `/etc/hostname` does not apply the change to the current session immediately. To apply it immediately, you must also run `sudo hostname <name>`. (But we've already done that just now, so it's fine.)

```shell
sudo rm /etc/hostname
hostname | sudo tee /etc/hostname
```

> [!Note]
>
> The output of `hostname` is piped (`|`) and written to the `/etc/hostname` file.

### 2-1-2. Register Hosts' IP Information

Each node must register the IP information for nuc01, nuc02, and nuc03 in its hosts file. Perform the following steps on **all NUCs**.

Edit the `/etc/hosts` file:

```shell
sudo vim /etc/hosts
```

Paste the following context and save the file:

```text
 <IP Address of NUC 1>  nuc01
 <IP Address of NUC 2>  nuc02
 <IP Address of NUC 3>  nuc03
```

### 2-1-3. Verify Connectivity

Use the `ping` command to verify whether the nodes can successfully reach each other.

> [!note]
>
> `ping` is a command used to test the network connectivity to a specific host. It sends an ICMP Echo Request packet to the target, and if the host replies with an ICMP Echo Reply, the connection is considered successful. You can also check for response time (RTT), network latency, and packet loss.

```shell
# At NUC 1
ping nuc02
ping nuc03

# At NUC 2
ping nuc01
ping nuc03

# At NUC 3
ping nuc01
ping nuc02
```

### 2-1-4. Enable Remote Access

Run the following command on each node to install the necessary package that allows remote access from other nodes.

```shell
sudo apt install -y openssh-server
```

### 2-1-5. Configure containerd

```bash
# For All NUCs
sudo apt-get update
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
```

### 2-1-6. At NUC1

Run the following commands on NUC1 to verify that you can remotely access NUC2 and NUC3.

> [!Warning]
>
> In the case of the CS lab, the `<nuc username>` is commonly set to `gist`.

```shell
# In new terminal
# e.g. ssh gist@nuc02
ssh <nuc2 username>@nuc02

# In another new terminal
# e.g. ssh gist@nuc03
ssh <nuc3 username>@nuc03
```

### 2-1-7. Reboot All NUCs

```shell
# For All NUCs
sudo reboot
```

# From now on, all tasks will be performed from the seat assigned to NUC1. Students using NUC2 and NUC3 should move to the NUC1 seat and work together

## 2-2. Preparations for Clustering

```shell
# From All NUCs
docker version
```

# At NUC1

Connect remotely from NUC1 to both NUC2 and NUC3.

```shell
# In a new terminal
ssh <NUC2 username>@nuc02

# In a new terminal
ssh <NUC3 username>@nuc03
```

> ## Screen Setup Tip (optional)
>
> Managing multiple windows can be inconvenient. Instead, open 3 terminal **tabs** and connect to NUC2 and NUC3 on the second and third tabs respectively, as shown below.
>
> The shortcut to open a new terminal tab is `Ctrl + Shift + T`.
>
> ![screen setup](img/screen-setup.png)

## 2-3. Kubernetes Installation (For All NUCs)

![Kubernetes Installation](img/nuc-prep.png)

- NUC 1 : Master
- NUC 2 : Worker 1
- NUC 3 : Worker 2

### 2-3-1. Swapoff

**Swap memory** is a feature that uses part of the disk as virtual memory when physical RAM is insufficient. However, Kubernetes needs to accurately track memory usage for scheduling, and using swap can cause unpredictable performance issues. In particular, memory limits might not be enforced correctly, or response time may suffer. Therefore, Kubernetes requires swap to be disabled for stable cluster operation.

```shell
# From All NUCs
sudo swapoff -a
```

The above command temporarily disables the use of swap memory. Therefore, after rebooting the NUC, you would need to run the same command again to disable swap memory, which can be inconvenient.  
To make swap memory remain disabled even after reboot, we will modify the following file. Please open the file.

```shell
sudo vim /etc/fstab
```

In the contents of the file, look for a line with the following format and add a # symbol at the beginning to comment it out.

> [!CAUTION]
>
> Be very careful not to modify anything other than the line related to swap memory, as making a mistake here can lead to critical system errors.  
> Please add a `#` symbol at the beginning of the line, not add a new line.

```text
# /swap.img      none   swap  sw    0  0 # As shown in this example, please add a `#` symbol at the beginning of the line.
```

### 2-3-2. Install Kubernetes

> [!warning]
>
> Make sure each step completes successfully before proceeding.

```shell
# At All NUCs
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl gpg

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update

sudo apt install -y kubeadm=1.34.6-1.1 kubelet=1.34.6-1.1 kubectl=1.34.6-1.1
```

Please execute the following command to open the file.
In Kubernetes, a module is required to enable iptables rules for bridged traffic. If this module is missing, kubeadm initialization will fail.
Let’s add the necessary configuration related to this.

```shell
sudo vim /etc/modules-load.d/modules.conf
```

If the `br_netfilter` entry is not present in the file, please add it.  
**Please enter only br_netfilter as shown in the example, without the ... .**

```text
...

br_netfilter #If this part is not present in the file, please add it.

...
```

By adding this entry, the bridge-nf-call-iptables kernel module will automatically load even after the NUC is rebooted.
Since this change will take effect only after a reboot, let’s manually load the bridge-nf-call-iptables kernel module for now using the following commands.

```shell
sudo modprobe br_netfilter
lsmod | grep br_netfilter
```

If `br_netfilter` appears in the terminal output, it means the module has been successfully loaded.

With that, the preparation to build a Kubernetes cluster is complete.

## 2-4. Kubernetes Configuration

Now let’s build the Kubernetes cluster.

### 2-4-1. Kubernetes Master Setting(For NUC1)

Now, proceed with the following commands to configure the master node:

```shell
# From NUC1
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

> [!warning]
>
> ⚠️ **If a preflight error occurs, follow the instructions below:**
>
> ![preflight error](img/preflight-error.png)
>
> **Cause of Error**
>
> This issue occurs when the `bridge-nf-call-iptables` kernel module is missing or not loaded. Kubernetes requires this module to enable iptables rules for bridged traffic. If it's not loaded, kubeadm initialization fails.
>
> **How to Fix**
>
> ```shell
> # Load the br_netfilter kernel module
> sudo modprobe br_netfilter
> # Verify that it has been loaded
> lsmod | grep br_netfilter
> # Run kubeadm again
> sudo kubeadm init --pod-network-cidr=10.244.0.0/16
> ```

<!-- -->

> [!note]
> If the installation does not proceed normally, please check the `SystemdCgroup` setting, swapoff status, and `br_netfilter` setting again.

If the `kubeadm` command runs successfully, it will generate a command including a token to allow other nodes to join the cluster. Save this command in a text file or somewhere secure so it doesn't get lost.

![kubeadm init](img/kubeadm-init.png)

Now run the following commands on NUC1:

```shell
# At NUC1
# rm -r $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
# The following command allows the master node to run Pods like a worker node (not required for this lab)
# kubectl taint nodes --all node-role.kubernetes.io/master-
```

### 2-4-2. Kubernetes Worker Setting (For NUC2, NUC3) [Used when resetting the cluster. Not required on first setup!]

```shell
# From NUC2, NUC3
# sudo kubeadm reset -f
# sudo rm -r /etc/cni/net.d
# sudo ipvsadm --clear
```

### 2-4-3. Worker Join

Now join the Worker Nodes to the Kubernetes cluster.

![kubeadm init](img/kubeadm-init-2.png)

Copy the command inside the red box and prepend `sudo` when running it on <ins>NUC2 and NUC3</ins>.

> [!warning]
>
> **Please don't enter the previous command on NUC1**
>
> **If a preflight error occurs**, append `--ignore-preflight-errors=all` to the end and re-run the command.

### 2-4-4. Check Nodes at NUC1

```shell
# At NUC1
kubectl get node
```

![get node not ready](img/get-node-notready.png)

In the above image, nuc02 and nuc03 are in a NotReady state because the **network plugin (CNI)** is not yet installed, or the worker nodes did not join properly. Kubernetes does not mark nodes as Ready until networking is configured. We'll install the CNI plugin next to resolve this.

## 2-5. Kubernetes Network Plugin Installation at NUC1

### What is CNI?

**CNI(Container Network Interface)** is a standard interface used by Kubernetes to configure and manage container networking. Kubernetes does not provide networking capabilities by itself, so it relies on CNI plugins to enable communication between Pods.

### What is Flannel?

`Flannel` is one of the most commonly used CNI plugins in Kubernetes. It provides a simple overlay network that enables communication between Pods. Flannel uses mechanisms such as VXLAN or Host-GW to implement the network and focuses on basic Pod-to-Pod communication without complex network policy management. Other alternatives include Calico, Cilium, and Weave.

```shell
# At NUC1
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

```shell
# At NUC1 -> Check node status
kubectl get nodes
```

After installing Flannel CNI, wait a moment and run the above command. You should now see the worker nodes’ status change to Ready.

![get node ready](img/get-node-ready.png)

```shell
# At NUC1 -> Check all Pods in the kube-system namespace
kubectl get po -n kube-system -o wide
```

> [!note]
>
> **Command Explanation**
>
> `kubectl get po -n kube-system -o wide`
>
> - `kubectl get po` → Lists Pods currently running in the cluster.
> - `-n kube-system` → Only queries Pods in the `kube-system` namespace.
> - `-o wide` → Displays additional details like Pod IP and node location.
>
> This shows the state of Kubernetes system components like Flannel, DNS, and Scheduler.
>
> For more details, refer to the [official Kubernetes documentation](https://kubernetes.io/ko/docs/concepts/overview/components/).

![kube-system](img/kube-system.png)

With this, the Kubernetes cluster's network is fully configured. Pods can now communicate with each other using Flannel, and we are ready to deploy applications in the cluster.

# 3. kubernetes example at NUC1

Let’s deploy a simple website within the Kubernetes environment.

All steps will be executed on **NUC1**.

## 3-1. Service Architecture

The service architecture to be deployed in **Section 3** is as follows. A `Service` receives external requests and routes traffic to one of the `Pods` managed by a `Deployment`.

![my-simple-app architecture](img/simple-app/my-simple-app-arch.png)

## 3-2. Application Code (v1) Overview

This is the application code that we will use. You do not need to write it yourself — the image is pre-uploaded to Docker Hub. **However, understanding the code is important.**

```python
from flask import Flask
import os

app = Flask(__name__)

# If you access this path through browser
@app.route('/')
def home():
    # 1. Get the running Pod name from the environment variable
    pod_name = os.getenv('POD_NAME', 'Unknown Pod')
    # 2. Show the Pod name on the browser.
    return f"Hello from {pod_name}! <br> This is the simple-app version 1. <br>"

if __name__ == '__main__':
    # You need to access the port 5000
    app.run(host='0.0.0.0', port=5000)
```

- When accessed via a browser, this application prints the **Pod name and version**.
- So, if multiple Pods run the same app, **you’ll get different responses depending on which Pod serves the request.**

## 3-3. Deploy my-simple-app on `Pod`

A Pod is the **smallest deployment unit** in Kubernetes and provides the execution environment for a container.

Typically, one Pod contains one container, and Kubernetes manages applications at the Pod level.

1. Create and move to a working directory:

   ```shell
   cd ~
   mkdir k8s
   cd k8s
   ```

2. Create and apply the Pod definition file:

   Create `simple-app.yaml` and input the following code:

   ```shell
   vim simple-app.yaml
   ```

   Contents of `simple-app.yaml`:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: simple-app
     labels:
       app: simple-app
   spec:
     containers:
       - name: simple-app
         image: cheolhuikim/my-simple-app:v1
         ports:
           - containerPort: 5000
         env:
           - name: POD_NAME
             valueFrom:
               fieldRef:
                 fieldPath: metadata.name
   ```

   ```shell
   kubectl apply -f simple-app.yaml
   ```

3. Verify that the Pod was successfully created:

   ```shell
   kubectl get pod -o wide
   ```

   ![simple 1](img/simple-app/simple-1.png)

4. After checking the Pod's IP address, access it via web browser:

   ```shell
   http://<POD_IP>:5000
   ```

   ![simple 2](img/simple-app/simple-2.png)

5. Delete the Pod:

   ```shell
   kubectl delete -f simple-app.yaml
   kubectl get pods
   ```

   ![simple 3](img/simple-app/simple-3.png)

6. Refresh the browser to confirm that the service has been terminated.

## 3-4. Deploy my-simple-app with `Deployment`

### What is a Deployment?

A Deployment is a Kubernetes controller that automates Pod creation and management.

It supports managing multiple Pods, scaling, rolling updates, and recovery.

1. Create and apply the Deployment definition file:

   ```shell
   vim simple-app-deployment.yaml
   ```

   `simple-app-deployment.yaml`

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: simple-app-deployment
     labels:
       app: simple-app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: simple-app
     template:
       metadata:
         labels:
           app: simple-app
       spec:
         containers:
           - name: simple-app
             image: cheolhuikim/my-simple-app:v1
             ports:
               - containerPort: 5000
             env:
               - name: POD_NAME
                 valueFrom:
                   fieldRef:
                     fieldPath: metadata.name
   ```

   ```shell
   kubectl apply -f simple-app-deployment.yaml
   kubectl get pods -o wide # Check that the multiple pods are running
   ```

   ![simple 4](img/simple-app/simple-4.png)

2. Check each Pod's IP address and verify in the browser that the response differs for each Pod.

   ```shell
   http://<POD_IP>:5000
   ```

   ![simple 5](img/simple-app/simple-5.png)
   ![simple 6](img/simple-app/simple-6.png)
   ![simple 7](img/simple-app/simple-7.png)

## 3-4-1. Self-healing of `Deployment`

The `Self-healing` feature of Deployments is one of Kubernetes' most powerful tools to maintain **high availability**.

Kubernetes **automatically detects** when a Pod managed through Deployment is **abnormally terminated or deleted**, and **creates a new Pod to maintain the specified number of replicas**. This feature allows the system to resolve the issue on its own, rather than requiring you to redeploy the Pod yourself.

The commands below will show that even if you manually delete a specific Pod, **Deployment will detect it and automatically create a new Pod.**

```shell
  # Check Pod status and identify one to delete
  kubectl get pod
```

```shell
  # Replace <pod name> with the name of the Pod you want to delete
  kubectl delete pod <pod name>
```

```shell
  # Confirm that a replacement Pod is created
  kubectl get pod
```

![self-healing](img/simple-app/k8s-healing.png)

## 3-5. Connect `Service` with `Deployment`

### What is a Service?

A Deployment creates and manages Pods, but each Pod gets a unique IP address, which can change whenever Pods restart or scale.

A Service solves this problem:

- It groups the Pods managed by a Deployment under a single network endpoint.
- Clients don’t need to know each Pod’s IP; they just use the fixed ClusterIP of the Service.
- Service provides **load balancing**, automatically routing requests to one of the Pods.

In other words, the Deployment manages the Pods, and the Service provides **reliable access** to them.

1. Create and apply a Service definition file:

   ```shell
   vim simple-app-service.yaml
   ```

   Contents of `simple-app-service.yaml`:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: simple-app-service
   spec:
     selector:
       app: simple-app
     ports:
       - protocol: TCP
         port: 80
         targetPort: 5000
     type: ClusterIP
   ```

   ```shell
   kubectl apply -f simple-app-service.yaml
   kubectl get svc # Check the Cluster IP
   ```

   ![simple 8](img/simple-app/simple-8.png)

2. Open a browser and access the following address:

   ```shell
   http://<Cluster IP>
   ```

   ![simple 9](img/simple-app/simple-9.png)

You’ll see the `Pod Name` change every time you refresh the page.

That’s because the Service acts as a **load balancer**, distributing traffic among the Pods it connects to.

## 3-6. Scaling up my-simple-app with Deployment

Suppose the number of users suddenly increases, and you need more than 3 Pods. Kubernetes Deployments make it easy to **scale up**.

1. Edit `simple-app-deployment.yaml` and change `replicas` to 10.

2. Apply the updated Deployment:

   ```shell
   kubectl apply -f simple-app-deployment.yaml
   kubectl get pods # Check the increasing pods
   ```

   ![simple 10](img/simple-app/simple-10.png)

3. Refresh the browser:
   - You’ll now see Pod Names that didn’t appear before.
   - These new Pods were created when the replica count was increased

## 3-7. Rolling Update

### What is a Rolling Update?

A Rolling Update **gradually replaces** existing Pods with new ones.

Instead of updating all Pods at once, it updates a few Pods at a time, making the process smooth and **without downtime**.

**Steps to perform a Rolling Update:**

1. Check the website:
   The currently deployed application version is v1 (displayed on the page).

   At this time, let's change to v2. We will use pre-built docker image.

2. Change the application version from v1 to v2:

   ```shell
   kubectl set image deployment/simple-app-deployment simple-app=cheolhuikim/my-simple-app:v2
   ```

   After running the above command, the Deployment settings will be updated as shown below.

   ![simple 11](img/simple-app/simple-11.png)

3. Check the Rolling Update status:

   ```shell
   kubectl rollout status deployment/simple-app-deployment
   kubectl get pods
   ```

   ![simple 12](img/simple-app/simple-12.png)

4. After deployment, refresh the website to confirm the version is now v2.

   ![simple 13](img/simple-app/simple-13.png)

Thanks to Kubernetes, application version updates are quick and easy.

## 3-8. Rollback

### Why Rollback Is Important

Sometimes after releasing a new version, **users encounter bugs** or features break.

For example, the new version v2 might have a broken API or a feature that doesn't work properly.

If an immediate fix isn’t possible, you need to **rollback to a stable previous version (v1)** to keep your service running.

Kubernetes makes rollback **easy and reliable**, with **zero downtime**.

**Steps to Rollback:**

1. Roll back the application (v2 -> v1):

   ```shell
   kubectl rollout undo deployment/simple-app-deployment
   ```

2. Check the Pods status (new v1 Pods will be created):

   ```shell
   kubectl get pods
   ```

   ![simple 14](img/simple-app/simple-14.png)

3. Refresh the browser:

   You’ll see that the app has successfully returned to version v1.

   ![simple 15](img/simple-app/simple-15.png)

   **Now scale in the Pods back to 3 and confirm that the number of running Pods decreases. (Do it yourself!)**

So far, you've practiced deploying and updating applications in Kubernetes using Pods, Deployment, and Service.

This enables you to effectively perform automated deployments, scaling, rolling updates, and rollbacks.

# 3. Review

## Lab Summary

In this lab, you practiced with Kubernetes to understand the concept, principles, and features of container orchestration.

Using 3 NUC machines, you learned how to deploy and manage container-based applications effectively.

## Why Is Container Orchestration Needed?

As container technology advances, it becomes critical to manage and deploy **many containers efficiently**.

Simply running containers isn't enough — you need orchestration tools to handle **scalability and availability**.

**1. Container Management Becomes Difficult as Numbers Grow**: As applications grow, the number of containers increases, making manual management harder.

**2. Need for Automated Deployment & Updates**: Manual deployments are slow and prone to service disruption.

**3. Scaling & Fault Recovery**: As demand increases, you need auto-scaling. When failures happen, quick recovery is essential.

In this lab, you learned how container orchestration solves these challenges through Kubernetes.

## Summary of Key Steps

1. **Built a Kubernetes Cluster**
   - Set NUC1 as the Master Node and NUC2/NUC3 as Worker Nodes.
   - Used kubeadm to initialize the cluster and join nodes.
   - Installed Flannel CNI to enable networking between containers.

2. **Deployed an Application with a Pod**
   - Deployed a single Pod to observe basic orchestration behavior.

3. **Managed Multiple Pods Using a Deployment**
   - Created and managed 3 Pods with a Deployment.
   - Scaled Pods easily using `replicas` (3 → 10).
   - Verified the Self-healing feature (auto-recovery after Pod deletion).

4. **Used a Service to Manage Network Access**
   - Solved the dynamic IP issue by exposing Pods through a ClusterIP Service.
   - Understood how multiple Pods share the same endpoint.
   - Verified load balancing by observing distributed requests.
   - Accessed the app via Service IP and confirmed it routed to different Pods.

5. **Performed Rolling Update and Rollback**
   - Upgraded the application from v1 to v2.
   - Rolled back from v2 to v1 when needed.
