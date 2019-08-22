# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 17:21:36 2019

@author: zxz58
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np

# =============================================================================
# mnist = tf.keras.datasets.mnist
# 
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0
# =============================================================================
'''convert nparray to list'''
x, y = [], label_set
max_y = int(max(y))
threshold_train = int(0.90 * len(y))
for array in data_set:
    x.append(array.tolist())
'''change label from int to [0, ..., 0, 1, 0,...]'''
yy = np.zeros([len(y), max_y+1])
j = -1
for i in y:
    j += 1
    yy[j][int(i)] = 1
y = yy

x_train, y_train = (np.asarray(x[0:threshold_train]), np.asarray(y[0:threshold_train]))
x_test, y_test = (np.asarray(x[threshold_train:]), np.asarray(y[threshold_train:]))
# =============================================================================
# x_train, y_train = tf.Variable(x[0:450], tf.float32), tf.Variable(y[0:450], tf.int32)
# x_test, y_test = tf.Variable(x[450:], tf.float32), tf.Variable(y[450:], tf.int32)
# =============================================================================

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(20, 20)),
  tf.keras.layers.Dense(400, activation=tf.nn.relu),
  tf.keras.layers.Dense(400, activation=tf.nn.relu),
  tf.keras.layers.Dense(400, activation=tf.nn.relu),
  tf.keras.layers.Dense(400, activation=tf.nn.relu),
  #tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(max_y+1, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, steps_per_epoch=30)
model.evaluate(x_test, y_test)
#model.evaluate(x_train, y_train)