# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:26:23 2019

@author: zxz58
"""
import networkx as nx
import circuittransform as ct
import numpy as np

def ShortestPath(G):
    """
    output:
        shortest_length_G: the number of needed swaps + 1 between nodes(control to target) and according paths
        shortest_length_G2: shortest_length_G plus possibile 4H in directed G
    """
    delete_fraction = False
    if nx.is_directed(G) == False:
        shortest_path_G = nx.shortest_path(G, source=None, target=None, weight=None, method='dijkstra')
        shortest_length_G = dict(nx.shortest_path_length(G, source=None, target=None, weight=None, method='dijkstra'))
    else:
        shortest_length_G ={}
        shortest_path_G = {}
        for node1 in G.nodes():
            shortest_length_G[node1] = {}
            shortest_path_G[node1] = {}
            for node2 in G.nodes():
                if node1 == node2:
                    shortest_length_G[node1][node2] = 0
                    shortest_path_G[node1][node2] = [node1]   
                else:
                    shortest_length_G[node1][node2] = 10000
                    shortest_path_G[node1][node2] = None
        for node in G.nodes():
            #print(node)
            unfinished_nodes = list(G.nodes())
            unfinished_nodes.remove(node)
            finished_nodes = [node]
            #print(finished_nodes)
            while len(unfinished_nodes) != 0:
                trans_nodes = []
                for edge in G.edges():
                    #print(finished_nodes)
                    if (edge[0] in finished_nodes) and (edge[1] in unfinished_nodes):
                        #print(edge[0])
                        #print(edge[1])
                        new_path = shortest_path_G[node][edge[0]].copy()
                        new_path.append(edge[1])
                        add_4H = ct.CheckCNOTNeedConvertDirection(node, edge[1], new_path, G.edges())
                        new_length = len(new_path) - 1 + add_4H*4/7
                        if new_length < shortest_length_G[node][edge[1]]:
                            shortest_length_G[node][edge[1]] = new_length
                            shortest_path_G[node][edge[1]] = new_path
                            trans_nodes.append(edge[1])
                    else:
                        if (edge[1] in finished_nodes) and (edge[0] in unfinished_nodes):
                            #print(edge[0])
                            #print(edge[1])
                            new_path = shortest_path_G[node][edge[1]].copy()
                            new_path.append(edge[0])
                            add_4H = ct.CheckCNOTNeedConvertDirection(node, edge[0], new_path, G.edges())
                            new_length = len(new_path) - 1 + add_4H*4/7
                            if new_length < shortest_length_G[node][edge[0]]:
                                shortest_length_G[node][edge[0]] = new_length
                                shortest_path_G[node][edge[0]] = new_path
                                trans_nodes.append(edge[0])
                trans_nodes = list(set(trans_nodes))
                for node2 in trans_nodes:
                    unfinished_nodes.remove(node2)
                    finished_nodes.append(node2)
    
    shortest_length_G_with4H = shortest_length_G.copy()
    
    if delete_fraction == False:
        for node1 in G.nodes():
            for node2 in G.nodes():
                shortest_length_G[node1][node2] = np.floor(shortest_length_G[node1][node2])
                            
    return shortest_length_G, shortest_path_G, shortest_length_G_with4H
                                
                
        