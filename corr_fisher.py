# read-in cifti (nifti2) format via Satra's nibabel repository:
# $ git clone --branch enh/cifti2 https://github.com/satra/nibabel.git

from glob import glob
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import nibabel as nb
import sys
import math
import time
from scipy.linalg import get_blas_funcs

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed

# fake this for testing: 8095...0.5 GB, 11448...1 GB, 16190...2 GB
NN = 1144

print "python version: ", sys.version[0:5]
# (HYDRA) 2.7.9
print "numpy version: ", np.__version__
# (HYDRA) 1.9.1

def load_nii_subject(subject, dtype=None):
    # four templates for each subject
    template = 'rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
    cnt_files = 4
    files = [val for val in sorted(glob(os.path.join(subject, template)))]
    files = files[:cnt_files]

    for x in xrange(0, cnt_files):

        img = nb.load(files[x])

        # brainModels[2] will include both left and right hemispheres
        # for only left hemisphere: brainModels[1]

        # count of brain nodes (e.g. n=59412)
        n = img.header.matrix.mims[1].brainModels[2].indexOffset

        # globally faked ... for testing
        # if 'NN' in globals():
        #    n = min(NN,n)

        single_t_series = img.data[:, :n].T
        # length of time series (e.g. m=1200)
        m = single_t_series.shape[1]

        mean_series = single_t_series.mean(axis=0)
        std_series = single_t_series.std(axis=0)

        if x == 0:
            # In first loop we initialize matrix K to be filled up and returned.
            # By default we are using the same dtype like input file (float32).
            init_dtype = single_t_series.dtype if dtype == None else dtype
            K = np.ndarray(shape=[n,m], dtype=init_dtype, order='F') #?
        else:
            if  m_last != m:
                print "Warning, %s contains time series of different length" % (subject)
            if  n_last != n:
                print "Warning, %s contains different count of time series" % (subject)
            K.resize([n, K.shape[1] + m])

        # concatenation of all 4-normalized scans from each subject
        K[:, -m:] = (single_t_series - mean_series) / std_series
        m_last = m
        n_last = n
        # TRANSPOSE of K!!!!
        del img
        del single_t_series

    return K

def load_random_subject(n,m):
    return np.random.randn(n, m)


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

def corrcoef_upper(x):
    # numpy.corrcoef 1.9.2 adapted for mem-usage optimization
    c, d = my_cov(x)
    print_time("cov:")

    d = np.sqrt(d)
    # calculate "c / multiply.outer(d, d)" row-wise for mem & speed
    k = 0
    for i in range(0, d.size - 1):
        len = d.size - i - 1
        c[k:k + len] /= (d[-len:] * d[i])
        k += len

    print_time ("outer d:")
    return c

def correlation_matrix(subject):
    set_time()
    K = load_nii_subject(subject)
    # K = load_random_subject(NN,4800)
    # K : matrix of similarities / Kernel matrix / Gram matrix
    print_time("load:")
    print "input data shape:", K.shape
    K = corrcoef_upper(K)
    print "corrcoef data shape: ", K.shape
    print_time("corrcoef:")
    return K

def fisher_r2z(R):
    return ne.evaluate('arctanh(R)')

def old_fisher_r2z(R):
    # convert 1.0's into largest smaller value than 1.0
    di = np.diag_indices(R.shape[1])
    epsilon = np.finfo(float).eps
    R[di] = 1.0 - epsilon
    # Fisher r to z transform 
    Z = np.arctanh(R)
    return Z 

def fisher_z2r(Z):
    X = ne.evaluate('exp(2*Z)')
    return ne.evaluate('(X - 1) / (X + 1)')

def old_fisher_z2r(Z):
    # Fisher z to r transform
    R = (np.exp(2*Z) - 1)/(np.exp(2*Z) +1)
    # set diagonals back to 1.0
    di = np.diag_indices(R.shape[1])
    R[di] = 1.0
    return R

def mat_to_upper_C(A):
    if not A.flags['C_CONTIGUOUS']:
        raise Exception("C_CONTIGUOUS required")
    n = A.shape[0]
    size = (n - 1) * n / 2
    U = A.reshape([n*n,])
    k = 0
    for i in range(0, n-1):
        len = n - 1 - i
        U[k:k+len] = A[i,i+1:n]
        k += len
    return size

def mat_to_upper_F(A):
    # check if input array Fortran style contiguous
    if not A.flags['F_CONTIGUOUS']:
        raise Exception("F_CONTIGUOUS required")
    n = A.shape[0]
    size = (n - 1) * n / 2
    # 'F': Fortran-like index ordering
    U = A.reshape([1,n*n], order='F') #?
    k = 0
    # fill out U by upper diagonal elements of A
    for i in range(0, n-1):
        len = n - 1 - i
        U[0,k:k+len] = A[i,i+1:n]
        k += len
    return size

## not in place! should work for F and C
def mat_to_upper_copy(A):
    n = A.shape[0]
    size = (n - 1) * n / 2
    U = np.ndarray(shape=[size,], dtype=A.dtype, order='C')
    k = 0
    for i in range(0, n-1):
        len = n - 1 - i
        U[k:k+len] = A[i,i+1:n]
        k += len
    return U

def upper_to_mat(M):
    if not M.flags['C_CONTIGUOUS']:
        raise Exception("C_CONTIGUOUS required")
    n = M.shape[0]
    size = (n - 1) * n / 2
    U = M.reshape([n*n,])
    k = size
    for i in range(n-1, -1, -1):
        len = n - 1 - i
        M[i+1:n,i] = U[k-len:k]
        M[i,i+1:n] = U[k-len:k]
        M[i,i] = 1.0
        k -= len

def write_upper(file, A, fmt="%g"):
    count = A.size
    print "count", count
    A = A.reshape([count,])
    step = 10000
    k = 0
    f = open(file,'wb') #?
    while k < count:
        i = min(step,count-k)
        np.savetxt(f,A[k:k+i].reshape([1,i]),fmt=fmt, delimiter='\n', newline='\n')
        k += i
    f.close()

last_time = 0

def set_time():
    global last_time
    last_time = time.time()

def print_time(s):
    global last_time
    now = time.time()
    print "time %s %.3f" % (s, (now - last_time))
    last_time = now

# here we go ...

# output prefix
out_prfx="/ptmp/sbayrak/embed_out_template/fisher_"
# output precision
out_prec="%g"
# list of all saubjects as numpy array
subject_list = np.array(sys.argv)[1:] # e.g. /ptmp/sbayrak/hcp/*
N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)
    # This always returns dtype=np.float64, consider adding .astype(np.float32) #?
    K = correlation_matrix(subject)

    for item in range(len(K)):
        if K[item] >= 0.9 :
            K[item] = 1.0
        else:
            K[item] = 0
    
    set_time()

    # For the next calculations we only use the upper triangular matrix!

    #K = fisher_r2z(K)
    #print_time("fisher_r2z:")

    if i == 0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')
    print_time("sum:")

    del K

print "loop done"
print

SUM = ne.evaluate('SUM / N')
print_time("final division:")
#SUM = fisher_z2r(SUM)
#print_time("final fisher_z2r:")

# save upper diagonal correlation matrix as 1D array
#write_upper(out_prfx + "upper.csv", SUM, fmt=out_prec)
#print_time("final save sum:")

n_orig = int(round( 0.5 + np.sqrt(0.25 + 2 * SUM.shape[0]) )) #?
print "n_orig", n_orig
SUM.resize([n_orig,n_orig])
upper_to_mat(SUM)
SUM = (SUM +1.0) / 2.0
#np.savetxt(out_prfx + "fw_bw.csv", SUM, fmt='%5.5e', delimiter='\t', newline='\n')
print "SUM.shape", SUM.shape
print_time("final upper_to_mat:")

print "do embed for correlation matrix:", SUM.shape
embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)
print_time("final embedding:")

np.savetxt(out_prfx + "embedding.csv", embedding, fmt='%5.5e', delimiter='\t', newline='\n')
#save_output(subject, embedding)
#np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
#np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
#np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
print_time("final save:")

print result['lambdas']

