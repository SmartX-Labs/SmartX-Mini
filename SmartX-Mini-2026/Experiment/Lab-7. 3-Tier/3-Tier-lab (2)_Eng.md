# 3-Tier Lab - Week 2

# 0. Objective

In the **Week 1** of 3-Tier Lab, we conducted **Development with Kubernetes**, deploying a 3-Tier web service in a Kubernetes cluster environment.

In this **Week 2** of 3-Tier Lab, we will proceed with **Operation with Kubernetes**, focusing on the operational aspects of the Kubernetes cluster.

This lab emphasizes the following elements:

- Building a Private **Container Image Registry** within Kubernetes and actually `push & pull` images
- Deploying a **Kubernetes Monitoring Stack** (Prometheus + Grafana, etc.) using **Helm**
- Monitoring the Kubernetes cluster (nodes, pods, etc.) using the **Grafana** dashboard

> [!note]
>
> This Lab is conducted on the Kubernetes Cluster configured in **Lab#5 (Cluster Lab)**, and the cluster has the following configuration:
>
> ![Kubernetes Installation](img/nuc-prep.png)
>
> Each participant remotely accesses **NUC1(master node)** from their PC via SSH, creates a Kubernetes namespace, and conducts the lab in an environment separated by namespace.

# 1. Concept

## 1-1. Container Image Registry

Container image registry serves as a central repository for storing and distributing container images. In Docker and Kubernetes environments, you can think of it as the target for pushing and pulling container images.

Examples of major container image registries are as follows:

1. Docker Hub  
   A public container image registry operated by Docker. It has been mainly used in our labs until now.
2. Amazon ECR  
   A container image registry provided by AWS.
3. GitHub Container Registry (GHCR)  
   A container image registry provided by GitHub.
4. Harbor  
   As a CNCF (Cloud Native Computing Foundation) Graduated Project, it is used to build registries in on-premise environments.
5. Self-hosted Docker Registry  
   A registry that can be built based on the registry:2 container image officially provided by Docker.

In this lab, we will deploy a private container registry in the Kubernetes cluster we have built, based on the registry:2 container image.

## 1-2. Importance of Kubernetes Cluster Monitoring

The necessity of Kubernetes cluster monitoring tools is as follows:

1. **Ensuring Availability** – Collecting CPU, memory, disk, and network metrics in advance to detect signs before overload
2. **Shortening Troubleshooting** – Tracking the cause through logs and metrics when pods are in CrashLoop / Pending state
3. **Capacity Planning** – Predicting node count, storage size, GPU demand based on historical data
4. **Alerting and Response** – Real-time alerts via Slack, PagerDuty, etc. by integrating with Alertmanager → Execute SRE Runbook

> [!note]
>
> 📈 **Monitoring Market**  
> According to the CNCF Survey (2024), "Prometheus + Grafana Stack" has been adopted by **77% of production Kubernetes clusters**. Commercial SaaS (New Relic, Datadog, Dynatrace, etc.) also support the Prometheus Remote-Write protocol as a standard, establishing it as the de facto standard.

## 1-3. Working Principles of Prometheus and Grafana

### 1-3-1. Working Principle of Prometheus

![prometheus-arch](img/prometheus-arch.png)

Prometheus is a monitoring tool specialized in collecting and storing time-series data. Its main features are as follows:

- **Data Collection Method**: Prometheus uses a Pull method to periodically collect metric data from monitoring targets. To do this, Exporters are installed on each target to expose metrics as HTTP endpoints.
- **Data Storage**: Collected metrics are stored in Prometheus's built-in time-series database. This data is stored with time information, allowing analysis of changes over time.
- **Data Query**: Prometheus provides its own query language, `PromQL`, to query and analyze metric data in various ways.
- **Alert Function**: You can send alerts via email, Slack, etc., by integrating with Alertmanager according to set conditions.

### 1-3-2. Role and Function of Grafana

![grafana](img/grafana.png)

Grafana is a dashboard tool that visualizes data from various data sources. When used with Prometheus, it provides the following benefits:

- **Data Visualization**: Visualizes metric data stored in Prometheus in various graphs, charts, gauges, etc., allowing you to grasp the system status at a glance.
- **Dashboard Configuration**: Users can create customized dashboards by selecting desired metrics. They can also use various dashboard templates shared by the Grafana community.
- **Alert Settings**: Grafana can set alerts independently to notify users when specific conditions are met.

### 1-3-3 Integration of Prometheus and Grafana

The integration of these two tools has the following structure:

1. **Metric Collection**: Exporters installed on the target systems expose metrics via HTTP endpoints.
2. **Data Collection and Storage**: Prometheus collects metrics from Exporters through a Pull method according to a set cycle and stores them in its own database.
3. **Data Visualization**: Grafana sets Prometheus as a data source and visualizes the necessary metrics on dashboards using PromQL.
4. **Alert and Response**: Alerts are delivered to users through Prometheus's Alertmanager or Grafana's alert function according to set conditions.

Through this structure, you can monitor system performance, resource usage, error states, etc. in real-time, and respond quickly when problems occur.

- **References**
  - **Prometheus Official Documentation**: <https://prometheus.io/docs/introduction/overview/>
  - **Grafana Official Documentation**: <https://grafana.com/docs/grafana/latest/>

### Summary

1. Exporters (Node Exporter, cAdvisor, kube-state-metrics) expose metrics via /metrics endpoint
2. Prometheus pulls from Exporter Endpoints at job intervals (default 30 s)
3. Recording Rules / Alert Rules are evaluated on collected time-series data
4. If conditions are met, Alertmanager sends alerts via email, Slack, etc.
5. Grafana visualizes dashboards through Prometheus API (PromQL) queries

# 2. Container Image Registry Deployment on Kubernetes

Most containers created so far were based on container images pulled from Docker Hub, a public container image repository existing remotely.

Now, we will not use public container image registries like Docker Hub, but instead build our own Private Container Image Registry and push and pull container images to and from that repository.

To do this, we need to build a Container Image Registry on our Kubernetes cluster that plays the same role as Docker Hub.

Following the steps below, we will simply build your own Private Container Image Registry.

## 2-1. Container Runtime Configuration

Until now, we have used Docker as our main container runtime.
However, there are various container runtimes besides Docker.
In fact, Kubernetes uses `Containerd` as its default container runtime.

In this lab, different container runtimes are used at two stages:

1. The process of building a container image using `Docker` installed on the Host machine and pushing that image to the container image registry
2. The process of using `Containerd`, Kubernetes's default container runtime, to look up and use container images from the private container image registry when creating Kubernetes pods

Therefore, we need to configure both container runtimes.

By default, both Docker and Containerd are implemented to use the https protocol for pushing and pulling container images.

However, in this lab, we will not cover the process of introducing SSL/TLS certificates to support https while building a private container image registry.

Since we will only use http through hostnames within the Kubernetes cluster, we need to make the following configurations:

## For NUC01

> [!WARNING]
> **In this lab, we will only configure Docker on NUC01.**  
> **Only the participant who has the role of NUC01 needs to configure Docker.**

Enter the command below to configure Docker:

```shell
sudo vim /etc/docker/daemon.json
```

Add the "insecure-registries" field inside the outermost curly braces in the file and write the corresponding values. This configuration allows you to push and pull container images using the http protocol.

> [!WARNING]
> 예Excluding the ... shown in the example, please only enter `"insecure-registries": ["nuc01:5000", "nuc02:5000", "nuc03:5000"]`. Do not modify other fields.

```json
{
  ...
  ...
  ...
  ...
  "insecure-registries": ["nuc01:5000", "nuc02:5000", "nuc03:5000"]
}
```

After completing the file modification, enter the following command to restart Docker:

```shell
sudo systemctl restart docker
```

## For All NUCs

> [!WARNING]
> **Containerd configuration must be done on all NUCs.**  
> **Participants should open a terminal on each of their respective NUCs, not on NUC01 accessed via ssh, and proceed with the Containerd configuration.**

Now, let's configure Containerd.  
Enter the command below to open the file:

```shell
sudo vim /etc/containerd/config.toml
```

Find the field `[plugins."io.containerd.grpc.v1.cri".registry]` in the file content and modify it as follows:

> [!WARNING]
> Please enter the content excluding the `...` shown in the example. Pay attention to indentation. Do not modify other parts.

```toml
...
...
...

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"

...
...
...
```

To add information for each NUC, modify the file as follows:

```shell
sudo vim /etc/containerd/certs.d/nuc01:5000/hosts.toml
```

```toml
server = "http://nuc01:5000"
[host."http://nuc01:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
  plain_http = true
```

```shell
sudo vim /etc/containerd/certs.d/nuc02:5000/hosts.toml
```

```toml
server = "http://nuc02:5000"
[host."http://nuc02:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
  plain_http = true
```

```shell
sudo vim /etc/containerd/certs.d/nuc03:5000/hosts.toml
```

```toml
server = "http://nuc03:5000"
[host."http://nuc03:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
  plain_http = true
```

After modifying everything, enter the command below to restart containerd:

```shell
sudo systemctl restart containerd
```

## From now on, NUC02 and NUC03 users will continue the lab on NUC01 accessed via ssh

## 2.2 Creating a Persistent Volume(PV)

When you push your self-built container image to the container registry, information about that image must remain permanently on the file system. This is necessary so that you can pull the image whenever you want.

As we have seen in previous lab processes, in Kubernetes, Persistent Volume and Persistent Volume Claim are used to store data in actual storage.

### What is a Persistent Volume?

> [!NOTE]  
> A Persistent Volume represents an actual storage area in the Kubernetes cluster. We create and delete various Pods in the Kubernetes environment, and Persistent Volumes can be used in situations where we want to preserve data even after a Pod is deleted.

Enter the command below to check the yaml file that defines the Persistent Volume.
Please modify the content of the yaml file based on your hostname and namespace.

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

Now, apply the modified file to create the PV.  
Enter the command below to apply the file content and check the PV list.

```shell
kubectl apply -f container-image-registry-pv.yaml
kubectl get pv
```

## 2.3 Creating a Persistent Volume Claim(PVC)

Next, we also create a Persistent Volume Claim.

> [!NOTE]
> A Persistent Volume Claim serves to declare that a user wants to use storage (PV) that meets certain conditions. Typically, when a Pod performing a specific function requires storage, it can use a pre-defined Persistent Volume through a Persistent Volume Claim.

Enter the command below to open the yaml file containing PVC content and modify it:

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

Once the modification is complete, enter the command below to create the PVC and check if the PVC has been created successfully:

```shell
kubectl apply -f container-image-registry-pvc.yaml
kubectl get pvc -n <your_namespace>
```

## 2.4 Creating a Deployment

Until now, we have set up the storage for when container images are pushed,
now we handle the process of creating the pod that actually processes container images.  
We define a Deployment to create the pod.

Enter the command below to open the yaml file defining the deployment and modify it:

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

Once the modification is complete, enter the command to create the deployment.  
And check if the deployment has been created successfully.

```shell
kubectl apply -f container-image-registry.yaml
kubectl get deploy -n <your_namespace>
```

## 2.5 Build & Push Container Image

Now you can build a container image and push it to your private container image registry.

Enter the command below to build a container image, tag it, and push it.  
Execute for both Frontend and Backend container images used previously.

```shell
sudo docker build -t <your_namespace>-frontend ~/<your_namespace>/frontend
sudo docker tag <your_namespace>-frontend <your_hostname>:5000/<your_namespace>-frontend
sudo docker push <your_hostname>:5000/<your_namespace>-frontend
```

After building and pushing the container image for Frontend, follow the same process for the Backend container image:

```shell
sudo docker build -t <your_namespace>-backend ~/<your_namespace>/backend
sudo docker tag <your_namespace>-backend <your_hostname>:5000/<your_namespace>-backend
sudo docker push <your_hostname>:5000/<your_namespace>-backend
```

Now that the self-built container images have been pushed to the private container image registry, you can check the actual physical data of those container images through the file system to verify if they have been saved properly.

In the yaml file for Persistent Volume, we set each PV to be configured on the participant's NUC.

Therefore, **to check the physical files for pushed container images, you need to enter the following command on your own NUC**:

> [!WARNING]
> The command below should be entered in your own terminal, not in the terminal accessed via ssh.

```shell
ls -al /mnt/data/<your_namespace>/registry/docker/registry/v2/repositories
```

If there were no problems in the process so far, you should be able to see the pushed container images through the above command.

## 2.6 Re-Deployment of Frontend and Backend

Now, let's redeploy the Frontend and Backend from the previous lab using the container images we've built.  
Simply modify the container image field in the yaml files related to previously created Deployments.

Please enter the command below to open the file to be modified:

```shell
cd ~/<your_namespace>/kubernetes/backend
vim deployment.yaml
```

And modify the image field value under containers to the following:

```yaml
---
spec:
  containers:
    - name: api
      image: <your_hostname>:5000/<your_namespace>-backend
      ports:
        - containerPort: 3000
```

After completing the modification, enter the command below to apply the changes:

```shell
kubectl apply -f deployment.yaml
```

Now, let's change the Frontend as well.  
Please enter the command below:

```shell
cd ~/<your_namespace>/kubernetes/frontend
vim fe-proxy.yaml
```

And, like Backend, modify the image field value under containers:

```yaml
containers:
  - name: nginx
    image: <your_hostname>:5000/<your_namespace>-frontend
    imagePullPolicy: Always
```

After completing the modification, enter the command below to apply the changes:

```shell
kubectl apply -f fe-proxy.yaml
```

Check if all Pods for Backend and Frontend have been recreated:

```shell
kubectl get pod -n <your_namespace> -o wide
```

Once all Pods have been recreated, enter the IP address of the NGINX Pod in your browser to check the execution result.

# 3. Installing Helm and Deploying Kubernetes Monitoring Tools

## 3-1. Installing Helm

### 3-1-1. What is Helm?

Helm is a package manager that helps deploy applications in Kubernetes more **simply and consistently.**

In the **traditional manual deployment method**, you had to **directly manage multiple YAML files** and **apply them in the correct order**. However, with Helm, you can **package these YAML files into a single Chart for deployment** and **manage variables and configurations uniformly.**

That is, Helm works similarly to Linux/Unix package managers like `apt`, `yum`, `brew`, defining applications as packages for easy installation, upgrading, and deletion.

> [!note]
>
> **What is a Chart?**
>
> It is a bundle of all resource definition files for a single application. Settings can be easily customized through the `values.yaml` file.

Helm also integrates naturally with **GitOps**, and is used when configuring pipelines to continuously synchronize **declarative configuration files** placed in Git repositories.

### 3-1-2. Installing Helm (For NUC1)

Enter the following commands to install Helm:

```bash
cd ~
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh


# After installation
# Verify successful installation with the command below
helm version
```

### 3-1.3. Helm Commands (All NUCs)

Helm is operated with the following basic commands:

```bash
helm version                             # Check Helm version
helm repo list                           # Check the list of registered Helm repositories
helm repo add <name> <url>               # Add a new Helm repository
helm repo update                         # Update repository list
helm install <release-name> <chart>      # Install Helm Chart
helm upgrade <release-name> <chart>      # Upgrade existing Helm Chart
helm uninstall <release-name>            # Delete Helm Chart
helm list -A                             # Check the list of installed Helm resources in all namespaces
```

Here are some **examples:**

```bash
# example
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

In this way, complex resources can be easily deployed and managed.

## 3-2. Installing Kubernetes Monitoring Tools, Prometheus and Grafana

### 3-2-1. Registering and Updating Helm Repository (For NUC1)

First, add and update the Helm Chart repository containing Prometheus and Grafana:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo list
helm repo update
```

### 3-2-2. Installing Kubernetes Prometheus Stack (For NUC1)

`kube-prometheus-stack`s a Helm Chart that helps install the following components at once:

- **Prometheus**: Metric collection
- **Alertmanager**: Alert dispatch
- **Grafana**: Visualization dashboard
- **Node Exporter**: Node-level metric collection
- **Kube State Metrics**: Kubernetes resource state collection

Typically, namespaces are defined according to each function, and resources are deployed in that namespace. Therefore, this Helm Chart is installed in a namespace called `monitoring`.

```bash
helm list -n monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace --set prometheus.prometheusSpec.maximumStartupDurationSeconds=300
helm list -n monitoring
```

After installation completes, you can check the deployed resources as follows:

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

You can see that a service named `prometheus-grafana` has been created. Access the Grafana dashboard through this IP (ClusterIP) address.

# 4. Accessing and Exploring Grafana (All NUCs)

## 4-1. Checking Grafana Access Account Information

Grafana's default login information is automatically stored in Secret during Helm installation. Check the password with the command below:

```bash
kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

The default ID is `admin`, and the password is the value output by the above command.

## 4-2. Accessing the Grafana Dashboard

Check the Cluster IP assigned to the `prometheus-grafana` service created by the Prometheus Stack:

```bash
kubectl get svc -n monitoring
```

Copy the `CLUSTER-IP` address of the `prometheus-grafana` item and access it in a web browser:

```bash
http://<CLUSTER-IP>:80
```

After accessing and entering the login information, the Grafana dashboard will open.

![grafana_login](img/grafana_login.png)

![grafana_main](img/grafana_main.png)

- Moving to **Dashboards** on the left menu, you can check various monitoring dashboards pre-configured by the Prometheus Stack.
- You can visually check real-time metrics for various resources such as **Nodes, Pods, Kubernetes Cluster**, etc.

> [!tip]
>
> Since Prometheus and Grafana are installed independently in each participant's namespace,
>
> you can filter and monitor only your services.

## 4-3. Missions

From now on, explore the Grafana dashboards according to the given missions without specific instructions. **Take screenshots upon completing each Mission**, and show them to the TA during the final check.

> [!tip]
>
> Ubuntu screen screenshot shortcut: `Shift + Ctrl + PrtScn`

### Mission 1

Find all Pods belonging to your namespace (nuc01, nuc02, or nuc03) in Grafana. These include backend-api, nginx-proxy, postgres, etc., deployed in the Week 1 of 3-Tier Lab.

### Mission 2

Check the CPU and memory usage of a specific Pod in a time-series graph. It's good to select a Pod that receives frequent requests, such as `backend-api` or `postgres`.

### Mission 3

Check the overall CPU/Memory usage of the NUC PC you are currently operating. This can be checked through the dashboard provided by `Node Exporter`.

### Mission 4

Find a dashboard that summarizes the overall status of the Kubernetes Cluster. It includes cluster resource status, alert occurrence, etc.

> [!tip]
>
> If you encounter unknown metrics or terms during the missions, search them directly or ask the TA.

# 5. Lab Summary

In this lab, following the direct deployment of a web service on Kubernetes last time, we set up **container image management, package management, and monitoring systems** that are essential in actual production environments.

The key points of the lab are as follows:

1. Through building a `Private Container Image Registry`, you can now store and manage your created container images directly.
2. You have experienced how easily complex resources can be installed through `Helm`, a Kubernetes package manager.
3. You easily deployed a monitoring stack including `Prometheus` and `Grafana` through the `kube-prometheus-stack` Helm Chart.
4. You visually confirmed the status and operation of the Kubernetes cluster in real-time through `Grafana`.

These labs go beyond simple web service deployment, forming an essential foundation for building DevOps capabilities needed in actual service operational environments.
