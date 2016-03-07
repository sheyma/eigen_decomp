# plot statistics
import pandas as pd
import numpy as np
import csv
import h5py
#sys.path.append(os.path.expanduser('/u/sbayrak/devel/brainsurfacescripts'))
sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))
import plotting

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

path_surface = '/nobackup/kocher1/bayrak/data/'
path = '/nobackup/kocher1/bayrak/palm_results/'


subject_list = []
with open(path_surface + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

surface_data = path_surface + 'data_surface.h5'
hemisphere = 'LH'
surface_type = 'midthickness'
n, vertices, triangles = get_surface(surface_data, hemisphere, surface_type)


DF = pd.read_csv(path + 'LH_01_dm_01_dpv_ztstat_c1.csv',
                 index_col=False, header=None)
A = np.array(DF).T



# JULIA
import matplotlib.pyplot as plt
plotting.plot_surf_stat_map(vertices, triangles, stat_map=A[:,0], cmap='jet', azim=180)
plt.colorbar()
plt.show()

plotting._get_plot_stat_map_params(stat_map_data=A[:,0])


# SABINE
#plotting.create_fig(data=A[0])

