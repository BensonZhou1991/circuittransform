# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 22:54:17 2019

@author: zxz58
"""

import circuittransform as ct
import tensorflow as tf
import numpy as np

ANN = tf.keras.models.load_model('my_model.h5')
method_AG = ['IBM QX20']
num_qubits = 20
num_data = 50
error = []
error2 = []
data_set = np.zeros([num_data, num_qubits, num_qubits])
data_set_add, label_set = ct.machinelearning.CreateRandomDataSet(num_data, num_qubits, method_AG)
for i in range(num_data):
    data_set[i] = data_set_add[i]
res = ct.machinelearning.CalSwapCostViaANN(ANN, data_set)
for i in range(num_data):
    error.append(label_set[i] - res[i])
'''cal dis via shortes distance'''
'''generate architecture graph'''
G = ct.GenerateArchitectureGraph(num_qubits, method_AG)
'''calculate shortest path and its length'''
shortest_length_G = ct.ShortestPath(G)[0]
label_shortest_dis = [0] * num_data
for k in range(num_data):
    for i in range(num_qubits):
        for j in range(num_qubits):
            if data_set[k][i][j] == 1: label_shortest_dis[k] += shortest_length_G[i][j]-1
for i in range(num_data):
    error2.append(label_shortest_dis[i] - res[i])
#print('error is ', error)
print('max error between our method and ANN is ', max(error))
print('max error between sum of shoteset path and ANN is ', max(error2))