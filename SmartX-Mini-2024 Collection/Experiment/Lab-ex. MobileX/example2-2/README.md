This practice page is provided as an additional resource in case example3 is not functioning properly. 

However, if you still wish to proceed with example3, you are to do so.

In this practice, we will provide more detailed instructions and code for using models deployed on Triton Server, 


Furthermore, in this practice, we will provide a more detailed example code for preprocessing data according to the config.pbtxt file before deploying a model. 

We will also provide an example code for implementing a service that uses multiple models simultaneously, which participants can run and experiment with.

## install environment

sudo dnf -y install epel-release

sudo dnf -y install python3-devel gcc

sudo pip3 install opencv-python

sudo pip3 install matplotlib

## Result

<img width="718" alt="스크린샷 2023-05-08 오후 8 24 29" src="https://user-images.githubusercontent.com/30370933/236811742-417e064d-8dde-4ce6-9186-fdf86acaa04f.png">



In this practice, we will provide an example code for detecting objects in an uploaded photo and drawing boxes around them. Similar to the previous practices, it is important to ensure that the preprocessing and inferencing code is aligned with the server's pbtxt file.

Participants can compare this example code with the code provided in Example2 to gain a better understanding of how to implement different computer vision tasks using Triton Server. 


max_batch_size: Specifies the maximum batch size that can be processed at once. In this example, up to 128 pieces of data can be processed at once.

input: Specifies information about the input data. Since there can be multiple inputs, it is written in list format.

name: Specifies the name of the input data. In this example, it is set to "image_tensor".

format: Specifies the format of the input data. In this example, the NHWC format is used.

data_type: Specifies the data type of the input data. In this example, an 8-bit integer (TYPE_UINT8) is used.

dims: Specifies the dimensions of the input data. -1 means a variable length dimension. In this example, the height and width are variable, and the number of channels is 3.



output: Specifies information about the output data. Since there can be multiple outputs, it is written in list format.

name: Specifies the name of the output data. In this example, names such as "num_detections" and "detection_classes" are used.

data_type: Specifies the data type of the output data. In this example, a floating-point (TYPE_FP32) is used.

dims: Specifies the dimensions of the output data. In this example, the dimensions are set to 1 for "num_detections" and 100 for "detection_classes".

reshape: Used when the dimensions of the output data need to be reshaped. In this example, it is used for "num_detections" and is set to reshape to the default shape.

```
max_batch_size: 128
input [
  {
    name: "image_tensor"
    format: FORMAT_NHWC
    data_type: TYPE_UINT8
    dims: [ -1, -1, 3]
  }
]
output [
  {
    name: "num_detections"
    data_type: TYPE_FP32
    dims: 1
    reshape {}
  },
  {
    name: "detection_classes"
    data_type: TYPE_FP32
    dims: 100
  },
...
]
```


Next is a problem using the resnet101 model.

A pbtxt and example code are provided, so try to complete the actual code to work during the practice time. Whether to implement the code to work on an actual web page is optional.


The final result will be similar to Example2.

```
name: "resnet101"
platform: "onnxruntime_onnx"
max_batch_size: 8
input [
  {
    name: "data"
    data_type: TYPE_FP32
    format: FORMAT_NCHW
    dims: [ 3, 224, 224 ]
  }
]
output [
  {
    name: "resnetv25_dense0_fwd"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]
instance_group [
  {
    count: 1
    kind: KIND_GPU
  }
]

```

<img width="560" alt="스크린샷 2023-05-08 오후 8 35 59" src="https://user-images.githubusercontent.com/30370933/236813937-8e96f31c-6918-451a-9c29-b89f4d94cff3.png">

## 보충 설명

포맷(format)은 데이터를 배열하는 방식을 의미합니다. 딥러닝 모델의 입력 및 출력 데이터를 다룰 때, 텐서의 형태와 순서를 정의하는 데 사용됩니다.

주로 사용되는 포맷은 NCHW와 NHWC입니다.

NCHW: (배치 크기, 채널, 높이, 너비) 순서로 배열된 텐서입니다. 대부분의 GPU 최적화 알고리즘은 NCHW 형식을 선호합니다.
NHWC: (배치 크기, 높이, 너비, 채널) 순서로 배열된 텐서입니다. 일부 CPU 및 모바일 기반 알고리즘에서 더 효율적일 수 있습니다.
모델에 따라 가변적인 것과 고정적인 것이 있는 이유는 주로 모델의 구조와 학습 목적에 따라 결정됩니다. 예를 들어, 이미지 분류 문제의 경우 입력 이미지의 크기가 고정될 수 있지만, 객체 탐지 문제에서는 가변적인 크기의 이미지를 다루어야 할 수 있습니다. 이 경우, 모델은 입력 데이터의 가변적인 부분을 처리할 수 있는 구조로 설계되어야 합니다.

예제로 제공된 출력 텐서의 차원이 경우, 차원수가 1인 "num_detections"와 차원수가 1000인 "detection_classes"가 있습니다.

"num_detections" (차원수 1): 각 입력 이미지에 대한 탐지된 객체의 수를 나타냅니다. 차원수가 1이므로, 각 이미지에는 객체 탐지는 하나만 된다는걸 확인할 수 있습니다.
"detection_classes" (차원수 1000): 탐지된 객체에 대한 클래스 확률 분포를 나타냅니다. 이 경우, 1000개의 클래스가 있으므로 각 클래스에 대한 확률 값을 가집니다.
따라서 출력 텐서의 차원은 모델이 예측하는 결과의 라벨 수에 따라 결정된다고 볼 수 있습니다. 
