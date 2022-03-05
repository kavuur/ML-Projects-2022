# -*- coding: utf-8 -*-
"""
@author: Shaon Sikder
"""

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import tensorflow_hub as hub
from sklearn import linear_model
import pickle


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
sys.modules['Image'] = Image 
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

MODEL_PATH ='C:/Users/Tinodashe J Mabika/Desktop/Livestock-Cattle-Weight-Estimation-main/Livestock-Cattle-Weight-Estimation-main/h5model.h5'

# Load your trained model
model = tf.keras.models.load_model((MODEL_PATH),custom_objects={'KerasLayer':hub.KerasLayer})
with open('C:/Users/Tinodashe J Mabika/Desktop/Livestock-Cattle-Weight-Estimation-main/Livestock-Cattle-Weight-Estimation-main/model_regression','rb') as file:
    regression_model = pickle.load(file)





def model_predict(img_path, model,regression_model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    #x = preprocess_input(x)

    preds = model.predict(x)
    p=preds
    print(p)
    preds=np.argmax(p, axis=1)
    print(preds)
    def check(confidence):
      if confidence<0.3 or confidence>1.7:
        confidence=0.9
      return confidence
    if preds==0:
      confidence=p[0][0]
      v=check(confidence)*2
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)-150
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==1:
      confidence=p[0][1]
      v=check(confidence)*3
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)-125
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==2:
      confidence=p[0][2]
      v=check(confidence)*4
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)-100
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==3:
      confidence=p[0][3]
      v=check(confidence)*5
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)-80
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==4:
      confidence=p[0][4]
      v=check(confidence)*6
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)-100
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==5:
      confidence=p[0][5]
      v=check(confidence)*7
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)+10
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    elif preds==6:
      confidence=p[0][6]
      v=check(confidence)*8
      print(v)
      value=regression_model.predict(np.array([v]).reshape(1, 1))[0]
      weight=(value/2.205)+20
      result="Estimated Weight: "+str("{:.2f}".format(weight))+"±15 KG"
    return result


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

	# Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        

        # Make prediction
        preds = model_predict(file_path, model,regression_model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
