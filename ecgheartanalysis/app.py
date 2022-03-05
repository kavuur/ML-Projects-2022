from flask import Flask, render_template, request, flash, redirect
import os

from werkzeug.utils import secure_filename

from detection import Detect, MODEL

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__,  static_folder='../static', template_folder='../templates')


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(file):
    d = Detect()
    image = d.process_image(file)
    pred = d.predict(MODEL, image)
    return pred


@app.route('/', methods=['POST', 'GET'])
def process():
    if request.method == "POST":
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("No selected file", "alert text-center")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('..static/uploads', filename))
            output = predict(f"static/uploads/{filename}")
            return render_template("index.html", image_url=filename, text=output)
    return render_template("index.html")


if __name__ == '__main__':
    app.run()