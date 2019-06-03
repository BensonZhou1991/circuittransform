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
E = ((1,0),(1,2),(2,3),(3,4),(3,8),(5,4),(6,5),(6,7),(7,4),(7,8),(9,0),\
     (9,2),(9,8))

H10=q10()
#H10=nx.Graph.to_undirected(H10)
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
    # this definition is different from undirected case
    # the returned value is 0 if the gate is solved by tau, 4 if its inverse is so
    p=gate[0]
    q=gate[1]
    taui=inv(tau)
    if (taui[p],taui[q]) in H10.edges():
        return 0    
    elif (taui[q],taui[p]) in H10.edges():
        return 4
    else:
        return 100

def dist(tau,gate):
    p=gate[0]
    q=gate[1]
    taui=inv(tau)
    s=nx.shortest_path_length(H10,source=taui[p],target=taui[q])
    return s

#transform tau to tau' with the images of tau[p] and tau[q] swapped
def swap(tau,i,j):
    if (i,j) not in H10.edges():
        return tau
    else:
        taunew=tau[:]
        taunew[i]=tau[j]
        taunew[j]=tau[i]
        return taunew

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# SWAP1 returns all mappings close (dist=1) to tau
def SWAP1(tau):
    SWAP1=[]
    for s1 in H10.edges():
        i=s1[0]
        j=s1[1]
        tau1=swap(tau,i,j)
        x1=[[s1],tau1]
        if x1 not in SWAP1:
            SWAP1.append(x1)

    return SWAP1
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# SWAP2 returns all mappings close (dist=2) to tau
def SWAP2(tau):
    SWAP2=[]
    t1=SWAP1(tau)
    for s1 in H10.edges():
        i=s1[0]
        j=s1[1]
        tau1=swap(tau,i,j)
        for s2 in H10.edges():
            if s2==s1:
                continue
            i=s2[0]
            j=s2[1]
            tau2=swap(tau1,i,j)
            x2=[[s1,s2],tau2]
            if (x2 not in t1) and (x2 not in SWAP2):
                SWAP2.append(x2)

    return SWAP2
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# SWAP3 returns all mappings close (dist≤3) to tau
def SWAP3(tau):
    SWAP3=[]
    t1=SWAP1(tau)
    t2=SWAP2(tau)
    for s1 in H10.edges():
        i=s1[0]
        j=s1[1]
        tau1=swap(tau,i,j)
        for s2 in H10.edges():
            if s2==s1:
                continue
            i=s2[0]
            j=s2[1]
            tau2=swap(tau1,i,j)
            for s3 in H10.edges():
                if s3==s1 or s3==s2:
                    continue
                i=s3[0]
                j=s3[1]
                tau3=swap(tau2,i,j)
                x3=[[s1,s2,s3],tau3]
                if (x3 not in t1) and (x3 not in t2)\
                   and (x3 not in SWAP3):
                    SWAP3.append(x3)

    return SWAP3

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# SWAP4 returns all mappings close (dist≤3) to tau
def SWAP4(tau):
    SWAP4=[]
##    t1=SWAP1(tau)
##    t2=SWAP2(tau)
##    t3=SWAP3(tau)
    for s1 in H10.edges():
        i=s1[0]
        j=s1[1]
        tau1=swap(tau,i,j)
        x1=[[s1],tau1]
        if x1 not in SWAP4:
            SWAP4.append(x1)
        for s2 in H10.edges():
            if s2==s1:
                continue
            i=s2[0]
            j=s2[1]
            tau2=swap(tau1,i,j)
            x2=[[s1,s2],tau2]
            if x2 not in SWAP4:
                SWAP4.append(x2)
            for s3 in H10.edges():
                if s3==s1 or s3==s2:
                    continue
                i=s3[0]
                j=s3[1]
                tau3=swap(tau2,i,j)
                x3=[[s1,s2,s3],tau3]
                if x3 not in SWAP4:
                    SWAP4.append(x3)
                for s4 in H10.edges():
                    if s4==s1 or s4==s2 or s4==s3:
                        continue
                    i=s4[0]
                    j=s4[1]
                    tau4=swap(tau3,i,j)
                    x4=[[s1,s2,s3,s4],tau4]
                    if x4 not in SWAP4:
##                    if (x4 not in t1) and (x4 not in t2)\
##                       and (x4 not in t3) and (x4 not in SWAP4):
                        SWAP4.append(x4)

##                    for s5 in H10.edges():
##                        if s5==s1 or s5==s2 or s5==s3 or s5==s4:
##                            continue
##                        i=s5[0]
##                        j=s5[1]
##                        tau5=swap(tau4,i,j)
##                        x5=[[s1,s2,s3,s4,s5],tau5]
##                        if x5 not in SWAP4:
##                            SWAP4.append(x5)



    return SWAP4
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
print(time.asctime())

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
##C = [(0, 1), (0, 1), (0, 2), (0, 2), (1, 2), (0, 3), (1, 2), (0, 3), (1, 3), (0, 4), (1, 3),\
##     (0, 4), (2, 3), (1, 4), (0, 5), (2, 3), (1, 4), (0, 5), (2, 4), (1, 5), (0, 6), (2, 4),\
##     (1, 5), (0, 6), (3, 4), (2, 5), (1, 6), (0, 7), (3, 4), (2, 5), (1, 6), (0, 7), (3, 5),\
##     (2, 6), (1, 7), (0, 8), (3, 5), (2, 6), (1, 7), (0, 8), (4, 5), (3, 6), (2, 7), (1, 8),\
##     (0, 9), (4, 5), (3, 6), (2, 7), (1, 8), (0, 9), (4, 6), (3, 7), (2, 8), (1, 9), (4, 6),\
##     (3, 7), (2, 8), (1, 9), (5, 6), (4, 7), (3, 8), (2, 9), (5, 6), (4, 7), (3, 8), (2, 9),\
##     (5, 7), (4, 8), (3, 9), (5, 7), (4, 8), (3, 9), (6, 7), (5, 8), (4, 9), (6, 7), (5, 8),\
##     (4, 9), (6, 8), (5, 9), (6, 8), (5, 9), (7, 8), (6, 9), (7, 8), (6, 9), (7, 9), (7, 9),\
##     (8, 9), (8, 9)]

#Open the circuit C
#with open('sys6.txt', 'r') as f: # 98 gates #results: 520+215 vs. 613
with open('ising.txt', 'r') as f: # 90 gates #results: 0+? 

#with open('max46.txt', 'r') as f:
#with open('sqn_list.txt', 'r') as f: # 90 gates #results: 287+200 vs. 447
    sqn = json.loads(f.read())
C=sqn
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
    # compared with undirected case, we introduced a cost output V, denoting the additional cost when entailing inverse gates
    L1=L[:] # the gates remaning to be solved
    CHANGE = True
#    B=[] # gates solved by mapping t
    T=[]
    V=-1
    while CHANGE==True:
        # as long as there are gates that can be solved by this mapping
        X=topgates(L1)
        lx=len(X)
        for i in X:
            e=C[i]
            v=entail(t,e)
            if v<100:
#                B.append(i)
                L1.remove(i)
                X.remove(i)
                if e not in T:
                    V=max(v,V+v) # in case v=0, V=-1, new V is 0
                T.append(e)                    
                                    
        if len(X)==lx: # t does not solve any top gate
            CHANGE = False

    return [T,L1,V]

#    B1=B[:]
#    T=list(C[j] for j in B1)   # solved gates         
    return [T,L1,V]
    # if the returned value V is -1, then no edge is entailed by t
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

np=0 # number of rounds
ACTION=[] # the list of actions we take to solve all gates in C
A = [] # the list of solved top gates

# rho in SWAP3(taux) has form [[s1,...],tau], where tau is a mapping, s1,... is a sequence of swaps
SG=[]
for rho in SWAP4(taux):
    x=solved_gates(rho[1],L,C)
    if x[0]==[]:
        continue
    t=len(x[0])/(7*len(rho[0])+x[2])
    SG.append([rho,t])

if SG==[]:
    s=random.choice(E)
    i=s[0]
    j=s[1]
    taux=swap(taux,i,j)
    path=[s]
##if SG==[]:
##    for rho in SWAP2(taux):
##        x=solved_gates(rho[1],L,C)
##        if x[0]==[]:
##            continue
##        t=len(x[0])/(14+x[2])
##        SG.append([rho,t])
##        
##if SG==[]:
##    for rho in SWAP3(taux):
##        x=solved_gates(rho[1],L,C)
##        if x[0]==[]:
##            continue
##        t=len(x[0])/(21+x[2])
##        SG.append([rho,t])
##        
##if SG==[]:
##    for rho in SWAP4(taux):
##        x=solved_gates(rho[1],L,C)
##        if x[0]==[]:
##            continue
##        t=len(x[0])/(28+x[2])
##        SG.append([rho,t])
        
##        else:
##            SG.sort(key=lambda t: t[1], reverse=True)
##    else:
##        SG.sort(key=lambda t: t[1], reverse=True)
##else:

SG.sort(key=lambda t: t[1], reverse=True)

sg=SG[0]
val=sg[1]
XT=solved_gates(taux,L,C)
if (XT[2]==-1 and val>0) or (XT[2]>0 and len(XT[0])/XT[2] < val):
    taux=sg[0][1]


XX=solved_gates(taux,L,C)
sgate=XX[0]
L1=XX[1]
#A = XX[2]
cost=XX[2]
#print(cost,taux)
COST=cost
#COST=0
print('This round has cost %s' %COST)
print('The initial mapping is %s' %tau)
print('Round 0: The gates solved are %s' %sgate)

while L1!=[]:
    np=np+1
    tau=taux[:]
    L0 = L1[:]
    SG=[]
    for rho in SWAP4(taux):
        x=solved_gates(rho[1],L1,C)
        if x[0]==[]:
            continue
        t=len(x[0])/(7*len(rho[0])+x[2])
        SG.append([rho,t])

##    if SG==[]:
##        for rho in SWAP2(taux):
##            x=solved_gates(rho[1],L1,C)
##            if x[0]==[]:
##                continue
##            t=len(x[0])/(14+x[2])
##            SG.append([rho,t])
##
##    if SG==[]:
##        for rho in SWAP3(taux):
##            x=solved_gates(rho[1],L1,C)
##            if x[0]==[]:
##                continue
##            t=len(x[0])/(21+x[2])
##            SG.append([rho,t])
##
##    if SG==[]:
##        for rho in SWAP4(taux):
##            x=solved_gates(rho[1],L1,C)
##            if x[0]==[]:
##                continue
##            t=len(x[0])/(28+x[2])
##            SG.append([rho,t])

##            else:
##                SG.sort(key=lambda t: t[1], reverse=True)
##        else:
##            SG.sort(key=lambda t: t[1], reverse=True)
##    else:
##        SG.sort(key=lambda t: t[1], reverse=True)
    if SG==[]:
        s=random.choice(E)
        i=s[0]
        j=s[1]
        taux=swap(taux,i,j)
        path=[s]
    else:       
        SG.sort(key=lambda t: t[1], reverse=True)
        sg=SG[0]
        val=sg[1]
#        XT=solved_gates(taux,L,C)
#        if (XT[3]==-1 and val>0) or (XT[3]>0 and len(XT[0])/XT[3] < val):

##    for rho in SWAP3(taux):
##        x=solved_gates(rho[1],L1,C)
##        t=len(x[0])/(7*len(rho[0])+x[3])
##        SG.append([rho,t])    
        rhox=sg[0] # select the first item
        taux=rhox[1]
        path=rhox[0]
#        print(taux,path)
##    else: # (XT[3]==-1 and val==0) or (XT[3]>0 and len(XT[0])/XT[3] >= val)
##        s=random.choice(E)
###        print(s)
##        i=s[0]
##        j=s[1]
##        taux=swap(taux,i,j)
##        path=[s]

    XX=solved_gates(taux,L1,C)
    # if we call this function twice or more, Ax will output as []???
    sgate=XX[0]
    L1=XX[1]
#    Ax=XX[2]
    cost=7*len(path)+max(XX[2],0) # we add at least one swap operation
    print('Round %s: The cost of this round is %s' %(np,cost))
    COST = COST + cost
    print('The mapping is %s and the actions are: %s' %(taux,path))
    print('The gates solved are %s' %sgate)

print('The cost is the number of additional gates introduced.')
print("The number of additional gates introduced are %s" %COST)

print(time.asctime())
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
end = time.time()
print('It takes time: %s seconds.' %(end-start))
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
