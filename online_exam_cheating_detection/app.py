import json
import os
import shutil

import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, flash

from test import live_capturing, ml_predict

MODEL = 'models/vgg/final_model1.h5'
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'static/uploads'  # setting the upload folder path.
app.config["PROCESSED_FOLDER"] = 'static/processed'   # setting the processed folder.
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def index():  # put application's code here
    return render_template('index.html', images_cheating=None, count=0, title="Total")
result_images = []
@app.route('/', methods=["POST"])
def upload():
    """Detects cheating instances in the video frame ."""
    if request.method == "POST":
        isExist = os.path.exists("static/processed")
        if isExist:
            shutil.rmtree("static/processed")
            shutil.rmtree("static/uploads")
        os.makedirs("static/processed")
        os.makedirs("static/uploads")
        if "file" not in request.files:
            flash("No file part")
            return "no File Uploaded"
        f = request.files["file"]  # get the input video from the server.
        # client_name = str(request.form.get("client"))

        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))  # save the input video in the static folder.
        # full_filename = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
        in_path = app.config["UPLOAD_FOLDER"]
        out_path = app.config["PROCESSED_FOLDER"]
        saved_model = tf.keras.models.load_model(MODEL)

        live_capture_object = live_capturing()
        live_capture_object.convert_vid_to_images('static/uploads', 'static/processed')
        arr= ml_predict('static/processed', MODEL)
        objects_file = 'detected_objects.txt'
        with open(objects_file, 'w') as f:
            f.write(json.dumps(arr))
        c_count = len([item for item in arr if item["status"] == "c"])
        nc_count = len([item for item in arr if item["status"] == "nc"])
        count = {"c": c_count, "nc": nc_count}
        return render_template('index.html', images_cheating=arr, count=count)
    return redirect(request.referrer)

@app.route('/<id>', methods=["GET"])
def display(id):
    objects_file = 'detected_objects.txt'
    with open(objects_file, 'r') as objects_file:
        objects = list(json.loads(objects_file.read()))
    c_count = len([item for item in objects if item["status"] =="c"])
    nc_count = len([item for item in objects if item["status"] =="nc"])
    count={"c":c_count ,"nc":nc_count}
    title=''
    if id=='c': title='Cheating'
    else: title='Non Cheating'

    result_images= [item for item in objects if item["status"] ==id]
    return render_template('index.html', images_cheating=result_images, count=count, title=title)


if __name__ == '__main__':
    app.run()
