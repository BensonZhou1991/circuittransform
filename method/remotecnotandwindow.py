# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 00:10:10 2019

@author: Xiangzhen Zhou
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:28:00 2019

@author: Xiangzhen Zhou

This module is for search algorithm introducing remote CNOT 
"""

import circuittransform as ct

def RemoteCNOTandWindow(q_phy, cir_phy, G, DG, initial_map, shortest_length_G, shortest_path_G, possible_swap_combination=None, draw=False):
    # only set True when debugging
    debug_model = False
    flag_fallback = False
    SWAP_cost = 3
    min_remoteCNOT_hop = 3
    ues_which_h = 1 #decide to use which heuristic cost(max, min or total?)
    '''initial level and map'''
    executable_vertex = ct.FindExecutableNode(DG)
    #executable_operation = ct.FindExecutableOperation(DG, executable_vertex)
    current_map = initial_map.Copy()
    '''find all possible SWAP combinations for search in level'''
    if possible_swap_combination == None:
        possible_swap_combination = ct.FindAllPossibleSWAPParallel(G)
    
    '''search in all levels'''
    swap_count = 0   
    
    while executable_vertex != []:
        '''this section is only for debugging'''
        if debug_model == True:
            jjj = 5
        #print(len(list(DG.node)), 'gates remaining')
        
        '''check whether this window already has appliable vertex'''
        temp = False
        for vertex in executable_vertex :
            if ct.IsVertexInDGOperatiable(vertex, DG, G, current_map) == True:
                ct.ConductOperationInVertex(DG, vertex, current_map, cir_phy, q_phy)
                temp = True
                flag_fallback = False
        if temp == True:
            executable_vertex = ct.FindExecutableNode(DG)
            continue
        
        '''calculate the heuristic cost for all vertexes in current window'''
        cost_h_total = ct.HeuristicCostZhou1(current_map, DG, executable_vertex, shortest_length_G, shortest_path_G)
        cost_h = cost_h_total[ues_which_h] * SWAP_cost + cost_h_total[5]*0.00001
        
        '''judge whether remote CNOT is applicable'''
        flag_remoteCNOT = False
        if cost_h_total[2] <= min_remoteCNOT_hop - 1:
            flag_remoteCNOT = True
            remoteCNOT_vertex = cost_h_total[3]
            remoteCNOT_path = cost_h_total[4]
            # number of additional CNOTs in this remote CNOT operation
            cost_CNOT_remoteCNOT = ct.CalRemoteCNOTCostinArchitectureGraph(remoteCNOT_path) - 1 #这里减1是因为要去除本身的CNOT                 
        
        #print('executable vertex is', executable_vertex)
        cost_h_current =cost_h
        #cost_total_best = None
        
        '''this section is only for debugging'''
        if debug_model == True:
            jjj -= 1
            if jjj == 0:
                break
            
        possible_swap_combination_remove = possible_swap_combination
        cost_h_best = cost_h_current
        cost_total_best = cost_h_current + 0
        swaps_best = None
        best_operation_type = None
        cost_h_backup = cost_h_total
        cost_h_backup2 = cost_h
        
        '''in each available window, search for best swap combination for next step'''
        for swaps in possible_swap_combination_remove:            
            cost_g_current = len(swaps)  * SWAP_cost
            current_map_copy = current_map.Copy()
            for current_swap in swaps:
                '''try to conduct each swap'''
                v0 = current_swap[0]
                v1 = current_swap[1]
                current_map_copy.RenewMapViaExchangeCod(v0, v1)
            cost_h_total = ct.HeuristicCostZhou1(current_map_copy, DG, executable_vertex, shortest_length_G, shortest_path_G)
            cost_h_current = cost_h_total[ues_which_h] * SWAP_cost + cost_h_total[5]*0.00001
            cost_total_current = cost_g_current + cost_h_current
            #print(cost_total_current,swaps)
            '''judge whether current state is better'''
            if cost_total_current <= cost_total_best:
                swaps_best = swaps
                cost_h_best = cost_h_current
                best_operation_type = 'SWAP'
                cost_total_best = cost_total_current
                
        '''in each available window, search for best remote CNOT for next step if remote CNOT exists'''
        if flag_remoteCNOT == True:
            cost_total_remoteCNOT = cost_h_backup2 + cost_CNOT_remoteCNOT - (len(remoteCNOT_path) - 2)*SWAP_cost
            if cost_total_remoteCNOT <= cost_total_best:
                '''conduct remote CNOT'''
                CNOT_add = ct.RemoteCNOTinArchitectureGraph(remoteCNOT_path, cir_phy, q_phy)
                DG.remove_node(remoteCNOT_vertex)
                executable_vertex.remove(remoteCNOT_vertex)
                swap_count = swap_count + (CNOT_add - 1)/SWAP_cost
                '''refresh executable operations and go to the next level'''
                executable_vertex = ct.FindExecutableNode(DG)
                flag_fallback = False
                
                #print('best remoteCNOT')  
                continue
        
        if (swaps_best != None) and (flag_fallback == False):
            '''conduct chosen best swap combination and renew swap counting and current map for next state'''
            #print(swaps_best)
            swap_count = swap_count + len(swaps_best)
            cost_h_current = cost_h_best
            for swap in swaps_best:
                v0 = swap[0]
                v1 = swap[1]
                ct.SWAPInArchitectureGraph(v0, v1, current_map, q_phy, cir_phy)
            if debug_model == True: print(cir_phy.draw())
        else:
            if flag_remoteCNOT == False:
                '''conduct swap along shorstest path'''
                flag_fallback = True
                v0 = cost_h_backup[4][0]
                v1 = cost_h_backup[4][1]
                ct.SWAPInArchitectureGraph(v0, v1, current_map, q_phy, cir_phy)
                swap_count = swap_count + 1
                
                #print('swap along shorstest path')
            else:
                '''conduct remote CNOT'''
                CNOT_add = ct.RemoteCNOTinArchitectureGraph(remoteCNOT_path, cir_phy, q_phy)
                DG.remove_node(remoteCNOT_vertex)
                executable_vertex.remove(remoteCNOT_vertex)
                executable_vertex = ct.FindExecutableNode(DG)
                swap_count = swap_count + (CNOT_add - 1)/SWAP_cost
                flag_fallback = False
                
                #print('remoteCNOT')
                
        '''conduct appliable operations in current level'''
        temp = False
        for vertex in executable_vertex :
            if ct.IsVertexInDGOperatiable(vertex, DG, G, current_map) == True:
                ct.ConductOperationInVertex(DG, vertex, current_map, cir_phy, q_phy)
                temp = True
                flag_fallback = False
        if temp == True:
            executable_vertex = ct.FindExecutableNode(DG)
        
        if debug_model == True: print(cir_phy.draw())       
    
    if draw == True: print(cir_phy.draw())
    return swap_count
