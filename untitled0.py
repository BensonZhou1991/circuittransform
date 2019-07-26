# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:13:02 2019

@author: zxz58
"""

import circuittransform as ct

'''this file is used to calculate the CNOT number of each qasm circuit'''

QASM_files = ['mini_alu_305.qasm',
'qft_10.qasm',
'sys6-v0_111.qasm',
'rd73_140.qasm',
'sym6_316.qasm',
'rd53_311.qasm',
'sym9_146.qasm',
'rd84_142.qasm',
'ising_model_10.qasm',
'cnt3-5_180.qasm',
'qft_16.qasm',
'ising_model_13.qasm',
'ising_model_16.qasm',
'wim_266.qasm',
'cm152a_212.qasm',
'cm42a_207.qasm',
'pm1_249.qasm',
'dc1_220.qasm',
'squar5_261.qasm',
'sqrt8_260.qasm',
'z4_268.qasm',
'adr4_197.qasm',
'sym6_145.qasm',
'misex1_241.qasm',
'square_root_7.qasm',
'ham15_107.qasm',
'dc2_222.qasm',
'sqn_258.qasm',
'inc_237.qasm',
'co14_215.qasm',
'life_238.qasm',
'max46_240.qasm',
'9symml_195.qasm',
'dist_223.qasm',
'sao2_257.qasm',
'plus63mod4096_163.qasm',
'urf6_160.qasm',
'hwb9_119.qasm']

CX_num = []
for file in QASM_files:
    print(file)
    res = ct.CreateDGfromQASMfile(file)
    res_qasm = ct.CreateDGfromQASMfile(file)
    DG = res_qasm[1][0]
    CX_num.append(len(DG.nodes()))