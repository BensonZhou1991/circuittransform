# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:38:18 2019

@author: zxz58
"""

'''
train a ANN for 5-layer circuit input
'''

#from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
import os
print(os.path.abspath('.'))
# =============================================================================
# mnist = tf.keras.datasets.mnist
# 
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0
# =============================================================================
ratio_train = 0.9
data_set_name = '5-layers-100000-circuits-depth1.npz'
load_file = np.load('C:/ProgramData/Anaconda3/Lib/site-packages/circuittransform/machinelearning/data_set/'
                    +data_set_name)
data_set_load = load_file['data_set']
label_set_load_raw = load_file['label_set']
max_y = int(max(label_set_load_raw))
'''change label from int to [0, ..., 0, 1, 0,...]'''
y = label_set_load_raw
yy = np.zeros([len(y), max_y+1])
j = -1
for i in y:
    j += 1
    yy[j][int(i)] = 1
label_set_load = yy

total_num_data = np.size(data_set_load,0)
data_train = data_set_load[0:int(np.floor(total_num_data*ratio_train)),:,:,:]
label_train = label_set_load[0:int(np.floor(total_num_data*ratio_train))]
data_test = data_set_load[int(np.floor(total_num_data*ratio_train)):,:,:,:]
label_test = label_set_load[int(np.floor(total_num_data*ratio_train)):]

#x_train, y_train = (np.asarray(x[0:threshold_train]), np.asarray(y[0:threshold_train]))
#x_test, y_test = (np.asarray(x[threshold_train:]), np.asarray(y[threshold_train:]))
# =============================================================================
# x_train, y_train = tf.Variable(x[0:450], tf.float32), tf.Variable(y[0:450], tf.int32)
# x_test, y_test = tf.Variable(x[450:], tf.float32), tf.Variable(y[450:], tf.int32)
# =============================================================================

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(5, 20, 20), dtype='float32'))
#model.add(tf.keras.layers.Conv2D(5, 4, data_format='channels_first', activation='linear'))
#model.add(tf.keras.layers.Flatten(data_format='channels_first'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(2000, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1800, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1500, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1200, activation=tf.nn.relu))
#model.add(tf.keras.layers.Dropout(0.2),)
model.add(tf.keras.layers.Dense(max_y+1, activation=tf.nn.softmax))

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

model.fit(data_train, label_train, epochs=10, steps_per_epoch=30)
model.evaluate(data_test, label_test)
#model.evaluate(x_train, y_train)
