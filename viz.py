import nibabel as nb
from nibabel import gifti
import numpy as np
import h5py 
import sys
import os
sys.path.append(os.path.expanduser('~/devel/eigen_decomp'))

# get embedding component
Lin = h5py.File('/var/tmp/embedding_959574.h5')
L_embed = Lin.get('embedding')
L_embed = np.array(L_embed)

surf = gifti.giftiio.read('/home/sheyma/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii')
vertices = np.array(surf.darrays[0].data, dtype=np.float64)
triangles = np.array(surf.darrays[1].data, dtype=np.int32)

# get the indices
img = nb.load('/var/tmp/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
n = img.header.matrix.mims[1].brainModels[0].vertexIndices.indices

data = np.zeros(len(vertices))
data[n] = L_embed[:,0] 

import plot_J
plt = plot_J.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=180)
plt.show()




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
