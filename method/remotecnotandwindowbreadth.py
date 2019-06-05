# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:28:00 2019

@author: Xiangzhen Zhou

This module is for search algorithm introducing remote CNOT and breadth first search
"""

import circuittransform as ct
import copy
import networkx as nx
from networkx import DiGraph, Graph

def CalculateHeuristicCost(current_map, DG, executable_vertex, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, DiG):
    '''
    cost_h1: sum_num_gate
    cost_h2: lookahead for all remaining gates
    '''
    num_remaining_vertex = len(DG.nodes()) - len(executable_vertex)
    cost_h_total = ct.HeuristicCostZhou1(current_map, DG, executable_vertex, shortest_length_G, shortest_path_G, DiG)
    cost_h1 = cost_h_total[1] * SWAP_cost + cost_h_total[5]*0.00001
    cost_h2 = SWAP_cost * num_remaining_vertex * (max_shortest_length_G - 1)/2
    cost_h2 = 0
    cost_h_list = [cost_h1, cost_h2, cost_h_total]
    
    return cost_h_list

def CalculateTotalCost(cost_h_list, cost_g): 
    cost_total = cost_g + cost_h_list[0] + cost_h_list[1]
    return cost_total

def SearchTreeNodePruning(search_tree, start_node, new_node, num_pruned_nodes_list):
    cost_h_total_start = search_tree.nodes[start_node]['cost_h'][2]
    cost_h_total_new = search_tree.nodes[new_node]['cost_h'][2]
    if search_tree.nodes[start_node]['cost_g'] > search_tree.nodes[new_node]['cost_g']:
        return False
    if search_tree.nodes[start_node]['cost_h'][0] > search_tree.nodes[new_node]['cost_h'][0]:
        return False
    if search_tree.nodes[start_node]['cost_h'][1] > search_tree.nodes[new_node]['cost_h'][1]:
        return False
    if search_tree.nodes[start_node]['num_executed_vertex'] < search_tree.nodes[new_node]['num_executed_vertex']:
        return False
    if cost_h_total_start[0] > cost_h_total_new[0]:
        return False    
    if cost_h_total_start[2] > cost_h_total_new[2]:
        return False  
    
    return True

def SearchTreeLeafNodesPruning(search_tree, start_node, leaf_nodes, num_pruned_nodes_list):
    '''
    Given a search tree and leaf nodes, judge whether the new node should be kept
    '''
    leaf_nodes_copy = copy.copy(leaf_nodes)
    for node in leaf_nodes_copy:
        flag_prune = SearchTreeNodePruning(search_tree, start_node, node, num_pruned_nodes_list)
        if flag_prune == True:
            search_tree.remove_node(node)
            leaf_nodes.remove(node)
            num_pruned_nodes_list[0] += 1

def ExpandTreeForNextStep(G, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, q_phy, draw, DiG):
    use_remoteCNOT = True
    best_cost_total = None
    flag_4H = 0
    finished_nodes = []
    added_nodes = []
    if DiG != None: edges_DiG = list(DiG.edges)
    '''find all possible operation for next step and expand the search tree accordingly'''
    for leaf_node in leaf_nodes:
        '''get attributes from current leaf node'''
        current_map = search_tree.nodes[leaf_node]['mapping']
        cost_g_current = search_tree.nodes[leaf_node]['cost_g']
        num_executed_vertex_current = search_tree.nodes[leaf_node]['num_executed_vertex']
        DG_current = search_tree.nodes[leaf_node]['DG']
        if draw == True: cir_phy_current = search_tree.nodes[leaf_node]['phy_circuit']
        executable_vertex_current = ct.FindExecutableNode(DG_current)
        '''add successor nodes to current node'''
        '''SWAP'''
        for swaps in possible_swap_combination:   
            DG_next = copy.deepcopy(DG_current)
            if draw == True: cir_phy_next = copy.deepcopy(cir_phy_current)
            executable_vertex_next = copy.copy(executable_vertex_current)
            num_executed_vertex_next = num_executed_vertex_current
            cost_g_next = cost_g_current + len(swaps)  * SWAP_cost
            next_map = current_map.Copy()
            for current_swap in swaps:
                '''conduct each swap'''
                v0 = current_swap[0]
                v1 = current_swap[1]
                next_map.RenewMapViaExchangeCod(v0, v1)
                if draw == True: cir_phy_next.swap(q_phy[v0], q_phy[v1])
            '''check whether this window already has appliable vertexes, if has, then execute them'''
            temp = True
            while temp == True:
                temp = False
                for vertex in executable_vertex_next :
                    if ct.IsVertexInDGOperatiable(vertex, DG_next, G, next_map) == True:
                        '''check whether this CNOT needs 4 H gates to convert direction'''
                        if DiG != None:
                            flag_4H = ct.CheckCNOTNeedConvertDirection2(vertex, DG_next, next_map, edges_DiG)
                            cost_g_next += flag_4H*4
                        if draw == True:
                            ct.ConductCNOTOperationInVertex(DG_next, vertex, next_map, cir_phy_next, q_phy, flag_4H)
                            cir_phy_next.barrier()
                        else:
                            DG_next.remove_node(vertex)
                            
                        num_executed_vertex_next += 1
                        temp = True
                if temp == True: executable_vertex_next = ct.FindExecutableNode(DG_next)
            '''calculate cost for the new node'''
            #print('executable_vertex_next is', executable_vertex_next)
            cost_h_next = CalculateHeuristicCost(next_map, DG_next, executable_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, DiG)
            cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next)
            '''generate next node'''
            next_node = next_node_list[0]
            next_node_list[0] = next_node_list[0] + 1
            added_nodes.append(next_node)
            search_tree.add_node(next_node)
            search_tree.add_edge(leaf_node, next_node)           
            search_tree.nodes[next_node]['mapping'] = next_map
            search_tree.nodes[next_node]['cost_g'] = cost_g_next
            search_tree.nodes[next_node]['cost_h'] = cost_h_next
            search_tree.nodes[next_node]['num_executed_vertex'] = num_executed_vertex_next
            search_tree.nodes[next_node]['DG'] = DG_next
            if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
            search_tree.nodes[next_node]['cost_total'] = cost_total_next
            '''renew best expanded node in search tree'''
            if len(DG_next.nodes()) == 0: finished_nodes.append(next_node)
            if best_cost_total == None:
                best_cost_total = cost_total_next
                best_node = next_node
            else:
                if cost_total_next < best_cost_total:
                    best_cost_total = cost_total_next
                    best_node = next_node
        '''remote CNOT'''
        if use_remoteCNOT == True and DiG == None:
            '''judge whether remote CNOT is applicable'''
            for current_vertex in executable_vertex_current:
                DG_next = copy.deepcopy(DG_current)
                next_map = current_map.Copy()
                '''calculate distance between two input qubits'''
                current_operation = DG_next.node[current_vertex]['operation']
                q0 = current_operation.involve_qubits[0]
                q1 = current_operation.involve_qubits[1]
                v0 = next_map.DomToCod(q0)
                v1 = next_map.DomToCod(q1)
                current_hop = shortest_length_G[v0][v1]
                '''if a remote CNOT can be done, then execute it'''
                if current_hop <= min_remoteCNOT_hop:
                    #print('current_hop is ', current_hop)
                    current_path = shortest_path_G[v0][v1]
                    # number of additional CNOTs in this remote CNOT operation
                    cost_CNOT_remoteCNOT = ct.CalRemoteCNOTCostinArchitectureGraph(current_path) - 1 #这里减1是因为要去除本身的CNOT
                    cost_g_next = cost_g_current + cost_CNOT_remoteCNOT
                    if draw == True:
                        cir_phy_next = copy.deepcopy(cir_phy_current)
                        ct.RemoteCNOTinArchitectureGraph(current_path, cir_phy_next, q_phy)
                        cir_phy_next.barrier()
                    DG_next.remove_node(current_vertex)
                    executable_vertex_next = ct.FindExecutableNode(DG_next)
                    num_executed_vertex_next = num_executed_vertex_current + 1
                    '''check whether this window already has appliable vertexes, if has, then execute them'''
                    temp = True
                    while temp == True:
                        temp = False
                        for vertex in executable_vertex_next:
                            if ct.IsVertexInDGOperatiable(vertex, DG_next, G, next_map) == True:
                                if draw == True:
                                    ct.ConductOperationInVertex(DG_next, vertex, next_map, cir_phy_next, q_phy)
                                    cir_phy_next.barrier()
                                else:
                                    DG_next.remove_node(vertex)
                                num_executed_vertex_next += 1
                                temp = True
                        if temp == True: executable_vertex_next = ct.FindExecutableNode(DG_next)
                    '''calculate cost for the new node'''
                    #print('executable_vertex_next is', executable_vertex_next)
                    cost_h_next = CalculateHeuristicCost(next_map, DG_next, executable_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, DiG)
                    cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next) 
                    '''generate next node'''
                    next_node = next_node_list[0]
                    next_node_list[0] = next_node_list[0] + 1
                    added_nodes.append(next_node)
                    search_tree.add_node(next_node)
                    search_tree.add_edge(leaf_node, next_node)
                    search_tree.nodes[next_node]['mapping'] = next_map
                    search_tree.nodes[next_node]['cost_g'] = cost_g_next
                    search_tree.nodes[next_node]['cost_h'] = cost_h_next
                    search_tree.nodes[next_node]['num_executed_vertex'] = num_executed_vertex_next
                    search_tree.nodes[next_node]['DG'] = DG_next
                    if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
                    search_tree.nodes[next_node]['cost_total'] = cost_total_next
                    '''renew best expanded node in search tree'''
                    if len(DG_next.nodes()) == 0: finished_nodes.append(next_node)
                    if best_cost_total == None:
                        best_cost_total = cost_total_next
                        best_node = next_node
                    else:
                        if cost_total_next < best_cost_total:
                            best_cost_total = cost_total_next
                            best_node = next_node
    
    return best_node, finished_nodes, added_nodes
    
def FindNextNodeAndRenewTree(search_tree, best_leaf_node, depth_lookahead):
    '''Find next state in the search and cut the residual nodes in the tree'''
    next_node = best_leaf_node
    for i in range(depth_lookahead):
        next_node = list(search_tree.predecessors(next_node))
        next_node = next_node[0]
    
    delete_nodes = []
    '''delete residual nodes in search tree'''    
    pre_node = list(search_tree.predecessors(next_node))
    pre_node = pre_node[0]
    '''find all barnches that you want to delete'''
    current_nodes =  list(search_tree.successors(pre_node))
    current_nodes.remove(next_node)
    
    while len(current_nodes) != 0:
        delete_nodes.extend(current_nodes)
        next_nodes = []
        for node in current_nodes:
            next_nodes.extend(list(search_tree.successors(node)))
        current_nodes = next_nodes
    search_tree.remove_nodes_from(delete_nodes)
    
    return next_node
    

def RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG, initial_map, shortest_length_G, shortest_path_G, depth_lookahead, use_prune, draw=False, DiG=None):
    SWAP_cost = 3
    IBM_QX_mode = False
    flag_4H = 0
    if DiG != None:
        edges_DiG = list(DiG.edges)
        SWAP_cost = 7
        IBM_QX_mode = True
    min_remoteCNOT_hop = 3
    max_shortest_length_G = max(shortest_length_G)
    
    '''initialize possible swap'''
    possible_swap_combination = []
    edges = list(G.edges()).copy()
    for current_edge in edges:
        possible_swap_combination.append([current_edge]) 
        
    '''check whether DG already has appliable vertexes, if has, then execute them'''
    cost_g_initial = 0
    num_executed_vertex = 0
    executable_vertex = ct.FindExecutableNode(DG)
    temp = True
    while temp == True:
        temp = False
        for vertex in executable_vertex:
            if ct.IsVertexInDGOperatiable(vertex, DG, G, initial_map) == True:
                #DG.remove_node(vertex)
                '''check whether this CNOT needs 4 H gates to convert direction'''
                if DiG != None:
                    flag_4H = ct.CheckCNOTNeedConvertDirection2(vertex, DG, initial_map, edges_DiG)
                    cost_g_initial += flag_4H*4
                '''conduct the operation'''
                ct.ConductCNOTOperationInVertex(DG, vertex, initial_map, cir_phy, q_phy, flag_4H)
                cir_phy.barrier()
                num_executed_vertex += 1
                temp = True

        if temp == True: executable_vertex = ct.FindExecutableNode(DG)
    
    '''initialize search tree'''
    search_tree = nx.DiGraph()
    search_tree.add_node(0)
    next_node_list = [1]
    cost_h_initial = CalculateHeuristicCost(initial_map, DG, executable_vertex, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, DiG)
    cost_total_initial = CalculateTotalCost(cost_h_initial, 0)
    search_tree.nodes[0]['mapping'] = initial_map
    search_tree.nodes[0]['cost_g'] = cost_g_initial#this is the count for number of added gates
    search_tree.nodes[0]['cost_h'] = cost_total_initial
    search_tree.nodes[0]['num_executed_vertex'] = num_executed_vertex
    search_tree.nodes[0]['DG'] = DG
    if draw == True: search_tree.nodes[0]['phy_circuit'] = cir_phy
    leaf_nodes = [0]
    num_pruned_nodes_list = [0]
    
    
    '''expand search tree for the first time'''
    finished_nodes = []
    for i in range(depth_lookahead+1):
        res = ExpandTreeForNextStep(G, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, q_phy, draw, DiG)
        leaf_nodes = res[2]
        finished_nodes.extend(res[1])

    best_leaf_node = res[0]
    
    while finished_nodes == []:
        next_node = FindNextNodeAndRenewTree(search_tree, best_leaf_node, depth_lookahead)
        leaf_nodes = ct.FindAllLeafNodesInDG(search_tree)
        if use_prune == True:
            SearchTreeLeafNodesPruning(search_tree, next_node, leaf_nodes, num_pruned_nodes_list)
        res = ExpandTreeForNextStep(G, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, q_phy, draw, DiG)
        best_leaf_node = res[0]
        finished_nodes = res[1]     
    
    '''find the best finished node'''
    best_CNOT_count = None
    for node in finished_nodes:
        if best_CNOT_count == None:
            best_finish_node = node
            best_CNOT_count = search_tree.nodes[node]['cost_g']
        else:
            current_CNOT_count = search_tree.nodes[node]['cost_g']
            if current_CNOT_count < best_CNOT_count:
                best_finish_node = node
                best_CNOT_count = current_CNOT_count
    swap_count = search_tree.nodes[best_finish_node]['cost_g']/SWAP_cost
    additional_gate_count = search_tree.nodes[best_finish_node]['cost_g']
    if draw == True:
        best_cir_phy = search_tree.nodes[best_finish_node]['phy_circuit']
        print(best_cir_phy.draw())
    '''number of traversed states'''
    num_total_state = next_node_list[0] - 1
    num_pruned_nodes = num_pruned_nodes_list[0]
    #nx.draw(search_tree, with_labels=True)
    return swap_count, num_total_state, num_total_state - num_pruned_nodes, additional_gate_count
