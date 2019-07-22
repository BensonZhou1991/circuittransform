# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:22:20 2019

@author: zxz58

This module is for the map from logical qubits to physical qubits
"""
import numpy as np
import networkx as nx
import circuittransform as ct
import matplotlib.pyplot as plt

class Map(object):
    
    instances_count = 0
    
    def __init__(self, q_reg, G, initial_map = None):
        '''
        if initial_map is None, q[0] -> v[0], q[1] -> v[1]...
        else, initial_map is a list q[0] -> initial_map[0], q[1] -> initial_map[1]...
        
        Input:
            initial_map: a dic{qi: vj...} reprenenting the initial map
                        or a list [v0, v1...] whose entry reprenents the physical qubit
        
        _DomToCod: dic from domain of definition to codomain
        _CodToDom: dic from codomain to domain of definition
        '''
        vertex = list(G.node())
        num_q = len(q_reg)
        num_v = len(list(G))
        self.logical_quantum_register = q_reg
        self.architecture_graph = G
        self.__DomToCod = {}
        self.__CodToDom = {}
        if initial_map == None:
            for q in q_reg:
                self.__DomToCod[q] = vertex[q[1]]
                self.__CodToDom[vertex[q[1]]] = q
            # define empty vertexes in architecture graph
            if num_v > num_q:
                for i in range(num_q, num_v):
                    self.__CodToDom[vertex[i]] = []
        else:
            if isinstance(initial_map, dict):
                # initialize __CodToDom
                for v in vertex:
                    self.__CodToDom[v] = []
                keys = list(initial_map.keys())
                for q in keys:
                    self.__DomToCod[q] = initial_map[q]
                    self.__CodToDom[initial_map[q]] = q
            if isinstance(initial_map, list):
                # initialize __CodToDom
                for v in vertex:
                    self.__CodToDom[v] = []
                for i in range(len(q_reg)):
                    q = q_reg[i]
                    self.__DomToCod[q] = initial_map[i]
                    self.__CodToDom[initial_map[i]] = q

        Map.instances_count = Map.instances_count + 1 
    
    def Copy(self):
        '''return a copy of a Map instance'''
        return Map(self.logical_quantum_register, self.architecture_graph, self.__DomToCod)
        
    def DomToCod(self, qubit):
        return self.__DomToCod[qubit]
    
    def CodToDom(self, vertex):
        return self.__CodToDom[vertex]

    def LogToPhy(self, qubit):
        return self.__DomToCod[qubit]
    
    def PhyToLog(self, vertex):
        return self.__CodToDom[vertex]
    
    def RenewMapViaExchangeDom(self, q0, q1):
        '''
        exchange mapping of qubits q0 and q1
        '''
        temp_q0 = self.__DomToCod[q0]
        temp_q1 = self.__DomToCod[q1]
        self.__DomToCod[q0] = temp_q1
        self.__DomToCod[q1] = temp_q0
        self.__CodToDom[temp_q0] = q1
        self.__CodToDom[temp_q1] = q0

    def RenewMapViaExchangeCod(self, v0, v1):
        '''
        exchange mapping of vertexes v0 and v1
        '''
        temp_v0 = self.__CodToDom[v0]
        temp_v1 = self.__CodToDom[v1]
        self.__CodToDom[v0] = temp_v1
        self.__CodToDom[v1] = temp_v0
        if temp_v0 != []:
            self.__DomToCod[temp_v0] = v1
        if temp_v1 != []:
            self.__DomToCod[temp_v1] = v0
    
    def RenewMapViaSWAP(self, operation_swap):
        '''
        update map after swap operation
        '''
        q0 = operation_swap.involve_qubits[0]
        q1 = operation_swap.involve_qubits[1]
        self.RenewMapViaExchangeDom(q0, q1)
        
    def MapToTuple(self):
        '''
        calculate corresponding tuple for the map
        it can be used to indetify the identical mapping
        '''
        out = []
        for q in self.logical_quantum_register:
            out.append(self.DomToCod(q))
        
        return out
    
    def MapToList(self):
        '''
        return the list(phy -> log) of the map
        '''
        map_list = []
        q_log = self.logical_quantum_register
        for q in q_log:
            map_list.append(self.LogToPhy(q))
        
        return map_list
            
    
def SortKey(qubit_weight):
    return qubit_weight[1]

def FindInitialMapping(DG, q_log, G, shortest_length_G):
    '''
    find a initial mapping
    step1: count the used times for each logical qubit and logical qubits pairs
    step2: choose the logical qubit mostly used and allocate it to physical qubit with the best connectivity
    step3: choose the logical qubits who will be used mostly to compose to CNOT with qubit in step2 and allocate
    them to to physical qubits conncted to the one in step2
    input:
        G must be an undirected graph
    '''
    len_q = len(q_log)
    len_v = len(G.nodes())
    qubit_weight = []
    vertex_weight = []
    qubit_qubit_weight = []
    initial_map = [-1]*len_q
    for q in range(len_q):
        qubit_weight.append([q, 0])
        attend_list = []
        for q2 in range(len_q):
            attend_list.append([q2, 0])
        qubit_qubit_weight.append(attend_list)
    for v in range(len_v):
        vertex_weight.append([v, 0])
    '''calculate the used times for each logical qubit'''
    for node in DG.nodes():
        op = DG.nodes[node]['operation']
        involve_qubits = op.involve_qubits
        qubit_qubit_weight[involve_qubits[0][1]][involve_qubits[1][1]][1] += 1
        qubit_qubit_weight[involve_qubits[1][1]][involve_qubits[0][1]][1] += 1
        for q_used in involve_qubits:
            qubit_weight[q_used[1]][1] += 1
    '''calculate the performance for each physical qubit'''
    for node in G.nodes():
        vertex_weight[node][1] += sum(shortest_length_G[node].values())
    '''sort the logical qubits'''
    #print(qubit_weight)
    qubit_weight.sort(key=SortKey, reverse=True)
    vertex_weight.sort(key=SortKey, reverse=False)
    
    #print(qubit_weight)
    #print(qubit_qubit_weight)
    #print(vertex_weight)
    
    for [current_qubit, current_qubit_weight] in qubit_weight:
        if initial_map[current_qubit] != -1: continue
        '''search best node in AG'''
        for [best_vertex, best_vertex_weight] in vertex_weight:
            if not best_vertex in initial_map: break
        '''allocate this node to qubit'''
        initial_map[current_qubit] = best_vertex
        '''allocate nodes in AG to qubits adjacent to current one'''
        next_qubits_list = qubit_qubit_weight[current_qubit]
        next_qubits_list.sort(key=SortKey, reverse=True)
        for [next_qubit, next_weight] in next_qubits_list:
            if next_weight == 0: break # if this qubit has no connection to current one
            if initial_map[next_qubit] != -1: continue
            next_vertexes = list(G[best_vertex])
            for [best_next_vertex, best_next_vertex_weight] in vertex_weight:
                if not best_next_vertex in next_vertexes: continue
                if not best_next_vertex in initial_map:
                    initial_map[next_qubit]
    return Map(q_log, G, initial_map), initial_map

def initpara():
    '''only for simulated annealing'''
    alpha = 0.98
    t = (1,100)#(1,100)
    markovlen = 100
    return alpha,t,markovlen

def CalCost(map_list, DG, counted_CNOT_nodes, shortest_length_G, shortest_path_G, q_log, G, DiG):
    '''only for simulated annealing'''
    if isinstance(map_list, list):
        cost = ct.HeuristicCostZulehner(Map(q_log, G, map_list), DG, counted_CNOT_nodes, shortest_length_G, shortest_path_G, DiG)
    else:
        cost = ct.HeuristicCostZulehner(map_list, DG, counted_CNOT_nodes, shortest_length_G, shortest_path_G, DiG)
    return cost[1]

def MapListReverse(map_list, num_v):
    v_list = [-1] * num_v
    for i in range(len(map_list)):
        v_list[map_list[i]] = i
    return v_list

def VListReverse(v_list, num_q):
    map_list = [-1] * num_q
    for i in range(len(v_list)):
        if v_list[i] == -1: continue
        map_list[v_list[i]] = i
    return map_list

def InitialMapSimulatedAnnealing(start_map, DG, G, DiG, q_log, shortest_length_G, shortest_path_G, num_consider_gates=0, convergence=False):
    '''
    this function is modified from "https://blog.csdn.net/qq_34798326/article/details/79013338"
    '''
    if convergence == True:
        temp = []
        solution = []
        solution_best = []
    if len(start_map) != len(G.nodes()):
        for v in G.nodes():
            if not v in start_map: start_map.append(v)
    if num_consider_gates <= 1:
        num_consider_gates = len(DG.nodes()) * num_consider_gates
        if num_consider_gates < 50: num_consider_gates = 50
    if num_consider_gates > len(DG.nodes()): num_consider_gates = len(DG.nodes())
    DG_copy = DG.copy()
    '''generate counted CNOTs'''
    counted_CNOT_nodes = []
    while len(counted_CNOT_nodes) < num_consider_gates:
        added_nodes = ct.FindExecutableNode(DG_copy)
        counted_CNOT_nodes.extend(added_nodes)
        DG_copy.remove_nodes_from(added_nodes)
    print('number of counted gates is', len(counted_CNOT_nodes))
    '''Simulated Annealing'''
    solutionnew = start_map
    num = len(start_map)
    #valuenew = np.max(num)
    solutioncurrent = solutionnew.copy()
    valuecurrent = 99000  #np.max这样的源代码可能同样是因为版本问题被当做函数不能正确使用，应取一个较大值作为初始值
    
    #print(valuecurrent)
    
    solutionbest = solutionnew.copy()
    valuebest = 99000 #np.max
    alpha,t2,markovlen = initpara()
    t = t2[1]#temperature
    result = [] #记录迭代过程中的最优解
    
    while t > t2[0]:
        for i in np.arange(markovlen):
            #下面的两交换和三角换是两种扰动方式，用于产生新解
            if np.random.rand() > 0.5:# 交换路径中的这2个节点的顺序
                # np.random.rand()产生[0, 1)区间的均匀随机数
                while True:#产生两个不同的随机数
                    loc1 = np.int(np.around(np.random.rand()*(num-1)))
                    loc2 = np.int(np.around(np.random.rand()*(num-1)))
                    ## print(loc1,loc2)
                    if loc1 != loc2:
                        break
                solutionnew[loc1],solutionnew[loc2] = solutionnew[loc2],solutionnew[loc1]
            else: #三交换
                while True:
                    loc1 = np.int(np.around(np.random.rand()*(num-1)))
                    loc2 = np.int(np.around(np.random.rand()*(num-1))) 
                    loc3 = np.int(np.around(np.random.rand()*(num-1)))
                    if((loc1 != loc2)&(loc2 != loc3)&(loc1 != loc3)):
                        break
                # 下面的三个判断语句使得loc1<loc2<loc3
                if loc1 > loc2:
                    loc1,loc2 = loc2,loc1
                if loc2 > loc3:
                    loc2,loc3 = loc3,loc2
                if loc1 > loc2:
                    loc1,loc2 = loc2,loc1
                #下面的三行代码将[loc1,loc2)区间的数据插入到loc3之后
                tmplist = solutionnew[loc1:loc2].copy()
                solutionnew[loc1:loc3-loc2+1+loc1] = solutionnew[loc2:loc3+1].copy()
                solutionnew[loc3-loc2+1+loc1:loc3+1] = tmplist.copy()  
            valuenew = CalCost(solutionnew, DG, counted_CNOT_nodes, shortest_length_G, shortest_path_G, q_log, G, DiG)
           # print (valuenew)
            if valuenew < valuecurrent: #接受该解
                #更新solutioncurrent 和solutionbest
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy()
                #renew best solution
                if valuenew < valuebest:
                    valuebest = valuenew
                    solutionbest = solutionnew.copy()
            else:#按一定的概率接受该解
                if np.random.rand() < np.exp(-(valuenew-valuecurrent)/t):
                    valuecurrent = valuenew
                    solutioncurrent = solutionnew.copy()
                else:
                    solutionnew = solutioncurrent.copy()

            if convergence == True:
                temp.append(t)
                solution.append(valuecurrent)
                solution_best.append(valuebest)
        
        t = alpha*t
        #print(valuebest)
        result.append(valuebest)
    print('initial_map is', solutionbest)
    '''draw convergence graph'''
    if convergence == True:
        figure_fig = plt.figure()
        plt.grid()
        plt.xlabel('Times of Iteration')
        plt.ylabel('Cost of States')
        plt.plot(solution)
        plt.plot(solution_best)
        figure_fig.savefig('simulated annealing convergence.eps', format='eps', dpi=1000)
        
    return Map(q_log, G, solutionbest), solutionbest
        