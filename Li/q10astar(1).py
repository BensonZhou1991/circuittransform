# Created on June 4, 2019 by Sanjiang Li mrlisj@gmail.com
## designed for checking how a 10-bit circuit can be efficiently implemented in IBM QX5

import networkx as nx
import heapq as hq
import json
##import random
import time

#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
start = time.time()
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

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
G10=nx.Graph.to_undirected(H10)
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

# tau is a mapping from 10 physical qubits in H10 to logic qubits in the circuit
# tau[i] is the logical qubit associated with the i-th physical qubit in H10

tau=list(range(10))

# the inverse mapping
taui=list(range(10))
# define the inverse mapping of tau

def inv(tau):
    K=list([i,tau[i]] for i in range(10))
    K.sort(key=lambda t: t[1])
    taui=list(K[i][0] for i in range(10))
    return taui

gate=[0]*2
# the vlaue that a gate is satisfied or entailed by tau
def entail(tau,gate):
    # the returned value is 0 if the gate is solved by tau, 4 if its inverse is so
    p=gate[0] # p is a logic qubit
    q=gate[1] # q is a logic qubit
    taui=inv(tau) # the inverse of tau
    if (taui[p],taui[q]) in H10.edges():
        return 0    
    elif (taui[q],taui[p]) in H10.edges():
        return 4
    else:
        return 100

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
# topgatges gives the indices of the gates in the first layer of a circuit

l=0
C=[(0,0)]*l
L0=list(range(l))
def topgates(L0):
    # return the indices of the gates in the *first* layer of C
    T=[]
    N=set()
    for i in L0:
        p=C[i][0]
        q=C[i][1]
        if N=={0,1,2,3,4,5,6,7,8,9,}:
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

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# function max_dist returns the maximum distance of a layer TG (topgates) given a mapping tau

    #one question is how do we know if any optimal transformation must
    #   move edges that involve qubits of some topgate?
    #   for example, suppose tau[0]=q0 and tau[6]=q1, then we should move q0 and q1 next to each other
    #   some swap (represented as an edge in H10) not incident to Q0 or Q6 will be used

tau=list(range(10)) # an initial mapping
tg=0 # the number of topgates
TG=[[0,0]]*tg # topgates (not their indices)
def max_dist(tau,TG):
    md=0
    MD=[]
    taui=inv(tau)
    for e in TG: # e=(x,y) is a gate in TG, where x, y are logic qubits
        p=taui[e[0]] # the physical qubit corresponds to e[0]
        q=taui[e[1]]
        d=nx.shortest_path_length(G10,p,q)
        if md >= d:
            continue
        md=d
        path=nx.shortest_path(G10,p,q)
        e0=e
    for e in TG:
        p=taui[e[0]]
        q=taui[e[1]]
        d=nx.shortest_path_length(G10,p,q)
        if d==md:
            path=nx.shortest_path(G10,p,q)
            MD.append([e,path])

    for t in MD:
        e=t[0]
        path=t[1]
        same_direction=False
        for i in range(len(path)-1):
            if (path[i],path[i+1]) in H10.edges():
                same_direction=True
                break
        if same_direction==False:
            return md*7+4           
    return md*7
        
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# function f_val defines the f value of a state specified by (tau, sequence of swaps, a layer of gates)

tau=list(range(10)) # a mapping
S=[] # sequence of swaps
def f_val(tau,S,TG):
    # f=g+h: estimated cost from taunew to goal and real cost from tau to taunew

    taunew=tau[:]
    ls=len(S)
    for s in S:
        taunew=swap(taunew,s[0],s[1])

    # taunew is the mapping obtained by swapping gates in S from tau
    m=max_dist(taunew,TG) # the heuristic value g of the current mapping taunew

    return ls*7+m

###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

def solve_topgates(tau,TG):
    
    HP=[(max_dist(tau,TG),tau,[])]
    # the initial root node of the heap, with form (f_value, a mapping, seq. swaps)
    cmp_node=[] # a complete node: a seq is *complete* if its induced mapping solves all gates in TG
                    # we could keep all complete nodes, but here I only keep one
    cmp_val=1000 # an upper bound of the f_value of any complete node
    
    while HP!=[]:
        ntop=hq.heappop(HP) # popout the top node and check if it is complete
        fval=ntop[0]

        if fval>cmp_val:
            # ntop cannot be a complete node and, since it is the top node, no other node can be complete
            break
        
        taux=ntop[1]
        S=ntop[2] # seq. swaps from tau to taux

        # Check if ntop is complete by checking if taux entails all gates in TG
        entail_all=False 
        V=7*len(S) # if ntop is complete, its f_val is at least V
        for g in TG:
            v=entail(taux,g)
            if v>4: # that is, taux does not entail g
                entail_all=False
                break
            V=V+v
            entail_all=True

        if V>cmp_val: # this will not lead to an optimal solution
            continue

        # if not a complete node then we expand ntop and consider the next node in HP
        elif entail_all==False:

            # Expand the top node ntop
            for e in H10.edges():
                # if the same swap appeared before, this seems not optimal, but need check
#                if e in S:
#                    continue
                taunew=swap(taux,e[0],e[1])
                S1=S[:]
                S1.append(e)
#                S2=S1[:]
                f_new=f_val(tau,S1,TG)
                if f_new>cmp_val:
                    continue
                hq.heappush(HP,(f_new,taunew,S1))
                
        # if yes and the value is better than the current best one, then update the cmp_node
        else:
            cmp_val=V
            tau1=taux[:]
            cmp_node=[tau1,S]
            
    if cmp_val==1000:
        print('ha')
    return (cmp_val,tau1,S)


###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
## The circuit

#qft_10 # 90 gates #results: 383+200 (if use q10) / 466+200 (if use q16) vs. 447
                    #results: +346 (astar) +385 (lookahead)
C = [(0, 1), (0, 1),(0, 2), (0, 2), (1, 2), (0, 3), (1, 2), (0, 3), (1, 3), (0, 4), (1, 3),\
     (0, 4), (2, 3), (1, 4), (0, 5), (2, 3), (1, 4), (0, 5), (2, 4), (1, 5), (0, 6), (2, 4),\
     (1, 5), (0, 6), (3, 4), (2, 5), (1, 6), (0, 7), (3, 4), (2, 5), (1, 6), (0, 7), (3, 5),\
     (2, 6), (1, 7), (0, 8), (3, 5), (2, 6), (1, 7), (0, 8), (4, 5), (3, 6), (2, 7), (1, 8),\
     (0, 9), (4, 5), (3, 6), (2, 7), (1, 8), (0, 9), (4, 6), (3, 7), (2, 8), (1, 9), (4, 6),\
     (3, 7), (2, 8), (1, 9), (5, 6), (4, 7), (3, 8), (2, 9), (5, 6), (4, 7), (3, 8), (2, 9),\
     (5, 7), (4, 8), (3, 9), (5, 7), (4, 8), (3, 9), (6, 7), (5, 8), (4, 9), (6, 7), (5, 8),\
     (4, 9), (6, 8), (5, 9), (6, 8), (5, 9), (7, 8), (6, 9), (7, 8), (6, 9), (7, 9), (7, 9),\
     (8, 9), (8, 9)]


###Open the circuit C
#with open('sys6.txt', 'r') as f:
    # 98 gates #results: 566/577+215 +693 (astar) +580-28(first round swap cost) (lookahead) vs. 613

#with open('ising.txt', 'r') as f:
    # 90 gates #results: 160+ (astar, lookahead)
##with open('max46.txt', 'r') as f: # 11844 gates # results: +97643 (1682.6s) +69592(greedy) (1542.9s)
#with open('sqn_list.txt', 'r') as f:
#    # 4459 C-Not gates # results: +32011 (astar) +25587 (lookahead)
#    sqn = json.loads(f.read())
#C=sqn

##\__/#\__/#\#/~\MAIN ALGORITH10M\__/#\__/#\#/~\
# The main algorithm
print(time.asctime())

l=len(C)
L = list(range(l)) # the indices of gates in C
print('The circuit has %s gates.' %l)
##print('D has form (cost, mapping, sequence of swaps)')

L1=L[:]
COST=0 # the total cost

tau=list(range(10)) # a mapping
taunew=tau[:]
np=0

while L1!=[]:
    np=np+1
    TG= list(C[i] for i in topgates(L1))
    taux=taunew[:]
    

    # D shows how do we solve the topgates in this round 
    D=solve_topgates(taux,TG) 

    cost=D[0]
    COST=COST+cost
    taunew=D[1] # the new mapping
    actions=D[2]

    print('Round %s: the new mapping %s is obtained by enforcing swaps in %s' %(np,taunew, actions))
    print('The gates solved are in %s and the cost is %s' %(TG,cost))

    for i in topgates(L1):
        L1.remove(i)
        
print('The number of additional gates introduced is %s' %COST)
    
#print(time.asctime())
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
end = time.time()
print('It takes time: %s seconds.' %(end-start))
#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
