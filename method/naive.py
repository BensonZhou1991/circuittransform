# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 02:07:40 2019

@author: Xiangzhen Zhou

This module is for naive method
"""

import circuittransform as ct

def NaiveSearch(q_phy, cir_phy, G, DG, initial_map, shortest_path_G, draw=False):
    executable_vertex = ct.FindExecutableNode(DG)
    #executable_operation = ct.FindExecutableOperation(DG, executable_vertex)
    current_map = initial_map.Copy()
    
    '''naive method'''
    swap_count = 0
    while executable_vertex != []:
        for current_vertex in executable_vertex:
            current_operation = DG.node[current_vertex]['operation']
            q_c = current_operation.control_qubit
            q_t = current_operation.target_qubit
            v_c = current_map.DomToCod(q_c)
            v_t = current_map.DomToCod(q_t)
            current_path = shortest_path_G[v_c][v_t].copy()
            flag_naive = True
            while len(current_path) > 2:
                if flag_naive == True:
                    ct.SWAPInArchitectureGraph(current_path[0], current_path[1], current_map, q_phy, cir_phy)
                    flag_naive = not flag_naive
                    current_path.pop(0)
                    swap_count = swap_count + 1
                else:
                    ct.SWAPInArchitectureGraph(current_path[-1], current_path[-2], current_map, q_phy, cir_phy)
                    flag_naive = not flag_naive
                    current_path.pop(-1)
                    swap_count = swap_count + 1
            ct.ConductOperationInVertex(DG, current_vertex, current_map, cir_phy, q_phy)
        executable_vertex = ct.FindExecutableNode(DG)
    
    if draw == True: print(cir_phy.draw())    
    return swap_count