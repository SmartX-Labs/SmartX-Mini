# Lab#4. IoT Lab

## 0. Concept

<img width="916" alt="image" src="https://user-images.githubusercontent.com/63437430/161034315-b201ae9e-463e-44d3-a02f-4796a90f6ee4.png">

- Raspberry Pi Box for IoT Sensors & Anchors
- NUC Box for IoT-Cloud Hub
- Tower Box for IoT-Cloud Service Visualization

### 0-1. Node.js

Node.js is an open-source, cross-platform, back-end JavaScript runtime environment that runs on the V8 engine and executes JavaScript code outside a web browser. Node.js lets developers use JavaScript to write command line tools and for server-side scripting—running scripts server-side to produce dynamic web page content before the page is sent to the user's web browser. Consequently, Node.js represents a "JavaScript everywhere" paradigm, unifying web-application development around a single programming language, rather than different languages for server-side and client-side scripts.

---

## 1. Preparation

<img width="846" alt="image" src="https://user-images.githubusercontent.com/63437430/160827300-04a1b986-7b04-452b-a78f-15d7293bb20b.png">

<img width="598" alt="image" src="https://user-images.githubusercontent.com/63437430/160827511-efe9e508-2541-4e77-9d72-dc683460921f.png">

---

## 2. Practice

### 2-1. Docker Container for Node.js Web Server: Run Container (NUC)

Run a Docker Container

```bash
sudo docker run -it --net=host --name=webserver lshyeung/smartx_webserver
```

On container

```bash
apt-get update

apt-get install vim
```

### 2-2. Docker Container for Node.js Web Server: Server code (NUC)

Open Server code and change NUC IP

```bash
vi /SmartX-mini/IoT-labs/webserver.js
```

<img width="418" alt="image" src="https://user-images.githubusercontent.com/63437430/160828580-7201f53f-e66a-40d3-8682-ca237476b20a.png">

### 2-3. Temperature / Humidity Sensor test on Raspberry PI:

#### 2-3-1. Install package (PI)

Download package from GitHub

```bash
git clone https://github.com/adafruit/Adafruit_python_DHT.git
```

Install package

```bash
cd Adafruit_python_DHT

sudo apt-get update

sudo apt-get install python3-pip

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo python3 setup.py install
```

If you have error while build package.

```bash
sudo apt install -y build-essential python3-dev
```

#### 2-3-2. TemSensor test (PI)

Move to example directory

```bash
cd ~/Adafruit_python_DHT/examples
```

Modify test code (Change python to python 3)

```bash
sudo vi AdafruitDHT.py
```

```python
#!/usr/bin/python
...

```

=>

```python
#!/usr/bin/python3
...

```

Execute test code

```bash
sudo ./AdafruitDHT.py 11 4
```

<img width="498" alt="image" src="https://user-images.githubusercontent.com/63437430/160829118-04bae048-2cf3-4c3f-8cd9-4b9295b019d0.png">

### 2-4. Sensor Data Capture and Transfer

#### 2-4-1. Sensor Data capture code (PI)

Install dependencies at RPi

```bash
sudo apt-get update

sudo apt-get install python3-numpy

sudo apt-get install mercurial
```

Open Sensor Data Capture code and Change IP Address

```bash
vi ~/SmartX-mini/IoT-labs/RPI_capture.py
```

<img width="472" alt="image" src="https://user-images.githubusercontent.com/63437430/160829267-f2198912-a27d-4ee3-9b44-e5af753aff6d.png">

#### 2-4-2. Sensor Data transfer code (PI)

Open Sensor Data Capture code and Change IP Address

```bash
vi ~/SmartX-mini/IoT-labs/RPI_transfer.py
```

<img width="498" alt="image" src="https://user-images.githubusercontent.com/63437430/160829383-8053b56c-a4ea-42d1-b4d1-220502b7754a.png">

### 2-5. Execute IoT Web service

At the Docker container in NUC (Webserver)

```bash
cd /SmartX-Mini/IoT-labs

nodejs webserver.js
```

At the Laptop (Tower)
Open Web browser and go to `http://<NUC_IP>`

At the Rpi (Sensor Data Capture and Transfer)

```bash
cd ~/SmartX-mini/IoT-labs

chmod +x process.sh

sudo ./process.sh
```

<img width="490" alt="image" src="https://user-images.githubusercontent.com/63437430/161033216-2c5035de-e827-4f05-a095-f912c2772777.png">

---

## 3. Lab Summary

An example-based realization of container-based IoT-Cloud services that can sense and actuate distributed IoT devices (i.e., Boxes).

For the cloud side, the required Web-app server realization is supported by utilizing Node.js programming.
