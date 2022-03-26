import keras.applications.mobilenet
import tensorflow as tf
from keras.preprocessing import image
from keras.applications import imagenet_utils
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
from petl import header

#mobile is a pretrained deep learning Model
mobile = tf.keras.applications.mobilenet_v2.MobileNetV2()

with open('./Assets/Resultfinal.csv', 'r+', encoding='UTF8', newline='') as f:
    reader = csv.DictReader(f)
    data = list(reader)

    for line in data :
        pic = line["image"]
        img = cv2.imread(pic)
        print(pic)
        try:
            img = cv2.resize(img, (224, 224))
        except:
            continue
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #used to show image
        #plt.show()

        resizedImg = image.img_to_array(img)
        final_image = np.expand_dims(resizedImg,axis=0)
        final_image=keras.applications.mobilenet.preprocess_input(final_image)

        #prediction
        prediction = mobile.predict(final_image)
        result = imagenet_utils.decode_predictions(prediction)
        print(result)
        line["predicted"]=result

    with open('./Assets/Resultpredicted.csv', 'w', encoding='UTF8', newline='') as f:
        fieldnames = list(header(data))
        # fieldnames= header(dataframe)
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

