# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 00:24:22 2018

@author: MGGG
"""
import numpy as np

alpha = .2200507
beta = .44068679


def left_side(area, perimeter):
    first_term = - 1* np.log(area)
    second_term = (area - 1) * np.log( 4 * np.exp(-1 * alpha))
    third_term = (-1 * beta * perimeter* ( 1 - 1 / area))
    
    return first_term + second_term + third_term

def right_side(area, perimeter):
    first_term =  first_term = - 1* np.log(area)
    second_term = (area - 1) * np.log(4)
    PP = perimeter**2 / area
    third_term = ( -1 * alpha * ( area - PP ))
    return first_term + second_term + third_term

k = 2*3*5*7*11*13
n = k**2
area = n
divisors = [i for i in range(1, int(np.sqrt(n) + 1)) if n % i == 0]
for t in divisors:
    height = t
    width = n / t
    perimeter = 2 * ( height + width)
    print(perimeter)
    print(area)
    left_side_bound = left_side(area, perimeter)
    right_side_bound = right_side(area, perimeter)
    print( [left_side_bound, right_side_bound])