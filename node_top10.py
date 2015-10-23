
import numpy as np
import os
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import load_hcp
import corr_faster
import corr_full

# here we go ...

# list of all saubjects as numpy array
subject_list = np.array(['100307', '912447']) 
#subject_list = np.array(sys.argv)[2:]

data_path = '/a/documents/connectome/_all'
template = 'MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'

#data_path = '/ptmp/sbayrak/hcp'
#template = 'rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
cnt_files = 4
#N_user = sys.argv[1]
#N_user = int(N_user)
#N_user = None
# nodes of left hemispheres only
N_user = 100


N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)
    
    # load time-series matrix of the subject    
    K = load_hcp.t_series(data_path, subject, template, cnt_files, N_user, subject_path=None, dtype=None)

    # get upper-triangular of correlation matrix of time-series as 1D array
    K = corr_faster.corrcoef_upper(K)   

    # convert upper-triangular to full matrix    
    N_orig = corr_full.N_original(K)
    K.resize([N_orig, N_orig])
    corr_full.upper_to_down(K)
    
    # find a threshold value for each row of corr matrix
    dbins = 0.1
    bins = np.arange(-1, 1+dbins, dbins)
    ten_percent = 0.1
    
    for j in range(0, N_orig):
        x, bins = np.histogram(K[j,:], bins) 
        back_sum = 0    
        for idx in range(x.shape[0]-1, -1, -1):    
            back_sum += x[idx]/float(x.sum())    
            if back_sum >= ten_percent:
                thr = bins[idx]
                #print "top-10percent node threshold:", thr
                break
        # binarize corr matrix via thresholding
        K[j,:][np.where( K[j,:] >= thr) ] = 1.0    
        K[j,:][np.where( K[j,:] < thr) ] = 0


    if i == 0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K

print "loop done"
