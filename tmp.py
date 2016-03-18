# plot statistics
import pandas as pd
import numpy as np
import h5py
import sys, os
import argparse
#sys.path.append(os.path.expanduser('/u/sbayrak/devel/brainsurfacescripts'))
sys.path.append(os.path.expanduser('/home/sheyma/devel/brainsurfacescripts'))
import plotting

## parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filenames", type=str, nargs="+")
args = parser.parse_args()

filenames = np.array(args.filenames)

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

#path_surface = '/nobackup/kocher1/bayrak/data/'
#path = '/nobackup/kocher1/bayrak/palm_results/'
path = '/home/sheyma/tmp/'
path_surface = '/home/sheyma/tmp/'

surface_data = path_surface + 'data_surface.h5'
hemisphere = 'LH'
surface_type = 'midthickness'
n, vertices, triangles = get_surface(surface_data, hemisphere, surface_type)



for filename in filenames:
    print filename
    DF = pd.read_csv(filename,index_col=False, header=None)
    A = np.array(DF).T
    import matplotlib.pyplot as plt
    plotting.plot_surf_stat_map(vertices, triangles, stat_map=A[:,0], cmap='jet', azim=180)
    plt.title(filename)
    plt.savefig(filename[:-4] + '.png')
        
#filename = '/home/sheyma/tmp/LH_01_dm_01_dpv_ztstat_c1.csv'


