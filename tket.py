# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:00:23 2019

@author: zxz58
"""


import qiskit
import pytket

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

from pytket._qiskit.pytket.qiskit import dagcircuit_to_tk, coupling_to_arc

from pytket import Architecture, route
from pytket import OpType, Transform
import pandas
import time

filename = 'alu-v0_27_example.qasm'

ibm_devices = {
    "ibmqx5": {"edges": [(1, 0), (1, 2), (2, 3), (3, 4), 
    (3, 14), (5, 4), (6, 5), (6, 7), (6, 11), (7, 10), 
    (8, 7), (9, 8), (9, 10), (11, 10), (12, 5), (12, 11), 
    (12, 13), (13, 4), (13, 14), (15, 0), (15, 2), (15, 14)],
    "nodes": 16},
    "ibmq_20_tokyo": {"edges": [(0, 1), (0, 5), (1, 2), (1, 6), (1, 7), (2, 3), (2, 6),
    (2, 7), (3, 4), (3, 8), (3, 9), (4, 8), (4, 9), (5, 6), (5, 10), (5, 11), (6, 7),
    (6, 10), (6, 11), (7, 8), (7, 12), (7, 13), (8, 9), (8, 12), (8, 13), (9, 14), (10, 11),
    (10, 15), (11, 12), (11, 16), (11, 17), (12, 13), (12, 16), (12, 17), (13, 14), (13, 18),
    (13, 19), (14, 18), (14, 19), (15, 16), (16, 17), (17, 18), (18, 19)], "nodes": 20}
}
    
    
device_name = 'ibmqx5' #'ibm_20_tokyo' ###Note: can also be ran using the Tokyo machine architecture
                                       ###      or with a user-defined coupling map
coupling_map = ibm_devices[device_name]["edges"]
directed_arc = coupling_to_arc(coupling_map)


def getStats(filename, directed_arc):
    qc = QuantumCircuit.from_qasm_file(filename)
    dag = circuit_to_dag(qc)
    tkcirc = dagcircuit_to_tk(dag)
    start_time = time.process_time()
    Transform.OptimisePhaseGadgets().apply(tkcirc)
    outcirc = route(tkcirc, directed_arc)
    # decompose swaps to CX gates and redirect CXs in wrong direction
    outcirc.decompose_SWAP_to_CX()
    outcirc.redirect_CX_gates(directed_arc)
    Transform.OptimisePostRouting().apply(outcirc)
    
    time_elapsed = time.process_time() - start_time
    
    print("Compilation time for circuit " + str(filename) + ": " + str(time_elapsed) + "s")
    if outcirc.n_gates==0:
        return [0,0,0,0,0]
    ###Returns: [number of vertices, circuit depth, nubmer of CX gates, number of parallel slices of CX gates]
    return [outcirc.n_gates, outcirc.depth(), outcirc.n_gates_of_type(OpType.CX), 
            outcirc.depth_by_type(OpType.CX), time_elapsed]
    ###Note: the raw number of vertices in the circuits and the raw depth 
    ###      need to have the i/o vertices removed for fair comparisons
    
getStats('inputs/QASM example/' + filename, directed_arc)