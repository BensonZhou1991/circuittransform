# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:28:00 2019

@author: Xiangzhen Zhou
"""

import circuittransform as ct

def HeuristicGreedySearch(q_phy, cir_phy, G, DG, initial_map, shortest_length_G, possible_swap_combination=None, draw=False):
    # only set True when debugging
    debug_model = False
    # adjust parameter to Heuristic Cost calculation, [worst, sum, best]
    adjust_parameter = (1, 0, 0, 0.0001)
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
        if debug_model == True:
            jjj = 5
        #print(len(list(DG.node)), 'gates remaining')
        
        cost_g = 0
        cost_h_total = ct.HeuristicCostZulehner(current_map, DG, executable_vertex, shortest_length_G)
        cost_h = cost_h_total[0]*adjust_parameter[0] + cost_h_total[1]*adjust_parameter[1] + cost_h_total[2]*adjust_parameter[2] + cost_h_total[3]*adjust_parameter[3]
        #print('executable vertex is', executable_vertex)
        cost_h_current = cost_h
        cost_total_best = cost_g + cost_h
        cost_h_best = cost_h
        best_vertex = cost_h_total[4]
        
        #cost_total_best = None
        
        while int(cost_h_current) != 0:
            if debug_model == True:
                jjj -= 1
                if jjj == 0:
                    break
                
            swaps_best = None
                
            '''remove swaps that have no effect on any operations in current level'''
            '''ATTENTION: this code block may be not correct'''
            '''
            v_op = []
            for op in executable_vertex:
                q = DG.node[op]['operation'].involve_qubits
                for i in q:
                    v_op.append(current_map.DomToCod(i))           
            possible_swap_combination_remove = possible_swap_combination.copy()
            for swaps in possible_swap_combination_remove:
                remove_flag = False
                for swap in swaps:
                    if (not (swap[0] in v_op)) and (not (swap[1] in v_op)):
                        remove_flag = True
                        break
                if remove_flag == True:
                    possible_swap_combination_remove.remove(swaps)
            '''
            possible_swap_combination_remove = possible_swap_combination
            
            '''search until find the goal state'''
            for swaps in possible_swap_combination_remove:
                '''evaluate all possible swap combinations and choose the best as next state'''
                cost_g_current = cost_g + len(swaps)
                current_map_copy = current_map.Copy()
                for current_swap in swaps:
                    '''try to conduct each swap'''
                    v0 = current_swap[0]
                    v1 = current_swap[1]
                    current_map_copy.RenewMapViaExchangeCod(v0, v1)
                cost_h_total = ct.HeuristicCostZulehner(current_map_copy, DG, executable_vertex, shortest_length_G)
                cost_h_current = cost_h_total[0]*adjust_parameter[0] + cost_h_total[1]*adjust_parameter[1] + cost_h_total[2]*adjust_parameter[2] + cost_h_total[3]*adjust_parameter[3]
                cost_total_current = cost_g_current + cost_h_current
                #print(cost_total_current,swaps)
                '''judge whether current state is better'''
                if (cost_total_current <= cost_total_best) and (cost_h_current < cost_h_best):
                    swaps_best = swaps
                    cost_h_best = cost_h_current
                    cost_total_best = cost_total_current
                    best_vertex = cost_h_total[4]
                        
            if swaps_best != None:
                '''conduct chosen best swap combination and renew swap counting and current map for next state'''
                #print(swaps_best)
                swap_count = swap_count + len(swaps_best)
                cost_h_current = cost_h_best
                cost_total_best = cost_h_best
                for swap in swaps_best:
                    v0 = swap[0]
                    v1 = swap[1]
                    ct.SWAPInArchitectureGraph(v0, v1, current_map, q_phy, cir_phy)
                if debug_model == True: print(cir_phy.draw())     
            else:
                '''no better swaps found, fallback, i.e., use the worst CNOT as the only gate in current operation''' 
                executable_vertex = [best_vertex]
                cost_h_total = ct.HeuristicCostZulehner(current_map, DG, executable_vertex, shortest_length_G)
                cost_h = cost_h_total[0]*adjust_parameter[0] + cost_h_total[1]*adjust_parameter[1] + cost_h_total[2]*adjust_parameter[2] + cost_h_total[3]*adjust_parameter[3]
                cost_h_current = cost_h
                cost_total_best = cost_g + cost_h
                cost_h_best = cost_h   
                best_vertex = cost_h_total[4]
            
                
                
        '''conduct operations in current level'''
        for vertex in executable_vertex :
            ct.ConductOperationInVertex(DG, vertex, current_map, cir_phy, q_phy)
        cir_phy.barrier()
        if debug_model == True: print(cir_phy.draw())
        '''refresh executable operations and go to the next level'''
        executable_vertex = ct.FindExecutableNode(DG)
    
    if draw == True: print(cir_phy.draw())
    return swap_count
