# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 18:12:57 2019

@author: zxz58
"""
import circuittransform as ct

def DrverseDG(DG):
    DG_reverse = DG.copy()
    for edge in DG.edges:
        edge_reverse = (edge[1], edge[0])
        DG_reverse.remove_edge(edge[0], edge[1])
        DG_reverse.add_edge(edge_reverse[0], edge_reverse[1])
    
    return DG_reverse

def ReverseMapForOneTime(q_phy, cir_phy, G, DG, finish_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw=False, DiG=None, level_lookahead=None, DG_reverse=None):
    '''
    end reverse to start, then use new initial map to traverse to the end again
    '''
    if  DG_reverse == None:
        DG_reverse = DrverseDG(DG)
    
    res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG_reverse, finish_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw, DiG, level_lookahead)  
    next_initial_map = res[5]
#    next_initial_map_list = next_initial_map.MapToList()
    
    res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG, next_initial_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw, DiG, level_lookahead)    
    next_finish_cost_addgate = res[3]
    next_finish_map = res[5]
#    next_finish_map_list = next_finish_map.MapToList()

    return next_initial_map, next_finish_map, next_finish_cost_addgate

def ReverseMap(reverse_time, q_phy, cir_phy, G, DG, initial_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw=False, DiG=None, level_lookahead=None, DG_reverse=None):

    cost_add_gates = []
    initial_maps_list = [initial_map.MapToList()]
    res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, DG, initial_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw, DiG, level_lookahead)    
    cost_add_gates.append(res[3])
#    finish_cost_addgate = res[3]
    finish_map = res[5]
#    finish_map_list = finish_map.MapToList()
    
    for time in range(reverse_time):
        res = ReverseMapForOneTime(q_phy, cir_phy, G, DG, finish_map, shortest_length_Gs, shortest_path_G, depth_lookahead, use_prune, draw, DiG, level_lookahead, DG_reverse)
        initial_map = res[0]
        finish_map = res[1]
        cost_add_gates.append(res[2])
        initial_maps_list.append(initial_map.MapToList())
    
    return cost_add_gates, initial_maps_list

if __name__ == '__main__':
    res = ReverseMap(4, q_phy, cir_phy, G, DG, initial_map, shortest_length_G, shortest_path_G, 1, use_prune=True, draw=False, DiG=None, level_lookahead=None, DG_reverse=None)
    