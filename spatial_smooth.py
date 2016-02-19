import sys, os
import csv
import pandas as pd
import nipype.interfaces.freesurfer as fs

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A

subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);
    
DATA = h5py.File(path + '468_alignments.h5', 'r')
mode = 'aligned'
component = 0
DATA_all = []
for subject_id in subject_list:
    subject_id = ''.join(subject_id)
    subject_component = choose_component(DATA, subject_id, mode, component)
    DATA_all.append(subject_component)
DATA_all = np.array(DATA_all)


tmp_read_LH = pd.read_csv(path + 'data_32492_left_01.csv', header=None)
tmp_read_LH = np.array(tmp_read_LH)

name = '/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/brainmask_fs.2.nii.gz'
img = nb.load(name)

A = nb.load('/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
dir(A)
A = nb.nifti2.load('/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
dir(A)
A.get_data().shape
tmp = np.random.rand(1, 1, 1, 1, 1,  91282)
A.dataobj[:] = tmp
outcifti = nb.nifti2.Nifti2Image(tmp, A.get_affine(), header=A.get_header())
outcifti.to_filename('tmp.nii')

# fill uninteresting parts by NaN's


