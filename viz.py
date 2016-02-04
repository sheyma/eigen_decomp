"""
load embedding components
load indices, triangles, vertices of surface
plot embedding component on brain template
"""

import numpy as np
import h5py 
import sys
import os
import csv
sys.path.append(os.path.expanduser('/u/sbayrak/devel/brainsurfacescripts'))
#sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))
#sys.path.append(os.path.expanduser('/home/sheyma/devel/brainsurfacescripts'))
import plotting
import argparse

## begin parse command line arguments
parser = argparse.ArgumentParser()
# input prefix, e.g. /ptmp/sbayrak/tmp
parser.add_argument('-i', '--inprfx', required=True)
# output prefix, e.g. /ptmp/sbayrak/hcp_embed_full_realigned_figures
parser.add_argument('-o', '--outprfx', required=True)
## end parse command line arguments
args = parser.parse_args()

def choose_random_subject(subject_list):
    random_int = np.random.permutation(len(subject_list))[0]
    subject_id = subject_list[random_int] 
    subject_id = ''.join(subject_id)
    print "chosen HCP subject : ", subject_id
    return subject_id

def choose_component(DATA, subject_id, component = 0, mode = 'aligned'):
    # choose a component of given subject    
    A = DATA[subject_id][mode]
    A = np.array(A)
    A = A[:, component]
    return A
    
def get_mean(DATA, subject_list, component = 0, mode = 'aligned'):
    # get mean of a component over all subjects    
    DATA_all = []    
    for subject_id in subject_list:
        subject_id = ''.join(subject_id)
        tmp = np.array(DATA[subject_id]['aligned'])[:,component]
        DATA_all.append(tmp)
    DATA_mean = np.mean(DATA_all, axis=0)
    return DATA_mean
    
def get_surface(surface_data, hemisphere, surface_type):
    """
    surface_data = hdf5 formatted surface data
    hemisphere = 'LH', 'RH', or 'full'
    surface_type = 'midthickness', 'inflated', or 'very_inflated'
    """

    tmp = h5py.File(surface_data, 'r')
    indices = np.array( tmp[hemisphere][surface_type]['indices'] )
    vertices = np.array( tmp[hemisphere][surface_type]['vertices'] )    
    triangles = np.array( tmp[hemisphere][surface_type]['triangles'])
    
    return indices, vertices, triangles

# here we go...
path = args.inprfx
path_out = args.outprfx

subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

surface_data = path + 'data_surface.h5'
hemisphere = 'full'
surface_type = 'inflated'
n, vertices, triangles = get_surface(surface_data, hemisphere, surface_type)

DATA = h5py.File(path + '468_alignments.h5', 'r')

# plot subjects individually
#for subject_id in subject_list:
#    ## chose subject_id randomly     
#    #subject_id = choose_random_subject(subject_list)
#    #subject_id = '100307'
#    subject_id = ''.join(subject_id)
#    component = 0
#    mode = 'aligned'
#    subject_component = choose_component(DATA, subject_id, component, mode)
#    data = np.zeros(len(vertices))
#    data[n] = subject_component
#    plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
#    import matplotlib.pyplot as plt
#    plt.title(subject_id + ' , component ' + str(component+1))
#    plt.savefig(path_out + subject_id + '_comp_' + str(component+1)+ '.png')


# plot a mean component over all subjects
components = np.arange(0, 10, 1)
for component in components:
    component = 0
    mode = 'aligned'
    DATA_mean = get_mean(DATA, subject_list, component=component, mode=mode)
    data = np.zeros(len(vertices))
    data[n] = DATA_mean
    plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    import matplotlib.pyplot as plt
    plt.title('mean_' + mode  + ' , component ' + str(component+1))   
    plt.savefig(path_out + 'mean_'+  mode + '_comp_' + str(component+1)+ '.png')
    
    
#A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/RcovS_468.h5', 'r')
#A = np.array(A_init.get('cov'))


