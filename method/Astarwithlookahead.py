# -*- coding: utf-8 -*-
"""
Created on Thu May  9 23:48:53 2019

@author: zxz58

See arXiv:1712.04722
"""

import circuittransform as ct
import networkx as nx
import copy

def ExpandSearchTree(DG, search_tree, next_node_list, father_node, none_leaf_nodes,  leaf_nodes, executable_vertex, shortest_length_G, possible_swap_combination, shortest_path_G, DiG):
    finished_node = None
    father_map = search_tree.nodes[father_node]['mapping']
    father_g = search_tree.nodes[father_node]['cost_g']
    father_exist_swaps = search_tree.nodes[father_node]['exist_swaps']
    '''move father node from leaf_nodes to none_leaf_nodes'''
    father_node_identity = search_tree.nodes[father_node]['identity']
    leaf_nodes.pop(str(father_node_identity))
    none_leaf_nodes[str(father_node_identity)] = father_node
    '''try all possible next state'''
    for swaps in possible_swap_combination:
        #print(swaps)
        next_map = father_map.Copy()
        '''try to conduct each swap'''
        for current_swap in swaps:
            v0 = current_swap[0]
            v1 = current_swap[1]
            next_map.RenewMapViaExchangeCod(v0, v1)
        next_identity = next_map.MapToTuple()
        '''judge whether next state should be kept'''
        if str(next_identity) in none_leaf_nodes.keys():
            #print('existed node')
            continue
        next_g = father_g + len(swaps)
        if  str(next_identity) in leaf_nodes.keys():
            #print('existed node2')
            exist_node = leaf_nodes[str(next_identity)]
            exist_g = search_tree.nodes[exist_node]['cost_g']
            if next_g >= exist_g:
                #print('existed node')
                continue
            '''if next leaf node if better than exist leaf node, then delete exist node'''
            leaf_nodes.pop(str(next_identity))
        '''add new leaf node'''
        next_h_total = ct.HeuristicCostZulehnerLookAhead(next_map, DG, executable_vertex, shortest_length_G, shortest_path_G, DiG)
        next_flag_finished = next_h_total[2]
        next_h = next_h_total[0]
        next_h_current_level = next_h_total[1]
        next_node = next_node_list[0]
        next_node_list[0] += 1
        next_swaps = copy.copy(father_exist_swaps)
        next_swaps.extend(swaps)
        search_tree.add_node(next_node)
        search_tree.add_edge(father_node, next_node)
        search_tree.nodes[next_node]['cost_h'] = next_h
        search_tree.nodes[next_node]['cost_h_current_level'] = next_h_current_level
        search_tree.nodes[next_node]['mapping'] = next_map
        search_tree.nodes[next_node]['cost_g'] = next_g
        search_tree.nodes[next_node]['flag_finished'] = next_flag_finished
        search_tree.nodes[next_node]['cost_total'] = search_tree.nodes[next_node]['cost_g'] + search_tree.nodes[next_node]['cost_h']
        search_tree.nodes[next_node]['exist_swaps'] = next_swaps
        #print('swaps are', next_swaps)
        search_tree.nodes[next_node]['identity'] = next_identity
        if next_flag_finished == True:
            if finished_node == None:
                finished_node = next_node
            else:
                if search_tree.nodes[next_node]['cost_g'] < search_tree.nodes[finished_node]['cost_g']:
                    finished_node = next_node
        '''add next node to leaf_nodes list'''
        leaf_nodes[str(next_identity)] = next_node
        
    return finished_node

def AStarSearchLookAhead(q_phy, cir_phy, G, DG, initial_map, shortest_length_G, shortest_path_G=None, possible_swap_combination=None, draw=False, DiG=None):
    # only set True when debugging
    debug_model = False
    if DiG != None:
        edges_DiG = list(DiG.edges)
        #print('egdes are', edges_DiG)
        SWAP_cost = 7
    '''initial level and map'''
    executable_vertex = ct.FindExecutableNode(DG)
    finished_map = initial_map
    #executable_operation = ct.FindExecutableOperation(DG, executable_vertex)
    '''find all possible SWAP combinations for search in level'''
    if possible_swap_combination == None:
        possible_swap_combination = ct.FindAllPossibleSWAPParallel(G)
    
    '''search in all levels'''
    swap_count = 0
    while executable_vertex != []:
        if debug_model == True:
            jjj = 5
        #print(len(list(DG.node)), 'gates remaining')
        
        '''initial search tree for current level'''
        search_tree = nx.DiGraph()
        search_tree.add_node(0)
        next_node_list = [1]
        search_tree.nodes[0]['mapping'] = finished_map.Copy()
        search_tree.nodes[0]['cost_g'] = 0
        search_tree.nodes[0]['exist_swaps'] = []
        search_tree.nodes[0]['identity'] = search_tree.nodes[0]['mapping'].MapToTuple()
        
        '''initial nodes set for current level'''        
        leaf_nodes_identity = search_tree.nodes[0]['identity']
        leaf_nodes = {str(leaf_nodes_identity): 0}
        none_leaf_nodes = {}
        
        '''calculate heuristic cost for initial node'''
        cost_h_total = ct.HeuristicCostZulehnerLookAhead(finished_map, DG, executable_vertex, shortest_length_G, shortest_path_G, DiG)
        cost_h = cost_h_total[0]
        cost_h_current_level = cost_h_total[1]
        flag_finished = cost_h_total[2]
        search_tree.nodes[0]['cost_h'] = cost_h
        search_tree.nodes[0]['cost_h_current_level'] = cost_h_current_level
        search_tree.nodes[0]['flag_finished'] = flag_finished
        search_tree.nodes[0]['cost_total'] = search_tree.nodes[0]['cost_g'] + search_tree.nodes[0]['cost_h']
        
        if cost_h_current_level == 0:
            finished_node = 0
            finished_map = search_tree.nodes[finished_node]['mapping']
        else:
            finished_node = None
        
        '''search til find the finished node'''
        while finished_node == None:
            if debug_model == True:
                jjj -= 1
                if jjj == 0:
                    break
            
            '''set best leaf node as current node to be expanded'''    
            father_node = None
            for node in leaf_nodes.values():
                if father_node == None:
                    father_node = node
                    father_cost = search_tree.nodes[father_node]['cost_total']
                else:
                    if search_tree.nodes[node]['cost_total'] < father_cost:
                        father_node = node
                        father_cost = search_tree.nodes[father_node]['cost_total']
            
            '''expand search tree based on current father node'''
            finished_node = ExpandSearchTree(DG, search_tree, next_node_list, father_node, none_leaf_nodes,  leaf_nodes, executable_vertex, shortest_length_G, possible_swap_combination, shortest_path_G, DiG)
        
        '''conduct SWAP operations before each level'''
        if draw == True:
            swaps = search_tree.nodes[finished_node]['exist_swaps']
            for current_swap in swaps:
                cir_phy.swap(q_phy[current_swap[0]], q_phy[current_swap[1]])
        
        '''conduct CNOT operations in current level'''
        #print('finished node is', finished_node)
        #print(search_tree.nodes[finished_node]['exist_swaps'])
        swap_count += len(search_tree.nodes[finished_node]['exist_swaps'])
        finished_map = search_tree.nodes[finished_node]['mapping']
        for vertex in executable_vertex:
            '''check whether this CNOT needs 4 H gates to convert direction'''
            if DiG != None:
                flag_4H = ct.CheckCNOTNeedConvertDirection2(vertex, DG, finished_map, edges_DiG)
                swap_count += flag_4H*4/7   
            ct.ConductCNOTOperationInVertex(DG, vertex, finished_map, cir_phy, q_phy, flag_4H)
        cir_phy.barrier()
        if debug_model == True: print(cir_phy.draw())
        '''refresh executable operations and go to the next level'''
        executable_vertex = ct.FindExecutableNode(DG)
    
    if draw == True: print(cir_phy.draw())
    '''number of traversed states'''
    num_total_state = next_node_list[0] - 1
    additional_gates = swap_count * SWAP_cost
    #nx.draw(search_tree, with_labels=True)
    return swap_count, num_total_state, additional_gates
