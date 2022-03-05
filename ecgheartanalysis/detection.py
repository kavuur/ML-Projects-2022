import cv2
import numpy as np
import tensorflow as tf
MODEL = tf.keras.models.load_model("model.h5")
class Detect:
    def __init__(self):
        self.diseases ={'Abnormal HB': 0, 'COVID-19': 1, 'HMI': 2, 'MI': 3, 'Normal Person': 4}

    def predict(self, model,image):
        return model.predict([image])

    def process_image(self, filepath):
        img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
        img_array = img_array / 255
        new_array = cv2.resize(img_array, (224, 224))
        return new_array.reshape(-1, 224, 224, 3)

    def prediction_cls(self, prediction):
        for key, clss in self.diseases.items():
            if np.argmax(prediction) == clss:
                return  key
