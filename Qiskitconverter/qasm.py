# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:43:58 2019

@author: zxz58
"""
import circuittransform as ct
from qiskit import QuantumCircuit

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

def DrawCircuitFromQASM(input_file_name):
    '''
    draw quantum circuit from QASM file, treat all single-qubit gate as H, support only
    single-qubit and CNOT gate
    '''
    QASM_location = 'C:/ProgramData/Anaconda3/Lib/site-packages/circuittransform/inputs/QASM example/'    
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
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''CNOT'''
                QASM = QASM + 'cx' + line[2:]
            else:
                '''single-qubit gate'''
                for i in range(len(line)):
                    if line[i] == ' ':
                        QASM = QASM + 'h' + line[i:]
                        break
    cir = QuantumCircuit.from_qasm_str(QASM)
    fig = (cir.draw(scale=0.7, filename=None, style=None, output='mpl', interactive=False, line_length=None, plot_barriers=True, reverse_bits=False))
    fig.savefig(input_file_name[0:-5] + '.eps', format='eps', dpi=1000)    
    
if __name__ == '__main__':
    '''use ConvertQASM'''
    file_names = ('4mod5-v1_22.qasm',
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
    #map(ConvertQASM, file_names)
    for file_name in file_names:
        ConvertQASM(file_name)
    
    '''use DrawCircuitFromQASM'''
# =============================================================================
#     DrawCircuitFromQASM
# =============================================================================


