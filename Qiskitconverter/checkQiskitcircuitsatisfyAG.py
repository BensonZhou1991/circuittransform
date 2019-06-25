# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:56:54 2019

@author: zxz58
"""

import circuittransform as ct

def CheckQiskitCircuitSatisfyAG(DG, cir, G, initial_map):
    '''
    check whether circuit satisfies architecture graph
    only support:
        1. undirected AG, 2. only swap added
    we will delete any gates except swap and CNOT
    '''
    current_map = initial_map.Copy()
    current_vertex = ct.FindExecutableNode(DG)
    executed_vertex = []
    data = cir.data
    '''search for all gates in physical circuit'''
    for Gate in data:
        if Gate.name == 'cx':
            flag_matched = False
            q_phys = Gate.qargs
            q_phy_pos = (q_phys[0][1], q_phys[1][1])
            '''find match in DG'''
            for vertex in current_vertex:
                op = DG.nodes[vertex]['operation']
                q_logs = op.involve_qubits
                q_log_pos = (current_map.LogToPhy(q_logs[0]), current_map.LogToPhy(q_logs[1]))
                if q_phy_pos == q_log_pos:
                    flag_matched = True
                    current_vertex = ct.FindExecutableNode(DG, executed_vertex, current_vertex, [vertex])
                    break
            '''judge whether a match has been found'''
            if flag_matched == False:
                #raise Exception('incompatible CNOT gate found')
                return False
        if Gate.name == 'swap':
            flag_matched = True
            q_phys = Gate.qargs
            v0 = q_phys[0][1]
            v1 = q_phys[1][1]
            current_map.RenewMapViaExchangeCod(v0, v1)
    
    if len(executed_vertex) == len(DG.nodes()) and current_vertex == []:
        return True
    else:
        return False