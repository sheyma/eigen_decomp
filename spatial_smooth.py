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

smoother = fs.SurfaceSmooth()
smoother.inputs.in_file = path + 'data_32492_left_01.csv'
smoother.inputs.subject_id = '100307'
smoother.inputs.hemi = 'lh'
smoother.inputs.fwhm = 5
smoother.run()