import io
import requests
import time
from PIL import Image
from torchvision import transforms
import json
import tritonclient.http as httpclient
import torch

"""
Please refer to the config values and modify the "..." appropriately to make the code work. If you combine this with example 2, you should be able to run model inference on a web page as well.
"""

# 이미지를 전처리하고 추론을 위해 데이터를 준비하는 함수
def preprocess(image_path):
    img = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(...),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.224, 0.243, 0.264])
    ])
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0)
    return input_batch

# 트라이톤 서버로부터 결과를 받아 분류를 출력하는 함수
def postprocess(result, topk=5):
    probabilities = torch.nn.functional.softmax(torch.tensor(result), dim=1)
    topk_prob, topk_indices = torch.topk(probabilities, topk)
    topk_prob = topk_prob.numpy().tolist()[0]
    topk_indices = topk_indices.numpy().tolist()[0]

    with open("imagenet-simple-labels.json") as f:
        labels_map = json.load(f)
    
    for i in range(topk):
        print(f"Class: {labels_map[topk_indices[i]]}, Probability: {topk_prob[i]}")

def infer(input_batch):
    
    try:
        client = httpclient.InferenceServerClient(url="triton.default.svc.ops.openark:8000")
        inputs = httpclient.InferInput("...", list(input_batch.shape), "FP32")  
        inputs.set_data_from_numpy(input_batch.numpy())
        outputs = httpclient.InferRequestedOutput("...", binary_data=True)  

        start_time = time.time()
        res = client.infer(model_name="resnet101", inputs=[inputs], outputs=[outputs])
        result = res.as_numpy("resnetv25_dense0_fwd")  
        end_time = time.time()

        inf_time = end_time - start_time

        print(f"Inference time: {inf_time * 1000:.3f} ms")
        print(f"Input shape: {input_batch.shape}")
        print(f"Output shape: {result.shape}")
        
        return result;

    except httpclient.InferenceServerException as e:
        print("Error occurred during inference:")
        print(str(e))
        if hasattr(e, 'status_code'):
            print(e.status_code)
        if hasattr(e, 'message'):
            print(e.message)

if __name__ == "__main__":
    image_path = "/{directory}/img.jpg"
    input_batch = preprocess(image_path)
    result = infer(input_batch)
    postprocess(result)
