import numpy as np
import h5py
import sys
import os
sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))
import plotting
import csv
import re
import matplotlib.pyplot as plt

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


surface_data = '/nobackup/kocher1/bayrak/tmp/' + 'data_surface.h5'
surface_type = 'midthickness'

n_lh, vertices_lh, triangles_lh = get_surface(surface_data, 'LH', surface_type)

n_rh, vertices_rh, triangles_rh = get_surface(surface_data, 'RH', surface_type)

path = '/nobackup/kocher1/bayrak/palm_results_SCPTs_NEW/'
fig_path = '/nobackup/kocher1/bayrak/palm_figures_SCPTs_NEW/'

results_list = []
with open(path + 'results_unique.csv', 'rb') as f:
    reader = csv.reader(f);
    results_list = list(reader);

fig_number = 1;
for result in results_list:
    result =  str(result)
    
    name_tmp = result[2:-2]
    name_tmp = re.sub('01', '04', name_tmp)    
    
    nameL1 = re.sub('c1', 'c1', name_tmp)
    nameL2 = re.sub('c1', 'c2', nameL1)
    nameR1 = re.sub('LH', 'RH', nameL1)
    nameR2 = re.sub('LH', 'RH', nameL2)    
    
    fig_name = re.sub("LH_", "", nameL1)
    
    print nameL1
    print nameL2
    print nameR1
    print nameR2
    
    #    nameL1 = 'LH_01_dpv_ztstat_cfdrp_c3.csv'

    L1 = np.loadtxt(os.path.join(path, nameL1), delimiter = ',') 
    L2 = np.loadtxt(os.path.join(path, nameL2), delimiter = ',')
    R1 = np.loadtxt(os.path.join(path, nameR1), delimiter = ',')
    R2 = np.loadtxt(os.path.join(path, nameR2), delimiter = ',')


    x = np.ones(len(vertices_lh))
    index = np.where(L1[n_lh] < 0.05)
    index_neg = np.where(L2[n_lh] < 0.05)
    if set(index[0]).intersection(index_neg[0]).__len__() != 0:
        print "OVERLAP"
    

    x[n_lh[index]] = L1[n_lh[index]]       
    x[n_lh[index_neg]] = -1 * L2[n_lh[index_neg]]

    print np.shape(index)[1], np.shape(index_neg)[1]

    
    if np.shape(index)[1] != 0 and np.shape(index_neg)[1] != 0:

        x[np.where(x==1)] = x[n_lh[index]].max() + 0.001

        
        plotting.plot_surf_stat_map(vertices_lh, triangles_lh, fig_number, 
                                    '221', stat_map = x, cmap='jet', azim=180, 
                                    threshold=x[n_lh[index]].max(), 
                                    figsize=(14, 10))
    
        plotting.plot_surf_stat_map(vertices_lh, triangles_lh, fig_number, 
                                    '223', stat_map = x, cmap='jet', azim=0, 
                                    threshold=x[n_lh[index]].max(), 
                                    figsize=(14, 10))
                               
    del index, index_neg

    y = np.ones(len(vertices_rh))        
    index = np.where(R1[n_rh] < 0.05)
    index_neg = np.where(R2[n_rh] < 0.05)
    if set(index[0]).intersection(index_neg[0]).__len__() != 0:
        print "OVERLAP" 

    y[n_rh[index]] = R1[n_rh[index]]
    y[n_rh[index_neg]] = -1 * R2[n_rh[index_neg]]
    
    print np.shape(index)[1], np.shape(index_neg)[1]
    
    if np.shape(index)[1] != 0 and np.shape(index_neg)[1] != 0:
        
        y[np.where(y==1)] = y[n_rh[index]].max() + 0.001

        plotting.plot_surf_stat_map(vertices_rh, triangles_rh, fig_number, 
                                    '222', stat_map = y, cmap='jet', azim=0, 
                                    threshold=y[n_rh[index]].max(), 
                                    figsize=(14, 10))
    
        plotting.plot_surf_stat_map(vertices_rh, triangles_rh, fig_number, 
                                    '224', stat_map = y, cmap='jet', azim=180, 
                                    threshold = y[n_rh[index]].max(), 
                                    figsize=(14, 10))
        plt.suptitle(fig_name)
        plt.savefig(fig_path + fig_name[:-4] + '.png')
    fig_number += 1
    