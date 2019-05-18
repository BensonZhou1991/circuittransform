# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 02:09:49 2019

@author: Xiangzhen Zhou

d
"""
import networkx as nx
from networkx import DiGraph, Graph
import numpy as np
from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from circuittransform import OperationU, OperationCNOT, OperationSWAP, Map
import circuittransform as ct
import matplotlib.pyplot as plt
import copy
import json

'''initialize parameters'''
'''number of CNOT operations'''
#list_num_CNOT = [8]
#list_num_CNOT = [3, 5, 10, 20 ,30, 50, 100, 150, 200, 250, 300, 350, 400]
#list_num_CNOT = [3, 5, 10, 20 ,30, 50, 100, 150, 200]
list_num_CNOT = [3, 5, 10, 20, 30, 50]
# number of logical qubits
num_qubits = 16
# description of architecture graph
num_vertex = 16
# repeat time
repeat_time = 10
# architecture graph generation control
#method_AG = ['circle']
#method_AG = ['grid', 3, 3]
#method_AG = ['IBM QX3']
#method_AG = ['IBM QX4']
method_AG = ['IBM QX5']
imoprt_swaps_combination_from_json = 0

'''method control'''
use_naive_search = 0
use_HeuristicGreedySearch = 0
use_Astar_search = 0
use_Astar_lookahead = 1
use_RemotoCNOTandWindow = 0
use_steiner_tree_and_remoteCNOT = 0
use_UDecompositionFullConnectivity = 0
use_UDecompositionFullConnectivityPATEL = 0
use_RemotoCNOTandWindowLookAhead0 = 0
use_RemotoCNOTandWindowLookAhead1 = 1
use_RemotoCNOTandWindowLookAhead2 = 0
use_RemotoCNOTandWindowLookAhead3 = 0
use_RemotoCNOTandWindowLookAhead2_nocut = 0
'''draw control'''
draw_circle = False
draw_Steiner_paper = False
draw_architecture_graph = 0
draw_DG = False
draw_logical_circuit = 0
draw_physical_circuit = False
draw_physical_circuit_niave = 0
draw_physical_circuit_HeuristicGreedySearch = 0
draw_physical_circuit_Astar = 0
draw_physical_circuit_RemotoCNOTandWindow = False
draw_physical_circuit_RemotoCNOTandWindowLookAhead = 0

x_label = []
y_label_naive = []
y_label_HeuristicGreedySearch = []
y_label_Astar = []
y_label_Astar_lookahead = []
y_label_Astar_lookahead_state = []
y_label_RemotoCNOTandWindow = []
y_label_SteinerTreeAndRemoteCNOT = []
y_label_UDecompositionFullConnectivity = []
y_label_UDecompositionFullConnectivityPATEL = []
y_label_RemotoCNOTandWindowLookAhead = []
y_label_RemotoCNOTandWindowLookAhead0 = []
y_label_RemotoCNOTandWindowLookAhead1 = []
y_label_RemotoCNOTandWindowLookAhead3 = []
y_label_RemotoCNOTandWindowLookAhead2nocut = []
y_label_RemotoCNOTandWindowLookAhead_state = []
y_label_RemotoCNOTandWindowLookAhead0_state = []
y_label_RemotoCNOTandWindowLookAhead1_state = []
y_label_RemotoCNOTandWindowLookAhead3_state = []
y_label_RemotoCNOTandWindowLookAhead2nocut_state = []
y_label_RemotoCNOTandWindowLookAhead_state_cut = []
y_label_RemotoCNOTandWindowLookAhead0_state_cut = []
y_label_RemotoCNOTandWindowLookAhead1_state_cut = []
y_label_RemotoCNOTandWindowLookAhead3_state_cut = []
ave_x_label = []
ave_y_label_naive = []
ave_y_label_HeuristicGreedySearch = []
ave_y_label_Astar = []
ave_y_label_Astar_lookahead = []
ave_y_label_Astar_lookahead_state = []
ave_y_label_RemotoCNOTandWindow = []
ave_y_label_SteinerTreeAndRemoteCNOT = []
ave_y_label_UDecompositionFullConnectivity = []
ave_y_label_UDecompositionFullConnectivityPATEL = []
ave_y_label_RemotoCNOTandWindowLookAhead = []
ave_y_label_RemotoCNOTandWindowLookAhead0 = []
ave_y_label_RemotoCNOTandWindowLookAhead1 = []
ave_y_label_RemotoCNOTandWindowLookAhead3 = []
ave_y_label_RemotoCNOTandWindowLookAhead2nocut = []
ave_y_label_RemotoCNOTandWindowLookAhead_state = []
ave_y_label_RemotoCNOTandWindowLookAhead0_state = []
ave_y_label_RemotoCNOTandWindowLookAhead1_state = []
ave_y_label_RemotoCNOTandWindowLookAhead3_state = []
ave_y_label_RemotoCNOTandWindowLookAhead2nocut_state = []
ave_y_label_RemotoCNOTandWindowLookAhead_state_cut = []
ave_y_label_RemotoCNOTandWindowLookAhead0_state_cut = []
ave_y_label_RemotoCNOTandWindowLookAhead1_state_cut = []
ave_y_label_RemotoCNOTandWindowLookAhead3_state_cut = []

'''generate architecture graph'''
'''q0 - v0, q1 - v1, ...'''
G = ct.GenerateArchitectureGraph(num_vertex, method_AG)
DiG = None
if isinstance(G, DiGraph): #check whether it is a directed graph
    DiG = G
    G = nx.Graph(DiG)
if draw_architecture_graph == True: nx.draw(G, with_labels=True)
'''calculate shortest path and its length'''
shortest_path_G = nx.shortest_path(G, source=None, target=None, weight=None, method='dijkstra')
shortest_length_G = dict(nx.shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra'))

if imoprt_swaps_combination_from_json == True:
    fileObject = open('inputs\\swaps for architecture graph\\'+method_AG[0]+'.json', 'r')
    possible_swap_combination = json.load(fileObject)
    fileObject.close()
else:
    if use_Astar_search == True or use_Astar_lookahead == True or use_RemotoCNOTandWindow == True or use_UDecompositionFullConnectivity == True or use_HeuristicGreedySearch == True:
        possible_swap_combination = ct.FindAllPossibleSWAPParallel(G)

for num_CNOT in list_num_CNOT:
    print('Number of CNOT is', num_CNOT)
    total_naive = 0
    total_HeuristicGreedySearch = 0
    total_Astar = 0
    total_Astar_lookahead = 0
    total_Astar_lookahead_state = 0
    total_RemotoCNOTandWindow = 0
    total_SteinerTreeAndRemoteCNOT = 0
    total_UDecompositionFullConnectivity = 0
    total_UDecompositionFullConnectivityPATEL = 0
    total_RemotoCNOTandWindowLookAhead = 0
    total_RemotoCNOTandWindowLookAhead0 = 0
    total_RemotoCNOTandWindowLookAhead1 = 0
    total_RemotoCNOTandWindowLookAhead3 = 0
    total_RemotoCNOTandWindowLookAhead2nocut = 0
    total_RemotoCNOTandWindowLookAhead_state = 0
    total_RemotoCNOTandWindowLookAhead0_state = 0
    total_RemotoCNOTandWindowLookAhead1_state = 0
    total_RemotoCNOTandWindowLookAhead3_state = 0
    total_RemotoCNOTandWindowLookAhead2nocut_state = 0
    total_RemotoCNOTandWindowLookAhead_state_cut = 0
    total_RemotoCNOTandWindowLookAhead0_state_cut = 0
    total_RemotoCNOTandWindowLookAhead1_state_cut = 0
    total_RemotoCNOTandWindowLookAhead3_state_cut = 0
    for repeat in range(repeat_time):
        print('The repeating time is ', repeat)
        '''initialize logical quantum circuit'''
        q_log = QuantumRegister(num_qubits, 'q')
        cir_log = QuantumCircuit(q_log)
        
        '''initialize physical quantum circuit'''
        q_phy = QuantumRegister(num_vertex, 'v')
        cir_phy = QuantumCircuit(q_phy)
        
        '''generate architecture graph'''
        '''q0 - v0, q1 - v1, ...'''
        '''
        G = ct.GenerateArchitectureGraph(num_vertex, method_AG)
        '''
        
        '''calculate shortest path and its length'''
        '''
        shortest_path_G = nx.shortest_path(G, source=None, target=None, weight=None, method='dijkstra')
        shortest_length_G = dict(nx.shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra'))
        if draw_architecture_graph == True: nx.draw(G, with_labels=True)
        '''
        
        '''generate CNOT operation randomly'''
        total_CNOT = ct.CreateCNOTRandomly(q_log, num_CNOT, cir_log)
        
        '''generate party map for CNOT circuits'''
        if use_steiner_tree_and_remoteCNOT == 1 or use_UDecompositionFullConnectivity ==1 or use_UDecompositionFullConnectivityPATEL ==1:
            party_map = np.eye(num_vertex)
            ct.PerformOperationCNOTinPartyMap(party_map, total_CNOT)
            new_G = ct.AllocateVertexToPartyMap(G, num_vertex)
        
        
        '''initialize map from logical qubits to physical qubits'''
        initial_map = Map(q_log, G)
        
        '''generate dependency graph'''
        DG = ct.OperationToDependencyGraph(total_CNOT)
        if draw_DG == True: nx.draw(DG, with_labels=True)
        
        '''draw logical quantum circuits'''
        if draw_logical_circuit == True: print(cir_log.draw())
        
        '''search using specific methods'''
        if use_naive_search == True:
            cost_naive = ct.NaiveSearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_path_G, draw_physical_circuit_niave)
            y_label_naive.append(cost_naive)
            total_naive = total_naive + cost_naive
        if use_HeuristicGreedySearch == True:
            cost_HeuristicGreedySearch = ct.HeuristicGreedySearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, possible_swap_combination, draw_physical_circuit_HeuristicGreedySearch)
            y_label_HeuristicGreedySearch.append(cost_HeuristicGreedySearch)
            total_HeuristicGreedySearch = total_HeuristicGreedySearch + cost_HeuristicGreedySearch
        #print('Astar')
        if use_Astar_search == True:
            res = ct.AStarSearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_Astar, DiG)
            cost_Astar = res[0]
            y_label_Astar.append(cost_Astar)
            total_Astar = total_Astar + cost_Astar
        if use_Astar_lookahead == True:
            res = ct.AStarSearchLookAhead(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_Astar, DiG)
            cost_Astar_lookahead = res[0]
            cost_Astar_lookahead_state = res[1]
            y_label_Astar_lookahead.append(cost_Astar_lookahead)
            total_Astar_lookahead = total_Astar_lookahead + cost_Astar_lookahead
            y_label_Astar_lookahead_state.append(cost_Astar_lookahead_state)
            total_Astar_lookahead_state = total_Astar_lookahead_state + cost_Astar_lookahead_state
        #print('RemotoCNOTandWindow')    
        if use_RemotoCNOTandWindow == True:
            cost_Astar_RemotoCNOTandWindow = ct.RemotoCNOTandWindow(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_RemotoCNOTandWindow)
            y_label_RemotoCNOTandWindow.append(cost_Astar_RemotoCNOTandWindow)
            total_RemotoCNOTandWindow = total_RemotoCNOTandWindow + cost_Astar_RemotoCNOTandWindow
        if use_steiner_tree_and_remoteCNOT == True:
            #cost_steiner_tree_and_remoteCNOT = (len(ct.SteinerTreeAndRemoteCNOT(copy.copy(party_map), new_G, q_phy, num_vertex)) - num_CNOT)/3            
            cost_steiner_tree_and_remoteCNOT = (len(ct.SteinerTreeAndRemoteCNOT(copy.copy(party_map), new_G, q_phy, num_vertex)))/3
            y_label_SteinerTreeAndRemoteCNOT.append(cost_steiner_tree_and_remoteCNOT)
            total_SteinerTreeAndRemoteCNOT = total_SteinerTreeAndRemoteCNOT + cost_steiner_tree_and_remoteCNOT
            
        if use_UDecompositionFullConnectivity == True:
            o_c = ct.UDecompositionFullConnectivity(copy.copy(party_map), q_log, num_vertex)
            o_c.reverse()
            cost_1 = len(o_c)
            new_DG = ct.OperationToDependencyGraph(o_c)
            ct.GenerateDependency(o_c, num_vertex)
            cost_2 = ct.RemotoCNOTandWindow(q_phy, cir_phy, G, copy.deepcopy(new_DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_RemotoCNOTandWindow)
            cost_2 = 0
            cost_UDecompositionFullConnectivity = cost_1 / 3 + cost_2
            #cost_UDecompositionFullConnectivity = cost_1 / 3 + cost_2 - num_CNOT/3
            y_label_UDecompositionFullConnectivity.append(cost_UDecompositionFullConnectivity)
            total_UDecompositionFullConnectivity = total_UDecompositionFullConnectivity + cost_UDecompositionFullConnectivity

        if use_UDecompositionFullConnectivityPATEL == True:
            o_c = ct.UDecompositionFullConnectivityPATEL(copy.copy(party_map), q_log, num_vertex)
            o_c.reverse()
            cost_1 = len(o_c)
            new_DG = ct.OperationToDependencyGraph(o_c)
            ct.GenerateDependency(o_c, num_vertex)
            cost_2 = ct.RemotoCNOTandWindow(q_phy, cir_phy, G, copy.deepcopy(new_DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_RemotoCNOTandWindow)
            cost_2 = 0
            cost_UDecompositionFullConnectivityPATEL = cost_1 / 3 + cost_2
            #cost_UDecompositionFullConnectivityPATEL = cost_1 / 3 + cost_2 - num_CNOT/3
            y_label_UDecompositionFullConnectivityPATEL.append(cost_UDecompositionFullConnectivityPATEL)
            total_UDecompositionFullConnectivityPATEL = total_UDecompositionFullConnectivityPATEL + cost_UDecompositionFullConnectivityPATEL        

        if use_RemotoCNOTandWindowLookAhead0 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=0, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            cost_RemotoCNOTandWindowLookAhead = res[0]
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead0.append(cost_RemotoCNOTandWindowLookAhead)
            total_RemotoCNOTandWindowLookAhead0 = total_RemotoCNOTandWindowLookAhead0 + cost_RemotoCNOTandWindowLookAhead  
            y_label_RemotoCNOTandWindowLookAhead0_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            total_RemotoCNOTandWindowLookAhead0_state = total_RemotoCNOTandWindowLookAhead0_state + cost_RemotoCNOTandWindowLookAhead_state
            y_label_RemotoCNOTandWindowLookAhead0_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)
            total_RemotoCNOTandWindowLookAhead0_state_cut = total_RemotoCNOTandWindowLookAhead0_state_cut + cost_RemotoCNOTandWindowLookAhead_state_cut           

        if use_RemotoCNOTandWindowLookAhead1 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=1, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            cost_RemotoCNOTandWindowLookAhead = res[0]
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead1.append(cost_RemotoCNOTandWindowLookAhead)
            total_RemotoCNOTandWindowLookAhead1 = total_RemotoCNOTandWindowLookAhead1 + cost_RemotoCNOTandWindowLookAhead        
            y_label_RemotoCNOTandWindowLookAhead1_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            total_RemotoCNOTandWindowLookAhead1_state = total_RemotoCNOTandWindowLookAhead1_state + cost_RemotoCNOTandWindowLookAhead_state
            y_label_RemotoCNOTandWindowLookAhead1_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)
            total_RemotoCNOTandWindowLookAhead1_state_cut = total_RemotoCNOTandWindowLookAhead1_state_cut + cost_RemotoCNOTandWindowLookAhead_state_cut

        if use_RemotoCNOTandWindowLookAhead2 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=2, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            cost_RemotoCNOTandWindowLookAhead = res[0]
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead.append(cost_RemotoCNOTandWindowLookAhead)
            total_RemotoCNOTandWindowLookAhead = total_RemotoCNOTandWindowLookAhead + cost_RemotoCNOTandWindowLookAhead  
            y_label_RemotoCNOTandWindowLookAhead_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            total_RemotoCNOTandWindowLookAhead_state = total_RemotoCNOTandWindowLookAhead_state + cost_RemotoCNOTandWindowLookAhead_state
            y_label_RemotoCNOTandWindowLookAhead_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)
            total_RemotoCNOTandWindowLookAhead_state_cut = total_RemotoCNOTandWindowLookAhead_state_cut + cost_RemotoCNOTandWindowLookAhead_state_cut
        
        if use_RemotoCNOTandWindowLookAhead3 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=3, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            cost_RemotoCNOTandWindowLookAhead =res[0]
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead3.append(cost_RemotoCNOTandWindowLookAhead)
            total_RemotoCNOTandWindowLookAhead3 = total_RemotoCNOTandWindowLookAhead3 + cost_RemotoCNOTandWindowLookAhead
            y_label_RemotoCNOTandWindowLookAhead3_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            total_RemotoCNOTandWindowLookAhead3_state = total_RemotoCNOTandWindowLookAhead3_state + cost_RemotoCNOTandWindowLookAhead_state
            y_label_RemotoCNOTandWindowLookAhead3_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)
            total_RemotoCNOTandWindowLookAhead3_state_cut = total_RemotoCNOTandWindowLookAhead3_state_cut + cost_RemotoCNOTandWindowLookAhead_state_cut 

        if use_RemotoCNOTandWindowLookAhead2_nocut == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=2, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            cost_RemotoCNOTandWindowLookAhead = res[0]
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead2nocut.append(cost_RemotoCNOTandWindowLookAhead)
            total_RemotoCNOTandWindowLookAhead2nocut = total_RemotoCNOTandWindowLookAhead2nocut + cost_RemotoCNOTandWindowLookAhead  
            y_label_RemotoCNOTandWindowLookAhead2nocut_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            total_RemotoCNOTandWindowLookAhead2nocut_state = total_RemotoCNOTandWindowLookAhead2nocut_state + cost_RemotoCNOTandWindowLookAhead_state
                
        x_label.append(num_CNOT)
        
        
        
    ave_x_label.append(num_CNOT)
    ave_y_label_naive.append(total_naive / repeat_time)
    ave_y_label_HeuristicGreedySearch.append(total_HeuristicGreedySearch / repeat_time)
    ave_y_label_Astar.append(total_Astar / repeat_time)
    ave_y_label_Astar_lookahead.append(total_Astar_lookahead / repeat_time)
    ave_y_label_Astar_lookahead_state.append(total_Astar_lookahead_state / repeat_time)
    ave_y_label_RemotoCNOTandWindow.append(total_RemotoCNOTandWindow / repeat_time)
    ave_y_label_SteinerTreeAndRemoteCNOT.append(total_SteinerTreeAndRemoteCNOT / repeat_time)
    ave_y_label_UDecompositionFullConnectivity.append(total_UDecompositionFullConnectivity / repeat_time)
    ave_y_label_UDecompositionFullConnectivityPATEL.append(total_UDecompositionFullConnectivityPATEL / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead.append(total_RemotoCNOTandWindowLookAhead / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead0.append(total_RemotoCNOTandWindowLookAhead0 / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead1.append(total_RemotoCNOTandWindowLookAhead1 / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead3.append(total_RemotoCNOTandWindowLookAhead3 / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead2nocut.append(total_RemotoCNOTandWindowLookAhead2nocut / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead_state.append(total_RemotoCNOTandWindowLookAhead_state / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead0_state.append(total_RemotoCNOTandWindowLookAhead0_state / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead1_state.append(total_RemotoCNOTandWindowLookAhead1_state / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead3_state.append(total_RemotoCNOTandWindowLookAhead3_state / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead2nocut_state.append(total_RemotoCNOTandWindowLookAhead2nocut_state / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead_state_cut.append(total_RemotoCNOTandWindowLookAhead_state_cut / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead0_state_cut.append(total_RemotoCNOTandWindowLookAhead0_state_cut / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead1_state_cut.append(total_RemotoCNOTandWindowLookAhead1_state_cut / repeat_time)
    ave_y_label_RemotoCNOTandWindowLookAhead3_state_cut.append(total_RemotoCNOTandWindowLookAhead3_state_cut / repeat_time)

'''draw physical quantum circuits'''
if draw_physical_circuit == True:
    image_phy = cir_phy.draw()
    print(image_phy)

'''draw results graph'''
figure_fig = plt.figure() 
#figure_fig = plt.gcf()  # 'get current figure'
if use_naive_search == True:
    plt.plot(ave_x_label, ave_y_label_naive, label='Naive')
    if draw_circle == True: plt.plot(x_label, y_label_naive, 'ro')
if use_HeuristicGreedySearch == True:
    plt.plot(ave_x_label, ave_y_label_HeuristicGreedySearch, label='Heuristic and greedy')
    if draw_circle == True: plt.plot(x_label, y_label_HeuristicGreedySearch, 'ro')
if use_Astar_search == True:
    plt.plot(ave_x_label, ave_y_label_Astar, label='Astar without lookahead')
    if draw_circle == True: plt.plot(x_label, y_label_Astar, 'ro')
if use_Astar_lookahead == True:
    plt.plot(ave_x_label, ave_y_label_Astar_lookahead, label='Astar with lookahead')
    if draw_circle == True: plt.plot(x_label, y_label_Astar_lookahead, 'ro')
if use_RemotoCNOTandWindow == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindow,  label='RCW without lookahead')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindow, 'ro')
if use_steiner_tree_and_remoteCNOT == True:
    plt.plot(ave_x_label, ave_y_label_SteinerTreeAndRemoteCNOT,  label='Party map via Steiner tree')
    if draw_circle == True: plt.plot(x_label, y_label_SteinerTreeAndRemoteCNOT, 'ro')
if use_UDecompositionFullConnectivity == True:
    plt.plot(ave_x_label, ave_y_label_UDecompositionFullConnectivity,  label='U decomposition with full connectivity')
    if draw_circle == True: plt.plot(x_label, y_label_UDecompositionFullConnectivity, 'ro')
if use_UDecompositionFullConnectivityPATEL == True:
    plt.plot(ave_x_label, ave_y_label_UDecompositionFullConnectivityPATEL,  label='U PATEL with full connectivity')
    if draw_circle == True: plt.plot(x_label, y_label_UDecompositionFullConnectivityPATEL, 'ro')
if use_RemotoCNOTandWindowLookAhead2 == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead,  label='Breadth first with look ahead 2')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead, 'ro')
if use_RemotoCNOTandWindowLookAhead0 == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead0,  label='Breadth first with look ahead 0')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead0, 'ro')
if use_RemotoCNOTandWindowLookAhead1 == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead1,  label='Breadth first with look ahead 1')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead1, 'ro')
if use_RemotoCNOTandWindowLookAhead3 == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead3,  label='Breadth first with look ahead 3')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead3, 'ro')
if use_RemotoCNOTandWindowLookAhead2_nocut == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead2nocut,  label='Breadth first with look ahead 2 no pruning')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead2nocut, 'ro')
    
if draw_Steiner_paper == True:
    plt.plot([3, 5, 10, 20, 30], [3/3, 5.2/3, 11.6/3, 25.85/3, 35.55/3],  label='Steiner tree')

plt.legend()
plt.grid()
#plt.axis([0, 450, 0, 100])
plt.show()
# save as local file
figure_fig.savefig('figure.eps', format='eps', dpi=1000)

'''draw graph for number of traversed states'''
figure_fig2 = plt.figure()
if use_Astar_lookahead == True:
    plt.plot(ave_x_label, ave_y_label_Astar_lookahead_state, label='Astar with lookahead')
    if draw_circle == True: plt.plot(x_label, y_label_Astar_lookahead_state, 'ro')
if use_RemotoCNOTandWindowLookAhead2 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead_state,  label='Breadth first with look ahead 2')
    #if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead_state, 'ro')
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead_state_cut, dashes=[6, 2], label='Breadth first with look ahead 2')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead_state_cut, 'ro')    
if use_RemotoCNOTandWindowLookAhead0 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead0_state,  label='Breadth first with look ahead 0')
    #if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead0_state, 'ro')
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead0_state_cut, label='Breadth first with look ahead 0')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead0_state_cut, 'ro')   
if use_RemotoCNOTandWindowLookAhead1 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead1_state,  label='Breadth first with look ahead 1')
    #if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead1_state, 'ro')
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead1_state_cut, dashes=[6, 2], label='Breadth first with look ahead 1')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead1_state_cut, 'ro')   
if use_RemotoCNOTandWindowLookAhead3 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead3_state,  label='Breadth first with look ahead 3')
    #if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead3_state, 'ro')
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead3_state_cut, dashes=[6, 2], label='Breadth first with look ahead 3')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead3_state_cut, 'ro')   
if use_RemotoCNOTandWindowLookAhead2_nocut == True:
    plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead2nocut_state,  label='Breadth first with look ahead 2 no pruning')
    if draw_circle == True: plt.plot(x_label, y_label_RemotoCNOTandWindowLookAhead2nocut_state, 'ro')
 
plt.legend()
plt.grid()
#plt.axis([0, 450, 0, 100])
plt.show()
# save as local file
figure_fig2.savefig('figure2.eps', format='eps', dpi=1000)

'''construct a level containing all operations that can be conducted currently'''
# to be implemented