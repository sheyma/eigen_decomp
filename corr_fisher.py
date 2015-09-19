# read-in cifti (nifti2) format via Satra's nibabel repository:
# $git clone --branch enh/cifti2 https://github.com/satra/nibabel.git

from glob import glob
import os
import numpy as np
import nibabel as nb
import sys
import math

print "python version: ", sys.version[0:5]
# (HYDRA) 2.7.9
print "numpy version: ", np.__version__
# (HYDRA) 1.9.1

subject_list = np.array(sys.argv)[1:] # e.g. /ptmp/sbayrak/hcp/100307
N = len(subject_list)

def correlation_matrix(subject):
    template = 'rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
    # template = ('%s/MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii' % subject)
    files = [val for val in sorted(glob(os.path.join(subject, template)))]
    filename = files[:4]

    # read in data and create correlation matrix:
    # for left hemisphere; 'range(0,nsamples)' for all ??
    # data_range = range(0,32492) ??

    tmp_t_series = []
    for x in xrange(0, 4):

        img = nb.load(filename[x])
        # ntimepoints, nsamples = img.data.shape

        # the following should be a concatenation of all 4 scans from each subject:
        # brainModels[2] will include both left and right hemispheres
        # for only left hemisphere: brainModels[1]

        header = img.header.matrix.mims[1].brainModels[2].indexOffset
        single_t_series = img.data[:, :header].T

        mean_series = single_t_series.mean(axis=0)
        std_series = single_t_series.std(axis=0)

        tmp_t_series.extend(((single_t_series - mean_series) / std_series).T)

        del img
        del single_t_series

    # K : matrix of similarities / Kernel matrix / Gram matrix
    K = np.corrcoef(np.array(tmp_t_series).T) 
    del tmp_t_series

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


for i in range(0, N):
	subject = subject_list[i]
	K = correlation_matrix(subject)
	K = fisher_r2z(K)
	if i == 0:
		SUM = K.copy()
	else:
		SUM = SUM + K

#del K

SUM /= float(N)

SUM = fisher_z2r(SUM)

np.allclose(K, SUM)
