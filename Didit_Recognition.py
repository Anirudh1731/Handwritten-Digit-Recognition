# -*- coding: utf-8 -*-
"""Copy of Digit_Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YLXzGzjoLWdrGgZ4GyWpAnna9FZ50zI9

<font face="Algerian" size="6"> Making ML model</font>

> <font size="5">Importing the required module</font>
"""

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

"""#### Digit recogniser

> <font size="5">Loading the training and testing dataset</font>
"""

# Loading the MNIST data set with samples and splitting it
mnist = tf.keras.datasets.mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

plt.imshow(X_train[0], cmap = plt.cm.binary)
plt.show()
print(y_train[0])

# Normalizing the data (making length = 1)
X_train = tf.keras.utils.normalize(X_train, axis=1)
X_test = tf.keras.utils.normalize(X_test, axis=1)

IMG_SIZE = 28

X_train = np.array(X_train).reshape(-1,IMG_SIZE, IMG_SIZE, 1)
X_test = np.array(X_test).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

"""

> <font size="5">Making a model</font>

"""

# Decide if to load an existing model or to train a new one
train_new_model = True


if train_new_model:

    # Create a neural network model
    model = Sequential()

    model.add(Conv2D(32, (3,3), input_shape = X_train.shape[1:]))
    model.add(Conv2D(32, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.1))

    model.add(Conv2D(32, (3,3)))
    model.add(Conv2D(32, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.1))
    
    model.add(Conv2D(64, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (2,2)))    

    model.add(Flatten())
    model.add(Dense(32))
    model.add(Activation('relu'))
    
    model.add(Dense(10))
    model.add(Activation('softmax'))

    # Compiling and optimizing model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.summary()

else:
    # Load the model
    model = tf.keras.models.load_model('handwritten_digits.model')

"""

> <font size="5">Training and testing the model</font>

"""

model.fit(X_train, y_train, epochs=3, validation_split = 0.3)

# Evaluating the model
val_loss, val_acc = model.evaluate(X_test, y_test)
print("Loss:-", val_loss)

"""

> <font size="5">Test using your own data</font>

"""

# Load custom images and predict them
image_number = 0
IMG_SIZE = 28

for i in range(0,10):
    img = cv2.imread('/content/{}.png'.format(i))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = cv2.resize(img, (IMG_SIZE,IMG_SIZE), interpolation = cv2.INTER_AREA)
    plt.imshow(img, cmap = plt.cm.binary)
    plt.axis(False)
    img = tf.keras.utils.normalize(img, axis = 1)
    img = np.array(img).reshape(-1,IMG_SIZE, IMG_SIZE, 1)
        
    prediction = model.predict(img)
    print(prediction)
    print(len(prediction[0]))
    left = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.10]
    height = prediction[0]
    plt.bar(left, height)
    print("Model 0 -> The number is probably a {} {:.2f}%".format(np.argmax(prediction), np.max(prediction)*100))
    plt.show()
    image_number += 1
    # except:
    #     print("Error reading image! Proceeding with next image...")
    #     image_number += 1

"""

> <font size="5">Save your model in Colab</font>

"""

# model.save('handwritten_digits.model')

"""

> <font size="5">Download your model</font>

"""

# !zip -r /content/file.zip /content/handwritten_digits.model
# from google.colab import files
# files.download("/content/file.zip")