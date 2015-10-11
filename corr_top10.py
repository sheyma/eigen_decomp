# -*- coding: utf-8 -*-
"""
top 10 percent of correlation matrices

"""
import numpy as np
import matplotlib.pyplot as pl 

        
N = 5
dN = 0.1
A = np.random.rand(N,N)
bins = np.arange(0, 1+dN, dN)
A = A.flatten()
pl.hist(A, bins)
x, xbins = np.histogram(A, bins)

x_length = x.shape[0]
back_sum = 0
x_sum = x.sum()
ten_percent = 0.10

for i in range(x_length-1, -1, -1):
    
    back_sum += x[i]/x_sum
    print i, x[i], back_sum, bins[i]    
    
    if back_sum >= ten_percent:
        threshold = bins[i]
        break

A_length = A.shape[0]
    
for i in range(0, A_length, 1):
    if A[i] >= threshold:
        A[i] = 1.0
    else:
        A[i] = 0
    

        

