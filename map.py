# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:22:20 2019

@author: zxz58

This module is for the map from logical qubits to physical qubits
"""

class Map(object):
    
    instances_count = 0
    
    def __init__(self, q_reg, G, initial_map = None):
        '''
        if initial_map is None, q[0] -> v[0], q[1] -> v[1]...
        else, initial_map is a list q[0] -> initial_map[0], q[1] -> initial_map[1]...
        
        Input:
            initial_map: a dic{qi: vj...} reprenenting the initial map
        
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
            # initialize __CodToDom
            for v in vertex:
                self.__CodToDom[v] = []
            keys = list(initial_map.keys())
            for q in keys:
                self.__DomToCod[q] = initial_map[q]
                self.__CodToDom[initial_map[q]] = q

        Map.instances_count = Map.instances_count + 1 
    
    def Copy(self):
        '''return a copy of a Map instance'''
        return Map(self.logical_quantum_register, self.architecture_graph, self.__DomToCod)
        
    def DomToCod(self, qubit):
        return self.__DomToCod[qubit]
    
    def CodToDom(self, vertex):
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
        '''
        out = []
        for q in self.logical_quantum_register:
            out.append(self.DomToCod(q))
        
        return out