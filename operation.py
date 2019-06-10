# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 00:45:34 2019

@author: zxz58

This module is for functions on operations
"""

import networkx as nx
import numpy as np

def OperationToDependencyGraph(operations):
    '''
    create dependency graph
    input:
        operations a list of all operations instances
    '''
    num_vertex = len(operations)
    DG = nx.DiGraph()
    DG.add_nodes_from(list(range(num_vertex)))
    for i in range(num_vertex):
        current_operation = operations[i]
        DG.add_node(i, operation = current_operation)
        if current_operation.dependent_operations != []:
            DG.add_node(i, root = False)
            for current_de in current_operation.dependent_operations:
                DG.add_edge(operations.index(current_de), i)
        else:
            DG.add_node(i, root = True)
    
    return DG

def FindExecutableNode(dependency_graph):
    '''
    Use dependency graph to find the executable vertexes/nodes, i.e., nodes in current level
    return:
        executable_node: a list of nodes. If no executable node, return []
    '''
    DG = dependency_graph
    degree = DG.in_degree
    executable_node = []
    for i in degree:
        if i[1] == 0:
            executable_node.append(i[0])
    return executable_node
    
def FindExecutableOperation(dependency_graph, executable_node = None):
    '''
    Use dependency graph to find the executable operations
    return:
        executable_operation: a list of operations. If no executable operation, return []
    '''
    DG = dependency_graph
    executable_operation = []
    if executable_node == None:
        executable_node = FindExecutableNode(DG)
    for node in executable_node:
        executable_operation.append(DG.node[node]['operation'])
    return executable_operation

def ConductOperationInVertex(DG, vertex, mapping, cir_phy, q_phy):
    '''
    Conduct operation in physical quantum circuit represented by
    a node/vertex in dependency graph(directed graph), then, erase the corresponding
    node/vertex in dependency graph
    '''
    conduct_operation = DG.node[vertex]['operation']
    q_c = conduct_operation.control_qubit
    q_t = conduct_operation.target_qubit
    v_c = mapping.DomToCod(q_c)
    v_t = mapping.DomToCod(q_t)
    q_phy_c = q_phy[v_c]
    q_phy_t = q_phy[v_t]
    conduct_operation.ConductOperationOutside(cir_phy, q_phy_c, q_phy_t)
    DG.remove_node(vertex)

def ConductCNOTOperationInVertex(DG, vertex, mapping, cir_phy, q_phy, reverse_drection=False):
    '''
    conduct CNOT operation in physical quantum circuit represented by
    a node/vertex in dependency graph(directed graph), then, erase the corresponding
    node/vertex in dependency graph
    input:
        convert_drection -> whether use 4 H gates to reverse direction of CNOT
    '''
    conduct_operation = DG.node[vertex]['operation']
    q_c = conduct_operation.control_qubit
    q_t = conduct_operation.target_qubit
    v_c = mapping.DomToCod(q_c)
    v_t = mapping.DomToCod(q_t)
    q_phy_c = q_phy[v_c]
    q_phy_t = q_phy[v_t]
    if reverse_drection == True:
        cir_phy.h(q_phy_c)
        cir_phy.h(q_phy_t)
        cir_phy.cx(q_phy_t, q_phy_c)
        cir_phy.h(q_phy_c)
        cir_phy.h(q_phy_t)
    else:
        cir_phy.cx(q_phy_c, q_phy_t)
    DG.remove_node(vertex)
    
def SWAPInArchitectureGraph(vertex0, vertex1, mapping, q_phy, cir_phy):
    '''
    Conduct SWAP in physical qubits represented by nodes in architerture graph
    Then, renew physical circuit and mapping
    '''
    cir_phy.swap(q_phy[vertex0], q_phy[vertex1])
    mapping.RenewMapViaExchangeCod(vertex0, vertex1)
    
def RemoveUnparallelEdge(remain_edge, remove_edge):
    '''
    this function if for function FindAllPossibleSWAPParallel
    given a remain_edge set and a to be removed edge, this function will remove
    the given edge and others edges that are effected by this edge
    '''
    remain_edge.remove(remove_edge)
    n1 = remove_edge[0]
    n2 = remove_edge[1]
    iterate_edge = remain_edge.copy()
    for current_edge in iterate_edge:
        c1 = current_edge[0]
        c2 = current_edge[1]
        if (n1 == c1) or (n1 == c2) or (n2 == c1) or (n2 == c2):
            remain_edge.remove(current_edge)

def AddEdgeToList(total_swap, remain_edge):
    '''
    this is only for function FindAllPossibleSWAPParallel
    '''
    basic_combination = total_swap[-1].copy()
    for new_edge in remain_edge:
        #print(remain_edge)  
        new_combination = basic_combination.copy()
        new_combination.append(new_edge)
        total_swap.append(new_combination)
        next_remain_edge = remain_edge.copy()
        RemoveUnparallelEdge(next_remain_edge, new_edge)
        #print(next_remain_edge)
        if next_remain_edge != []:
            AddEdgeToList(total_swap, next_remain_edge)
        #print(remain_edge)

def RemoveRepetitiveSWAPCombination(total_swap):
    '''
    this is only for function FindAllPossibleSWAPParallel
    '''
    
    '''sort'''
    sort_key = lambda arg: arg[0]
    for current_swap in total_swap:
        current_swap.sort(key=sort_key)
        
    '''delete repetitive SWAP combinations'''
    i = -1
    while i < (len(total_swap) - 2):
        i += 1
        j = i
        while j < (len(total_swap) - 1):
            j += 1
            if total_swap[i] == total_swap[j]:
                total_swap.pop(j)
                j -= 1
    
def FindAllPossibleSWAPParallel(G, availiavle_vertex=None):
    '''
    find all possible combinations of SWAPs that can conducted in parallel
    return:
        list of vertex pairs each representing a SWAP, i.e., (((v00, v01), (v10, v11)...)...)
    '''
    total_swap = []
    if availiavle_vertex == None:
        node = list(G.node)
    else:
        node = availiavle_vertex
    edge = list(G.edges).copy()
    for current_edge in edge:
        total_swap.append([current_edge])
        remain_edge = edge.copy()
        RemoveUnparallelEdge(remain_edge, current_edge)
        if remain_edge != []:
            AddEdgeToList(total_swap, remain_edge)
    RemoveRepetitiveSWAPCombination(total_swap)
        
    return total_swap

def CalRemoteCNOTCostinArchitectureGraph(path, shortest_length_G=None):
    '''Calculate the number of CNOT in remote CNOT implementation, including the target CNOT operation'''
    dis = len(path) - 1
    if dis == 2:
        CNOT_cost = 4
    else:
        if dis ==3:
            CNOT_cost = 6
            
    return CNOT_cost

def RemoteCNOTinArchitectureGraph(path, cir_phy, q_phy):
    '''
    implement remote CNOT in physical circuit via path of nodes in architecture graph, i.e., [v_c, ..., v_t]
    '''
    num_CNOT = 0
    dis = len(path) - 1
    q = q_phy
    v_c = path[0]
    v_t = path[-1]
    if dis == 2:
        cir_phy.cx(q[v_c], q[path[1]])
        cir_phy.cx(q[path[1]], q[v_t])
        cir_phy.cx(q[v_c], q[path[1]])
        cir_phy.cx(q[path[1]], q[v_t])
        num_CNOT = num_CNOT + 4
    else:
        if dis == 3:
            cir_phy.cx(q[v_c], q[path[1]])
            cir_phy.cx(q[path[2]], q[v_t])
            cir_phy.cx(q[path[1]], q[path[2]])
            cir_phy.cx(q[v_c], q[path[1]])  
            cir_phy.cx(q[path[1]], q[path[2]])
            cir_phy.cx(q[path[2]], q[v_t])
            num_CNOT = num_CNOT + 6
                   
    return num_CNOT

def IsVertexInDGOperatiable(vertex, DG, G, mapping):
    '''check whether the vertex of DG can be executed, ignoring the dependency'''
    op = DG.node[vertex]['operation']
    q0 = op.involve_qubits[0]
    q1 = op.involve_qubits[1]
    v0 = mapping.DomToCod(q0)
    v1 = mapping.DomToCod(q1)
    if (v0, v1) in G.edges():
        return True
    else:
        return False
    
def CheckCNOTNeedConvertDirection(v_c, v_t, path, edges):
    l = len(path)
    for i in range(l-1):
        c_i = path[i]
        t_i = path[i+1]
        if (c_i, t_i) in edges:
            return False
    
    return True

def CheckCNOTNeedConvertDirection2(vertex, DG, mapping, edges):
    '''input is a node in DG'''
    op = DG.node[vertex]['operation']
    q0 = op.involve_qubits[0]
    q1 = op.involve_qubits[1]
    v0 = mapping.DomToCod(q0)
    v1 = mapping.DomToCod(q1)
    if (v0, v1) in edges:
        return False
    
    return True

def CheckSWAPInvolved(swaps, executable_vertex, DG, mapping):
    '''
    check whether the swaps has swap having no effect on any executable gate, if yes, return False
    '''
    q_phy = []
    for vertex in executable_vertex:
        op = DG.node[vertex]['operation']
        q0 = op.involve_qubits[0]
        q1 = op.involve_qubits[1]
        v0 = mapping.DomToCod(q0)
        v1 = mapping.DomToCod(q1)
        q_phy.extend([v0, v1])
    for swap in swaps:
        if (not (swap[0] in q_phy)) and (not (swap[1] in q_phy)):
            return False
    return True
        