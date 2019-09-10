# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 20:00:51 2019

@author: zxz58
"""

import threading
import time

def function(i):
    for j in range(6000000):
        pass  
    print ("function called by thread %i\n" % i)


threads = []

s1 = time.time()
for i in range(40):
    t = threading.Thread(target=function , args=(i, ))
    threads.append(t)
    t.start()
#    t.join()
e1 = time.time()

s2 = time.time()
for i in range(40):
    function(i)
e2 = time.time()

print('multi thread running time is %ss' %(e1-s1))
print('single thread running time is %ss' %(e2-s2))