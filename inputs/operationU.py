# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:57:54 2019

@author: Xiangzhen Zhou

"""

from qiskit.circuit import Gate
from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit.extensions import standard
from qiskit.extensions.standard.cx import CnotGate
import circuittransform as ct

class OperationU(object):
    '''
    Unitary operation
    '''
    
    instances_count = 0
    
    def __init__(self, qbits, d_o=[], time_cost=1):
        '''
        qbits: list of all input qubits
        d_qs: list of dependent operations
        '''
        self.involve_qubits = qbits
        self.dependent_operations = list(set(d_o))
        self.DeleteRedundantDependentOperation()
        # whether this instance is conducted in QPU
        self.conducted = False
        self.time_cost = time_cost
        self._RefreshDependencySet()
        OperationU.instances_count = OperationU.instances_count + 1
        
    def _RefreshDependencySet(self):
        self.dependency_set = []
        if self.dependent_operations != []:
            for dependent_operation in self.dependent_operations:
                self.dependency_set.extend(dependent_operation.dependency_set)
                self.dependency_set.append(dependent_operation)
        # remove reduplicative elements
        self.dependency_set = list(set(self.dependency_set))
    
    def DeleteRedundantDependentOperation(self):
        '''
        delete some dependent operations that already have dependent relationship
        '''
        if self.dependent_operations != []:
            for current_operation in self.dependent_operations:
                flag = False
                for test_operation in self.dependent_operations:
                    if current_operation in test_operation.dependency_set:
                        flag = True
                        break
                if flag == True:
                    self.dependent_operations.remove(current_operation)
        
    def CheckImplementation(self):
        '''
        check whether this operation is ready to be conducted, i.e.,
        all its dependent_operations have been conducted
        Return:
            True: this operation can be implemented
        '''
        if self.dependent_operations == []:
            return True
        else:
            re = True
            for i in self.dependent_operations:
                re = re and i.conducted
            return re
        

class OperationCNOT(OperationU):
    '''
    CNOT Unitary operation
    '''
    
    instances_count = 0
    
    def __init__(self, c_q, t_q, d_o=[]):
        '''
        d_qs: list of dependent operations
        '''
        self.control_qubit = c_q
        self.target_qubit = t_q        
        super().__init__([c_q, t_q], d_o, time_cost=10)
        OperationCNOT.instances_count = OperationCNOT.instances_count + 1
        
    def ConductOperation(self, cir):
        '''
        Perform operation in Quantum Circuit object Cir
        '''        
        cir.cx(self.control_qubit, self.target_qubit)
        
    def ConductOperationOutside(self, cir, q_c, q_t):
        '''
        Perform operation in other quantum quits
        '''             
        cir.cx(q_c, q_t)
        self.conducted = 1
        
    def CalSWAPCost(self, mapping, shortest_length_G_with4H):
        v_c = mapping.LogToPhy(self.control_qubit)
        v_t = mapping.LogToPhy(self.target_qubit)
        swap_cost = shortest_length_G_with4H[v_c][v_t] - 1
        return swap_cost

class OperationSWAP(OperationU):
    '''
    SWAP Unitary operation
    the input may be logical or physical qubits
    '''
    
    instances_count = 0
    
    def __init__(self, q0, q1, d_o=[]):      
        super().__init__([q0, q1], d_o, time_cost=30)
        OperationSWAP.instances_count = OperationSWAP.instances_count + 1
        
    def ConductOperation(self, cir):
        '''
        Perform operation in Quantum Circuit object Cir
        '''        
        cir.swap(self.involve_qubits[0], self.involve_qubits[1])
        
    def ConductOperationOutside(self, cir, q0, q1):
        '''
        Perform operation in other quantum quits
        '''             
        cir.swap(q0, q1)
        self.conducted = 1
        
    def ConductOperationInPhysicalCircuit(self, cir_phy, mapping):
        v0 = self.involve_qubits[0][1]
        v1 = self.involve_qubits[1][1]
        q_phy = self.involve_qubits[0][0]
        ct.SWAPInArchitectureGraph(v0, v1, mapping, q_phy, cir_phy)
        self.conducted = 1

class OperationBarrier():
    instances_count = 0
    
    def __init__(self):
        OperationBarrier.instances_count += 1
    
    def ConductOperationInPhysicalCircuit(self, cir, mapping=None):
        cir.barrier()

'''
test OperationCNOT
'''
if __name__ == '__main__':
    q = QuantumRegister(3, 'q')
    cir = QuantumCircuit(q)
    o1 = OperationCNOT(q[0], q[1])
    o2 = OperationCNOT(q[1], q[2], [o1])
    o3 = OperationCNOT(q[0], q[2], [o2])
    o1.ConductOperation(cir)
    o2.ConductOperation(cir)
    o3.ConductOperation(cir)
    image = cir.draw()
    print(image)