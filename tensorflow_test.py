# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 12:37:36 2019

@author: zxz58
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import circuittransform as ct
import numpy as np

model = tf.keras.models.load_model('my_model.h5')
data = np.zeros([1, 20, 20])
data[0] = ct.machinelearning.CreateCircuitMap([(0,5)],20)
result = model.predict(data)