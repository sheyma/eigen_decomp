
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

# load sulc
D = []
for index, row in subfile.iterrows():
	S = nb.load('/a/documents/connectome/_all/%s/MNINonLinear/fsaverage_LR32k/%s.sulc.32k_fs_LR.dscalar.nii' % (str(row[0]),str(row[0])))
	print i 
	D.append(S.data[ind])

D = np.array(D) 

# load embedding
E = []
for index, row in subfile.iterrows():
	S = h5py.File('/nobackup/kocher1/bayrak/hcp_embed_full/embeddings_full_%s.h5' % str(row[0]) , 'r').get('embedding')
	E.append(np.array(S))
	print row[0]

E = np.array(E) 



# load aligned
A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/realigned_100n_468.h5', 'r')
A = np.array(A_init.get('aligned'))


# save group-level matrices:
h = h5py.File('/nobackup/kocher1/bayrak/tmp/sulc_468.h5', 'w')
h.create_dataset('sulc', data=D)
h.close()

#h = h5py.File('/nobackup/kocher1/bayrak/tmp/embeddings_full_468.h5', 'w')
#h.create_dataset('embedding', data=E)
#h.close()


E_in = h5py.File('/nobackup/kocher1/bayrak/tmp/embeddings_full_468.h5', 'r')
E = np.array(E_in.get('embedding'))

D_in = h5py.File('/nobackup/kocher1/bayrak/tmp/sulc_468.h5', 'r')
D = np.array(D_in.get('sulc'))


# Correlate two datasets
C = []
for i in range(np.shape(E)[1]):
	C.append(np.cov(E.T[0][i],D.T[i])[0][1])
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

  
