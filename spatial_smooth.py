import numpy as np
import nibabel as nb
import h5py
import csv
from subprocess import call

subject_list = []
with open('/home/sheyma/tmp/subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

DATA = h5py.File('/home/sheyma/tmp/468_alignments.h5', 'r')
mode = 'aligned'

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A


surf_lh = "/home/sheyma/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii"
surf_rh = "/home/sheyma/devel/topography/data/Q1-Q6_R440.R.midthickness.32k_fs_LR.surf.gii"

filename = '/home/sheyma/tmp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii'
A = nb.load(filename)


component = 0
DATA_all = []
for subject_id in subject_list[0]:
    subject_id = ''.join(subject_id)
    print subject_id
    subject_component = choose_component(DATA, subject_id, mode, component)
    tmp = np.array(subject_component)
    print tmp.shape
    A.data[0, 0:len(tmp)] = tmp
    A.data[0, len(tmp):np.shape(A.data)[1]] = np.NaN
    A.data[1:, :] = np.NaN
    A.to_filename('/home/sheyma/tmp/' + subject_id + '_align.nii')
    
    B = '/home/sheyma/tmp/' + subject_id + '_align.nii' 
    C = '/home/sheyma/tmp/' + subject_id + '_align_smooth.nii'

    retcode = call(["wb_command", "-cifti-smoothing",  B, "2", "2", "COLUMN",
                    C, "-left-surface", surf_lh, "-right-surface", surf_rh])  

    print retcode
    
    D = nb.load(C)
    D = np.array(D.data[0, 0:len(tmp)])    
    h = h5py.File('/home/sheyma/tmp/'+ subject_id+'align_smooth_59412.h5','w')
    h.create_dataset('smooth', data=D)
    h.close()


