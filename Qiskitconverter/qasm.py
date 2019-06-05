# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:43:58 2019

@author: zxz58
"""
import circuittransform as ct

def ConvertQASM(input_file_name, output_file_name=None):
    '''
    convert a QASM file to a new one containing only CNOT gates
    '''
    QASM_location = 'C:/ProgramData/Anaconda3/Lib/site-packages/circuittransform/inputs/QASM example/'
#    QASM_location2 = 'inputs/QASM example/'
    QASM_file = open(QASM_location + input_file_name, 'r')
    iter_f = iter(QASM_file)
    QASM = ''
    reserve_line = 4
    num_line = 0
    for line in iter_f: #遍历文件，一行行遍历，读取文本
        num_line += 1
        '''keep head'''
        if num_line <= reserve_line:
            QASM = QASM + line
        else:
            if line[0:2] == 'cx':
                QASM = QASM + line
    QASM_file.close()
    '''write to new QASM file'''
    if output_file_name == None:
        new_file = open(QASM_location + input_file_name[0:-5] + '_CXonly' + '.qasm', 'w')
    else:
        new_file = open(QASM_location + output_file_name, 'w')
    new_file.write(QASM)
    new_file.close()
    
if __name__ == '__main__':
    ConvertQASM('ising_model_10.qasm')