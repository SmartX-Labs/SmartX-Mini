import cv2
import numpy as np


class YOLOModel:
    def __init__(self, weight_path="./yolov3-tiny.weights", cfg_path="./yolov3-tiny.cfg"):
        self.model = cv2.dnn.readNet(weight_path, cfg_path)
        self.output_layer = self.get_output_layer()

    def get_output_layer(self):
        layers = self.model.getLayerNames()
        output_layer = [layers[i[0] - 1] for i in self.model.getUnconnectedOutLayers()]
        return output_layer

    def inference(self, input_img):
        blob = cv2.dnn.blobFromImage(input_img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.output_layer)
        return outs


def read_classes(class_path):
    classes = []
    with open(class_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return classes


def show_detected_objects(image, detection_results, classes, threshold=0.5):
    h, w, c = image.shape

    boxes = []
    confidences = []
    class_ids = []

    for result in detection_results:
        for detection in result:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > threshold:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                x = int(center_x - (dw / 2))
                y = int(center_y - (dh / 2))
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(image, label, (x, y-20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)

    cv2.imshow("Object Detection Output", image)


if __name__ == "__main__":
    IMG_PATH = "../dataset/objects/padestrian.jpg"
    CLASS_PATH = "./coco.names"
    THRESHOLD = 0.4

    image = cv2.imread(IMG_PATH)
    classes = read_classes(CLASS_PATH)

    model = YOLOModel()
    outs = model.inference(image)

    cv2.imshow("Original image", image)
    show_detected_objects(image, outs, classes, threshold=THRESHOLD)

    cv2.waitKey(0)
