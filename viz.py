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
import matplotlib.pyplot as plt

## begin parse command line arguments
parser = argparse.ArgumentParser()
# input prefix, e.g. /ptmp/sbayrak/tmp
parser.add_argument('-i', '--inprfx', required=True)
# output prefix, e.g. /ptmp/sbayrak/hcp_embed_full_realigned_figures
parser.add_argument('-o', '--outprfx', required=True)
parser.add_argument('-A', '--begin', type=int, required=True)
parser.add_argument('-B', '--end', type=int, required=True)
## end parse command line arguments
args = parser.parse_args()

def choose_random_subject(subject_list):
    random_int = np.random.permutation(len(subject_list))[0]
    subject_id = subject_list[random_int] 
    subject_id = ''.join(subject_id)
    print "chosen HCP subject : ", subject_id
    return subject_id

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A
      
def get_mean(DATA, subject_list, mode, component = None):
    # get mean of a component over all subjects    
    DATA_all = []    
    for subject_id in subject_list:
        subject_id = ''.join(subject_id)
        
        if component != None:
            tmp = choose_component(DATA, subject_id, mode, component)
            
        else:
            tmp = choose_component(DATA, subject_id, mode)            
            
        DATA_all.append(tmp)
    DATA_mean = np.mean(DATA_all, axis=0)
    return DATA_mean

def get_cov(DATA, DATA_new, subject_list, mode, mode_new, comp, comp_new):
   
    DATA_list = []    
    DATA_new_list = []
        
    for subject_id in subject_list:
        subject_id = ''.join(subject_id)

        tmp = choose_component(DATA, subject_id, mode, comp)
        DATA_list.append(tmp)
       
        tmp_new = choose_component(DATA_new, subject_id, mode_new, comp_new)
        DATA_new_list.append(tmp_new)
    
    DATA_01 = np.array(DATA_list)
    DATA_02 = np.array(DATA_new_list)
    
    C = []
    for i in range(np.shape(DATA_01)[1]):
        # covariance of one region (over subjects) in two datasets
        C.append(np.cov(DATA_01[:,i] , DATA_02[:,i])[0][1])
        print i
        
    C = np.array(C) 
    return C

    
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
surface_type = 'midthickness'
n, vertices, triangles = get_surface(surface_data, hemisphere, surface_type)

DATA = h5py.File(path + '468_smoothing.h5', 'r')
mode = 'smooth'

#DATA = h5py.File(path + '468_alignments.h5', 'r')
#mode = 'aligned'

#DATA_new = h5py.File(path +  '468_sulcs.h5' , 'r')
#mode_new = 'sulc'

#DATA = h5py.File(path + '468_embeddings.h5', 'r')
#mode = 'embedding'

# plot subjects individually
for subject_id in subject_list[args.begin : args.end]:
    ## chose subject_id randomly     
    #subject_id = choose_random_subject(subject_list)
    #subject_id = '100307'
    subject_id = ''.join(subject_id)
    print subject_id
    component = None
    subject_component = choose_component(DATA, subject_id, mode, component)
    data = np.zeros(len(vertices))
    data[n] = subject_component
    plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    plt.title(subject_id + ' , component 1' )
    plt.savefig(path_out + subject_id + '_comp_01' + '_000.png')
    plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=180)   
    plt.title(subject_id + ' , component 1' )
    plt.savefig(path_out + subject_id + '_comp_01' + '_180.png')
    #plt.show()
 	
# save out group level results...
#tmp_list = []

# plot a component over all subjects
#components = np.arange(0, 10, 1)
#for component in components:
    #tmp = get_mean(DATA, subject_list, mode, component)
   
#    tmp = get_cov(DATA, DATA_new, subject_list, mode, mode_new, 
#                      comp=component, comp_new=None)    
#    tmp_list.append(tmp)
    
    #data = np.zeros(len(vertices))
    #data[n] = tmp
    #plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    #plt.title('aligned_COV_sulc' +  ' , component ' + str(component+1))   
    #plt.savefig(path_out + 'a_COV_s'+ '_comp_' + str(component+1)+ '.png')


#print "group level matrix shape: ", np.shape(tmp_list)
#f = h5py.File(path + 'test_cov.h5', 'w')
#f.create_dataset('cov', data=np.transpose(np.array(tmp_list)))


