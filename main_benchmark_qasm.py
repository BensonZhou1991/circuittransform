# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:45:37 2019

@author: zxz58
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:33:23 2019

@author: zxz58
"""

import circuittransform as ct
import networkx as nx
from networkx import DiGraph, Graph
import numpy as np
from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from circuittransform import OperationU, OperationCNOT, OperationSWAP, Map
import matplotlib.pyplot as plt
import copy
import json
import time

'''initialize parameters'''
# choose quantum circuits
QASM_files = ct.CreateQASMFilesFromExample()
# number of logical qubits
num_qubits = 20
# description of architecture graph
num_vertex = 20
# repeat time for simulated annealing
repeat_time = 5
# architecture graph generation control
#method_AG = ['circle']
#method_AG = ['grid', 4, 5]
#method_AG = ['IBM QX3']
#method_AG = ['IBM QX4']
#method_AG = ['IBM QX5']
method_AG = ['IBM QX20']
#method_AG = ['directed grid', 3, 3]
imoprt_swaps_combination_from_json = True
'''initial mapping method'''
initial_mapping_control = 3#0: naive; 1: optimized; 2: only for IBM QX5; 3: annealing search; 4: specified by list
num_consider_gates = 0.5#counted gates for annealing search, 0-1 represents number gates * 0-1
initial_map_list = [10, 17, 11, 1, 2, 6, 12, 9, 4, 3, 13, 8, 7, 15, 0, 14]#only used for initial_mapping_control = 4
'''method control'''
use_RemotoCNOTandWindowLookAhead0 = 0
use_RemotoCNOTandWindowLookAhead1 = 1
use_RemotoCNOTandWindowLookAhead2 = 0
use_RemotoCNOTandWindowLookAhead1_nocut = 0
'''QASM input control'''
'''QX20'''
# =============================================================================
# QASM_files = ['4mod5-v1_22.qasm',
# 'mod5mils_65.qasm',
# 'alu-v0_27.qasm',
# 'decod24-v2_43.qasm',
# '4gt13_92.qasm',
# 'ising_model_10.qasm',
# 'ising_model_13.qasm',
# 'ising_model_16.qasm',
# 'qft_10.qasm',
# 'qft_16.qasm',
# 'rd84_142.qasm',
# 'adr4_197.qasm',
# 'radd_250.qasm',
# 'z4_268.qasm',
# 'sym6_145.qasm',
# 'misex1_241.qasm',
# 'rd73_252.qasm',
# 'cycle10_2_110.qasm',
# 'square_root_7.qasm',
# 'sqn_258.qasm',
# 'rd84_253.qasm',
# 'co14_215.qasm',
# 'sym9_193.qasm',
# '9symml_195.qasm']
# '''initial map for QX 20'''
# initial_map_best = [\
# [4, 14, 8, 13, 7, 11, 16, 0, 2, 18, 3, 19, 6, 12, 15, 9, 5, 10, 1, 17],
# [8, 6, 13, 7, 12, 11, 2, 17, 1, 16, 3, 18, 4, 10, 9, 14, 0, 5, 15, 19],
# [8, 1, 7, 2, 13, 9, 19, 16, 6, 17, 18, 12, 14, 4, 15, 0, 3, 11, 10, 5],
# [3, 8, 9, 4, 0, 14, 1, 5, 18, 11, 19, 15, 13, 10, 2, 6, 7, 16, 17, 12],
# [7, 8, 14, 19, 13, 4, 11, 5, 16, 1, 12, 15, 10, 6, 17, 0, 18, 9, 2, 3],
# [19, 13, 12, 17, 11, 6, 2, 3, 8, 9, 0, 15, 10, 4, 14, 16, 18, 5, 1, 7],
# [15, 16, 11, 10, 6, 2, 3, 4, 9, 8, 13, 12, 7, 18, 19, 1, 17, 14, 0, 5],
# [12, 16, 15, 10, 5, 6, 11, 17, 18, 14, 9, 8, 7, 2, 1, 0, 4, 13, 19, 3],
# [7, 6, 12, 5, 10, 11, 1, 8, 2, 13, 16, 15, 18, 0, 4, 3, 17, 19, 9, 14],
# [12, 13, 7, 11, 10, 5, 6, 2, 1, 16, 17, 8, 18, 14, 9, 4, 0, 3, 19, 15],
# [19, 18, 13, 8, 4, 1, 10, 12, 14, 9, 3, 2, 6, 11, 17, 16, 5, 7, 15, 0],
# [17, 3, 0, 10, 11, 5, 2, 8, 13, 12, 1, 7, 6, 18, 16, 4, 9, 19, 15, 14],
# [5, 15, 13, 18, 19, 6, 10, 16, 8, 7, 12, 17, 11, 9, 3, 2, 0, 4, 14, 1],
# [11, 6, 4, 1, 2, 8, 3, 13, 9, 7, 12, 15, 18, 14, 16, 0, 5, 10, 17, 19],
# [7, 13, 12, 6, 1, 8, 11, 19, 5, 18, 16, 14, 2, 4, 15, 0, 17, 9, 3, 10],
# [2, 1, 10, 3, 8, 16, 5, 17, 11, 13, 7, 6, 12, 18, 14, 9, 0, 4, 19, 15],
# [1, 6, 9, 12, 3, 8, 2, 4, 13, 7, 16, 10, 19, 11, 14, 18, 0, 5, 15, 17],
# [13, 16, 17, 12, 1, 10, 5, 8, 11, 6, 7, 2, 9, 19, 3, 14, 18, 15, 4, 0],
# [6, 7, 13, 2, 1, 8, 18, 0, 11, 10, 16, 12, 17, 5, 19, 4, 9, 3, 14, 15],
# [17, 16, 13, 8, 1, 2, 6, 11, 7, 12, 15, 5, 18, 0, 10, 14, 3, 9, 4, 19],
# [8, 2, 0, 5, 13, 16, 10, 6, 1, 11, 12, 7, 17, 15, 19, 4, 14, 9, 3, 18],
# [18, 16, 19, 3, 7, 1, 5, 10, 11, 6, 2, 8, 13, 12, 17, 14, 15, 0, 9, 4],
# [17, 16, 13, 5, 1, 2, 10, 6, 7, 12, 11, 0, 3, 4, 18, 9, 19, 14, 15, 8],
# [16, 17, 8, 10, 1, 2, 5, 6, 7, 12, 11, 18, 14, 19, 4, 0, 9, 15, 13, 3]]
# =============================================================================

'''QX5'''
# =============================================================================
# QASM_files = ['mini_alu_305.qasm',
# 'qft_10.qasm',
# 'sys6-v0_111.qasm',
# 'rd73_140.qasm',
# 'sym6_316.qasm',
# 'rd53_311.qasm',
# 'sym9_146.qasm',
# 'rd84_142.qasm',
# 'ising_model_10.qasm',
# 'cnt3-5_180.qasm',
# 'qft_16.qasm',
# 'ising_model_13.qasm',
# 'ising_model_16.qasm',
# 'wim_266.qasm',
# 'cm152a_212.qasm',
# 'cm42a_207.qasm',
# 'pm1_249.qasm',
# 'dc1_220.qasm',
# 'squar5_261.qasm',
# 'sqrt8_260.qasm',
# 'z4_268.qasm',
# 'adr4_197.qasm',
# 'sym6_145.qasm',
# 'misex1_241.qasm',
# 'square_root_7.qasm',
# 'ham15_107.qasm',
# 'dc2_222.qasm',
# 'sqn_258.qasm',
# 'inc_237.qasm',
# 'co14_215.qasm',
# 'life_238.qasm',
# 'max46_240.qasm',
# '9symml_195.qasm',
# 'dist_223.qasm',
# 'sao2_257.qasm',
# 'plus63mod4096_163.qasm',
# 'urf6_160.qasm',
# 'hwb9_119.qasm']
# =============================================================================

'''Lookahead 2 QX20'''
# =============================================================================
# QASM_files = ['qft_10.qasm',
# 'rd84_142.qasm',
# 'qft_16.qasm',
# 'z4_268.qasm',
# 'adr4_197.qasm',
# 'rd73_252.qasm'
# ]
# initial_map_best = [\
# [7, 6, 12, 5, 10, 11, 1, 8, 2, 13, 16, 15, 18, 0, 4, 3, 17, 19, 9, 14],
# [19, 18, 13, 8, 4, 1, 10, 12, 14, 9, 3, 2, 6, 11, 17, 16, 5, 7, 15, 0],
# [12, 13, 7, 11, 10, 5, 6, 2, 1, 16, 17, 8, 18, 14, 9, 4, 0, 3, 19, 15],
# [11, 6, 4, 1, 2, 8, 3, 13, 9, 7, 12, 15, 18, 14, 16, 0, 5, 10, 17, 19],
# [17, 3, 0, 10, 11, 5, 2, 8, 13, 12, 1, 7, 6, 18, 16, 4, 9, 19, 15, 14],
# [1, 6, 9, 12, 3, 8, 2, 4, 13, 7, 16, 10, 19, 11, 14, 18, 0, 5, 15, 17]]
# =============================================================================

'''Cambridge, QX5'''
QASM_files = ['graycode6_47.qasm',
'xor5_254.qasm',
'ex1_226.qasm',
'4gt11_84.qasm',
'ex-1_166.qasm',
'ham3_102.qasm',
'4mod5-v0_20.qasm',
'4mod5-v1_22.qasm',
'mod5d1_63.qasm',
'4gt11_83.qasm',
'4gt11_82.qasm',
'rd32-v0_66.qasm',
'mod5mils_65.qasm',
'4mod5-v0_19.qasm',
'rd32-v1_68.qasm',
'alu-v0_27.qasm',
'3_17_13.qasm',
'4mod5-v1_24.qasm',
'alu-v1_29.qasm',
'alu-v1_28.qasm',
'alu-v3_35.qasm',
'alu-v2_33.qasm',
'alu-v4_37.qasm',
'miller_11.qasm',
'decod24-v0_38.qasm',
'alu-v3_34.qasm',
'decod24-v2_43.qasm',
'mod5d2_64.qasm',
'4gt13_92.qasm',
'4gt13-v1_93.qasm',
'one-two-three-v2_100.qasm',
'4mod5-v1_23.qasm',
'4mod5-v0_18.qasm',
'one-two-three-v3_101.qasm',
'4mod5-bdd_287.qasm',
'decod24-bdd_294.qasm',
'4gt5_75.qasm',
'alu-v0_26.qasm',
'rd32_270.qasm',
'alu-bdd_288.qasm',
'decod24-v1_41.qasm',
'4gt5_76.qasm',
'4gt13_91.qasm',
'4gt13_90.qasm',
'alu-v4_36.qasm',
'4gt5_77.qasm',
'one-two-three-v1_99.qasm',
'rd53_138.qasm',
'one-two-three-v0_98.qasm',
'4gt10-v1_81.qasm',
'decod24-v3_45.qasm',
'aj-e11_165.qasm',
'4mod7-v0_94.qasm',
'alu-v2_32.qasm',
'4mod7-v1_96.qasm',
'cnt3-5_179.qasm',
'mod10_176.qasm',
'4gt4-v0_80.qasm',
'4gt12-v0_88.qasm',
'0410184_169.qasm',
'4_49_16.qasm',
'4gt12-v1_89.qasm',
'4gt4-v0_79.qasm',
'hwb4_49.qasm',
'4gt4-v0_78.qasm',
'mod10_171.qasm',
'4gt12-v0_87.qasm',
'4gt12-v0_86.qasm',
'4gt4-v0_72.qasm',
'4gt4-v1_74.qasm',
'mini-alu_167.qasm',
'one-two-three-v0_97.qasm',
'rd53_135.qasm',
'ham7_104.qasm',
'decod24-enable_126.qasm',
'mod8-10_178.qasm',
'4gt4-v0_73.qasm',
'ex3_229.qasm',
'mod8-10_177.qasm',
'alu-v2_31.qasm',
'C17_204.qasm',
'rd53_131.qasm',
'alu-v2_30.qasm',
'mod5adder_127.qasm',
'rd53_133.qasm',
'majority_239.qasm',
'ex2_227.qasm',
'cm82a_208.qasm',
'sf_276.qasm',
'sf_274.qasm',
'con1_216.qasm',
'rd53_130.qasm',
'f2_232.qasm',
'rd53_251.qasm',
'hwb5_53.qasm',
'radd_250.qasm',
'rd73_252.qasm',
'cycle10_2_110.qasm',
'hwb6_56.qasm',
'cm85a_209.qasm',
'rd84_253.qasm',
'root_255.qasm',
'mlp4_245.qasm',
'urf2_277.qasm',
'sym9_148.qasm',
'hwb7_59.qasm',
'clip_206.qasm',
'sym9_193.qasm',
'dist_223.qasm',
'sao2_257.qasm',
'urf5_280.qasm',
'urf1_278.qasm',
'sym10_262.qasm',
'hwb8_113.qasm',
'urf2_152.qasm']

QASM_files = ['qft_10.qasm',
'xor5_254.qasm',
'ex1_226.qasm']

# =============================================================================
# QASM_files = ['urf5_280.qasm',
# 'urf1_278.qasm',
# 'sym10_262.qasm']
# =============================================================================

# =============================================================================
# QASM_files = [
#                 'max46_240',
#                 '9symml_195',
#                 'dist_223',
#                 'sao2_257',
#                 'plus63mod4096_163']
# =============================================================================

print('QASM file is', QASM_files)
'''output control'''
out_num_swaps = False
out_num_add_gates = True
'''draw control'''
draw_circle = False
draw_Steiner_paper = False
draw_architecture_graph = 0
draw_DG = 0
draw_logical_circuit = 0
draw_physical_circuit = 0
draw_physical_circuit_RemotoCNOTandWindowLookAhead = 0

x_label = []
x_lable_filename = []

results = {}

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
    shortest_length_G = (res[0], res[2])
else:
    res = ct.ShortestPath(DiG)
    shortest_path_G = res[1]
    shortest_length_G = (res[0], res[2])

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
original_cir_size = []

for file in QASM_files:
    if file[-5:] != '.qasm': file += '.qasm'
    num_file += 1
    res_qasm = ct.CreateDGfromQASMfile(file)
    x_lable_filename.append(file)
    results[file[0:-5]] = {}
    results[file[0:-5]]['initial map'] = []
    results[file[0:-5]]['initial map time'] = []
    results[file[0:-5]]['gates'] = []
    results[file[0:-5]]['gates time'] = []
    
    print('Number of circuits is', num_file)
    for repeat in range(repeat_time):
        print('The repeating time is ', repeat)
        '''initialize logical quantum circuit'''
        q_log = res_qasm[1][2]
        cir_log = res_qasm[0]
        x_label.append(cir_log.size())
        if repeat == 0: original_cir_size.append(cir_log.size())
        
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
        total_CNOT = res_qasm[1][3]
 
        '''generate dependency graph'''
        DG = res_qasm[1][0]
        if draw_DG == True: nx.draw(DG, with_labels=True)       
        
        '''initialize map from logical qubits to physical qubits'''
        '''1-1, 2-2 ...'''
        if initial_mapping_control == 0:
            t_s = time.time()
            initial_map = Map(q_log, G)
            t_e = time.time()
        '''for circuit with only 10 qubit, we mannually map last 5 qubits to the down line'''
        if initial_mapping_control == 2:
            initial_map = Map(q_log, G)
            initial_map.RenewMapViaExchangeCod(9, 15)
            initial_map.RenewMapViaExchangeCod(8, 14)
            initial_map.RenewMapViaExchangeCod(7, 13)
            initial_map.RenewMapViaExchangeCod(6, 12)
        '''specific initial map through vertex list in AG'''
# =============================================================================
#         initial_map = Map(q_log, G, [1,2,3,8,7,6,11,12,13,16,17,18,4,9,14,19])
# =============================================================================
        '''optimized initial mapping'''
        if initial_mapping_control == 1:
            t_s = time.time()
            map_res = ct.FindInitialMapping(DG, q_log, G, shortest_length_G[0])
            t_e = time.time()
            initial_map = map_res[0]
            print('initial_map is', map_res[1])
        '''annealing search'''
        if initial_mapping_control == 3:
            start_map = ct.FindInitialMapping(DG, q_log, G, shortest_length_G[0])
            t_s = time.time()
            map_res = ct.InitialMapSimulatedAnnealing(start_map[1], DG, G, DiG, q_log, shortest_length_G[0], shortest_path_G, num_consider_gates)
            t_e = time.time()
            initial_map = map_res[0]
            initial_map_list = map_res[1]
        if initial_mapping_control == 4:
            t_s = time.time()
            initial_map = Map(q_log, G, initial_map_list)
            t_e = time.time()
        
        results[file[0:-5]]['initial map'].append(initial_map_list)
        results[file[0:-5]]['initial map time'].append(t_e - t_s)
        
        '''draw logical quantum circuits'''
        if draw_logical_circuit == True: print(cir_log.draw())
        
        '''search using specific methods'''
        if use_RemotoCNOTandWindowLookAhead0 == True:
            t_s = time.time()
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=0, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            t_e = time.time()
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            results[file[0:-5]]['gates'].append(cost_RemotoCNOTandWindowLookAhead)
            results[file[0:-5]]['gates time'].append(t_e - t_s)

        if use_RemotoCNOTandWindowLookAhead1 == True:
            t_s = time.time()
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=1, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            t_e = time.time()
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            results[file[0:-5]]['gates'].append(cost_RemotoCNOTandWindowLookAhead)
            results[file[0:-5]]['gates time'].append(t_e - t_s)

        if use_RemotoCNOTandWindowLookAhead2 == True:
            t_s = time.time()
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=2, use_prune=True, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            t_e = time.time()
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            results[file[0:-5]]['gates'].append(cost_RemotoCNOTandWindowLookAhead)
            results[file[0:-5]]['gates time'].append(t_e - t_s)

        if use_RemotoCNOTandWindowLookAhead1_nocut == True:
            t_s = time.time()
            res = ct.RemoteCNOTandWindowLookAhead(q_phy, cir_phy, G, copy.deepcopy(DG), initial_map, shortest_length_G, shortest_path_G, depth_lookahead=1, use_prune=False, draw=draw_physical_circuit_RemotoCNOTandWindowLookAhead, DiG=DiG)
            t_e = time.time()
            if out_num_add_gates == True: cost_RemotoCNOTandWindowLookAhead = res[3] + cir_log.size()
            results[file[0:-5]]['gates'].append(cost_RemotoCNOTandWindowLookAhead)
            results[file[0:-5]]['gates time'].append(t_e - t_s)

'''draw physical quantum circuits'''
if draw_physical_circuit == True:
    image_phy = cir_phy.draw()
    print(image_phy)

'''data processing'''
post_res = []
post_res_t1 = []#time for initial map
post_res_t2 = []#time for searching
post_res_map= []
for name in QASM_files:#results.keys():
    if name[-5:] == '.qasm': name = name[0:-5]
    best_num = None#number of output gates
    best_t1 = None
    best_t2 = None
    best_map = None
    pos = -1
    for num_gate in results[name]['gates']:
        pos += 1
        if best_num == None:
            best_num = num_gate
            best_map = results[name]['initial map'][pos]
        else:
            if num_gate < best_num:
                best_num = num_gate
                best_map = results[name]['initial map'][pos]
    for num in results[name]['initial map time']:
        if best_t1 == None:
            best_t1 = num
        else:
            if num < best_t1:
                best_t1 = num
    for num in results[name]['gates time']:
        if best_t2 == None:
            best_t2 = num
        else:
            if num < best_t2:
                best_t2 = num
    post_res.append(best_num)
    post_res_t1.append(best_t1)
    post_res_t2.append(best_t2)
    post_res_map.append(best_map)