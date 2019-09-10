# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 20:35:16 2019

@author: zxz58
"""

import math
from random import random
from scoop import futures
from time import time


def evaluate_number_of_points_in_unit_circle(attempts):
  points_fallen_in_unit_disk = 0
  for i in range (0,attempts) :
       x = random()
       y = random()
       radius = math.sqrt(x*x + y*y)
       #the test is ok if the point fall in the unit circle
       if radius < 1 :
           #if ok the number of points in a disk is increased
           points_fallen_in_unit_disk = \
                   points_fallen_in_unit_disk + 1
  return points_fallen_in_unit_disk

def pi_calculus_with_Montecarlo_Method(workers, attempts):
     print("number of workers %i - number of attempts %i" %(workers,attempts))
     bt = time()
     #in this point we call scoop.futures.map function
     #the evaluate_number_of_points_in_unit_circle \
     #function is executed in an asynchronously way
     #and several call this function can be made concurrently
     evaluate_task = futures.map(evaluate_number_of_points_in_unit_circle,
                        [attempts] * workers)
     taskresult= sum(evaluate_task)
     print ("%i points fallen in a unit disk after " \
            %(taskresult/attempts))
     piValue = (4. * taskresult/ float(workers * attempts))
     computationalTime = time() - bt
     print("value of pi = " + str(piValue))
     print ("error percentage = " + \
            str((((abs(piValue - math.pi)) * 100) / math.pi)))
     print("total time: " + str(computationalTime))

def pi_calculus_with_Montecarlo_Method2(workers, attempts):
     print('single thread')
     bt = time()
     #in this point we call scoop.futures.map function
     #the evaluate_number_of_points_in_unit_circle \
     #function is executed in an asynchronously way
     #and several call this function can be made concurrently
     evaluate_task = map(evaluate_number_of_points_in_unit_circle,
                        [attempts] * workers)
     taskresult= sum(evaluate_task)
     print ("%i points fallen in a unit disk after " \
            %(taskresult/attempts))
     piValue = (4. * taskresult/ float(workers * attempts))
     computationalTime = time() - bt
     print("value of pi = " + str(piValue))
     print ("error percentage = " + \
            str((((abs(piValue - math.pi)) * 100) / math.pi)))
     print("total time: " + str(computationalTime))

if __name__ == "__main__":
#   for i in range (1,100):
      # let's fix the numbers of workers...only two,
      # but it could be much greater
      pi_calculus_with_Montecarlo_Method(8, 1000000)
      pi_calculus_with_Montecarlo_Method2(8, 1000000)
      print(" ")