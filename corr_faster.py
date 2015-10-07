
from glob import glob
import os
import numpy as np
#import numexpr as ne
#ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
#import nibabel as nb
import sys
import math
import time
from scipy.linalg import get_blas_funcs

fname = sys.argv[1]

rnd_mtx = np.loadtxt(fname)
print rnd_mtx

def set_time():
    global last_time
    last_time = time.time()

def print_time(s):
    global last_time
    now = time.time()
    print "time %s %.3f" % (s, (now - last_time))
    last_time = now

def cool_syrk(fact, X): #?
    syrk = get_blas_funcs("syrk", [X])
    print "syrk", syrk
    R = syrk(fact, X)

    d = np.diag(R).copy()
    size = mat_to_upper_F(R)
    R.resize([size,])
    return R,d


def my_cov(m):
    # numpy.cov 1.9.2 adapted for real arrays
    m = np.asarray(m)
    dtype = np.result_type(m, np.float64)
    X = np.array(m, ndmin=2, dtype=dtype)
    N = X.shape[1]

    fact = float(N - 1)
    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice", RuntimeWarning)
        fact = 0.0

    X -= X.mean(axis=1, keepdims=True)
    print_time("mean:")

    # This returns np.dot(X, X.T) / fact #?
    return cool_syrk(1.0/fact, X)

last_time = 0
print my_cov(rnd_mtx)


#def corrcoef_upper(x):
    ## numpy.corrcoef 1.9.2 adapted for mem-usage optimization
    #c, d = my_cov(x)
    #print_time("cov:")

    #d = np.sqrt(d)
    ## calculate "c / multiply.outer(d, d)" row-wise for mem & speed
    #k = 0
    #for i in range(0, d.size - 1):
        #len = d.size - i - 1
        #c[k:k + len] /= (d[-len:] * d[i])
        #k += len

    #print_time ("outer d:")
    #return c


#def correlation_matrix(matrix):
    #set_time()
    ##K = load_nii_subject(subject)
    ## K = load_random_subject(NN,4800)
    ## K : matrix of similarities / Kernel matrix / Gram matrix
    ##print_time("load:")
    ##print "input data shape:", K.shape
    #K = corrcoef_upper(matrix)
    #print "corrcoef data shape: ", K.shape
    #print_time("corrcoef:")
    #return K