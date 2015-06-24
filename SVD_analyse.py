#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pylab import *
import scipy
from scipy.sparse import linalg
from scipy import sparse, linalg
import psutil, os
from memory_profiler import memory_usage
import pylab as pl

print "python version: ", sys.version[0:5]
print "scipy version: ", scipy.__version__
print "psutil version: ", psutil.__version__

# singular value decomposition (SVD) of a matrix A (MxN)
# if the input matrix is dense
# if all singular values are required

def random_matrix(M, N):
    return np.random.randn(M, N)  # + 1.j*np.random.randn(M,N)

def simple_svd(A):
    # try with full_matrices = True
    U, s, Vh = linalg.svd(A, full_matrices=True, compute_uv=True)
    M, N = np.shape(A)
    S = np.zeros((M, N), dtype=complex)
    S[:N, :N] = np.diag(s)
    A_check = np.dot(np.dot(U, S), Vh)
    # check if SVD-resulting matrix is accurate enough
    for i in range(0, M):
        for j in range(0, N):
            try:
                abs(A[i, j] - A_check[i, j]) < 1.0e-14
            except ValueError:
                print "Oops! A and A_check are not accurately close to each other."
    return U, S, Vh

def simple_svd_reduced(A):
    # try with full_matrices=False
    U, s, Vh = linalg.svd(A, full_matrices=False, compute_uv=True)
    S = np.diag(s)
    print np.shape(U), np.shape(S), np.shape(Vh)
    # check if SVD-resulting matrix is accurate enough
    A_check = np.dot(np.dot(U, S), Vh)
    print np.allclose(A, A_check)
    return U, S, Vh

def simple_svd_dim_reduc(A):
    # rank: measure of nondegenareteness
    k_adjust = matrix_rank(A, tol=None)
    U, s, Vh = scipy.sparse.linalg.svds(A, k=k_adjust/2)
    S = np.diag(s)
    return U, S, Vh

def memory_usage_psutil():
    # python system and process utilities = psutil
    # print psutil.cpu_times()
    # print "CPU percent" , psutil.cpu_percent()
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / float(2 ** 20)
    return mem

#A = random_matrix(1000, 1000)

dims = np.arange(100, 1500 , 20)
print dims
n_iter = dims.shape[0]

memo_svd = np.zeros((n_iter, 1))
memo_rdc = np.zeros((n_iter, 1))

for i in range(0, n_iter):
    M = dims[i]
    N = M
    A = random_matrix(M, N)
    tmp = memory_usage((linalg.svd, (A,)))
    memo_svd[i] = np.max(tmp)
    tmp = memory_usage((sparse.linalg.svds, (A,)))
    memo_rdc[i] = np.max(tmp)

pl.plot(dims, memo_svd)
pl.plot(dims, memo_rdc, 'r')
pl.show()
# U, S, Vh = simple_svd(A)
# mem_1 = memory_usage_psutil()
# print "memory used 01 : ", mem_1, "MB"
# print memory_usage((linalg.svd, (A,)))
#
# U, S, Vh = simple_svd_dim_reduc(A)
# mem_2 = memory_usage_psutil()
# print "memory used 02: ", mem_2, "MB"
# print memory_usage((sparse.linalg.svds, (A,)))



# U, S, Vh = simple_svd_reduced(A)




