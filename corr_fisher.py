# read-in cifti (nifti2) format via Satra's nibabel repository:
# $git clone --branch enh/cifti2 https://github.com/satra/nibabel.git

from glob import glob
import os
import numpy as np
import nibabel as nb
import sys
import math

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed

# fake this for testing: 8095...0.5 GB, 11448...1 GB, 16190...2 GB
#NN = 11448

print "python version: ", sys.version[0:5]
# (HYDRA) 2.7.9
print "numpy version: ", np.__version__
# (HYDRA) 1.9.1

def load_nii_subject(subject, dtype=None):
    template = 'rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
    cnt_files = 4
    files = [val for val in sorted(glob(os.path.join(subject, template)))]
    files = files[:cnt_files]

    # read in data and create correlation matrix:
    # for left hemisphere; 'range(0,nsamples)' for all ??
    # data_range = range(0,32492) ??

    for x in xrange(0, cnt_files):

        img = nb.load(files[x])
        # ntimepoints, nsamples = img.data.shape

        # the following should be a concatenation of all 4 scans from each subject:
        # brainModels[2] will include both left and right hemispheres
        # for only left hemisphere: brainModels[1]

        # count of time series
        n = img.header.matrix.mims[1].brainModels[2].indexOffset

        # globally faked ... for testing
        if 'NN' in globals():
            n = min(NN,n)

        single_t_series = img.data[:, :n].T
        # length of time series
        m = single_t_series.shape[1]

        mean_series = single_t_series.mean(axis=0)
        std_series = single_t_series.std(axis=0)

        if x == 0:
            # In first loop we initialize matrix K to be filled up and returned.
            # By default we are using the same dtype like input file (float32).
            init_dtype = single_t_series.dtype if dtype == None else dtype
            K = np.ndarray(shape=[n,m], dtype=init_dtype, order='F')
        else:
            if  m_last != m:
                print "Warning, %s contains time series of different length" % (subject)
            if  n_last != n:
                print "Warning, %s contains different count of time series" % (subject)
            K.resize([n, K.shape[1] + m])

        K[:, -m:] = (single_t_series - mean_series) / std_series
        m_last = m
        n_last = n

        del img
        del single_t_series

    return K

def load_random_subject(n,m):
    return np.random.randn(n, m)

def correlation_matrix(subject):
    K = load_nii_subject(subject)
    #K = load_random_subject(NN,4800)
    # K : matrix of similarities / Kernel matrix / Gram matrix
    K = np.corrcoef(K)
    return K

def fisher_r2z(R):
    # convert 1.0's into largest smaller value than 1.0
    di = np.diag_indices(R.shape[1])
    epsilon = np.finfo(float).eps
    R[di] = 1.0 - epsilon
    # Fisher r to z transform 
    Z = np.arctanh(R)
    return Z 

def fisher_z2r(Z):
    # Fisher z to r transform
    R = (np.exp(2*Z) - 1)/(np.exp(2*Z) +1)
    # set diagonals back to 1.0
    di = np.diag_indices(R.shape[1])
    R[di] = 1.0
    return R

# here we go ...

subject_list = np.array(sys.argv)[1:] # e.g. /ptmp/sbayrak/hcp/100307
N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print i, "do corr"
    K = correlation_matrix(subject)
    print i, "do r2z"
    K = fisher_r2z(K)
    if i == 0:
        SUM = np.zeros(K.shape,K.dtype)
    print i, "do sum"
    SUM = SUM + K
    del K

print "loop done, do fisher_z2r"
SUM /= float(N)
SUM = fisher_z2r(SUM)

print "do embed"
print "correlation matrix:", SUM.shape
embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

#save_output(subject, embedding)
np.savetxt("out_test", embedding, fmt='%5.5e', delimiter='\t', newline='\n')

print result['lambdas']

