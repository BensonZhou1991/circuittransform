# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:36:58 2019

@author: zxz58
"""

import numpy as np
import time
from numba import vectorize
from numba import jit, cuda

@vectorize(['float32(float32, float32)'], target='cuda')
def Add(a, b):
  return a + b

@vectorize(['float32(float32, float32)'], target='cpu')
def Add2(a, b):
  return a + b


@cuda.jit
def add_kernel(x, y, out):
    start = cuda.grid(1)      # 1 = one dimensional thread grid, returns a single value
    stride = cuda.gridsize(1) # ditto

    # assuming x and y inputs are same length
    for i in range(start, x.shape[0], stride):
        out[i] = x[i] + y[i]

# =============================================================================
# @jit(nopython=True)
# def cannot_compile(x):
#     return x['key']
# =============================================================================

# Initialize arrays
N = 100000
A = np.arange(N).astype(np.float32)
B = 2 * A
C = np.empty_like(A, dtype=A.dtype)
a = np.array(['1', '2'])
b = np.array(['a', 'b'])
a = np.empty_like(a, dtype=a.dtype)


# Add arrays on GPU
start = time.time()
C = Add(A, B)
end = time.time()

start2 = time.time()
C = Add2(A, B)
end2 = time.time()

# Add via kernel
threads_per_block = 128
blocks_per_grid = 30


add_kernel[blocks_per_grid, threads_per_block](A, B, C)
print(C[:10])

print('time consumption for GPU is %ss' %(end-start))
print('time consumption for CPU is %ss' %(end2-start2))


