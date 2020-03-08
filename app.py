from flask import Flask
from flask import render_template
import os

root_path = os.getcwd()
UPLOAD_FOLDER = root_path + '\\uploads\\'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # limit file size to 10mb


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
