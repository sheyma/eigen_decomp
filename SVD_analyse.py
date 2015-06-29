#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pylab import *
import scipy
from scipy.sparse import linalg
from scipy import sparse, linalg
import psutil, os
from memory_profiler import memory_usage
import time
import pylab as pl


print "python version: ", sys.version[0:5]
print "scipy version: ", scipy.__version__
print "psutil version: ", psutil.__version__

# construct a random matrix sized MxN
def random_matrix(M, N):
    return np.random.randn(M, N)  # + 1.j*np.random.randn(M,N)

# singular value decomposition (SVD) of matrix A
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

# SVD tranformation with reduced dimensions
def simple_svd_dim_reduc(A):
    # rank: measure of nondegenareteness
    k_adjust = matrix_rank(A, tol=None)
    # get eigenvectors corresp. to largest eigenvalues
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

dims = np.arange(500, 2000, 20)
n_iter = dims.shape[0]

# zero arrays for memory usage
memo_svd = np.zeros((n_iter, 1))
memo_rdc = np.zeros((n_iter, 1))

# time arrays for time consume
t_svd = np.zeros((n_iter, 1))
t_rdc = np.zeros((n_iter, 1))

for i in range(0, n_iter):
    M = dims[i]
    N = M
    A = random_matrix(M, N)
    tmp = memory_usage((simple_svd, (A,)))
    memo_svd[i] = np.max(tmp)
    tmp = memory_usage((simple_svd_dim_reduc,(A,)))
    memo_rdc[i] = np.max(tmp)

for i in range(0, n_iter):
    M = dims[i]
    N = M
    A = random_matrix(M, N)
    t0 = time.time()
    simple_svd(A)
    t_svd[i] = time.time() - t0
    t0 = time.time()
    simple_svd_dim_reduc(A)
    t_rdc[i] = time.time() - t0

fig, ax = pl.subplots()
ax.plot(dims, memo_svd, label='scipy.linalg.svd')
ax.plot(dims, memo_rdc, 'r', label='scipy.sparse.linalg.svds')
legend = ax.legend(loc='upper left')
pl.xlabel('Matrix Size [NxN]', fontsize=18)
pl.ylabel('Memory Use (MB)', fontsize=18)
pl.xticks(fontsize=14)
pl.yticks(fontsize=14)

fig, ax = pl.subplots()
ax.plot(dims, t_svd, label='scipy.linalg.svd')
ax.plot(dims, t_rdc, 'r', label='scipy.sparse.linalg.svds')
legend = ax.legend(loc='upper left')
pl.xlabel('Matrix Size [NxN]', fontsize=18)
pl.ylabel('Time (s)', fontsize=18)
pl.xticks(fontsize=14)
pl.yticks(fontsize=14)

pl.show()






