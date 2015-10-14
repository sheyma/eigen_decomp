# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 13:45:04 2015
More important is that we will safe 1/3 memory. For example corrcoef()
for a [23k, m] matrix needs 8GB now instead of 12GB.
@author: bayrak
"""
import warnings
import sys
import os
import numpy as np
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

from memory_profiler import profile
from memory_profiler import memory_usage

import corr_faster
import corr_full

N = sys.argv[1]


A = np.random.rand(int(N), 4800)
#B = np.corrcoef(A)
B = corr_faster.corrcoef_upper(A)
#
#
#from scipy.linalg import get_blas_funcs
#
#def cool_syrk(fact, X):
#    syrk = get_blas_funcs("syrk", [X])
#    R = syrk(fact, X)
#
#    d = np.diag(R).copy()
#    size = mat_to_upper_F(R)
#    R.resize([size,])
#    return R,d
#
#def my_cov(m):
#
#    # Handles complex arrays too
#    m = np.asarray(m)
#    dtype = np.result_type(m, np.float64)
#    X = np.array(m, ndmin=2, dtype=dtype)
#    N = X.shape[1]
#
#    fact = float(N - 1)
#    if fact <= 0:
#        warnings.warn("Degrees of freedom <= 0 for slice", RuntimeWarning)
#        fact = 0.0
#
#    X -= X.mean(axis=1, keepdims=True)
#
#
#    # This returns np.dot(X, X.T) / fact
#    return cool_syrk(1.0/fact, X)
#
## This is corrcoef from numpy 1.9.2 ... mem usage optimized
#def corrcoef_up(x):
#    c, d = my_cov(x)
#
#    d = np.sqrt(d)
#
#    # calculate "c / multiply.outer(d, d)" row-wise to ... for memory and speed
#    k = 0
#    for i in range(0, d.size - 1):
#        len = d.size - i - 1
#        c[k:k + len] /= (d[-len:] * d[i])
#        k += len
#
#    return c
#
#def mat_to_upper_F(A):
#    if not A.flags['F_CONTIGUOUS']:
#        raise Exception("F_CONTIGUOUS required")
#    n = A.shape[0]
#    size = (n - 1) * n / 2
#    U = A.reshape([1,n*n], order='F')
#    k = 0
#    for i in range(0, n-1):
#        len = n - 1 - i
#        U[0,k:k+len] = A[i,i+1:n]
#        k += len
#    return size
#
##
#B = corrcoef_up(A)



