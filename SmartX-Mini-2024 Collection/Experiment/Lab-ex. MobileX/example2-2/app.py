import os
from flask import Flask,render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import cv2
from inference import preprocess, infer, draw_boxes_on_image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image, max_size=600):
    height, width, _ = image.shape
    scale = max_size / max(height, width)
    if scale < 1:
        new_height, new_width = int(height * scale), int(width * scale)
        return cv2.resize(image, (new_width, new_height))
    return image

@app.route('/api/detect_objects', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        input_batch = preprocess(filepath)
        num_detections, detection_classes, detection_scores, detection_boxes = infer(input_batch)
        num_detections = int(num_detections[0][0])
        detection_classes = detection_classes[0][:num_detections]
        detection_scores = detection_scores[0][:num_detections]
        detection_boxes = detection_boxes[0][:num_detections]

        image = cv2.imread(filepath)
        min_score_thresh = 0.1
        with open('labels.txt', 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        labels_map = {i + 1: {"id": i + 1, "name": label} for i, label in enumerate(labels)}

        result_image = draw_boxes_on_image(image, detection_boxes, detection_classes, detection_scores, labels_map, min_score_thresh)

        # Resize the resulting image
        result_image = resize_image(result_image, max_size=600)
        # Encode the resulting image to PNG format
        png_image = cv2.imencode('.png', result_image)[1].tobytes()

        # Return the binary data as a response
        return png_image, 200, {'Content-Type': 'image/png'}

    return "An error occurred", 400


if __name__ == '__main__':
    app.run(debug=True)
