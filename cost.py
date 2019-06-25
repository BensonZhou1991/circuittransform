# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:20:10 2019

@author: Xiangzhen Zhou
"""

from circuittransform import OperationU
from qiskit import QuantumRegister
import networkx as nx
import circuittransform as ct
import copy

def OperationCost(dom, mapping, G = None, shortest_length = None, edges_DiG=None, shortest_path_G=None):
    '''
    calculate the cost(number of swaps) of input operation with its corresponding map in an unidrected architecture graph
    via the length of shortest path between 2 input qubits
    input:
        dom: an U operation or a list of its corresponding qubits or vertexes in architecture graph
    '''
    if isinstance(dom, OperationU):
        q0 = dom.involve_qubits[0]
        q1 = dom.involve_qubits[1]
        v0 = mapping.DomToCod(q0)
        v1 = mapping.DomToCod(q1)
    if isinstance(dom, list):
        # dom is qubits
        if isinstance(dom[0], tuple):
            q0 = dom[0]
            q1 = dom[1]
            v0 = mapping.DomToCod(q0)
            v1 = mapping.DomToCod(q1)
        # dom is vertexes
        else:
            v0 = dom[0]
            v1 = dom[1]
    
    if shortest_length != None:
        cost = shortest_length[v0][v1] - 1
    else:
        cost = nx.shortest_path_length(G, source=v0, target=v1, weight=None, method='dijkstra') - 1
    
    if edges_DiG != None:
        flag_4H = ct.CheckCNOTNeedConvertDirection(v0, v1, shortest_path_G[v0][v1], edges_DiG)
        cost += flag_4H * 4/7 #we only count the number of SWAP gates
    return cost

def HeuristicCostZulehner(current_map, DG, executable_vertex, shortest_length_G, shortest_path_G=None, DiG=None):
    '''
    Calculate heuristic cost for remaining gates
    see "An Efficient Methodology for Mapping Quantum Circuits to the IBM QX Architectures"
    '''
    worst_num_swap = None
    count_same_worst = 0
    sum_num_swap = 0
    best_num_swap = None
    mapping = current_map
    flag_finished = True
    if DiG != None: edges = list(DiG.edges)
    for v_DG in executable_vertex:
        current_operation = DG.node[v_DG]['operation']
        q0 = current_operation.involve_qubits[0]
        q1 = current_operation.involve_qubits[1]
        v0 = mapping.DomToCod(q0)
        v1 = mapping.DomToCod(q1)
        current_num_swap = shortest_length_G[v0][v1] - 1
        if current_num_swap > 0: flag_finished = False
        '''if architecture graph is directed, confirm whether use 4 H gates to change direction'''
        if DiG != None:
            flag_4H = ct.CheckCNOTNeedConvertDirection(v0, v1, shortest_path_G[v0][v1], edges)
            #print('flag_4H is', flag_4H)
            current_num_swap += flag_4H * 4/7 #we only count the number of SWAP gates
        '''renew number of all swaps'''
        sum_num_swap = sum_num_swap + current_num_swap
        '''renew swap number of worst operation'''
        if worst_num_swap == None:
            worst_num_swap = current_num_swap
            worst_vertex = v_DG
        else:
            if current_num_swap > worst_num_swap:
                worst_num_swap = current_num_swap
                worst_vertex = v_DG
                count_same_worst = 0
            else:
                if current_num_swap == worst_num_swap:
                    count_same_worst += 1
        '''renew swap number of best operation'''
        if best_num_swap == None:
            best_num_swap = current_num_swap
        else:
            if current_num_swap < best_num_swap:
                best_num_swap = current_num_swap
        
# =============================================================================
#     worst_num_swap += sum_num_swap/100 #when identical worst costs for different gates exist, consider sum of swaps as second goal
# =============================================================================
    return worst_num_swap, sum_num_swap, best_num_swap, count_same_worst, worst_vertex, flag_finished

def HeuristicCostZulehnerLookAhead(current_map, DG, executable_vertex, shortest_length_G, shortest_path_G=None, DiG=None):
    '''
    Calculate heuristic cost for remaining gates
    see "An Efficient Methodology for Mapping Quantum Circuits to the IBM QX Architectures"
    '''
    sum_num_swap = 0
    current_H_num = 0
    mapping = current_map
    finished = False
    if DiG != None: edges = list(DiG.edges)
    '''calculate cost for current level'''
    for v_DG in executable_vertex:
        current_operation = DG.node[v_DG]['operation']
        q0 = current_operation.involve_qubits[0]
        q1 = current_operation.involve_qubits[1]
        v0 = mapping.DomToCod(q0)
        v1 = mapping.DomToCod(q1)
        current_num_swap = shortest_length_G[v0][v1] - 1
        '''if architecture graph is directed, confirm whether use 4 H gates to change direction'''
        if DiG != None:
            flag_4H = ct.CheckCNOTNeedConvertDirection(v0, v1, shortest_path_G[v0][v1], edges)
            current_H_num += flag_4H * 4/7 #we only count the number of SWAP gates
        '''renew number of all swaps'''
        sum_num_swap = sum_num_swap + current_num_swap
    current_level_num_swap = sum_num_swap
    if current_level_num_swap == 0: finished = True
    current_level_num_swap += current_H_num
    sum_num_swap += current_H_num
    '''calculate cost for next level'''
    DG_copy = DG.copy()
    DG_copy.remove_nodes_from(executable_vertex)
    lookahead_vertex = ct.FindExecutableNode(DG_copy)
    for v_DG in lookahead_vertex:
        current_operation = DG.node[v_DG]['operation']
        q0 = current_operation.involve_qubits[0]
        q1 = current_operation.involve_qubits[1]
        v0 = mapping.DomToCod(q0)
        v1 = mapping.DomToCod(q1)
        current_num_swap = shortest_length_G[v0][v1] - 1
        '''if architecture graph is directed, confirm whether use 4 H gates to change direction'''
        if DiG != None:
            flag_4H = ct.CheckCNOTNeedConvertDirection(v0, v1, shortest_path_G[v0][v1], edges)
            current_num_swap += flag_4H * 4/7
        '''renew number of all swaps'''
        sum_num_swap = sum_num_swap + current_num_swap
    
    return sum_num_swap, current_level_num_swap, finished

def HeuristicCostZhou1(current_map, DG, executed_vertex, executable_vertex, shortest_length_G, shortest_path_G, level_lookahead, DiG=None):
    '''
    Calculate heuristic cost for remaining gates and return best path
    this cost is based on the minimial distance in architecture graph between two input qubits of each operations
    '''
    worst_num_swap = None
    count_same_worst = 0
    sum_num_swap = 0
    best_num_swap = None
    mapping = current_map
    best_executable_vertex = None
    best_path = None
    if DiG != None: edges = list(DiG.edges)
    #DG_copy = copy.deepcopy(DG)
    executable_vertex_copy = executable_vertex.copy()
    executed_vertex_copy = executed_vertex.copy()
    for current_lookahead_level in range(len(level_lookahead)):
        if current_lookahead_level == 0:
            '''current level'''
            current_executable_vertex = executable_vertex_copy
            weight = 1
        else:
            '''lookahead level'''
            #DG_copy.remove_nodes_from(executable_vertex)
            current_executable_vertex = ct.FindExecutableNode(DG, executed_vertex_copy, current_executable_vertex, current_executable_vertex.copy())
            weight = level_lookahead[current_lookahead_level - 1]
            
        for v_DG in current_executable_vertex:
            flag_4H = 0
            current_operation = DG.node[v_DG]['operation']
            q0 = current_operation.involve_qubits[0]
            q1 = current_operation.involve_qubits[1]
            v0 = mapping.DomToCod(q0)
            v1 = mapping.DomToCod(q1)
            current_num_swap = shortest_length_G[v0][v1] - 1
            '''if architecture graph is directed, confirm whether use 4 H gates to change direction'''
            if DiG != None:
                flag_4H = ct.CheckCNOTNeedConvertDirection(v0, v1, shortest_path_G[v0][v1], edges)
            current_num_swap += flag_4H * 4/7
            '''renew number of all swaps'''
            current_num_swap = current_num_swap * weight#multiply the weight for cost of gates in different levels
            sum_num_swap = sum_num_swap + current_num_swap
            '''renew swap number of worst operation'''
            if worst_num_swap == None:
                worst_num_swap = current_num_swap
                count_same_worst = 0
            else:
                if current_num_swap > worst_num_swap:
                    worst_num_swap = current_num_swap
                    count_same_worst = 0
                else:
                    if current_num_swap == worst_num_swap:
                        count_same_worst += 1
            '''renew swap number of best operation'''
            if best_num_swap == None:
                best_num_swap = current_num_swap
                best_path = shortest_path_G[v0][v1]
                best_executable_vertex = v_DG
            else:
                if current_num_swap < best_num_swap:
                    best_num_swap = current_num_swap
                    best_path = shortest_path_G[v0][v1]
                    best_executable_vertex = v_DG
        
    return worst_num_swap, sum_num_swap, best_num_swap, best_executable_vertex, best_path, count_same_worst