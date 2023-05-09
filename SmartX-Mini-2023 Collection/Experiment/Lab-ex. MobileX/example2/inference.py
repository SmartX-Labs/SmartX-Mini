import io
import requests
import time
from PIL import Image
from torchvision import transforms
import torch
import json
import tritonclient.http as httpclient

def preprocess(image_path):
    img = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0)
    return input_batch

def postprocess(result, labels_file, topk=5):
    probabilities = torch.nn.functional.softmax(torch.tensor(result), dim=0)
    topk_prob, topk_indices = torch.topk(probabilities, topk)
    topk_prob = topk_prob.numpy().tolist()
    topk_indices = topk_indices.numpy().tolist()

    with open(labels_file) as f:
        labels_map = [line.strip() for line in f.readlines()]

    result_text = ""
    for i in range(topk):
        result_text += f"Class: {labels_map[topk_indices[i]]}, Probability: {topk_prob[i]}\n"

    return result_text



def infer(input_batch):
    try:
        client = httpclient.InferenceServerClient(url="triton.default.svc.ops.openark:8000")
        inputs = httpclient.InferInput("data_0", list(input_batch.shape), "FP32")
        inputs.set_data_from_numpy(input_batch.numpy())
        outputs = httpclient.InferRequestedOutput("fc6_1", binary_data=True)

        start_time = time.time()
        res = client.infer(model_name="densenet_onnx", inputs=[inputs], outputs=[outputs])
        result = res.as_numpy("fc6_1")
        end_time = time.time()

        inf_time = end_time - start_time

        print(f"Inference time: {inf_time * 1000:.3f} ms")
        print(f"Input shape: {input_batch.shape}")
        print(f"Output shape: {result.shape}")
        
        return result

    except httpclient.InferenceServerException as e:
        print("Error occurred during inference:")
        print(str(e))
        if hasattr(e, 'status_code'):
            print(e.status_code)
        if hasattr(e, 'message'):
            print(e.message)
