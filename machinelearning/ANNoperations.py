# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 18:06:26 2019

@author: zxz58
"""


def CalSwapCostViaANN(ANN, data_set):
    '''
    input:
        ANN and data set to be inputted
    output:
        
    '''
    result_raw = ANN.predict(data_set)
    result = []
    num_data = result_raw.shape[0]
    num_label = result_raw.shape[1]
    '''cal result for each data'''
    for i in range(num_data):
        res_add = 0
        for j in range(num_label):
            possibility = result_raw[i][j]
            if possibility > 0.01:
                res_add += possibility * j
        result.append(res_add)
    
    return result