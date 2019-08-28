# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 23:33:00 2019

@author: zxz58
"""

import circuittransform as ct
from qiskit import QuantumCircuit
from qiskit import QuantumRegister

# =============================================================================
# q = QuantumRegister(5, 'q')
# cir = QuantumCircuit(q)
# cir.cx(q[0], q[2])
# cir.cx(q[3], q[4])
# cir.cx(q[0], q[1])
# cir.cx(q[1], q[2])
# cir.cx(q[2], q[3])
# =============================================================================


# =============================================================================
# q = QuantumRegister(6, 'q1')
# cir = QuantumCircuit(q)
# for qq in range(len(q)-1):
#     cir.h(q[qq])
# cir.cx(q[0], q[2])
# cir.cx(q[0], q[1])
# cir.cx(q[0], q[4])
# cir.cx(q[0], q[3])
# cir.barrier()
# cir.swap(q[1], q[2])
# cir.swap(q[3], q[4])
# =============================================================================

q = QuantumRegister(4, 'q')
cir = QuantumCircuit(q)
# =============================================================================
# cir.cx(q[0], q[1])
# cir.barrier()
# cir.h(q[0])
# cir.h(q[1])
# cir.cx(q[1], q[0])
# cir.h(q[0])
# cir.h(q[1])
# cir.barrier()
# cir.swap(q[0], q[1])
# cir.barrier()
# cir.cx(q[0], q[1])
# cir.cx(q[1], q[0])
# cir.cx(q[0], q[1])
# cir.barrier()
# cir.cx(q[0], q[1])
# cir.h(q[0])
# cir.h(q[1])
# cir.cx(q[0], q[1])
# cir.h(q[0])
# cir.h(q[1])
# cir.cx(q[0], q[1])
# cir.barrier()
# =============================================================================
# =============================================================================
# cir.cx(q[1], q[0])
# cir.cx(q[0], q[1])
# cir.cx(q[1], q[0])
# =============================================================================
cir.cx(q[0], q[3])
cir.barrier()
ct.RemoteCNOTinArchitectureGraph([0,1,2,3], cir, q)

fig = (cir.draw(scale=0.7, filename=None, style=None, output='mpl', interactive=False, line_length=None, plot_barriers=True, reverse_bits=False))
fig.savefig('cir.svg', format='svg', papertype='a4')