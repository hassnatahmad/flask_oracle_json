import os
from flask import render_template, jsonify
from flask_restful import Resource
from app import auth, app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import json_parser


class UploadResource(Resource):
    allowed_extensions = {'json'}

    def is_file_allowed(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    @auth.login_required
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and self.is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response_message = json_parser.save_all_json(filename)
            resp = jsonify({'message': response_message})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file type is .json and maximum size should be less then 10mb'})
            resp.status_code = 400
            return resp


@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')


class PingResource(Resource):
    @auth.login_required
    def get(self):
        resp = jsonify({'message': 'Hello!'})
        resp.status_code = 200
        return resp
