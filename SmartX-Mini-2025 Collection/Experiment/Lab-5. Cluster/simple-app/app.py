from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def home():
    pod_name = os.getenv('POD_NAME', 'Unknown Pod')
    return f"Hello from {pod_name}! <br> This is the simple-app version 1. <br>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
