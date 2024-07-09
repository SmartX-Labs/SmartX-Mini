import argparse
import cv2
import numpy as np

class YOLOModel:
    def __init__(self, weights_path, cfg_path):
        self.model = cv2.dnn.readNet(weights_path, cfg_path)
        self.output_layer = self.get_output_layer()

    def get_output_layer(self):
        layer_names = self.model.getLayerNames()
        output_layers = [layer_names[i - 1] for i in self.model.getUnconnectedOutLayers()]
        return output_layers

    def inference(self, img):
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.output_layer)
        return outs

def read_classes(class_path):
    with open(class_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return classes

def show_detected_objects(img, outs, classes, threshold=0.4):
    height, width, channels = img.shape
    class_ids, confidences, boxes = [], [], []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, threshold, 0.4)
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (0, 255, 0)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Object Detection", img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight_path", type=str, default="./yolov3-tiny.weights")
    parser.add_argument("--cfg_path", type=str, default="./yolov3-tiny.cfg")
    parser.add_argument("--class_path", type=str, default="./coco.names")
    parser.add_argument("--img_path", type=str, default="../dataset/objects/dog_bicycle.jpg")
    args = parser.parse_args()

    print("모델을 로딩합니다... ")
    model = YOLOModel(args.weight_path, args.cfg_path)
    print("모델 로딩이 완료되었습니다")

    classes = read_classes(args.class_path)

    img = cv2.imread(args.img_path)
    print("객체 검출을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")

    outs = model.inference(img)
    show_detected_objects(img, outs, classes, threshold=0.4)

    while True:
        if cv2.waitKey(1) > 0:
            break

    print("객체 검출을 종료합니다")
    cv2.destroyAllWindows()
