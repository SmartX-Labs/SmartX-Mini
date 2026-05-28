# 3-Tier Lab - Week 1

# 0. Objective

In this lab, we will go through the process of deploying a web service based on **3 Tier Architecture** in a Kubernetes environment. The entire lab spans two weeks, and the Week 1 lab focuses on the following components:

- Deploying a PostgreSQL Database on Kubernetes
- Deploying a NestJS-based Backend on Kubernetes and connecting it to the database
- Delivering a React-based web page via NGINX, or forwarding requests to the Backend

> [!note]
>
> This Lab is conducted on a Kubernetes Cluster set up in **Lab#5 (Cluster Lab)** and consists of the following structure:
>
> ![Kubernetes Installation](img/nuc-prep.png)
>
> Each participant remotely accesses NUC1 (master node) from their PC using SSH, creates their own Kubernetes namespace, and proceeds with the lab in an isolated environment within that namespace.

# 1. Concept

## 1-1. 3-Tier Architecture

**3-Tier Architecture** refers to an architectural design method that separates a single application into three layers (physically/logically) based on functionality.

It is widely used especially in systems like web services that interact with users, process data, and need to store that data.

### Components

![3-Tier Architecture](img/3-Tier-Arch.png)

1. Presentation Tier (Frontend)
   - This is the layer that directly interacts with users.
   - Representative technologies include web frameworks/libraries like React, Vue, and Angular that run in browsers.
   - Mobile apps also fall into this tier, including native (Android, SwiftUI) and cross-platform (Flutter, React Native) apps.
2. Application Tier (Backend)
   - Handles user requests from the Presentation Tier, executes business logic, and communicates with the database.
   - Typically built using frameworks like Express, NestJS, Django, and Spring.
   - Also called the Business Logic Tier or Transaction Tier.
3. Data Tier (Database)
   - Manages reading and writing to the database.
   - Permanently stores application data.
   - Databases like PostgreSQL, MySQL, and MongoDB are commonly used.

### Background

In the past, web applications were often built in **a Monolithic structure**, where a single server handled everything (UI, logic, data storage).

However, due to the following issues, the 3-Tier Architecture emerged:

- As functionality grows, project and code size become large and hard to maintain
- Server load increases as the number of users grows
- Structural limitations where changing one feature affects the entire service
- Inefficient scaling as it requires scaling the whole service

To solve these issues, separating each layer and enabling independent deployment and management became necessary. This is the 3-Tier Architecture.

### Differences from Traditional Structure

| Category        | Monolithic Architecture      | 3-Tier Architecture                |
| --------------- | ---------------------------- | ---------------------------------- |
| Code Separation | X (Functions mixed)          | O (Functions separated by layer)   |
| Maintainability | Hard to trace issues         | Manageable per layer               |
| Scalability     | Must scale entire service    | Can scale each layer independently |
| Failure Scope   | Can propagate across service | Can isolate within a single layer  |
| Deployment      | Single deployment            | Independent layer deployments      |

### Advantages

- **Independence**: Frontend, Backend, and DB can be developed and deployed independently
- **Maintainability**: Easy to identify which layer has an issue
- **Scalability**: Can scale only the high-load layer (e.g., scale BE but not DB)
- **Security**: DB is not directly exposed and only accessible via Backend

### Disadvantages

- **Operational Complexity**: More complex communication and deployment structure
- **Network Overhead**: Inter-tier traffic increases network usage
- **Higher Development Effort**: Requires interface/API/data format design between tiers

### Why Use 3-Tier Architecture on Kubernetes?

Using 3-Tier Architecture in Kubernetes provides several modern cloud-native benefits:

1. **Automated Deployment**
   - Each tier is a separate Deployment, allowing independent rolling updates

2. **Self-Healing**
   - If a Pod in any tier crashes, it is automatically restarted

3. **Horizontal Scaling**
   - High-load tiers can scale automatically to distribute traffic

4. **Unified Observability**
   - Prometheus, Grafana, and other tools allow cross-tier monitoring

5. **Infrastructure Independence**
   - Consistent deployments across cloud and on-prem environments

6. **Namespace-Based Isolation**
   - Practice or run services in isolated environments by namespace

In conclusion, 3-Tier Architecture works very well with Kubernetes and is foundational to modern service deployment and management.

## 1-2. Why Companies Use Kubernetes?

As mentioned in **Lab#5 (Cluster Lab)**, many companies are migrating to Kubernetes-based infrastructure for the following reasons:

### 1. **High Availability**

- Pods automatically recover if they crash
- Failing health checks trigger Pod restarts
- Allows partial recovery without full service downtime

### 2. **Automated Operations**

- Use of `Deployment`, `StatefulSet` for rolling updates and rollbacks
- Easy integration with CI/CD pipelines

### 3. **Maintainability**

- YAML-based declarative configuration allows version control of infrastructure
- Tools like Helm and Kustomize simplify complex configuration

### 4. **Scalability**

- Adjust replica count of `Deployment` to handle high traffic
- Use HPA (Horizontal Pod Autoscaler) for automatic scaling

### 5. **Resource Efficiency**

- Schedules workloads at the Pod level for better resource utilization
- CPU and memory limits prevent overuse

### 6. **Environment Consistency**

- Keep development, testing, and production environments aligned
- Developers' settings can be reflected in production

### 7. **Cloud & On-Prem Support**

- Works consistently on public clouds (AWS, GCP, Azure) and on-prem servers
- Enables multi-cloud strategy without vendor lock-in

As a result, Kubernetes is becoming the de facto standard for modern infrastructure—not only in enterprises, but also in startups, educational institutions, and public sectors.

# 2. Lab Preparation

Let's begin the 3-Tier Lab in earnest.

## 2-1. Remote Access to Master Node (For NUC2, NUC3)

If you're using NUC2 or NUC3, enter the following command in your terminal to remotely access the Master Node:

```bash
ssh <username>@nuc01
# After entering the command, input your password.
```

## 2-2. Checking Kubernetes Cluster Status (For all NUCs)

Once connected to the Kubernetes Master Node, enter the following commands to check the status of nodes and pods to ensure the Kubernetes cluster is running correctly:

```bash
# View the status of all nodes in the Kubernetes cluster
kubectl get nodes

# View the status of all pods across all namespaces
kubectl get pods -A
```

All nodes should be in the `Ready` state, and all pods should be in the `Running` state.

> [!warning]
>
> If any nodes are not `Ready` or any pods are not in `Running` state, the lab may not proceed properly.

## 2-3. Creating a Kubernetes Namespace (For all NUCs)

Since each student is remotely accessing the Kubernetes Master Node on their own NUC, we will use Kubernetes namespaces to logically separate resources among users.

> [!note]
>
> **What is a Namespace?**
>
> A namespace is a logical way to isolate resources within a Kubernetes cluster. It allows multiple users or teams to work simultaneously in the same cluster without interfering with each other.
>
> In this lab, each student will create **their own namespace**, and all resources must be created/managed **within that namespace only**. This allows multiple users to perform the lab concurrently without conflicts.

Run the following commands to create your own namespace:

```bash
# Check the current list of namespaces
kubectl get namespace

# Replace <your_namespace> with your machine name (e.g., nuc01, nuc02, or nuc03)
kubectl create namespace <your_namespace>

# Verify that your namespace has been created
kubectl get namespace
```

## 2-4. Practicing Basic Kubernetes Commands

In this section, we’ll practice the basic commands needed to operate a Kubernetes cluster.  
During the lab, you will primarily use `kubectl` to deploy and manage resources.  
These commands are frequently used and serve as the foundation for upcoming tasks.

### (1) Viewing Resources: `kubectl get <resource>`

Use this command to check the current state of Kubernetes resources.

```bash
kubectl get pods          # View pods in the current namespace
kubectl get services      # View services in the current namespace
kubectl get deployments   # View deployments in the current namespace
kubectl get namespaces    # View all namespaces in the cluster
kubectl get nodes         # View all nodes in the cluster
```

> [!tip]
>
> You can use **abbreviations** like:
>
> `pods` → `po`  
> `services` → `svc`  
> `deployments` → `deploy`  
> `namespaces` → `ns`

### (2) Namespace Options: `-n <namespace>` and `-A`

- `-n <namespace>`: View resources in a specific namespace
- `-A` or `--all-namespaces`: View resources across all namespaces

```bash
# View all pods in the 'nuc01' namespace
kubectl get po -n nuc01

# View all services across all namespaces
kubectl get svc -A
```

### (3) Show Extra Info: `-o wide`

Add the `-o wide` option to display more information, such as IP and node location.

```bash
# Shows which node each pod is running on, and its cluster IP
kubectl get pods -o wide
```

### (4) Create / Apply / Delete Resources: `create`, `apply`, `delete`

- `create`: Creates a new resource. Only works if the resource doesn’t already exist.
- `apply`: Creates or updates a resource based on a YAML file.
- `delete`: Deletes a resource.

```bash
# Example usage
kubectl apply -f deployment.yaml     # Apply or create the resource
kubectl delete -f deployment.yaml    # Delete the resource
```

These commands will be used repeatedly throughout the lab. You don’t need to memorize them, but getting used to them is important.

## 2-5. What is a YAML File?

In Kubernetes, resources are managed in a **declarative** way, and the core of this is the **YAML file**.

### What is YAML?

`YAML (YAML Ain’t Markup Language)` is a human-readable data serialization format.  
It expresses structured data based on indentation. Kubernetes uses YAML to define resources such as Deployment, Pod, and Service.

### Basic Structure Example

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

You can apply YAML files to the cluster using:

```bash
kubectl apply -f <file>.yaml
```

#### Main Fields

- `apiVersion`: API version used for the resource
- `kind`: Type of resource (Pod, Service, Deployment, Secret, etc.)
- `metadata`: Metadata such as name, namespace, labels
- `spec`: The main configuration and behavior of the resource

### Tips for Writing YAML

- Use consistent indentation (2 or 4 spaces)
- Always put a space after `:`
- Badly formatted YAML will cause `kubectl apply` to fail

**Understanding YAML is one of the core skills in Kubernetes labs.**

> All `.yaml` files used in this lab are provided in the Git repository.  
> You may modify them or write your own as needed.

## 2-6. Cloning the Git Repository

### 2-6-1. Create Directory and Clone the Repository

First, create your personal lab directory based on your PC name:

```bash
cd ~
mkdir <your_directory>  # e.g., nuc01, nuc02, or nuc03
cd <your_directory>
```

This lab includes **code templates** for the Frontend and Backend, along with `yaml` templates to deploy them on Kubernetes.

Run the following command to clone the prepared repository:

```bash
git clone https://github.com/SmartX-Labs/SmartX-Mini.git
cp -r SmartX-Mini/SmartX-Mini-2026/Experiment/Lab-7.\ 3-Tier/* ./

# Check the templates
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

### 3-1-1. Creating a Persistent Volume

#### What is a Persistent Volume?

> **PersistentVolume (PV)**: Represents actual storage on a node in the Kubernetes cluster. It defines a connection to external storage (e.g., disk) so that data persists even when a Pod is deleted.
>
> **PersistentVolumeClaim (PVC)**: A resource used to request specific storage. A Pod uses a PVC to indirectly access the PV.

In other words, the PV is the actual storage, and the PVC is the user request. Connecting the two allows Pods to safely use external storage.

**First, edit the predefined Persistent Volume template to match your own namespace.**

```bash
cd ~/<your_directory>/kubernetes/database
vim postgres-pv.yaml
```

```yaml
# postgres-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv-<your_namespace> # Edit to match your own namespace
  labels:
    volume: postgres-pv-<your_namespace> # Edit to match your own namespace
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  hostPath:
    path: /mnt/data/<your_namespace>/postgres # Edit to match your own namespace
  persistentVolumeReclaimPolicy: Retain
```

```bash
# Deploy the Persistent Volume for PostgreSQL
kubectl apply -f postgres-pv.yaml

# Check the created Persistent Volume
# You may see PVs from other students as well.
kubectl get pv
```

### 3-1-2. Deploying PostgreSQL Database

Next, deploy the PostgreSQL Database:

```bash
vim postgres.yaml
```

The `postgres.yaml` defines three resources:

1. **Secret**: Stores user, password, and database information.
2. **Service**: Exposes PostgreSQL within the cluster.
3. **StatefulSet**: Maintains the actual PostgreSQL instance.

> [!note]
>
> **Secret**: Used to securely store sensitive information like passwords or API keys. Here, it securely stores PostgreSQL credentials so they can be referenced by other resources.
>
> **StatefulSet**: Used for deploying applications that maintain state (e.g., databases). Unlike Deployments, it ensures fixed names and volumes for each instance.

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

Apply the file:

```bash
kubectl apply -f postgres.yaml

# Check the created Secret
kubectl get secret -n <your_namespace>

# Check the Service
kubectl get svc -n <your_namespace>

# Check the StatefulSet
kubectl get statefulset -n <your_namespace>
```

You’ve now deployed the **PostgreSQL Database**, the Data Tier of the 3-Tier Architecture.

## 3-2. Backend Deployment on Kubernetes

Now, let’s deploy the **Backend Service**, which corresponds to the Application Tier in the 3-Tier Architecture.

### 3-2-1. Creating a Secret for Database Access

To connect the backend to PostgreSQL, it needs credentials and connection information.  
We will store this info in a Kubernetes Secret.

```bash
cd ~/<your_directory>/kubernetes/backend
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

Apply the file:

```bash
kubectl apply -f secret.yaml
kubectl get secret -n <your_namespace>
```

### 3-2-2. Creating the Backend Deployment

Now that the backend can access the database, let’s deploy it using a pre-built Docker image.

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
          resources: # You can limit container's resource usage by doing like this:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

Apply and check:

```bash
kubectl apply -f deployment.yaml
kubectl get deploy -n <your_namespace>
```

### 3-2-3. Creating the Backend Service

Now create the Service that exposes the backend inside the cluster.

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
    app: backend-api # should match with spec.selector.matchLabels.app in deployment.yaml
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

Apply the file:

```bash
kubectl apply -f service.yaml
kubectl get svc -n <your_namespace>
```

At this point, you’ve completed the deployment of the Data Tier (PostgreSQL) and Application Tier (Backend) in the 3-Tier Architecture.

# 4. Frontend Deployment on Kubernetes

## 4-1. Background on Frontend Deployment

### 4-1-1. Kubernetes Object: ConfigMap

In section `4.2.1`, we'll use a `ConfigMap` to inject configuration files into containers. But what exactly is a ConfigMap?

A `ConfigMap` is a Kubernetes object that stores non-sensitive configuration data in plain text.  
Unlike `Secret`, which stores sensitive information (like passwords), `ConfigMap` stores data such as URLs, port numbers, or log levels that are safe to expose.  
You can use them in two main ways:

1. Inject `ConfigMap` data as environment variables
2. Mount `ConfigMap` as files inside the container (also called a “projection”)

In this lab, the Frontend deployment uses a `ConfigMap` to inject NGINX configuration files.  
This configuration is mounted as a file using the `fe-proxy.yaml` in `kubernetes/frontend`.

> [!note]
>
> This explanation references “Start with Docker & Kubernetes” by Chanho Yong (Wikibooks), pp. 344–355.  
> For more detailed information, please consult the book.

### 4-1-2. React

React is a JavaScript-based frontend library developed by Meta.  
It is widely used along with Angular and Vue for building modern web frontends.

It enables SPA (Single Page Application) development by modifying only specific parts of the page using JavaScript, without reloading the entire page.  
React components divide the UI into modular pieces and update only the changed elements.

In addition to web services, React can be used for developing native UIs for mobile apps as well.

> [!note]
>
> You don’t need to understand the full React source code to complete this lab.  
> However, if you're interested, refer to `frontend/README.md` for more information.

### 4-1-3. NGINX

To serve HTML and JavaScript files to users or browsers, either:

- The Backend server must be configured to serve static files, or
- A Proxy server (e.g., NGINX) must be placed in front to serve the files and forward requests

In the second case, NGINX receives the requests, serves the files, or forwards the request to the appropriate Backend server.

![What-is-proxy](img/proxy.png)

By placing a proxy server, the backend can focus solely on service logic and reduce load, while the proxy handles file delivery and request routing.

NGINX can:

- Serve static files like HTML
- Forward requests to specific backend services
- Distribute load (load balancing)

In this lab, NGINX will:

- Serve the HTML and JavaScript files built from the React project
- Forward API requests to the backend server

We’ll use a pre-built Docker image for this purpose.

## 4-2. Frontend Deployment on Kubernetes

> [!note]
>
> This lab uses a pre-built image.  
> If you want to modify the web UI, source code and Dockerfile are located under `./frontend`, which you can modify and rebuild.

### 4-2-1. Creating the Frontend ConfigMap

To allow NGINX to serve HTML/JS files properly, we need to configure it using a `ConfigMap`.

Open the `fe-proxy-cm.yaml` file:

```bash
cd ~/<your_directory>/kubernetes/frontend
vim fe-proxy-cm.yaml
```

In this file:

- Replace `metadata.namespace` with your namespace
- Modify the `upstream backend-svc` block to match your Backend Service URL

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-proxy-cm
  namespace: <your_namespace> # EDIT THIS
data:
  app.conf: | # EDIT THIS
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

After saving the file, apply it:

```bash
kubectl apply -f ./fe-proxy-cm.yaml
```

Verify that it was created correctly:

```bash
kubectl get cm -n <your_namespace>
kubectl describe cm nginx-proxy-cm -n <your_namespace>
```

### 4-2-2. Creating the Frontend Deployment

Now we’ll deploy the NGINX server that serves the HTML files.

Open the `fe-proxy.yaml` file:

```bash
vim ./fe-proxy.yaml
```

Replace `metadata.namespace` with your namespace:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-proxy
  namespace: <your_namespace> # EDIT THIS
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

Apply the deployment:

```bash
kubectl apply -f ./fe-proxy.yaml
```

Check the deployment:

```bash
kubectl get deploy -n <your_namespace>
kubectl describe deploy nginx-proxy -n <your_namespace>
kubectl get pod -n <your_namespace>
```

# 5. Verifying the Deployed Web Service

## 5-1. Browser Access

### 5-1-1. Check Web Server IP

To access the deployed web service via a browser, first check the IP address of the Pod:

```bash
# `-o wide` shows more information such as IP address and node name
kubectl get pod -n <your_namespace> -o wide
```

From the output, find the Pod that starts with `nginx-proxy` and copy its IP address.

![Deploy List](./img/deploy-complete.png)

In the example above, the IP address is `10.244.2.107`.

> [!NOTE]
>
> Usually, you cannot access Pods directly using their internal IPs.  
> However, since the device you are using is also part of the cluster nodes, direct access is possible.  
> This works because the node's kernel routing table and iptables are configured to deliver packets to the Pod.

### 5-1-2. Check Web Service

> [!Note]
>
> Because of time shortage of creating this lab, english version of website cannot be prepared.
>
> So, this guide will let you know meaning of each button, or interface, which are written in Korean. If you are confused, then please call TA.
>
> Sorry for your inconvenience.

In your browser, go to: `http://<nginx-ip-addr>`. You should see a page like the one below:

![WebPage_Main](./img/webpage.png)

This is an anonymous message board service. Anyone can create and view posts without logging in.  
Currently, no posts exist, so the list is empty. Click the “Create Post(게시글 작성)” button to add a post.  
You’ll see a screen like this:

![WebPage_Write](./img/write.png)

Enter a title, nickname, password, and post content. Then click the “Submit(작성)” button.

You will now see your newly created post.

![WebPage_with_post](./img/list-with-post.png)

Next, try using the search function(Type Something, and press "검색").  
This search performs a combined search across titles and content.

![WebPage_Search](./img/post-search.png)

Once finished, click “Post List(게시판 목록)” to go back to the list.  
Now click on your post to view it:

![WebPage_Detail](./img/post-without-comment.png)

You’ll see the title, nickname("작성자"), and post content(below "작성일"), along with the comment section("댓글 작성(Write Comment)" & "댓글 목록(Comment List)").

Write a comment and click “Submit Comment(댓글 작성)”.  
You’ll see the comment appear like this:

![WebPage_WithComment](./img/post-with-comment.png)

Let’s edit the post. Click the “Edit(수정)” button to open the post editor:

![WebPage_Edit](./img/edit-post.png)

Modify the text and enter the correct password to update it.  
If you enter the wrong password or encounter a server error, an error message will appear.

You can also change the password in the same way. ("수정"="Edit" / "취소"="Cancel")

![WebPage_Editing](./img/comment-editing.png)

Once editing is complete, the result will look like this:

![WebPage_AfterEdit](./img/post-after-edit.png)

Finally, let’s delete the post. Click “Delete(삭제)” and enter the post password to delete it.

You’ll see the board return to the empty state:

![WebPage_AfterDel](./img/webpage.png)

You have now tested all features of the anonymous message board.  
We also recommend accessing your teammates’ services to test theirs as well.

## 5-2. Checking Server-Side Behavior

> [!TIP]
>
> The steps below show how requests are handled in real-time by the system.  
> For a better understanding, use the web service while checking logs simultaneously.

### 5-2-1. Check NGINX Logs

As described earlier, NGINX acts as a proxy that serves static files and forwards requests to the backend.

To check how NGINX handled requests, view its logs with:

```bash
# If you're unsure of the Pod name, use: kubectl -n <your_namespace> get po
kubectl -n <your_namespace> logs <nginx-proxy-pod>
```

The logs will show which requests were forwarded and which were served directly.

### 5-2-2. Check Database

The web server stores data (posts and comments) in the database.  
Whenever a user sends a request, the server fetches data from the database and returns it.

So if you inspect the database tables, you’ll see the exact content that appeared in the web interface.

To access PostgreSQL, open a terminal session in the database Pod and start the CLI:

```bash
# The default PostgreSQL pod name is postgres-0
# Use: kubectl -n <your_namespace> get po to confirm
# `-U`: Specifies the PostgreSQL user
# `-d`: Specifies the database to connect to
kubectl -n <your_namespace> exec -it po/postgres-0 -- psql -U myuser -d mydb
```

> [!note]
>
> The command means “execute the following command inside the specified Pod.”  
> Options:
>
> | Option           | Description                                                                     |
> | ---------------- | ------------------------------------------------------------------------------- |
> | `-n <namespace>` | Specifies the namespace of the Pod                                              |
> | `-it`            | Combines `--stdin (-i)` and `--tty (-t)` for interactive shell access           |
> | `-- <cmd>`       | The command to run inside the Pod (note the space between `--` and the command) |

If successful, you’ll see the PostgreSQL CLI prompt:

![psql_start](img/psql_img.png)

To list the tables, enter:

```sql
\d
```

![psql_tables](./img/psql_tables.png)

> [!TIP]
>
> In PostgreSQL, `\d` lists tables in the connected database.  
> `\d <table_name>` shows column details.  
> `\d+` provides more detailed metadata.

Here:

- `Post` is the table for posts
- `Comment` is the table for comments

To view the content, run:

```sql
-- SQL statements must end with a semicolon
SELECT * FROM "Post";     -- Show all posts
SELECT * FROM "Comment";  -- Show all comments
```

You should now see the data you submitted through the web interface.

Note: Passwords are hashed, so the raw text is not viewable.

To exit PostgreSQL, type `\q` or press `Ctrl + D`.

# 6. Lab Review

In this lab, we deployed a **3-Tier architecture** web service in a Kubernetes environment.

The 3-Tier structure consists of:

- `Presentation Tier`: directly interacts with users
- `Application Tier`: processes user requests and communicates with the database
- `Data Tier`: stores and manages generated data persistently

We used Kubernetes, a container orchestration tool, to deploy each component.  
Although we deployed only a small number of Pods for this lab, if you were to operate a real, large-scale service, Kubernetes would allow you to scale easily and manage services reliably with minimal effort.

Using declarative `YAML` files, we created various Kubernetes resources, deployed the Frontend, Backend, and Database, and verified the system functionality.

We also experimented with **NGINX**, which acts as a proxy server between the Frontend (Presentation Tier) and Backend (Application Tier).

By extending this lab:

- You could develop your own custom Frontend and Backend services
- Package them as container images
- Deploy them along with a Database in a Kubernetes environment

This will allow you to gain real experience in designing and deploying a well-structured, production-ready service.
