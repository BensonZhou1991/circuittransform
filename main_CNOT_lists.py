# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:30:49 2019

@author: zxz58

create CNOT Lists
"""

import circuittransform as ct

num_file = 0
#QASM_files = ['ising_model_10.qasm', 'max46_240.qasm', 'qft_10.qasm', 'sqn_258.qasm', 'sys6-v0_111.qasm', 'hwb9_119.qasm']
QASM_files = ('4mod5-v1_22.qasm',
    'mod5mils_65.qasm',
    'alu-v0_27.qasm',
    'decod24-v2_43.qasm',
    '4gt13_92.qasm',
    'ising_model_10.qasm',
    'ising_model_13.qasm',
    'ising_model_16.qasm',
    'qft_10.qasm',
    'qft_16.qasm',
    'rd84_142.qasm',
    'adr4_197.qasm',
    'radd_250.qasm',
    'z4_268.qasm',
    'sym6_145.qasm',
    'misex1_241.qasm',
    'rd73_252.qasm',
    'cycle10_2_110.qasm',
    'square_root_7.qasm',
    'sqn_258.qasm',
    'rd84_253.qasm',
    'co14_215.qasm',
    'sym9_193.qasm',
    '9symml_195.qasm',
    )

for file in QASM_files:
    num_file += 1
    res = ct.CreateDGfromQASMfile(file)
    DG = res[1][0]
    CNOT_list = ct.CreateCNOTList(DG)
    f = open('CNOT_lists/' + file + '.txt', 'w')
    f.write(str(CNOT_list))
    f.close()

