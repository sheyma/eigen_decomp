# run PALM...

import sys, os
import csv
import pandas as pd

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

DATA = h5py.File(path + '468_embeddings.h5', 'r')
mode = 'embedding'

DATA = h5py.File(path + '468_alignments.h5', 'r')
mode = 'aligned'
component = 0
DATA_all = []
for subject_id in subject_list:
    subject_id = ''.join(subject_id)
    subject_component = choose_component(DATA, subject_id, mode, component)
    DATA_all.append(subject_component)
DATA_all = np.array(DATA_all)


surface_data = path + 'data_surface.h5'
surface_type = 'midthickness'

hemisphere = 'full'
n, vertices, triangles = get_surface(surface_data, 
                                     hemisphere, surface_type)
hemisphere = 'LH'
n_LH, vertices_LH, triangles_LH = get_surface(surface_data, 
                                              hemisphere, surface_type)
hemisphere = 'RH'
n_RH, vertices_RH, triangles_RH = get_surface(surface_data, 
                                              hemisphere, surface_type)


data_full = np.zeros((len(subject_list), len(vertices)))
data_full[:, n] = DATA_all


DATA_all_LH = DATA_all[:, 0:len(n_LH)]
data_LH = np.zeros((len(subject_list), len(vertices_LH)))
data_LH[:, n_LH] = DATA_all_LH

DATA_all_RH = DATA_all[:, len(n_LH):len(n_RH)+len(n_LH)]
data_RH = np.zeros((len(subject_list), len(vertices_RH)))
data_RH[:, n_RH] = DATA_all_RH

tmp_full = pd.DataFrame(data_full)
tmp_full.to_csv(path + 'data_64984_full_01.csv', header=False, index=False)

tmp_LH = pd.DataFrame(data_LH)
tmp_LH.to_csv(path + 'data_32492_left_01.csv', header=False, index=False)

tmp_RH = pd.DataFrame(data_RH)
tmp_RH.to_csv(path + 'data_32492_right_01.csv', header=False, index=False)


tmp_read_full = pd.read_csv(path + 'data_64984_full_01.csv', header=None)
tmp_read_full = np.array(tmp_read_full)

tmp_read_LH = pd.read_csv(path + 'data_32492_left_01.csv', header=None)
tmp_read_LH = np.array(tmp_read_LH)

tmp_read_RH = pd.read_csv(path + 'data_32492_right_01.csv', header=None)
tmp_read_RH = np.array(tmp_read_RH)


plotting.plot_surf_stat_map(vertices, triangles, 
                            stat_map=tmp_read_full[447, :], 
                            cmap='jet', azim=180)

plotting.plot_surf_stat_map(vertices_LH, triangles_LH, 
                            stat_map=tmp_read_LH[447, :],
                            cmap='jet', azim=180)

plotting.plot_surf_stat_map(vertices_RH, triangles_RH, 
                            stat_map=tmp_read_RH[447, :],
                            cmap='jet', azim=0)


sys.path.append(os.path.expanduser('/home/raid/bayrak/src/PALM'))
os.system('./palm')

# load a certain component for each subject and save as .csv





./palm -i ~/tmp/data_lh.csv -s ~/devel/topography/data/lh.pial -d ~/tmp/design_matrix.csv -t test.con -n 1000 -o myresults/second_run  -zstat -fdr -logp

path = '/home/raid/bayrak/tmp/'

# read-in subject_list
subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);


# save out group level results...
tmp_list = []

# plot a component over all subjects
components = np.arange(0, 10, 1)
for component in components:
    #tmp = get_mean(DATA, subject_list, mode, component)
   
    tmp = get_cov(DATA, DATA_new, subject_list, mode, mode_new, 
                      comp=component, comp_new=None)    
    tmp_list.append(tmp)