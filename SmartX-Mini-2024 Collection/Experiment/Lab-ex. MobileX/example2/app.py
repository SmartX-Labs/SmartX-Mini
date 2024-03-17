import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from inference import preprocess, infer, postprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            input_batch = preprocess(filepath)
            result = infer(input_batch)
            labels_file = "./densenet_labels.txt"
            result_text = postprocess(result, labels_file)

            return jsonify(text=result_text)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
