# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 20:14:13 2018

@author: Temporary
"""
import numpy as np
import random
#This samples from rank B elements from a partition matroid with constraints d_i.
#Said more simply, we want to sample a total of B balls from I urns, subject to the contraint that we take no more than b_i balls from urn i.

#Essentially, this expands on the discussion here:
#https://stats.stackexchange.com/questions/184348/how-to-generate-samples-uniformly-at-random-from-multiple-discrete-variables-sub

#We first dynamically compute $P( n_I | B, b_{1:I})$.


#For a given tree, and given subforest of acceptable nodes, we should as much of this data as possible. Don't prematurely optimie though.

'''

PART I:
    
My natural numbers $\mathbb{N}$ include $0$. Also, $[i] = \{0, \ldots, i\}$.
Fix a constraint function $d : J \to \mathbb{N}$.
Definition: $F_{J,r}= \{ f : J \to \mathbb{N} | \sum_{j in J} f(j) = r, f(j) \leq d(j) \forall j \in J\}$

Facts: 
    
    1) $F_{[i],B} = \sum_{m = 0}^{d_i} \{ f \in F_{[i],B} | f(i) = m}$.
    2) $\{f \in F_{[i - 1], B - n} | f(i - 1) = k} \cong \{ f \in F_{[i],B} | f(i - 1) = k, f(i) = n\}$.
    3) From 1 and 2 follow that $F_{[i],B} \cong \bicup_{m = 0}^{d_i} F_{[i - 1], B - m}$.
    
Thus, we have the following recurrance:
    
(RECURRANCE) $|F_{[i],B}| = \sum_{m = 0}^{d_I} |F_{[i - 1], B - m}|$.

We also have :
    
a) $F_{[i], B} = 0$ if $\sum_{j \leq i} d(j) < B$.
b) $F_{ [0], B} = 1$ if $d(1) > B$.
    
From recurrance and a) and b), we can compute $|F_{[i],B}|$ by a dynamical programming algorithm.
    
The algorithm works as follows:
    
    
1) Initialize an array $F_{[i], r} = F[i,r]$ set to zeros.
2) Use $a$ and $b$ to compute the column where $i = 0$.
3) For i \in range(1,I):
    For r in range(B):
        add $|F_{[i], r}$ to the table using (RECURRANCE). Note that sometimes recurrance will call $|F_{[j], c}|$, where $c < 0$. This summand is always zero.
        
In the code below, $B$ is represented by $total_amount$, and $d$ by constraints.


PART II:

Now we use the data constructed in part I to compute the marginals. This is simple:
    
Here $P_{[i],B}$ refers to drawing a function uniformly from $F_{[i], B}4
    
Claim: $P_{[i],B}(f(i) = n ) = \frac{ |F_{[i - 1], B - n}| }{|F_{[i], B}|}$.
Proof: This follows easily from the observation that $\{ f \in F_{[i], B} | f(i) = n\} \cong \{ f \in F_{[i-1], B-n}}$.'

PART II:
    
Finally, we use part II to samplefrom the uniform distribution on $F_{I, B, d} \{ f : I \to \mathbb{N}| \sum_{i \in I} f(i) = B , f \leq d\}$.

To do this, we sample inductively backwards:
    
'''

    
    
def sampler(constraints, total_amount):
    '''Goal: To sample from $\{ f : I \to \mathbb{N}_{\geq 0} | \int f d\mu = total_amount, f(i) \leq constraints[i]}
    
    '''
    I = len(constraints)
    sample = []
    while len(sample) < I:
        sample_n = sample_last_index(constraints, total_amount)
        sample.append(sample_n)
        total_amount = total_amount - sample_n
        constraints.pop()
        
    sample.reverse()
    return sample
    
    
def sample_last_index(constraints, total_amount):
    '''
    
    Uses $P(f(I) = n)$ computations [prob_last_is_n] to sample the value of $f(I)$.
    '''
    
    '''how to sanity check this?'''
    
    size_list = make_size_list(constraints, total_amount)
    d_I = constraints[-1]
    probabilities = []
    for n in range(min(d_I, total_amount)+1):
        probabilities.append(prob_last_is_n(size_list, n))
    choices = np.arange(0, min(d_I, total_amount) + 1)
    if len(constraints) == 1:
        return total_amount
        #This is a hack I'm uncomfortable with; the edge case when we are down to the last one and must pick the remaining from it causes problems... TODO: sanity check this
    return random.choices(choices, probabilities)[0]
    
def prob_last_is_n(size_list, n):
    '''this computes the probability that f(I) = n'''
    
    
    '''sanity checked this against 
    constraints = [2,2,3]
total_amount = 2
size_list = make_size_list(constraints, total_amount)
for j in range(len(constraints)):
    print( prob_last_is_n(size_list, j))'''
    
    i= size_list.shape[0] - 1
    B = size_list.shape[1] -1
    num = size_list[i - 1, B - n] 
    den = size_list[i, B]
    return num / den
    
    
def make_size_list(constraints, total_amount):
    #To make indexing agree with the math, we pad with zeros
    #I debugged this on the example constraints = [2,2,3] and total_amount = 2
    I = len(constraints)
    M = np.zeros([I, total_amount + 1])
    for r in range(0, total_amount + 1):
        if constraints[0] >= r:
            M[0,r] = 1
    for i in range(1, I):
        for r in range(0, total_amount + 1):
            for k in range(constraints[i] + 1):
                if r >= k:
                    M[i,r] += M[i- 1,r - k]
    return M

def test():
    '''sanity check this against simple rejection sampling'''
    sampler([3,5,8,4,6,3],20)
