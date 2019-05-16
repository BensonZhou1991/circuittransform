# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:38:14 2019

@author: Xiangzhen Zhou
"""

import networkx as nx
from networkx.algorithms import approximation
import circuittransform as ct
import matplotlib.pyplot as plt
import numpy as np
from circuittransform import OperationCNOT
from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit import Aer, execute
import copy

def PerformRawAddinPartyMap(party_map, control_raw, target_raw):
    party_map[target_raw][:] = np.logical_xor(party_map[control_raw][:], party_map[target_raw][:])

def PerformOperationCNOTinPartyMap(party_map, operations):
    '''conduct CNOT operations in a party map'''
    flag_debug = 0
    for operation in operations:
        control_raw = operation.control_qubit[1]
        target_raw = operation.target_qubit[1]
        PerformRawAddinPartyMap(party_map, control_raw, target_raw)
        if flag_debug == 1: print('perform CNOT', [control_raw, target_raw])

def RemoteCNOTinArchitectureGraph(path, party_map, q):
    '''
    implement remote CNOT in party map via path of nodes in architecture graph, i.e., [v_c, ..., v_t]
    '''
    operation_CNOT = []
    dis = len(path) - 1
    v_c = path[0]
    v_t = path[-1]
    if dis == 2:
        add_CNOT = OperationCNOT(q[v_c], q[path[1]])
        operation_CNOT.append(add_CNOT)
        PerformRawAddinPartyMap(party_map, v_c, path[1])
        add_CNOT = OperationCNOT(q[path[1]], q[v_t])
        operation_CNOT.append(add_CNOT)
        PerformRawAddinPartyMap(party_map, path[1], v_t)
        add_CNOT = OperationCNOT(q[v_c], q[path[1]])
        operation_CNOT.append(add_CNOT)
        PerformRawAddinPartyMap(party_map, v_c, path[1])
        add_CNOT = OperationCNOT(q[path[1]], q[v_t])
        operation_CNOT.append(add_CNOT)
        PerformRawAddinPartyMap(party_map, path[1], v_t)
    else:
        if dis == 3:
            add_CNOT = OperationCNOT(q[v_c], q[path[1]])
            operation_CNOT.append(add_CNOT)
            PerformRawAddinPartyMap(party_map, v_c, path[1])
            add_CNOT = OperationCNOT(q[path[2]], q[v_t])
            operation_CNOT.append(add_CNOT)
            PerformRawAddinPartyMap(party_map, path[2], v_t)
            add_CNOT = OperationCNOT(q[path[1]], q[path[2]])
            operation_CNOT.append(add_CNOT)
            PerformRawAddinPartyMap(party_map, path[1], path[2])
            add_CNOT = OperationCNOT(q[v_c], q[path[1]])  
            operation_CNOT.append(add_CNOT)
            PerformRawAddinPartyMap(party_map, v_c, path[1])
            add_CNOT = OperationCNOT(q[path[1]], q[path[2]])
            operation_CNOT.append(add_CNOT)
            PerformRawAddinPartyMap(party_map, path[1], path[2])
        else:
            '''See Section 2B , arXiv:1904.01972'''
            '''first part'''
            for i in range(dis):
                R = []
                add_CNOT = OperationCNOT(q[path[-1-i-i]], q[path[-1-i]])
                R.append(add_CNOT)
            R_prime = copy.deepcopy(R_operation)
            R_prime.pop()
            R_prime.reverse()
            operation_CNOT.extend(R + R_prime)
            R_star = copy.deepcopy(R + R_prime)
            R_star.pop()
            R_star.pop(0)
            operation_CNOT.extend(R_star)
    
    return operation_CNOT

def GetSteinerTree(G, terminal_nodes):
    steiner_tree = nx.algorithms.approximation.steinertree.steiner_tree(G, terminal_nodes)

    return steiner_tree

def GenerateGetSteinerTreeInColunm(G, num_qubit, party_map, colunm):
    '''generate a Steiner tree in a column of a party map'''
    
    '''generate Steiner tree'''
    #nodes = party_map[(colunm+1):, colunm]
    terminal_nodes = [colunm]
    for i in range((colunm+1), num_qubit):
        if party_map[i][colunm] == 1:
            terminal_nodes.append(i)
    steiner_tree = GetSteinerTree(G, terminal_nodes)
    
    '''set values of nodes'''
    nodes = list(steiner_tree.nodes)
    for current_node in nodes:
        if party_map[current_node][colunm] == 1:
            steiner_tree.node[current_node]['party_map_value'] = 1
        else:
            steiner_tree.node[current_node]['party_map_value'] = 0    
            
    return steiner_tree, terminal_nodes

def FillSteinerTree(q, steiner_tree, party_map, terminal_nodes, shortest_path_steiner_tree):
    '''
    Use CNOT operation to set all nodes in steiner tree 1
    Refresh party map
    Return:
        list of CNOT operations
    '''
    
    operation_CNOT = []
    num_leaf = len(terminal_nodes) - 1
    root_node = terminal_nodes[0]
    
    for i in range(num_leaf):
        leaf_node = terminal_nodes[i+1]
        path = shortest_path_steiner_tree[root_node][leaf_node]
        l = len(path)
        for current_pos in range(l-2,-1,-1):
            current_node = path[current_pos]
            son_node = path[current_pos+1]
            if steiner_tree.node[current_node]['party_map_value'] == 0:
                add_CNOT = OperationCNOT(q[son_node], q[current_node])
                operation_CNOT.append(add_CNOT)
                party_map[current_node][:] = np.logical_xor(party_map[current_node][:], party_map[son_node][:])
                steiner_tree.node[current_node]['party_map_value'] = 1
                
    return operation_CNOT

def FillSteinerTreeRootToLeaf(q, steiner_tree, party_map, terminal_nodes, shortest_path_steiner_tree):
    '''
    Use CNOT operation to set all nodes in steiner tree 1 from root to leaf
    Refresh party map
    Return:
        list of CNOT operations
    '''
    
    operation_CNOT = []
    num_leaf = len(terminal_nodes) - 1
    root_node = terminal_nodes[0]
    
    for i in range(num_leaf):
        leaf_node = terminal_nodes[i+1]
        path = shortest_path_steiner_tree[leaf_node][root_node]
        l = len(path)
        for current_pos in range(l-2,-1,-1):
            current_node = path[current_pos]
            son_node = path[current_pos+1]
            if steiner_tree.node[current_node]['party_map_value'] == 0:
                add_CNOT = OperationCNOT(q[son_node], q[current_node])
                operation_CNOT.append(add_CNOT)
                party_map[current_node][:] = np.logical_xor(party_map[current_node][:], party_map[son_node][:])
                steiner_tree.node[current_node]['party_map_value'] = 1
                
    return operation_CNOT

def EmptySteinerTree(q, steiner_tree, party_map, terminal_nodes):            
    
    operation_CNOT = []
    DFT_edges = list(nx.dfs_edges(steiner_tree, source=terminal_nodes[0]))
    DFT_edges.reverse()
    
    for edge in DFT_edges:
        current_node = edge[0]
        son_node = edge[1]
        add_CNOT = OperationCNOT(q[current_node], q[son_node])
        operation_CNOT.append(add_CNOT)
        party_map[son_node][:] = np.logical_xor(party_map[current_node][:], party_map[son_node][:])
        steiner_tree.node[son_node]['party_map_value'] = 1
                
    return operation_CNOT
    
def PartyMapToUpperMatrix(party_map, G, q, num_qubit):
    '''
    Transform a party map to upper matrix
    See arXiv:1904.00633
    Return:
        Corresponding CNOT operations
    '''
    operation_CNOT = []
    nodes = list(G.nodes())
    nodes.sort()
    for column in nodes:
        if column == num_qubit-1: continue
        '''generate Steiner tree'''
        res = GenerateGetSteinerTreeInColunm(G, num_qubit, party_map, column)
        steiner_tree = res[0]
        terminal_nodes = res[1]
        # if all elements under diagonal element are 0, no need to do any transformation
        if len(terminal_nodes) == 1:
            G.remove_node(column)
            continue
        shortest_path_steiner_tree = nx.shortest_path(steiner_tree, source=None, target=None, weight=None, method='dijkstra')
        '''fill Steiner tree'''
        add_CNOTs = FillSteinerTree(q, steiner_tree, party_map, terminal_nodes, shortest_path_steiner_tree)
        operation_CNOT.extend(add_CNOTs)
        '''empty Steiner tree'''
        add_CNOTs = EmptySteinerTree(q, steiner_tree, party_map, terminal_nodes)
        operation_CNOT.extend(add_CNOTs)
        '''delete corresponding nodes in architecture graph'''
        G.remove_node(column)
        
    return operation_CNOT

def AllocateVertexToPartyMap(G, num_qubit):
    '''
    Allocate raws in patry map matrix to qubits in architecture graph
    See chapter 4.1, arXiv:1904.00633
    Return:
        a new architecture graph whose nodes correspond to raw, i.e., node0 -> raw0, node1 -> raw1...
    '''
    edges = list(G.edges())
    span_tree = nx.minimum_spanning_tree(G)
    nodes = list(G.nodes())
    '''find the starting node'''
    nodes.reverse()
    for current_node in nodes:
        if span_tree.degree(current_node) == 1:
            start_node = current_node
            break
    '''renumber each node'''
    new_edges = []
    for i in range(len(edges)):
        new_edges.append([start_node, start_node])
    DFT_edges = list(nx.dfs_edges(span_tree, source=start_node))
    DFT_edges.reverse()
    node_after = 0
    for DFT_edge in DFT_edges:
        node_before = DFT_edge[1]
        for i in range(len(edges)):
            edge = edges[i]
            '''
            if edge[0] == node_after:
                new_edge[0] = node_before
            if edge[1] == node_after:
                new_edge[1] = node_before
            '''
            if edge[0] == node_before:
                new_edges[i][0] = node_after
            if edge[1] == node_before:
                new_edges[i][1] = node_after
        node_after += 1
    '''generate new architecture graph'''
    new_G = nx.Graph()
    vertex = list(range(num_qubit))
    new_G.add_nodes_from(vertex)
    new_G.add_edges_from(new_edges)
    
    return new_G

def FindAllLeafNodesInTree(tree):
    '''find all leaf nodes in a indirected tree'''
    leaf_nodes = []
    nodes = tree.nodes()
    for node in nodes:
        if tree.degree(node) == 1:
            leaf_nodes.append(node)
    
    return leaf_nodes

def FindAllLeafNodesInDG(DG):
    '''find all leaf nodes in a directed tree'''
    leaf_nodes = []
    nodes = DG.nodes()
    for node in nodes:
        if DG.out_degree(node) == 0:
            leaf_nodes.append(node)
    
    return leaf_nodes

def SteinerUp(party_map, max_leaf, max_node, DFT_tree, W):
    '''
    See chapter 4.1, arXiv:1904.00633
    '''
    operation = []
    '''generate Steiner tree with W'''
    terminal_nodes = [max_leaf]
    for i in range(max_leaf):
        if party_map[i][max_leaf] == 1:
            terminal_nodes.append(i)
    if len(terminal_nodes) == 1: return []
    steiner_tree = GetSteinerTree(DFT_tree, terminal_nodes)
    # make the graph revisible
    steiner_tree = nx.Graph(steiner_tree)
    print(list(steiner_tree.edges()))
    #steiner_tree.add_nodes_from(W)
    #for i in range(len(W)-1):
    #    steiner_tree.add_edge(W[i], W[i+1])
    #W_copy = copy.deepcopy(W)
    #terminal_nodes.pop(0)
    #terminal_nodes = [W_copy[0]] + terminal_nodes
    
    '''set values of nodes'''
    nodes = list(steiner_tree.nodes)
    for current_node in nodes:
        if party_map[current_node][max_leaf] == 1:
            steiner_tree.node[current_node]['party_map_value'] = 1
        else:
            steiner_tree.node[current_node]['party_map_value'] = 0    
    
    '''FillSteinerTree'''
    shortest_path_steiner_tree = nx.shortest_path(steiner_tree, source=None, target=None, weight=None, method='dijkstra')
    add_CNOTs = FillSteinerTreeRootToLeaf(q, steiner_tree, party_map, terminal_nodes, shortest_path_steiner_tree)
    operation.extend(add_CNOTs)
    '''empty Steiner Tree'''
    add_CNOTs = EmptySteinerTree(q, steiner_tree, party_map, terminal_nodes)
    operation.extend(add_CNOTs)
    
    return operation
    
def SteinerGaussRec(party_map, G, q, num_qubit, DFT_tree_total, DFT_tree_current=None):
    '''
    See chapter 4.1, arXiv:1904.00633
    '''
    '''make a copy of DFT_tree'''
    if DFT_tree_current == None:
        DFT_tree_current = copy.deepcopy(DFT_tree_total)
    '''step 1'''
    operation_CNOT = []
    add_CNOTs = PartyMapToUpperMatrix(party_map, copy.deepcopy(G), q, num_qubit)
    operation_CNOT.extend(add_CNOTs)
    
    nodes_DFT_tree_current = list(DFT_tree_current.nodes())
    while len(nodes_DFT_tree_current) > 1:
        '''step2'''
        max_node = max(nodes_DFT_tree_current)
        #leaf_nodes = FindAllLeafNodesInTree(DFT_tree_current)
        #max_leaf = max(leaf_nodes)
        max_leaf = max_node
        '''step 3'''
        W = nx.shortest_path(G, max_leaf, max_node)
        print('current column is', max_leaf)
        print(W)
        W = []
        add_CNOTs = SteinerUp(party_map, max_leaf, max_node, DFT_tree_total, W)
        print(party_map)
        operation_CNOT.extend(add_CNOTs)
        '''step 4'''
        if len(W) > 1000:
            print(W)
            sub_G = nx.Graph()
            sub_G.add_nodes_from(W)
            for i in range(len(W)-1):
                sub_G.add_edge(W[i], W[i+1])
            add_CNOTs = SteinerGaussRec(party_map, sub_G, q, num_qubit, sub_G)
            operation_CNOT.extend(add_CNOTs)
            print(party_map)
        '''step 5'''
        DFT_tree_current.remove_node(max_leaf)
        nodes_DFT_tree_current = list(DFT_tree_current.nodes())
        
    return operation_CNOT

def DivideSteinerTree(steiner_tree_total, terminal_nodes):
    '''
    See section B, arXiv:1904.01972
    '''
    flag_debug = 0
    
    sub_steiner_trees = []
    root_node = terminal_nodes[0]
    BFS_edges = list(nx.bfs_edges(steiner_tree_total, source=root_node))
    #print(BFS_edges)
    
    root_nodes = [root_node]
    sub_trees_root_node = []
    while len(root_nodes) > 0:        
        father_nodes = [root_nodes.pop(0)]
        current_sub_tree_nodes = [father_nodes[0]]
        current_sub_tree_edges = []
        for edge in BFS_edges:    
            if edge[0] in father_nodes:
                current_sub_tree_nodes.append(edge[1])
                current_sub_tree_edges.append(edge)
                if (edge[1] in terminal_nodes) and (steiner_tree_total.degree(edge[1]) != 1):
                    root_nodes.append(edge[1])
                if not edge[1] in terminal_nodes:
                    father_nodes.append(edge[1])
        
        '''generate sub_tree'''
        sub_tree = nx.Graph()
        if flag_debug == 1: print(current_sub_tree_nodes)
        sub_tree.add_nodes_from(current_sub_tree_nodes)
        sub_tree.add_edges_from(current_sub_tree_edges)
        sub_steiner_trees.append(sub_tree)
        sub_trees_root_node.append(current_sub_tree_nodes[0])
        if flag_debug == 1: print(list(sub_tree.edges()))
        
    return sub_steiner_trees, sub_trees_root_node

def EliminateOneEntryInColumn(party_map, steiner_tree_total, sub_steiner_trees, sub_trees_root_node, terminal_nodes, q):
    '''
    See chapter 4.1, arXiv:1904.01972
    '''
    flag_debug = 0
    
    operation_CNOT = []

    for i in range(len(sub_steiner_trees)):
        '''if root node of a sub Steiner tree is not the biggest'''
        current_tree = sub_steiner_trees[i]
        current_root = sub_trees_root_node[i]
        leaf_nodes = FindAllLeafNodesInTree(current_tree)
        if current_root < max(leaf_nodes):
            #print('testing')
            add_operations = EliminateOneEntryInColumn(party_map, steiner_tree_total, [steiner_tree_total], [max(terminal_nodes)], terminal_nodes, q)
            operation_CNOT.extend(add_operations)
            return operation_CNOT
        '''else'''
    
    for i in range(len(sub_steiner_trees)):
        tree = sub_steiner_trees[i]
        root_node = sub_trees_root_node[i]
        R_operation = []
        shortest_length_tree = dict(nx.shortest_path_length(tree, source=None, target=None, weight=None, method='dijkstra'))
        BFS_edges = list(nx.bfs_edges(tree, source=root_node))
        BFS_edges.reverse()
        if flag_debug == 1: print('BFS edges are', BFS_edges)
        for edge in BFS_edges:
            if shortest_length_tree[edge[0]][root_node] < shortest_length_tree[edge[1]][root_node]:
                control_q = q[edge[0]]
                target_q = q[edge[1]]
            else:
                control_q = q[edge[1]]
                target_q = q[edge[0]]
            R_operation.append(OperationCNOT(control_q, target_q))
            
        '''calculate R_prime'''
        R_prime = copy.deepcopy(R_operation)
        
        '''delete redundancy of R_prime'''
        for operation in copy.copy(R_prime):
            if operation.control_qubit[1] == root_node:
                R_prime.remove(operation)
        
        #R_prime.pop()
        R_prime.reverse()
        '''calculate R_star'''
        add_R_star = []
        leaf_nodes = FindAllLeafNodesInTree(tree)
        R_star = copy.deepcopy(R_operation) + copy.deepcopy(R_prime)
        for operation in copy.copy(R_star):
            if (operation.target_qubit[1] in terminal_nodes) and (operation.target_qubit[1] in leaf_nodes):
                R_star.remove(operation)
            '''这个部分不正确，但是可以用来预估增加的CNOT数目'''
            if (operation.target_qubit[1] in terminal_nodes) and (not operation.target_qubit[1] in leaf_nodes):
                add_R_star.append(OperationCNOT(operation.target_qubit , operation.control_qubit))
        add_R_star_copy = copy.deepcopy(add_R_star)
        add_R_star_copy.reverse()
        if add_R_star != []: R_star = add_R_star + R_star + add_R_star_copy
        
        
        '''total operation'''
        R_total = R_operation + R_prime + R_star
        operation_CNOT.extend(R_total)
        if flag_debug == 1: print('R_operation')
        PerformOperationCNOTinPartyMap(party_map, R_operation)
        if flag_debug == 1: print('R_prime')
        PerformOperationCNOTinPartyMap(party_map, R_prime)
        if flag_debug == 1: print('R_star')
        PerformOperationCNOTinPartyMap(party_map, R_star)
        #PerformOperationCNOTinPartyMap(party_map, R_total)
        
    return operation_CNOT
        
        

def SteinerTreeAndRemoteCNOT(party_map, G, q, num_qubit):
    '''
    See Section 2B , arXiv:1904.01972
    '''
    flag_debug = 0
    
    operation_CNOT = []
    add_CNOTs = PartyMapToUpperMatrix(party_map, copy.deepcopy(G), q, num_qubit)
    operation_CNOT.extend(add_CNOTs)
    if flag_debug == 1: print(party_map)
    
    for column in range(num_qubit-1,-1,-1):
        if flag_debug == 1: print('current column is', column)
        terminal_nodes = [column]
        for i in range(column):
            if party_map[i][column] == 1:
                terminal_nodes.append(i)
        if flag_debug == 1: print('terminal nodes are', terminal_nodes)
        if len(terminal_nodes) == 1: continue
        '''generate steiner tree for each column'''
        steiner_tree_total = GetSteinerTree(G, terminal_nodes)
        if flag_debug == 1: print('steiner_tree_total edges are', list(steiner_tree_total.edges()))
        '''divide Steiner tree into sub trees'''
        res = DivideSteinerTree(steiner_tree_total, terminal_nodes)
        sub_steiner_trees = res[0]
        sub_trees_root_node = res[1]
         
        sub_steiner_trees.reverse()
        sub_trees_root_node.reverse()
        
        if flag_debug == 1: print('root node is', sub_trees_root_node)
        if flag_debug == 1: 
            for tree in sub_steiner_trees:
                print('one of sub tree edges are', list(tree.edges()))  
        
        '''perform CNOT in all sub trees'''
        add_CNOTs = EliminateOneEntryInColumn(party_map, steiner_tree_total, sub_steiner_trees, sub_trees_root_node, terminal_nodes, q)
        operation_CNOT.extend(add_CNOTs)
               
        if flag_debug == 1: print(party_map)
        
    return operation_CNOT


def UDecompositionFullConnectivity(party_map, q, num_qubit):
    '''
    Naive methods for converting a party map with full connectivity
    '''
    debug_flag = 0
    
    operation_CNOT = []
    for colunm in range(num_qubit):
        '''set diagonal entry to 1'''
        if party_map[colunm][colunm] == 0:
            for raw in list(range(colunm+1, num_qubit)):
                if party_map[raw][colunm] == 1:
                    if debug_flag == 1: print('control', raw, 'target', colunm)
                    PerformRawAddinPartyMap(party_map, raw, colunm)
                    if debug_flag == 1: print(party_map)
                    add_CNOT = OperationCNOT(q[raw], q[colunm])
                    operation_CNOT.append(add_CNOT)
                    break
        
        for raw in list(range(colunm)) + list(range(colunm+1, num_qubit)):
            if party_map[raw][colunm] == 1:
                if debug_flag == 1: print('control', colunm, 'target', raw)
                PerformRawAddinPartyMap(party_map, colunm, raw)
                if debug_flag == 1: print(party_map)
                add_CNOT = OperationCNOT(q[colunm], q[raw])
                operation_CNOT.append(add_CNOT)
                
    return operation_CNOT
        
def UDecompositionFullConnectivityPATEL(party_map, q, num_qubit, m=None):
    '''
    Optimal methods for converting a party map with full connectivity
    Using partition
    See "OPTIMAL SYNTHESIS OF LINEAR REVERSIBLE CIRCUITS"
    '''       
    operation_CNOT = []
    '''set value of m'''
    if m == None:
        cuurent_m = int(np.log2(num_qubit))
        while int(num_qubit / cuurent_m) != (num_qubit / cuurent_m):
            cuurent_m -= 1
        m = cuurent_m
    
    '''transform to upper triangle'''
    '''traverse all sections'''
    for start_col in range(0, num_qubit, m):
        list_all_col = list(range(start_col, start_col+m))
        '''delete duplicate sub-rows'''
        for raw in list_all_col:
            module = party_map[raw][list_all_col]
            if np.sum(module) > 1:
                for raw2 in range(list_all_col[-1]+1, num_qubit):
                    module2 = party_map[raw2][list_all_col]
                    if np.array_equal(module, module2) == True:
                        PerformRawAddinPartyMap(party_map, raw, raw2)
                        add_CNOT = OperationCNOT(q[raw], q[raw2])
                        operation_CNOT.append(add_CNOT)
        '''set values of all entries in each column of current subsection'''
        for current_col_sec in list_all_col:
            '''set diagonal entry to 1'''
            if party_map[current_col_sec][current_col_sec] != 1:
                for i in range(current_col_sec+1, num_qubit):
                    if party_map[i][current_col_sec] == 1:
                        PerformRawAddinPartyMap(party_map, i, current_col_sec)
                        add_CNOT = OperationCNOT(q[i], q[current_col_sec])
                        operation_CNOT.append(add_CNOT)
                        break
            '''set other entries in this column'''
            for current_raw in range(current_col_sec+1, num_qubit):
                if party_map[current_raw][current_col_sec] == 1:
                    PerformRawAddinPartyMap(party_map, current_col_sec, current_raw)
                    add_CNOT = OperationCNOT(q[current_col_sec], q[current_raw])
                    operation_CNOT.append(add_CNOT)
                    
    '''transform to upper identity'''
    '''traverse all sections'''
    for start_col in range(num_qubit-1, -1, -1*m):
        list_all_col = list(range(start_col, start_col-m, -1))
        '''delete duplicate sub-rows'''
        for raw in list_all_col:
            module = party_map[raw][list_all_col]
            if np.sum(module) > 1:
                for raw2 in range(list_all_col[-1]-1, -1, -1):
                    module2 = party_map[raw2][list_all_col]
                    if np.array_equal(module, module2) == True:
                        PerformRawAddinPartyMap(party_map, raw, raw2)
                        add_CNOT = OperationCNOT(q[raw], q[raw2])
                        operation_CNOT.append(add_CNOT)
        '''set values of all entries in each column of current subsection'''
        for current_col_sec in list_all_col:
            '''set diagonal entry to 1'''
            if party_map[current_col_sec][current_col_sec] != 1:
                for i in range(current_col_sec-1, -1, -1):
                    if party_map[i][current_col_sec] == 1:
                        PerformRawAddinPartyMap(party_map, i, current_col_sec)
                        add_CNOT = OperationCNOT(q[i], q[current_col_sec])
                        operation_CNOT.append(add_CNOT)
                        break
            '''set other entries in this column'''
            for current_raw in range(current_col_sec-1, -1, -1):
                if party_map[current_raw][current_col_sec] == 1:
                    PerformRawAddinPartyMap(party_map, current_col_sec, current_raw)
                    add_CNOT = OperationCNOT(q[current_col_sec], q[current_raw])
                    operation_CNOT.append(add_CNOT)   
                    
    return operation_CNOT
        
        
if __name__ == '__main__': 
    l=2
    w=2
    num_qubit=l*w+2*(l+w)
    
    #num_qubit = 8
    num_CNOT = 150
    '''generate quantum register and quantum circuit'''
    q = QuantumRegister(num_qubit, 'q')
    cir_original = QuantumCircuit(q)
    cir_transformed = QuantumCircuit(q)
    '''generate party map'''
    res = ct.CreatePartyMapRandomly(num_qubit, num_CNOT, q)
    party_map = res[0]
    original_CNOT_operation = res[1]
    print(party_map)
    '''generate architecture graph'''
    method_AG = ['grid', 2, 4]
    terminal_nodes = [0, 8, 10, 5]
    #G = ct.GenerateArchitectureGraph(8, method_AG)
    G = ct.GenerateArchitectureGraph(num_qubit, ['grid2', l, w])
    fig1 = plt.figure()
    nx.draw(G, with_labels=True)
    '''generate Steiner tree'''
    '''
    res = GenerateGetSteinerTreeInColunm(G, num_qubit, party_map, 1)
    steiner_tree = res[0]
    terminal_nodes = res[1]
    shortest_path_steiner_tree = nx.shortest_path(steiner_tree, source=None, target=None, weight=None, method='dijkstra')
    fig2 = plt.figure()
    nx.draw(steiner_tree, with_labels=True)
    FillSteinerTree(q, steiner_tree, party_map, terminal_nodes, shortest_path_steiner_tree)
    print(party_map)
    fig3 = plt.figure()
    nx.draw(steiner_tree, with_labels=True)
    EmptySteinerTree(q, steiner_tree, party_map, terminal_nodes)
    print(party_map)
    '''
    ''''''
    new_G = AllocateVertexToPartyMap(G, num_qubit)
    fig4 = plt.figure()
    nx.draw(new_G, with_labels=True)
    '''transter party map into upper triangle matrix'''
    '''
    PartyMapToUpperMatrix(party_map, copy.deepcopy(new_G), q, num_qubit)
    print(party_map)
    '''
    '''whole process for arXiv:1904.00633'''
    '''
    max_node = max(list(new_G.nodes()))
    DFT_tree = nx.dfs_tree(new_G, max_node)
    DFT_tree = nx.to_undirected(DFT_tree)
    DFT_tree = nx.Graph(DFT_tree)
    fig5 = plt.figure()
    nx.draw(DFT_tree, with_labels=True)
    SteinerGaussRec(party_map, copy.deepcopy(new_G), q, num_qubit, DFT_tree)
    print(party_map)
    '''
    '''whole process for arXiv:1904.01972'''
    party_map1 = copy.copy(party_map)
    transformed_operation_CNOT1 = SteinerTreeAndRemoteCNOT(party_map1, new_G, q, num_qubit)
    print('Remote CNOT and Steiner tree')
    print(party_map1)
    #transformed_operation_CNOT.reverse()
    '''Naive methods for converting a party map with full connectivity'''
    party_map2 = copy.copy(party_map)
    transformed_operation_CNOT2 = UDecompositionFullConnectivity(party_map2, q, num_qubit)
    print('Naive')
    print(party_map2)
    '''Optimal methods for converting a party map with full connectivity'''
    party_map3 = copy.copy(party_map)
    transformed_operation_CNOT3 = UDecompositionFullConnectivityPATEL(party_map3, q, num_qubit)
    print('Optimal')
    print(party_map3)
    
    '''conduct operation in quantum circuits'''
    '''
    transformed_operation_CNOT = transformed_operation_CNOT3
    for operation in original_CNOT_operation:
        operation.ConductOperation(cir_original)
    for operation in transformed_operation_CNOT:
        operation.ConductOperation(cir_transformed)
        operation.ConductOperation(cir_original)
    # Select the UnitarySimulator from the Aer provider
    simulator = Aer.get_backend('unitary_simulator')    
    # Execute and get counts
    result = execute(cir_original, simulator).result()
    unitary = result.get_unitary(cir_original)
    print(unitary)
    '''
    
    
