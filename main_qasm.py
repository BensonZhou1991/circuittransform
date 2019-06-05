# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:33:23 2019

@author: zxz58
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
# choose quantum circuits
QASM_files = ct.CreateQASMFilesFromExample()
# number of logical qubits
num_qubits = 16
# description of architecture graph
num_vertex = 16
# repeat time
repeat_time = 1
# architecture graph generation control
#method_AG = ['circle']
#method_AG = ['grid', 8, 2]
method_AG = ['IBM QX3']
method_AG = ['IBM QX4']
method_AG = ['IBM QX5']
imoprt_swaps_combination_from_json = True

# method control
use_naive_search = 0
use_HeuristicGreedySearch = 0
use_Astar_search = 1
use_Astar_lookahead = 1
use_RemotoCNOTandWindow = 0
use_steiner_tree_and_remoteCNOT = 0
use_UDecompositionFullConnectivity = 0
use_UDecompositionFullConnectivityPATEL = 0
use_RemotoCNOTandWindowLookAhead0 = 0
use_RemotoCNOTandWindowLookAhead1 = 0
use_RemotoCNOTandWindowLookAhead2 = 0
use_RemotoCNOTandWindowLookAhead3 = 0
use_RemotoCNOTandWindowLookAhead2_nocut = 0
'''output control'''
out_num_swaps = False
out_num_add_gates = True
# draw control
draw_circle = False
draw_Steiner_paper = False
draw_architecture_graph = 0
draw_DG = 0
draw_logical_circuit = 0
draw_physical_circuit = False
draw_physical_circuit_niave = 0
draw_physical_circuit_HeuristicGreedySearch = 0
draw_physical_circuit_Astar = 1
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

'''generate architecture graph'''
'''q0 - v0, q1 - v1, ...'''
G = ct.GenerateArchitectureGraph(num_vertex, method_AG)
DiG = None
if isinstance(G, DiGraph): #check whether it is a directed graph
    DiG = G
    G = nx.Graph(DiG)
if draw_architecture_graph == True: nx.draw(G, with_labels=True)
'''calculate shortest path and its length'''
#shortest_path_G = nx.shortest_path(G, source=None, target=None, weight=None, method='dijkstra')
#shortest_length_G = dict(nx.shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra'))
if DiG == None:
    res = ct.ShortestPath(G)
    shortest_path_G = res[1]
    shortest_length_G = res[0]
else:
    res = ct.ShortestPath(DiG)
    shortest_path_G = res[1]
    shortest_length_G = res[0]

'''use all possible swaps in parallel'''
# =============================================================================
# if imoprt_swaps_combination_from_json == True:
#     fileObject = open('inputs\\swaps for architecture graph\\'+method_AG[0]+'.json', 'r')
#     possible_swap_combination = json.load(fileObject)
#     fileObject.close()
# else:
#     if use_Astar_search == True or use_Astar_lookahead == True or use_RemotoCNOTandWindow == True or use_UDecompositionFullConnectivity == True or use_HeuristicGreedySearch == True:
#         possible_swap_combination = ct.FindAllPossibleSWAPParallel(G)
# =============================================================================
'''only use single swap'''      
possible_swap_combination = []
edges = list(G.edges()).copy()
for current_edge in edges:
    possible_swap_combination.append([current_edge]) 

num_file = 0

'''only test specific circuits'''
QASM_files = ['test3.qasm']

for file in QASM_files:
    num_file += 1
    res = ct.CreateDGfromQASMfile(file)
    
    print('Number of circuits is', num_file)
    for repeat in range(repeat_time):
        print('The repeating time is ', repeat)
        '''initialize logical quantum circuit'''
        q_log = res[1][2]
        cir_log = res[0]
        x_label.append(cir_log.size())
        
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
        
        '''generate CNOT operation'''
        total_CNOT = res[1][3]
        
        '''generate party map for CNOT circuits'''
        if use_steiner_tree_and_remoteCNOT == 1 or use_UDecompositionFullConnectivity ==1 or use_UDecompositionFullConnectivityPATEL ==1:
            party_map = np.eye(num_vertex)
            ct.PerformOperationCNOTinPartyMap(party_map, total_CNOT)
            new_G = ct.AllocateVertexToPartyMap(G, num_vertex)
        
        
        '''initialize map from logical qubits to physical qubits'''
        '''1-1, 2-2 ...'''
        initial_map = Map(q_log, G)
        initial_map.RenewMapViaExchangeCod(0, 1)
        
        
        '''generate dependency graph'''
        DG = res[1][0]
        if draw_DG == True: nx.draw(DG, with_labels=True)
        
        '''draw logical quantum circuits'''
        if draw_logical_circuit == True: print(cir_log.draw())
        
        '''search using specific methods'''
        if use_naive_search == True:
            cost_naive = ct.NaiveSearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_path_G, draw_physical_circuit_niave)
            y_label_naive.append(cost_naive)
        if use_HeuristicGreedySearch == True:
            cost_HeuristicGreedySearch = ct.HeuristicGreedySearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, possible_swap_combination, draw_physical_circuit_HeuristicGreedySearch)
            y_label_HeuristicGreedySearch.append(cost_HeuristicGreedySearch)
        #print('Astar')
        if use_Astar_search == True:
            res = ct.AStarSearch(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_Astar, DiG)
            if out_num_add_gates == True: cost_Astar = res[1]# + cir_log.size()#0: swap count, 1: additional gates count
            y_label_Astar.append(cost_Astar)
        if use_Astar_lookahead == True:
            res = ct.AStarSearchLookAhead(q_phy, QuantumCircuit(q_phy), G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_Astar, DiG=DiG)
            if out_num_add_gates == True: cost_Astar_lookahead = res[2]# + cir_log.size()#0: swap count, 2: additional gates count
            cost_Astar_lookahead_state = res[1]
            y_label_Astar_lookahead.append(cost_Astar_lookahead)
            y_label_Astar_lookahead_state.append(cost_Astar_lookahead_state)
        #print('RemotoCNOTandWindow')    
        if use_RemotoCNOTandWindow == True:
            cost_Astar_RemotoCNOTandWindow = ct.RemotoCNOTandWindow(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, possible_swap_combination, draw_physical_circuit_RemotoCNOTandWindow)
            y_label_RemotoCNOTandWindow.append(cost_Astar_RemotoCNOTandWindow)
        if use_steiner_tree_and_remoteCNOT == True:
            #cost_steiner_tree_and_remoteCNOT = (len(ct.SteinerTreeAndRemoteCNOT(copy.copy(party_map), new_G, q_phy, num_vertex)) - num_CNOT)/3            
            cost_steiner_tree_and_remoteCNOT = (len(ct.SteinerTreeAndRemoteCNOT(copy.copy(party_map), new_G, q_phy, num_vertex)))/3
            y_label_SteinerTreeAndRemoteCNOT.append(cost_steiner_tree_and_remoteCNOT)
            
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

        if use_RemotoCNOTandWindowLookAhead0 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=0, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead0.append(cost_RemotoCNOTandWindowLookAhead)
            y_label_RemotoCNOTandWindowLookAhead0_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            y_label_RemotoCNOTandWindowLookAhead0_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)

        if use_RemotoCNOTandWindowLookAhead1 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=1, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead1.append(cost_RemotoCNOTandWindowLookAhead)
            y_label_RemotoCNOTandWindowLookAhead1_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            y_label_RemotoCNOTandWindowLookAhead1_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)

        if use_RemotoCNOTandWindowLookAhead2 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=2, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead.append(cost_RemotoCNOTandWindowLookAhead)
            y_label_RemotoCNOTandWindowLookAhead_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            y_label_RemotoCNOTandWindowLookAhead_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)
        
        if use_RemotoCNOTandWindowLookAhead3 == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=3, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead =res[3] + cir_log.size()
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead3.append(cost_RemotoCNOTandWindowLookAhead)
            y_label_RemotoCNOTandWindowLookAhead3_state.append(cost_RemotoCNOTandWindowLookAhead_state)
            y_label_RemotoCNOTandWindowLookAhead3_state_cut.append(cost_RemotoCNOTandWindowLookAhead_state_cut)

        if use_RemotoCNOTandWindowLookAhead2_nocut == True:
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=2, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            cost_RemotoCNOTandWindowLookAhead_state = res[1]
            cost_RemotoCNOTandWindowLookAhead_state_cut = res[2]
            y_label_RemotoCNOTandWindowLookAhead2nocut.append(cost_RemotoCNOTandWindowLookAhead)
            y_label_RemotoCNOTandWindowLookAhead2nocut_state.append(cost_RemotoCNOTandWindowLookAhead_state)

'''draw physical quantum circuits'''
if draw_physical_circuit == True:
    image_phy = cir_phy.draw()
    print(image_phy)

'''draw results graph'''
figure_fig = plt.figure() 
#figure_fig = plt.gcf()  # 'get current figure'
if use_naive_search == True:
    #plt.plot(ave_x_label, ave_y_label_naive, label='Naive')
    if draw_circle == True: plt.plot(y_label_naive, 'o')
if use_HeuristicGreedySearch == True:
    #plt.plot(ave_x_label, ave_y_label_HeuristicGreedySearch, label='Heuristic and greedy')
    if draw_circle == True: plt.plot(y_label_HeuristicGreedySearch, 'o')
if use_Astar_search == True:
    #plt.plot(ave_x_label, ave_y_label_Astar, label='Astar without lookahead')
    if draw_circle == True: plt.plot(y_label_Astar, 'o')
if use_Astar_lookahead == True:
    #plt.plot(ave_x_label, ave_y_label_Astar_lookahead, label='Astar with lookahead')
    if draw_circle == True: plt.plot(y_label_Astar_lookahead, 'o')
if use_RemotoCNOTandWindow == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindow,  label='RCW without lookahead')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindow, 'o')
if use_steiner_tree_and_remoteCNOT == True:
    #plt.plot(ave_x_label, ave_y_label_SteinerTreeAndRemoteCNOT,  label='Party map via Steiner tree')
    if draw_circle == True: plt.plot(y_label_SteinerTreeAndRemoteCNOT, 'o')
if use_UDecompositionFullConnectivity == True:
    #plt.plot(ave_x_label, ave_y_label_UDecompositionFullConnectivity,  label='U decomposition with full connectivity')
    if draw_circle == True: plt.plot(y_label_UDecompositionFullConnectivity, 'o')
if use_UDecompositionFullConnectivityPATEL == True:
    #plt.plot(ave_x_label, ave_y_label_UDecompositionFullConnectivityPATEL,  label='U PATEL with full connectivity')
    if draw_circle == True: plt.plot(y_label_UDecompositionFullConnectivityPATEL, 'o')
if use_RemotoCNOTandWindowLookAhead2 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead,  label='Breadth first with look ahead 2')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindowLookAhead, 'o')
if use_RemotoCNOTandWindowLookAhead0 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead0,  label='Breadth first with look ahead 0')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindowLookAhead0, 'o')
if use_RemotoCNOTandWindowLookAhead1 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead1,  label='Breadth first with look ahead 1')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindowLookAhead1, 'o')
if use_RemotoCNOTandWindowLookAhead3 == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead3,  label='Breadth first with look ahead 3')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindowLookAhead3, 'o')
if use_RemotoCNOTandWindowLookAhead2_nocut == True:
    #plt.plot(ave_x_label, ave_y_label_RemotoCNOTandWindowLookAhead2nocut,  label='Breadth first with look ahead 2 no pruning')
    if draw_circle == True: plt.plot(y_label_RemotoCNOTandWindowLookAhead2nocut, 'o')
    
if draw_Steiner_paper == True:
    plt.plot([3, 5, 10, 20, 30], [3/3, 5.2/3, 11.6/3, 25.85/3, 35.55/3],  label='Steiner tree')

plt.legend()
plt.grid()
#plt.axis([0, 450, 0, 100])
plt.show()
# save as local file
figure_fig.savefig('figure.eps', format='eps', dpi=1000)

'''draw graph for number of traversed states'''
'''
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
'''

'''construct a level containing all operations that can be conducted currently'''
# to be implemented