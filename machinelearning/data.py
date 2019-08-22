# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 17:40:04 2019

@author: zxz58
"""
import numpy as np
from circuittransform import Map
import circuittransform as ct
import networkx as nx
from networkx import DiGraph, Graph
from qiskit import QuantumRegister, QuantumCircuit

def CreateCircuitMap(CNOT_list, num_q_log, layer_cheak=False):
    '''
    create a numpy matrix to represent the circuit with only one layer containing
    only CNOT gates
    input:
        num_q_log -> total number of logical qubits. E.g., 4
        CNOT_list -> list of CNOT contains tuples showing input logical qubits
                     for corresponding CNOT gates.
                     E.g., [(0, 2), (3, 1), ...]
        output:
            [0 0 1 0
             0 0 0 0
             0 0 0 0
             0 1 0 0]
    '''
    cir_map = np.zeros([num_q_log, num_q_log])
    for CNOT in CNOT_list:
        q_c = CNOT[0]
        q_t = CNOT[1]
        cir_map[q_c][q_t] += 1
    if layer_cheak == True:
        check1 = sum(cir_map)
        check2 = sum(np.transpose(cir_map))
        for i in range(num_q_log):
            if check1[i] > 1 or check2[i] > 1:
                raise(BaseException('input CNOT list forms more than 1 layer'))
    return cir_map

def CreateLabelViaAstar(CNOT_list, G, q_phy, q_log, shortest_length_G, possible_swap_combination):
    '''
    create minimum SWAP cost for a single layer via Astar
    '''
    DG = ct.OperationToDependencyGraph(CNOT_list)
    cir_phy = QuantumCircuit(q_phy)
    initial_map = Map(q_log, G)
    res = ct.AStarSearch(q_phy, cir_phy, G, DG, initial_map, shortest_length_G,
                         possible_swap_combination=possible_swap_combination)
    return res[0]

def CreateLabelViaZHOU(CNOT_list, G, q_phy, q_log, shortest_length_G, shortest_path_G):
    '''
    create minimum SWAP cost for a single layer via our proposed method
    '''
    DG = ct.OperationToDependencyGraph(CNOT_list)
    cir_phy = QuantumCircuit(q_phy)
    initial_map = Map(q_log, G)
    res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG, initial_map,
                                          shortest_length_G, shortest_path_G,
                                          depth_lookahead=1, use_prune=False,
                                          draw=False, DiG=None, level_lookahead=None)
    return res[0]

def CreateOneRandomData(num_CNOT, num_qubits, G, q_phy, q_log, shortest_length_G,
                        shortest_path_G, possible_swap_combination):
    '''
    generate specific number of CNOT gates randomly in one layer exactly
    input:
        num_CNOT -> number of CNOT gates
    output:
        data, label(mini swap cost)
    '''
    CNOT_list, CNOT_operations = ct.CreateCNOTRandomlyOneLayer(q_log, num_CNOT)
# =============================================================================
#     label = CreateLabelViaAstar(CNOT_operations, G, q_phy, q_log, shortest_length_G,
#                                 possible_swap_combination)
# =============================================================================
    label = CreateLabelViaZHOU(CNOT_operations, G, q_phy, q_log,
                               shortest_length_G, shortest_path_G)
    data = CreateCircuitMap(CNOT_list, num_qubits, layer_cheak=True)
    return data, label

def CreateRandomDataSet(num_data, num_qubits, method_AG):
    '''
    generate data set for single layer containing only CNOT gates
    '''
    
    '''generate quantum qubits'''
    q_phy = QuantumRegister(num_qubits, 'v')
    q_log = QuantumRegister(num_qubits, 'q')
    
    '''generate architecture graph'''
    '''q0 - v0, q1 - v1, ...'''
    G = ct.GenerateArchitectureGraph(num_qubits, method_AG)
    DiG = None
    if isinstance(G, DiGraph): #check whether it is a directed graph
        DiG = G
        G = nx.Graph(DiG)
        
    '''only use single swap'''
    possible_swap_combination = []
    edges = list(G.edges()).copy()
    for current_edge in edges:
        possible_swap_combination.append([current_edge]) 
        
    '''calculate shortest path and its length'''
    if DiG == None:
        res = ct.ShortestPath(G)
        shortest_path_G = res[1]
        shortest_length_G = (res[0], res[2])
    else:
        res = ct.ShortestPath(DiG)
        shortest_path_G = res[1]
        shortest_length_G = (res[0], res[2])
        
    '''create data set'''
    data_set = []
    label_set = []
    for i in range(num_data):
        print('generating ', i, '/', num_data,'data')
        num_CNOT = np.random.randint(np.floor(num_qubits/2)) + 1
        data_add, label_add = CreateOneRandomData(num_CNOT, num_qubits, G, q_phy, q_log,
                                                  shortest_length_G, shortest_path_G,
                                                  possible_swap_combination)
        data_set.append(data_add)
        label_set.append(label_add)
    
    return data_set, label_set
    
if __name__ == '__main__': 
    method_AG = ['IBM QX20']
    num_qubits = 20
    data_set = []
    label_set = []
    for i in range(5):
        num_data = 10000
        data_set_add, label_set_add = CreateRandomDataSet(num_data, num_qubits, method_AG)
        data_set.extend(data_set_add)
        label_set.extend(label_set_add)