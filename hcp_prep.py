# First it is necessary to install a branch of nibabel from satra that can read cifti (nifti2) files:
# pip install git+https://github.com/satra/nibabel.git@enh/cifti2

from glob import glob
import os
import numpy as np
import nibabel as nb

# set as a local input directory (MPI)
data_path = '/a/documents/connectome/_all'
# set a list for the subject ID's
subject_list = ['100307', '100408', '101006', '101107', '101309']
# set as local output directory:
out_path = '/home/raid/bayrak/devel/eigen_decomp'

# data_path = '/ptmp/mdani/hcp'
# template = ('%s/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii' % subject)
# img = nb.load('/ptmp/mdani/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')

def correlation_matrix(subject):
    template = ('%s/MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii' % subject)
    files = [val for val in sorted(glob(os.path.join(data_path, template)))]
    filename = files[:2]

    # read in data and create correlation matrix:
    # for left hemisphere; 'range(0,nsamples)' for all ??
    # data_range = range(0,32492) ??

    tmp_t_series = []
    for x in xrange(0, 4):
        # why is it not filename[x]?
        img = nb.load(filename[0])
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
    K = (np.corrcoef(np.array(tmp_t_series).T) + 1) / 2.
    del tmp_t_series

    return K


def save_output(subject, matrix):
    out_dir = os.path.join(out_path, subject)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = subject + '_hcp_out.csv'
    print filename
    out_file = os.path.join(out_dir, filename)
    # %.e = Floating point exponential format (lowercase)
    np.savetxt(out_file, matrix, fmt='%e', delimiter='\t', newline='\n')
    return out_file


K = correlation_matrix(subject_list[0])
save_output(subject_list[0], K)
