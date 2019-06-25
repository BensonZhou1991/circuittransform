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
from numba import jit
#from time import time

'''parameter control'''
use_remoteCNOT = 0
use_remoteCNOT_fallback = 1
min_remoteCNOT_hop = 2
use_fallback = True
fallback_mode = 0#0:choose the current best gate, 1: current worst gate
display_complete_state = 1
debug_mode = False
level_lookahead_default = [1, 0.8, 0.6, 0.4]

def AddNewNodeToSearchTree(next_node, search_tree, next_map, cost_g_next, cost_h_next, cost_total_next, executed_vertex_next, executable_vertex_next):
    '''generate next node'''
    search_tree.add_node(next_node)
    search_tree.nodes[next_node]['mapping'] = next_map
    search_tree.nodes[next_node]['cost_g'] = cost_g_next
    search_tree.nodes[next_node]['cost_h'] = cost_h_next
    search_tree.nodes[next_node]['cost_total'] = cost_total_next
    search_tree.nodes[next_node]['executed_vertex'] = executed_vertex_next
    search_tree.nodes[next_node]['executable_vertex'] = executable_vertex_next
    
def CalculateHeuristicCost(current_map, DG, executable_vertex, executed_vertex, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG):
    '''
    cost_h1: sum_num_gate for lookahead level with weights
    cost_h2: lookahead for all remaining gates
    '''
    num_remaining_vertex = len(DG.nodes()) - len(executed_vertex)
    cost_h_total = ct.HeuristicCostZhou1(current_map, DG, executed_vertex, executable_vertex, shortest_length_G, shortest_path_G, level_lookahead, DiG)
    cost_h1 = cost_h_total[1] * SWAP_cost + cost_h_total[5]*0.00001
    cost_h2 = SWAP_cost * num_remaining_vertex * (max_shortest_length_G - 1) * level_lookahead[-1]
    #cost_h2 = 0#only for test, remember to delete it
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
    if len(search_tree.nodes[start_node]['executed_vertex']) < len(search_tree.nodes[new_node]['executed_vertex']):
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
    #print('leaf nodes before purning', leaf_nodes)
    leaf_nodes_copy = leaf_nodes.copy()
    for node in leaf_nodes_copy:
        flag_prune = SearchTreeNodePruning(search_tree, start_node, node, num_pruned_nodes_list)
        if flag_prune == True:
            search_tree.remove_node(node)
            leaf_nodes.remove(node)
            num_pruned_nodes_list[0] += 1
    #print('leaf nodes after purning', leaf_nodes)

def ExpandTreeForNextStep(G, DG, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, level_lookahead, q_phy, draw, DiG):
    best_cost_total = None
    flag_4H = 0
    finished_nodes = []
    added_nodes = []
    cir_phy_next = None
    num_all_vertex = len(DG.nodes())
    if DiG != None:
        edges_DiG = list(DiG.edges)
    else:
        edges_DiG = None
    '''find all possible operation for next step and expand the search tree accordingly'''
    #print('number of leaf nodes is', len(leaf_nodes))
    for leaf_node in leaf_nodes:
        #print('current leaf node is', leaf_node)
        '''get attributes from current leaf node'''
        current_map = search_tree.nodes[leaf_node]['mapping']
        cost_g_current = search_tree.nodes[leaf_node]['cost_g']
        executed_vertex_current = search_tree.nodes[leaf_node]['executed_vertex']
        executable_vertex_current = search_tree.nodes[leaf_node]['executable_vertex']
        if draw == True: cir_phy_current = search_tree.nodes[leaf_node]['phy_circuit']
        '''add successor nodes to current node'''
        '''SWAP'''
        for swaps in possible_swap_combination:
            '''judge whether the swap in trivial to avoid unnecessary state'''
            flag_nontrivial = ct.CheckSWAPInvolved(swaps, executable_vertex_current, DG, current_map)
            if flag_nontrivial == False:
                #print('trivival swap')
                continue
            
            #print(swaps)
            #start = time()
            #elapsed = (time() - start)
            #print("deep copy Time used:", elapsed, 's')
            if draw == True: cir_phy_next = copy.deepcopy(cir_phy_current)
            executable_vertex_next = executable_vertex_current.copy()
            executed_vertex_next = executed_vertex_current.copy()
            cost_g_next = cost_g_current + len(swaps)  * SWAP_cost
            next_map = current_map.Copy()
            for current_swap in swaps:
                '''conduct each swap'''
                v0 = current_swap[0]
                v1 = current_swap[1]
                next_map.RenewMapViaExchangeCod(v0, v1)
                if draw == True: cir_phy_next.swap(q_phy[v0], q_phy[v1])
            '''check whether this window already has appliable vertexes, if has, then execute them'''
            res = ct.ExecuteAllPossibileNodesInDG(executable_vertex_next, executed_vertex_next, G, DG, next_map, draw, DiG, edges_DiG, cir_phy_next, q_phy)
            executed_vertex_next = res[0]
            executable_vertex_next = res[1]
            '''calculate cost for the new node'''
            #print('executable_vertex_next is', executable_vertex_next)
            cost_h_next = CalculateHeuristicCost(next_map, DG, executable_vertex_next, executed_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG)
            cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next)
            '''generate next node'''
            next_node = next_node_list[0]
            next_node_list[0] = next_node_list[0] + 1
            added_nodes.append(next_node)
            AddNewNodeToSearchTree(next_node, search_tree, next_map, cost_g_next, cost_h_next, cost_total_next, executed_vertex_next, executable_vertex_next)
            search_tree.add_edge(leaf_node, next_node)
            if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
            '''renew best expanded node in search tree'''
            num_remaining_vertex_next = num_all_vertex - len(executed_vertex_next)
            if num_remaining_vertex_next == 0: finished_nodes.append(next_node)
            if best_cost_total == None:
                best_cost_total = cost_total_next
                best_node = next_node
            else:
                if cost_total_next < best_cost_total:
                    best_cost_total = cost_total_next
                    best_node = next_node
        '''execute possible CNOT needing 4 extra 4 H'''
        if DiG != None:
            for vertex in executable_vertex_current:
                if ct.IsVertexInDGOperatiable(vertex, DG, G, next_map) == True:
                    '''check whether this CNOT needs 4 H gates to convert direction'''
                    flag_4H = ct.CheckCNOTNeedConvertDirection2(vertex, DG, current_map, edges_DiG)
                    if flag_4H == False: raise Exception('unexpected operatible CNOT without 4 H gates')
                    if flag_4H == True:
                        '''if need 4 extra H, then execute it and add to the new node'''
                        next_map = current_map.Copy() 
                        cost_g_next = cost_g_current + flag_4H*4
                        executed_vertex_next = executed_vertex_current.copy()
                        if draw == True:
                            cir_phy_next = copy.deepcopy(cir_phy_current)
                            ct.ConductCNOTOperationInVertex(DG, vertex, current_map, cir_phy_next, q_phy, reverse_drection=flag_4H, remove_node=False)
                            cir_phy_next.barrier()
                        executable_vertex_next = executable_vertex_current.copy()
                        executable_vertex_next = ct.FindExecutableNode(DG, executed_vertex_next, executable_vertex_next, [vertex])
                        '''check whether this window already has appliable vertexes, if has, then execute them'''
                        res = ct.ExecuteAllPossibileNodesInDG(executable_vertex_next, executed_vertex_next, G, DG, next_map, draw, DiG, edges_DiG, cir_phy_next, q_phy)
                        executed_vertex_next = res[0]
                        executable_vertex_next = res[1]
                        '''calculate cost for the new node'''
                        #print('executable_vertex_next is', executable_vertex_next)
                        cost_h_next = CalculateHeuristicCost(next_map, DG, executable_vertex_next, executed_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG)
                        cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next)
                        '''generate next node'''
                        next_node = next_node_list[0]
                        next_node_list[0] = next_node_list[0] + 1
                        added_nodes.append(next_node)
                        AddNewNodeToSearchTree(next_node, search_tree, next_map, cost_g_next, cost_h_next, cost_total_next, executed_vertex_next, executable_vertex_next)
                        search_tree.add_edge(leaf_node, next_node) 
                        if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
                        '''renew best expanded node in search tree'''
                        num_remaining_vertex_next = num_all_vertex - len(executed_vertex_next)
                        if num_remaining_vertex_next == 0: finished_nodes.append(next_node)
                        if best_cost_total == None:
                            best_cost_total = cost_total_next
                            best_node = next_node
                        else:
                            if cost_total_next < best_cost_total:
                                best_cost_total = cost_total_next
                                best_node = next_node                       
            
        '''remote CNOT'''
        #f use_remoteCNOT == True and DiG == None:
        if use_remoteCNOT == True:
            '''judge whether remote CNOT is applicable'''
            for current_vertex in executable_vertex_current:
                '''calculate distance between two input qubits'''
                current_operation = DG.node[current_vertex]['operation']
                q0 = current_operation.involve_qubits[0]
                q1 = current_operation.involve_qubits[1]
                v0 = current_map.DomToCod(q0)
                v1 = current_map.DomToCod(q1)
                current_hop = shortest_length_G[v0][v1]
                '''if a remote CNOT can be done, then execute it'''
                if (current_hop <= min_remoteCNOT_hop) and (current_hop >= 2):
                    next_map = current_map.Copy()
                    executable_vertex_next = executable_vertex_current.copy()
                    executed_vertex_next = executed_vertex_current.copy()
                    #print('current_hop is ', current_hop)
                    current_path = shortest_path_G[v0][v1]
                    # number of additional CNOTs in this remote CNOT operation
                    cost_CNOT_remoteCNOT = ct.CalRemoteCNOTCostinArchitectureGraph(current_path, DiG) - 1 #这里减1是因为要去除本身的CNOT
                    cost_g_next = cost_g_current + cost_CNOT_remoteCNOT
                    if draw == True:
                        cir_phy_next = copy.deepcopy(cir_phy_current)
                        ct.RemoteCNOTinArchitectureGraph(current_path, cir_phy_next, q_phy, DiG)
                        cir_phy_next.barrier()
                    executable_vertex_next = ct.FindExecutableNode(DG, executed_vertex_next, executable_vertex_next, [current_vertex])
                    '''check whether this window already has appliable vertexes, if has, then execute them'''
                    '''old version without considering the direction of CNOT gate'''
# =============================================================================
#                     temp = True
#                     while temp == True:
#                         temp = False
#                         for vertex in executable_vertex_next:
#                             if ct.IsVertexInDGOperatiable(vertex, DG_next, G, next_map) == True:
#                                 if draw == True:
#                                     ct.ConductOperationInVertex(DG_next, vertex, next_map, cir_phy_next, q_phy)
#                                     cir_phy_next.barrier()
#                                 else:
#                                     DG_next.remove_node(vertex)
#                                 num_executed_vertex_next += 1
#                                 temp = True
#                         if temp == True: executable_vertex_next = ct.FindExecutableNode(DG_next)
# =============================================================================
                    '''check whether this window already has appliable vertexes, if has, then execute them'''
                    '''new version considering the direction of CNOT gate'''
                    res = ct.ExecuteAllPossibileNodesInDG(executable_vertex_next, executed_vertex_next, G, DG, next_map, draw, DiG, edges_DiG, cir_phy_next, q_phy)
                    executed_vertex_next = res[0]
                    executable_vertex_next = res[1]
                    '''calculate cost for the new node'''
                    cost_h_next = CalculateHeuristicCost(next_map, DG, executable_vertex_next, executed_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG)
# =============================================================================
#                     cost_h_next = search_tree.nodes[leaf_node]['cost_h'].copy()
#                     cost_h_next[0] = cost_h_next[0] - ct.OperationCost(current_operation, next_map, G, shortest_length_G, edges_DiG, shortest_path_G)
# =============================================================================
                    cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next)
                    '''generate next node'''
                    next_node = next_node_list[0]
                    next_node_list[0] = next_node_list[0] + 1
                    added_nodes.append(next_node)
                    AddNewNodeToSearchTree(next_node, search_tree, next_map, cost_g_next, cost_h_next, cost_total_next, executed_vertex_next, executable_vertex_next)
                    search_tree.add_edge(leaf_node, next_node)
                    if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
                    '''renew best expanded node in search tree'''
                    num_remaining_vertex_next = num_all_vertex - len(executed_vertex_next)
                    if num_remaining_vertex_next == 0: finished_nodes.append(next_node)
                    if best_cost_total == None:
                        best_cost_total = cost_total_next
                        best_node = next_node
                    else:
                        if cost_total_next < best_cost_total:
                            best_cost_total = cost_total_next
                            best_node = next_node
    
    return best_node, finished_nodes, added_nodes
    
def FindNextNodeAndRenewTree(search_tree, best_leaf_node, depth_lookahead):
    #print('number of nodes in search tree before', len(list(search_tree.nodes())))
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
    
    #print('number of nodes in search tree after', len(list(search_tree.nodes())))
    return next_node

def FallBack(father_node, G, DG, search_tree, next_node_list, shortest_path_G, shortest_length_G, shortest_length_G_with4H, max_shortest_length_G, level_lookahead, possible_swap_combination, depth_lookahead, SWAP_cost, draw, q_phy, edges_DiG, DiG):
    '''fallback'''    
    leaf_nodes = []
    '''get attributes from current leaf node'''
    current_map = search_tree.nodes[father_node]['mapping']
    cost_g_current = search_tree.nodes[father_node]['cost_g']
    executed_vertex_current = search_tree.nodes[father_node]['executed_vertex']
    executable_vertex_current = search_tree.nodes[father_node]['executable_vertex']
    #print('remaining gates before', len(DG_current.nodes()))
    if draw == True: cir_phy_current = search_tree.nodes[father_node]['phy_circuit']
    '''fallback method: find the vertex in DG to be executed along shoetest path'''
    select_vertex = None
    for current_vertex in executable_vertex_current:
        current_operation = DG.nodes[current_vertex]['operation']
        if select_vertex == None:
            select_vertex = current_vertex
            select_gate_cost = current_operation.CalSWAPCost(current_map, shortest_length_G_with4H) * SWAP_cost
        else:
            current_swap_cost = current_operation.CalSWAPCost(current_map, shortest_length_G_with4H) * SWAP_cost
            if fallback_mode == 1 and current_swap_cost > select_gate_cost:
                select_vertex = current_vertex
                select_gate_cost = current_swap_cost
            if fallback_mode == 0 and current_swap_cost < select_gate_cost:
                select_vertex = current_vertex
                select_gate_cost = current_swap_cost                
    '''initialize next node'''
    next_map = current_map.Copy()
    executable_vertex_next = executable_vertex_current.copy()
    executed_vertex_next = executed_vertex_current.copy()
    cost_g_next = cost_g_current

    if draw == True:
        cir_phy_next = copy.deepcopy(cir_phy_current)
    else:
        cir_phy_next = None
    '''execute selected operation'''
    select_operation = DG.nodes[select_vertex]['operation']
    v_c = current_map.LogToPhy(select_operation.control_qubit)
    v_t = current_map.LogToPhy(select_operation.target_qubit)  
    select_path = shortest_path_G[v_c][v_t]
    if  (use_remoteCNOT_fallback == True) and (shortest_length_G[v_c][v_t] <= min_remoteCNOT_hop) and (shortest_length_G[v_c][v_t] >= 2):
        '''remote CNOT'''
        #print('current_hop is ', current_hop)
        # number of additional CNOTs in this remote CNOT operation
        cost_CNOT_remoteCNOT = ct.CalRemoteCNOTCostinArchitectureGraph(select_path, DiG) - 1 #这里减1是因为要去除本身的CNOT
        print('number of added gates for fallback is', cost_CNOT_remoteCNOT)
        #if cost_CNOT_remoteCNOT <= ct.OperationCost(current_operation, next_map, G, shortest_length_G, edges_DiG, shortest_path_G)
        cost_g_next = cost_g_current + cost_CNOT_remoteCNOT
        if draw == True:
            cir_phy_next = copy.deepcopy(cir_phy_current)
            ct.RemoteCNOTinArchitectureGraph(select_path, cir_phy_next, q_phy, DiG)
            cir_phy_next.barrier()
        executable_vertex_next = ct.FindExecutableNode(DG, executed_vertex_next, executable_vertex_next, [select_vertex])
# =============================================================================
#         else:
#             '''swap along the shortest path'''  
#             add_gates_count = ct.ConductCNOTInDGAlongPath(DG_next, select_vertex, select_path, next_map, draw, q_phy, cir_phy_next, edges_DiG)
#             num_executed_vertex_next += 1
#             executable_vertex_next = ct.FindExecutableNode(DG_next)
#             cost_g_next += add_gates_count            
# =============================================================================
    else:
        '''swap along the shortest path'''  
        add_gates_count = ct.ConductCNOTInDGAlongPath(DG, select_vertex, select_path, next_map, draw, False, q_phy, cir_phy_next, edges_DiG)
        print('number of added gates for fallback is', add_gates_count)
        executable_vertex_next = ct.FindExecutableNode(DG, executed_vertex_next, executable_vertex_next, [select_vertex])
        cost_g_next += add_gates_count
    '''check whether this window already has appliable vertexes, if has, then execute them'''
    res = ct.ExecuteAllPossibileNodesInDG(executable_vertex_next, executed_vertex_next, G, DG, next_map, draw, DiG, edges_DiG, cir_phy_next, q_phy)
    executed_vertex_next = res[0]
    executable_vertex_next = res[1]  
    '''calculate h cost'''
    cost_h_next = CalculateHeuristicCost(next_map, DG, executable_vertex_next, executed_vertex_next, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG)
    cost_total_next = CalculateTotalCost(cost_h_next, cost_g_next)
    '''generate next node'''
    next_node = next_node_list[0]
    new_father_node = next_node
    next_node_list[0] = next_node_list[0] + 1
    leaf_nodes.append(next_node)
    AddNewNodeToSearchTree(next_node, search_tree, next_map, cost_g_next, cost_h_next, cost_total_next, executed_vertex_next, executable_vertex_next)
    search_tree.add_edge(father_node, next_node)           
    #print('remaining gates after', len(DG_next.nodes()))
    if draw == True: search_tree.nodes[next_node]['phy_circuit'] = cir_phy_next
    
    '''delete residula nodes in search tree'''
    delete_nodes = list(search_tree.nodes())
    delete_nodes.remove(new_father_node)
    search_tree.remove_nodes_from(delete_nodes)

    '''expand search tree for the first time'''
    finished_nodes = []
    for i in range(depth_lookahead+1):
        res = ExpandTreeForNextStep(G, DG, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, level_lookahead, q_phy, draw, DiG)
        leaf_nodes = res[2]
        finished_nodes.extend(res[1])
    best_node = res[0]
    
    return best_node, finished_nodes, leaf_nodes, new_father_node

#@jit
def RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG, initial_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw=False, DiG=None, level_lookahead=None):
    if level_lookahead == None: level_lookahead = level_lookahead_default
    '''initialize other parameters'''
    #use_prune = False
    SWAP_cost = 3
    flag_4H = 0
    if DiG != None:
        edges_DiG = list(DiG.edges)
        SWAP_cost = 7
    else:
        edges_DiG = None
    shortest_length_G = shortest_length_Gs[0]
    shortest_length_G_with4H = shortest_length_Gs[1]
    max_shortest_length_G = max(shortest_length_G)
    total_fallback_num = max_shortest_length_G / 2#maximum fall back count 
    finished_nodes = []
    if debug_mode == True: draw = True
    
    '''initialize possible swap'''
    possible_swap_combination = []
    edges = list(G.edges()).copy()
    for current_edge in edges:
        possible_swap_combination.append([current_edge]) 
        
    '''check whether DG already has appliable vertexes, if has, then execute them'''
    cost_g_initial = 0#this is the count for number of added gates
    num_all_vertex = len(DG.nodes())
    executed_vertex = []
    executable_vertex = ct.FindExecutableNode(DG)
    if display_complete_state == True:
        print('RemoteCNOTandWindowLookAhead start')
        print('level_lookahead is', level_lookahead)
        print('fall back count is', total_fallback_num)
    res = ct.ExecuteAllPossibileNodesInDG(executable_vertex, executed_vertex, G, DG, initial_map, draw, DiG, edges_DiG, cir_phy, q_phy)
    executed_vertex = res[0]
    executable_vertex = res[1]
    
    '''initialize search tree'''
    search_tree = nx.DiGraph()
    next_node_list = [1]
    cost_h_initial = CalculateHeuristicCost(initial_map, DG, executable_vertex, executed_vertex, shortest_length_G, shortest_path_G, SWAP_cost, max_shortest_length_G, level_lookahead, DiG)
    cost_total_initial = CalculateTotalCost(cost_h_initial, 0)
    AddNewNodeToSearchTree(0, search_tree, initial_map, cost_g_initial, cost_h_initial, cost_total_initial, executed_vertex, executable_vertex)
    '''old version for adding nodes'''
# =============================================================================
#     search_tree.nodes[0]['mapping'] = initial_map
#     search_tree.nodes[0]['cost_g'] = cost_g_initial#this is the count for number of added gates
#     search_tree.nodes[0]['cost_h'] = cost_total_initial
#     search_tree.nodes[0]['num_executed_vertex'] = num_executed_vertex
# =============================================================================
    if draw == True: search_tree.nodes[0]['phy_circuit'] = cir_phy
    if len(executed_vertex) == num_all_vertex: finished_nodes.append(0)
    leaf_nodes = [0]
    num_pruned_nodes_list = [0]
    
    if display_complete_state == True: print(num_all_vertex - len(search_tree.nodes[0]['executed_vertex']), 'gates remaining')
    
    '''expand search tree for the first time'''
    for i in range(depth_lookahead+1):
        if finished_nodes != []: break
        res = ExpandTreeForNextStep(G, DG, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, level_lookahead, q_phy, draw, DiG)
        leaf_nodes = res[2]
        finished_nodes.extend(res[1])
    if finished_nodes == []: best_leaf_node = res[0]
    '''initialize fall back module'''
    if use_fallback == True:
        fallback_count = total_fallback_num
        fallback_vertex = 0
        pre_num_executed_vertex = len(executed_vertex)
        flag_no_leaf_fallback = False
    
    while finished_nodes == []:
        next_node = FindNextNodeAndRenewTree(search_tree, best_leaf_node, depth_lookahead)
        leaf_nodes = ct.FindAllLeafNodesInDG(search_tree)
        if use_prune == True:
            SearchTreeLeafNodesPruning(search_tree, next_node, leaf_nodes, num_pruned_nodes_list)
            '''check whether fallback is needed'''
            if len(leaf_nodes) == 0:
                flag_no_leaf_fallback = True
            else:
                res = ExpandTreeForNextStep(G, DG, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, level_lookahead, q_phy, draw, DiG)
        else:
            res = ExpandTreeForNextStep(G, DG, search_tree, leaf_nodes, possible_swap_combination, SWAP_cost, shortest_length_G, shortest_path_G, next_node_list, max_shortest_length_G, min_remoteCNOT_hop, level_lookahead, q_phy, draw, DiG)
        best_leaf_node = res[0]
        '''renew fallback count'''
        if use_fallback == True:
            #print(fallback_count)
            current_num_executed_vertex = len(search_tree.nodes[next_node]['executed_vertex'])
            #print(current_num_executed_vertex)
            if pre_num_executed_vertex == current_num_executed_vertex:
                fallback_count -= 1
            else:
                if pre_num_executed_vertex < current_num_executed_vertex:
                    pre_num_executed_vertex = current_num_executed_vertex
                    fallback_vertex = next_node
                    fallback_count = total_fallback_num
            '''check whether fallback is needed'''
            if fallback_count < 0 or flag_no_leaf_fallback == True:
                if display_complete_state == True:
                    if fallback_count < 0: print('fall back')
                    if flag_no_leaf_fallback == True: print('no leaf fall back')
                fallback_count = total_fallback_num
                flag_no_leaf_fallback = False
                res = FallBack(fallback_vertex, G, DG, search_tree, next_node_list, shortest_path_G, shortest_length_G, shortest_length_G_with4H, max_shortest_length_G, level_lookahead, possible_swap_combination, depth_lookahead, SWAP_cost, draw, q_phy, edges_DiG, DiG)
                best_leaf_node = res[0]
                next_node = res[3]
                
        
        if debug_mode == True: print(search_tree.nodes[best_leaf_node]['phy_circuit'].draw())
        if display_complete_state == True: print(num_all_vertex - len(search_tree.nodes[best_leaf_node]['executed_vertex']), 'gates remaining')
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
    '''draw physical circuit'''
    if draw == True:
        best_cir_phy = search_tree.nodes[best_finish_node]['phy_circuit']
        #print(best_cir_phy.draw())
        if debug_mode == True: print('start saving output physical circuit')
        fig = (best_cir_phy.draw(scale=0.7, filename=None, style=None, output='mpl', interactive=False, line_length=None, plot_barriers=True, reverse_bits=False))
        fig.savefig('Circuit_RemoteCNOTandWindowLookAhead.pdf', format='pdf', papertype='a4')
        if debug_mode == True: print('circuit saved')
    else:
        best_cir_phy = None
    '''number of traversed states'''
    num_total_state = next_node_list[0] - 1
    num_pruned_nodes = num_pruned_nodes_list[0]
    #nx.draw(search_tree, with_labels=True)
    return swap_count, num_total_state, num_total_state - num_pruned_nodes, additional_gate_count, best_cir_phy, search_tree.nodes[best_finish_node]['mapping']

if __name__ == '__main__':
    '''test FindNextNodeAndRenewTree'''
    tree = nx.DiGraph()
    tree.add_nodes_from(list(range(13)))
    tree.add_edges_from([(0,1), (0,2), (0,3), (1,4), (1,5), (1,6), (2,7), (2,8), (2,9),\
                         (3,10), (3,11), (3,12), (0,13), (13,14), (13,15), (14,17), (14,16)])
    FindNextNodeAndRenewTree(tree, 17, 1)
    nx.draw(tree, with_labels=True)