# Created on May 30, 2019 by Sanjiang Li mrlisj@gmail.com
## designed for checking how a 10-bit circuit can be efficiently implemented in IBM QX3 (the first 6 qubits)

import networkx as nx
import json
import random
import time

#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
start = time.time()
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# IBM QX3 (the first part: 10 qubits)
##def q10():
##    g = nx.DiGraph()
##    g.add_nodes_from([0,9])
##    g.add_edge(0,1)
##    g.add_edge(1,2)
##    g.add_edge(2,3)
##    g.add_edge(3,8)
##    g.add_edge(4,3)
##    g.add_edge(4,5)
##    g.add_edge(6,5)
##    g.add_edge(6,7)
##    g.add_edge(7,4)
##    g.add_edge(7,8)
##    g.add_edge(9,0)
##    g.add_edge(9,8)
##    return g

# IBM QX5 (the first part: 10 qubits)
def q10():
    g = nx.DiGraph()
    g.add_nodes_from([0,9])
    g.add_edge(1,0)
    g.add_edge(1,2)
    g.add_edge(2,3)
    g.add_edge(3,4)
    g.add_edge(3,8)
    g.add_edge(5,4)
    g.add_edge(6,5)
    g.add_edge(6,7)
    g.add_edge(7,4)
    g.add_edge(7,8)
    g.add_edge(9,0)
    g.add_edge(9,2)
    g.add_edge(9,8)
    return g
E = ((1,0),(1,2),(2,3),(3,4),(3,8),(5,4),(6,5),(6,7),(7,4),(7,8),(9,0),(9,2),(9,8))

H10=q10()
G10=nx.Graph.to_undirected(H10)
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
tau=list(range(10))
taui=list(range(10))
def inv(tau):
    K=list([i,tau[i]] for i in range(10))
    K.sort(key=lambda t: t[1])
    taui=list(K[i][0] for i in range(10))
    return taui

gate=[0]*2
def entail(tau,gate):
    p=gate[0]
    q=gate[1]
    taui=inv(tau)
    if (taui[p],taui[q]) in G10.edges():
        return True
    else:
        return False

def dist(tau,gate):
    p=gate[0]
    q=gate[1]
    taui=inv(tau)
    s=nx.shortest_path_length(G10,source=taui[p],target=taui[q])
    return s

#transform tau to tau' with the images of tau[p] and tau[q] swapped
def swap(tau,i,j):
    if (i,j) not in G10.edges():
        return tau
    else:
        taunew=tau[:]
        taunew[i]=tau[j]
        taunew[j]=tau[i]
        return taunew
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

def SWAP3(tau):
    SWAP3=[]
    for s1 in G10.edges():
        i=s1[0]
        j=s1[1]
        tau1=swap(tau,i,j)
        x1=[[s1],tau1]
        if x1 not in SWAP3:
            SWAP3.append(x1)
        for s2 in G10.edges():
            if s2==s1:
                continue
            i=s2[0]
            j=s2[1]
            tau2=swap(tau1,i,j)
            x2=[[s1,s2],tau2]
            if x2 not in SWAP3:
                SWAP3.append(x2)

            for s3 in G10.edges():
                if s3==s1 or s3==s2:
                    continue
                i=s3[0]
                j=s3[1]
                tau3=swap(tau2,i,j)
                x3=[[s1,s2,s3],tau3]
                if x3 not in SWAP3:
                    SWAP3.append(x3)
    return SWAP3
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\


l=0
C=[(0,0)]*l
L=list(range(l))
L0=L[:]
def topgates(L0):
    T=[]
    N=set()
    for i in L0:
        p=C[i][0]
        q=C[i][1]
        if N=={0,1,2,3,4,5,6,7,8,9}:
            return T

        if p in N or q in N:
            N.add(p)
            N.add(q)
            continue
        else: 
            N.add(p)
            N.add(q)
            T.append(i)
    return T
            

##\__/#\__/#\#/~\MAIN ALGORITH10M\__/#\__/#\#/~\
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

#qft_10
'''
C = [(0, 1), (0, 1), (0, 2), (0, 2), (1, 2), (0, 3), (1, 2), (0, 3), (1, 3), (0, 4), (1, 3),\
     (0, 4), (2, 3), (1, 4), (0, 5), (2, 3), (1, 4), (0, 5), (2, 4), (1, 5), (0, 6), (2, 4),\
     (1, 5), (0, 6), (3, 4), (2, 5), (1, 6), (0, 7), (3, 4), (2, 5), (1, 6), (0, 7), (3, 5),\
     (2, 6), (1, 7), (0, 8), (3, 5), (2, 6), (1, 7), (0, 8), (4, 5), (3, 6), (2, 7), (1, 8),\
     (0, 9), (4, 5), (3, 6), (2, 7), (1, 8), (0, 9), (4, 6), (3, 7), (2, 8), (1, 9), (4, 6),\
     (3, 7), (2, 8), (1, 9), (5, 6), (4, 7), (3, 8), (2, 9), (5, 6), (4, 7), (3, 8), (2, 9),\
     (5, 7), (4, 8), (3, 9), (5, 7), (4, 8), (3, 9), (6, 7), (5, 8), (4, 9), (6, 7), (5, 8),\
     (4, 9), (6, 8), (5, 9), (6, 8), (5, 9), (7, 8), (6, 9), (7, 8), (6, 9), (7, 9), (7, 9),\
     (8, 9), (8, 9)]
'''

C = [(1, 4), (2 ,5), (1,3)]

###Open the circuit C
##with open('sqn_list.txt', 'r') as f:
##    sqn = json.loads(f.read())
##C=sqn
l=len(C)
L = list(range(l))
print('The circuit has %s gates.' %l)
#print(C[0:100])
L1 = L[:] # the gates remaining to be solved
taux=list(range(10))
# the initial mapping

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
def solved_gates(t,L,C):
    #t is a mapping, L the indexes of unsolved gates, C the given input circuit
    L1=L[:] # the gates remaning to be solved
    CHANGE = True
    B=[] # gates solved by mapping t
    while CHANGE==True:
        # as long as there are gates that can be solved by this mapping
        X=topgates(L1)
        lx=len(X)
        for i in X:
            e=C[i]
            if entail(t,e):
                B.append(i)
                L1.remove(i)
                X.remove(i)
        if len(X)==lx: # t does not solve any top gate
            CHANGE = False

    B1=B[:]
    T=list(C[j] for j in B1)           
    return [T,L1,B1]    
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

np=0 # number of rounds
##C0=C[:] # ?
ACTION=[] # the list of actions we take to solve all gates in C
##mx=0
A = [] # the list of solved top gates

# rho in SWAP3(taux) has form [[s1,...],tau], where tau is a mapping, s1,... is a sequence of swaps
SG=list([rho,len(solved_gates(rho[1],L,C)[0])/len(rho[0])] for rho in SWAP3(taux))
SG.sort(key=lambda t: t[1], reverse=True)

val=SG[0][1]
if len(solved_gates(taux,L,C)[0])<val:
    taux=SG[0][0][1]

sgate=solved_gates(taux,L,C)[0]
L1=solved_gates(taux,L,C)[1]
A = solved_gates(taux,L,C)[2]

print(A)
print('The initial mapping is %s' %tau)
print('Round 0: The gates solved are %s' %sgate)

while L1!=[]:
    np=np+1
    tau=taux[:]
    L0 = L1[:]
    SG=list([rho,len(solved_gates(rho[1],L1,C)[0])/len(rho[0])] for rho in SWAP3(taux))
    SG.sort(key=lambda t: t[1], reverse=True)
    val=SG[0][1]
    if len(solved_gates(taux,L1,C)[0])<val:
        rhox=SG[0][0]
        taux=rhox[1]
        path=rhox[0]
    else:
        s=random.choice(E)
        i=s[0]
        j=s[1]
        taux=swap(taux,i,j)
        path=[s]
        print(s)
    XX=solved_gates(taux,L1,C)
    # if we call this function twice or more, Ax will output as []???
    sgate=XX[0]
    L1=XX[1]
    Ax=XX[2]
    ACTION = ACTION + path
    print('Round %s: mapping %s actions: %s' %(np,taux,path))
    print('Round %s: gates solved are %s' %(np,sgate))

print("The number of swap actions are %s" %len(ACTION))

#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
end = time.time()
print('It takes time: %s seconds.' %(end-start))
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
