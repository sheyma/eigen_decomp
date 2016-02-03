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
    A = DATA[subject_id][mode]
    A = np.array(A)
    A = A[:, component]
    return A
    
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

# plot several subjects
for subject_id in subject_list[0:100]:
    ## chose subject_id randomly     
    #subject_id = choose_random_subject(subject_list)
    #subject_id = '100307'
    subject_id = ''.join(subject_id)
    component = 0
    mode = 'aligned'
    subject_component = choose_component(DATA, subject_id, component, mode)
    data = np.zeros(len(vertices))
    data[n] = subject_component
    plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    import matplotlib.pyplot as plt
    plt.title(subject_id + ' , component ' + str(component+1))
    plt.savefig(path_out + subject_id + '_comp_' + str(component+1)+ '.png')

#A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/RcovS_468.h5', 'r')
#A = np.array(A_init.get('cov'))

## get mean of Aligned components over subjects
#A_mean = np.mean(A, axis=0)
#A_hem = A_mean[0:29696,:]
##A_hem = A_mean[29696:29696+len(n),:]
#A_hem = A_hem[:,0]
#
#data = np.zeros(len(vertices))
#data[n] = A_hem
#plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)

#del A_hem
#A_hem = A[29696:29696+len(n)]
#A_hem = A[0:29696]

#data = np.zeros(len(vertices))
#import h5py
#A = h5py.File('/nobackup/kocher1/bayrak/embed_out/LH_node_average.h5', 'r')
#L = A.get('sum')
#data[n] = L[20015]
#data[n] = L[:][10015]
#plot_surf_stat_map(vertices, triangles, stat_map=data)
#from mayavi import mlab
#mlab.triangular_mesh(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles, scalars=data)
#import numpy as np
#b = np.loadtxt('/nobackup/kocher1/bayrak/embed_out/daniel_embedding.csv')
#def vizData(a, n, num):
#    data = np.zeros(len(vertices))
#    data[n] = a[n,num]
#    mlab.triangular_mesh(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles, scalars=data)    
#vizData(a,n,0)
