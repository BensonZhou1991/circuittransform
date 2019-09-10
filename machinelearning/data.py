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
from scoop import futures
import time

def GenNumCNOT(max_num):
    '''Generate number of CX gates randomly'''
    num_gate = np.random.randint(max_num) + 1
    return num_gate

def GenNumCNOTMultiLayer(max_num, num_layer):
    '''Generate numbers of CX gates randomly for multilayers'''
    num_gate = np.random.randint(1, max_num + 1, num_layer)
    return num_gate

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

def CreateCircuitMapMultiLayer(CNOT_list, num_q_log, num_layer):
    '''
    create a numpy matrix to represent the circuit with multi-layers containing
    only CNOT gates
    input:
        num_q_log -> total number of logical qubits. E.g., 4
        CNOT_list -> list of CNOT contains tuples showing input logical qubits
                     for corresponding CNOT gates.
                     E.g., [(0, 2), (3, 1), (2, 3) ...]
        output:
            [0 0 1 0
             0 0 0 0
             0 0 0 0
             0 1 0 0]
            [0 0 0 0
             0 0 0 0
             0 0 0 1
             0 0 0 0]
            ......
    '''
    cir_map = np.zeros([num_layer, num_q_log, num_q_log]).astype(np.float32)
    qubit_usage = [0]*num_q_log
    for CNOT in CNOT_list:
        q_c = CNOT[0]
        q_t = CNOT[1]
        '''check the number of layer'''
        l1 = qubit_usage[q_c]
        l2 = qubit_usage[q_t]
        layer = max(l1, l2)
        '''renew map data'''
        cir_map[layer][q_c][q_t] += 1
        '''renew qubit usage'''
        qubit_usage[q_c] = layer + 1
        qubit_usage[q_t] = layer + 1
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

def CreateOneRandomDataMultiLayer(num_CNOT, num_qubits, G, q_phy, q_log, shortest_length_G,
                        shortest_path_G, possible_swap_combination, num_layer):
    '''
    generate specific number of CNOT gates randomly in one layer exactly
    input:
        num_CNOT -> list for numbers of CNOT gates in each layer
    output:
        data, label(mini swap cost)
    '''
    CNOT_list, CNOT_operations = [], []
    for i in range(num_layer):
        CNOT_list_add, CNOT_operations_add = ct.CreateCNOTRandomlyOneLayer(q_log, num_CNOT[i])
        CNOT_list.extend(CNOT_list_add)
        CNOT_operations.extend(CNOT_operations_add)
    '''create data map'''
    data = CreateCircuitMapMultiLayer(CNOT_list, num_qubits, num_layer)
    '''check whether last layer has no gates, if yes, add gates randomly until no'''
    while np.max(data[num_layer-1]) == 0:
        CNOT_list_add, CNOT_operations_add = ct.CreateCNOTRandomlyOneLayer(q_log, 1)
        CNOT_list.extend(CNOT_list_add)
        CNOT_operations.extend(CNOT_operations_add)
        data = CreateCircuitMapMultiLayer(CNOT_list, num_qubits, num_layer)
        
    ct.GenerateDependency(CNOT_operations, num_qubits)
    '''create label'''
# =============================================================================
#     label = CreateLabelViaAstar(CNOT_operations, G, q_phy, q_log, shortest_length_G,
#                                 possible_swap_combination)
# =============================================================================
    label = CreateLabelViaZHOU(CNOT_operations, G, q_phy, q_log,
                               shortest_length_G, shortest_path_G)
    return data, label

def CreateRandomDataSet(num_data, num_qubits, method_AG, num_layer=1):
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
        
    '''create data set for 1 layer'''
    if num_layer == 1:
        data_set = []
        label_set = []
        for i in range(num_data):
            print('generating ', i+1, '/', num_data,'data')
            num_CNOT = GenNumCNOT(np.floor(num_qubits/2))
            data_add, label_add = CreateOneRandomData(num_CNOT, num_qubits, G, q_phy, q_log,
                                                      shortest_length_G, shortest_path_G,
                                                      possible_swap_combination)
            data_set.append(data_add)
            label_set.append(label_add)
    else:
        data_set = np.zeros([num_data, num_layer, num_qubits, num_qubits]).astype(np.float32)
        label_set = np.zeros([num_data]).astype(np.float32)
# =============================================================================
#         for i in range(num_data):
#             print('generating ', i+1, '/', num_data,'data')
#             num_CNOT = GenNumCNOTMultiLayer(np.floor(num_qubits/2), num_layer)
# #            print('num of CNOTs are ', num_CNOT)
#             data_add, label_add = CreateOneRandomDataMultiLayer(
#                     num_CNOT, num_qubits,G, q_phy, q_log, shortest_length_G,
#                     shortest_path_G, possible_swap_combination, num_layer)
#             data_set[i] = data_add
#             label_set[i] = label_add
# =============================================================================
        '''map implememtation for multi-layers'''
        print('generating CNOT numbers')
        num_CNOT = futures.map(GenNumCNOTMultiLayer, [np.floor(num_qubits/2)]*num_data,
                                              [num_layer]*num_data)
        print('generating layer layouts and labels')
        res = futures.map(CreateOneRandomDataMultiLayer, num_CNOT, [num_qubits]*num_data,
                  [G]*num_data, [q_phy]*num_data, [q_log]*num_data,
                  [shortest_length_G]*num_data, [shortest_path_G]*num_data,
                  [possible_swap_combination]*num_data, [num_layer]*num_data)
        print('processing output data')
        i = -1
        for data in res:
            i += 1
            data_add, label_add = data
            data_set[i] = data_add
            label_set[i] = label_add
    
    return data_set, label_set
    
if __name__ == '__main__': 
    '''this template is to generate data set with map and label'''
    method_AG = ['IBM QX20']
    num_qubits = 20
    data_set = []
    label_set = []
    total_num = 4
    set_num = 2
    num_layer = 5
    num_data = int(total_num/set_num)
    data_set = np.zeros([total_num, num_layer, num_qubits, num_qubits]).astype(np.float32)
    label_set = np.zeros([total_num]).astype(np.float32)
    print('total circuits number is %d and will be divided into %d sets' %(total_num, set_num))
    for i in range(set_num):
        start = time.time()
        print('round ', i+1, ' of ', set_num)
        data_set_add, label_set_add = CreateRandomDataSet(num_data, num_qubits,
                                                          method_AG, num_layer)
        data_set[i*num_data:i*num_data+num_data] = data_set_add
        label_set[i*num_data:i*num_data+num_data] = label_set_add
        end = time.time()
        print('time cost for this round is %s seconds' %(end-start))
    np.savez(str(num_layer)+' layers '+str(total_num)+' circuits',
             data_set=data_set, label_set=label_set)
    load_file = np.load(str(num_layer)+' layers '+str(total_num)+' circuits.npz')
    data_set_load = load_file['data_set']
    label_set_load = load_file['label_set']
    load_file.close()