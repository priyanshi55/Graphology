from flask import Flask, render_template, flash, request, url_for, redirect,jsonify
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import os
import numpy as np
import pandas as pd
import pickle
import train_predict

app = Flask(__name__, template_folder='./')


app.config['UPLOAD_FOLDER'] = '/content/web/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

run_with_ngrok(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def main():
    error_msg = ''
    image = ''
    if request.method=='POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            image = uploaded_file.filename
            if not allowed_file(uploaded_file.filename):
                return render_template('index.html', result={}, error_msg='Invalid extension')
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename))
            result = train_predict.predict_all(uploaded_file.filename)
            return render_template('index.html', result=result, error_msg=error_msg, image= '/static/uploads/' + uploaded_file.filename)
    return render_template('index.html',result={},error_msg=error_msg)

if __name__ == '__main__':
    app.run()
