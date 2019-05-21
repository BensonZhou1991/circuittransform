# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:30:49 2019

@author: zxz58

create CNOT Lists
"""

import circuittransform as ct

num_file = 0
QASM_files = ['ising_model_10.qasm', 'max46_240.qasm', 'qft_10.qasm', 'sqn_258.qasm', 'sys6-v0_111.qasm', 'hwb9_119.qasm']
#QASM_files = ['qft_10.qasm', 'sqn_258.qasm']

for file in QASM_files:
    num_file += 1
    res = ct.CreateDGfromQASMfile(file)
    DG = res[1][0]
    CNOT_list = ct.CreateCNOTList(DG)
    f = open('CNOT_lists/' + file + '.txt', 'w')
    f.write(str(CNOT_list))
    f.close()

