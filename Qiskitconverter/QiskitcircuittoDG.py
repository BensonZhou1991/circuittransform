# -*- coding: utf-8 -*-
"""
Created on Tue May 14 22:14:39 2019

@author: zxz58
"""
import networkx as nx
import circuittransform as ct
from circuittransform import OperationU, OperationCNOT

def QiskitGateToOperation(Gate):
    '''
    convert a Qiskit Gate object to OperationU
    only support CNOT
    '''
    if Gate.name == 'cx':
        qargs = Gate.qargs
        return OperationCNOT(qargs[0], qargs[1])
    
    return None
        

def QiskitCircuitToDG(cir):
    '''
    convert Qiskit circuit to DG
    support only CNOT gate
    '''
    operations = []
    num_unidentified_gates = 0
    qregs = cir.qregs
    if len(qregs) > 1:
        raise Exception('quantum circuit has more than 1 quantum register')
    q = qregs[0]
    data = cir.data
    for gate in data:
        operation = QiskitGateToOperation(gate)
        if operation == None:
            num_unidentified_gates += 1
        else:
            operations.append(operation)
    ct.GenerateDependency(operations, q.size)
    DG = ct.OperationToDependencyGraph(operations)
    
    return DG, num_unidentified_gates, q, operations