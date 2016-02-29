import numpy as np
import nibabel as nb
import h5py
import csv
from subprocess import call
import argparse

## begin parse command line arguments
parser = argparse.ArgumentParser()
# output prefix, e.g. /ptmp/sbayrak/smooth
parser.add_argument('-o', '--outprfx', required=True)
## end parse command line arguments
args = parser.parse_args()

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A

# create a symbolic link for the "data" directory!
subject_list = []
with open('data/subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

DATA = h5py.File('data/468_alignments.h5', 'r')
mode = 'aligned'

surf_lh = "data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii"
surf_rh = "data/Q1-Q6_R440.R.midthickness.32k_fs_LR.surf.gii"

filename = 'data/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii'
A = nb.load(filename)

path_out = args.outprfx
components = np.arange(0,10,1)

for subject_id in subject_list[0:100]:
    subject_id = ''.join(subject_id)
    print subject_id
    for component in components:
        subject_component = choose_component(DATA, subject_id, mode, component)
        tmp = np.array(subject_component)
        A.data[component, 0:len(tmp)] = tmp
        A.data[component, len(tmp):np.shape(A.data)[1]] = np.NaN
    
    A.data[components[-1]+1:, :] = np.NaN
    
    B = path_out + subject_id + '_align.nii' 
    C = path_out + subject_id + '_align_smooth.nii'
    A.to_filename(B)

    retcode = call(["wb_command", "-cifti-smoothing",  B, "4", "2", "COLUMN",
                    C, "-left-surface", surf_lh, "-right-surface", surf_rh])  

    if retcode != 0:
        print "Error with wb_command"
        break

    suffix = '_smooth_59412.h5'
    D = nb.load(C)
    
    smoothed_components = []
    for component in components:
        smoothed_component = np.array(D.data[component, 0:len(tmp)])    
        smoothed_components.append(smoothed_component)
    smoothed_components = np.array(smoothed_components).T    

    h = h5py.File(path_out + subject_id + suffix, 'w')
    h.create_dataset('smooth', data = smoothed_components)
    h.close()