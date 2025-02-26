# 2. Demonstration of an inference service using Triton Server

This tutorial demonstrates how to create a simple service that identifies objects in an image using Triton Inference Server.

The advantage of Triton server is that it provides a unified API for models using various frameworks such as PyTorch or TensorFlow.

And it makes dynamic allocation easier for multiple GPUs.

This reduces the effort required to manage the model when using the ai model in practice.


![example2 diagram](https://user-images.githubusercontent.com/30370933/236705836-2c1468b2-5fed-4fe1-9a1d-ec4afe3911ce.JPG)

The diagram of the Flask app we ran is as follows: 

If the Flask server is running normally, it will connect to the Triton pod inside the mobile x Cluster. 

The Triton pod will search for the model name requested by the user in storage and perform the model inference task through A10 deployed inside the HPC.


## install environment

sudo pip3 install --upgrade pip

sudo dnf install -y gcc gcc-c++ python3-devel

sudo pip3 install nvidia-pyindex

sudo pip3 install flask tritonclient geventhttpclient

sudo pip3 install torch torchvision


Some workstations may have Jupyter Notebook installed.
In this case, even if the libraries are installed correctly, the modules may not run properly.

In this situation, open a command prompt and type jupyter notebook and press Enter to run.

Once Jupyter Notebook is running, proceed with the exercises within the Jupyter Notebook environment.

To install packages within Jupyter Notebook, use the following method:

!pip install ...

Replace the "..." with the package name you want to install.

thanks


## Execution command

Change directory to the example2 folder and execute the command "python3 app.py"


## result
<img width="707" alt="스크린샷 2023-05-07 오후 7 10 17" src="https://user-images.githubusercontent.com/30370933/236671302-7224fdc8-6647-4e6e-ae58-6b036e14d7ce.png">


You can create a model service that measures what objects are in a photo by dragging the photo. If no additional settings are configured, it will run on port 5000 by default.



### here is a more detailed explanation

```python
#connecting server
client = httpclient.InferenceServerClient(url="triton.default.svc.ops.openark:8000")

#inferencing
outputs = httpclient.InferRequestedOutput("fc6_1", binary_data=True)
res = client.infer(model_name="densenet_onnx", inputs=[inputs], outputs=[outputs])
result = res.as_numpy("fc6_1")

```

Currently, Triton server does not allow ordinary users to upload directly due to security reasons. This is because have same name multiple models can be uploaded simultaneously, which may cause conflicts and even lead to the deletion of other models. Instead, a simple explanation of how to deploy to Triton server is provided below.

Now, let's provide a simple explanation of how to deploy models to Triton server:

1.Prepare your model files (e.g., PyTorch .pt, TensorFlow .pb, ONNX .onnx, etc.) and create a directory named with your model_name under the model_repository directory.

2.Place the model files in a subdirectory named 1 (which represents the version number) within the model_name directory.

3.Create a config.pbtxt file in the model_name directory, specifying the model configuration details such as input and output dimensions, data types, and framework used.


The correct directory would be as follows:
```
model_repository/
└── {model_name}/
    ├── config.pbtxt
    └── 1/
        ├── model.pytorch  # For a PyTorch model
        └── model.savedmodel  # For a TensorFlow model
```         

And there is an example of a valid config.pbtxt
```
name: "densenet_onnx"
platform: "onnxruntime_onnx"
max_batch_size : 0
input [
  {
    name: "data_0"
    data_type: TYPE_FP32
    dims: [1, 3, 224, 224 ]
  }
]

output [
  {
    name: "fc6_1"
    data_type: TYPE_FP32
    dims: [ 1000 ]
    reshape { shape: [ 1, 1000, 1, 1 ] }
    label_filename: "densenet_labels.txt"
  }
]
```

We have looked at a simple web programming example of serving a deployed model on a Triton server through APIs provided by the Triton server. Once Triton server is set up, it is easy to maintain the deployment pipeline even when the model is updated.
