
import numpy as np
import h5py
import pandas as pd
import nibabel as nb
import sys
import os
import plotting
from nibabel import gifti

sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))

subfile = pd.read_csv('/nobackup/kocher1/bayrak/subject_list.csv', header=None)

# Specify the hemisphere data
file_name = '/nobackup/kocher1/bayrak/data_full.h5'
ind = np.array(h5py.File(file_name, 'r').get('indices'))
vertices = np.array(h5py.File(file_name, 'r').get('vertices'))
triangles = np.array(h5py.File(file_name, 'r').get('triangles'))


# load embedding
E_in = h5py.File('/nobackup/kocher1/bayrak/tmp/embeddings_full_468.h5', 'r')
E = np.array(E_in.get('embedding'))

# load aligned
A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/realigned_full_n10_468.h5', 'r')
A = np.array(A_init.get('aligned'))

# load sulc
D_in = h5py.File('/nobackup/kocher1/bayrak/tmp/sulc_full_468.h5', 'r')
D = np.array(D_in.get('sulc'))

# get first component
A = A[:,:,0]

# Correlate two datasets
C = []
for i in range(np.shape(A)[1]):
    # covariance of one region (over subjects) in two datasets
    C.append(np.cov(A[:,i],D[:,i])[0][1])
    print i
C = np.array(C)


# Vizualize data:
data = np.zeros(len(vertices))
data[ind] = C
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=0)
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=90)
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=180)
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=270)
plt.show()

  
