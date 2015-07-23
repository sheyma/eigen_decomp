# First it is necessary to install a branch of nibabel from satra that can read cifti (nifti2) files:
# pip install git+https://github.com/satra/nibabel.git@enh/cifti2

from glob import glob
import os, numpy as np
import nibabel as nb

data_dir = '/ptmp/mdani/hcp' #'/a/documents/connectome/_all'
# Set as local output directory:
results_dir = './'

subject_list = ['100307' '100408' '101006' '101107' '101309']

def createCorrMatrix(subject):
    # For local institute:
    #template = ('%s/MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii' % subject)
    template = ('%s/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii' % subject)
    files = [val for val in sorted(glob(os.path.join(data_dir, template)))]
    filename = files[:2]
    print filename

    # read in data and create correlation matrix:
    # for left hemisphere; 'range(0,nsamples)' for all
    # data_range = range(0,32492) 

    input_timeseries = []
    for x in xrange(0,4):
        img = nb.load(filename[0])
        ntimepoints, nsamples = img.data.shape

        # the following should be a concatenation of all 4 scans from each subject:
        # brainModels[2] will include both left and right hemispheres
        # for only left hemisphere: brainModels[1]
        single_run_timeseries = img.data[:, :img.header.matrix.mims[1].brainModels[2].indexOffset].T
        # old: img.get_data()[:,:,:,:,:,data_range].squeeze().T
        input_timeseries.extend(((single_run_timeseries - single_run_timeseries.mean(axis=0)) / single_run_timeseries.std(axis=0)).T)
        del img
        del single_run_timeseries

    # create correlation matrix and shift values between [0,1]:
    K = (np.corrcoef(np.array(input_timeseries).T) + 1) / 2.
    del input_timeseries
    print K
    return K

A = createCorrMatrix('100307')

# import nibabel as nb
#
# img = nb.load('/ptmp/mdani/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
#
# img
#
# img.data
#
# img.data.shape
#
# single_run_timeseries = img.data[:, :img.header.matrix.mims[1].brainModels[2].indexOffset].T
#
# single_run_timeseries.shape
#
# single_run_timeseries = img.data[:, :100].T
#
# single_run_timeseries.shape
#
# (100, 1200)
#
# import numpy as np
#
# K = (np.corrcoef(np.array(single_run_timeseries).T) + 1) / 2.
#
# K.shape
#
# (1200, 1200)
#
# K = (np.corrcoef(np.array(single_run_timeseries)) + 1) / 2.
#
# K.shape
#
# (100, 100)