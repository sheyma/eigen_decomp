
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

# load 'ind' which are the indices to grap from the sulc file corresponding here to the LH
img = nb.load('/ptmp/sbayrak/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
ind = img.header.matrix.mims[1].brainModels[0].vertexIndices.indices
surf = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii')
vertices = np.array(surf.darrays[0].data, dtype=np.float64)
triangles = np.array(surf.darrays[1].data, dtype=np.int32)

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
	S = h5py.File('/nobackup/kocher1/bayrak/hcp_embed/embedding_%s.h5' % str(row[0]) , 'r').get('embedding')
	E.append(np.array(S))
	print row[0]

E = np.array(E) 

# load aligned
A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/aligned_468.h5', 'r')
A = A_init.get('rel')
A = np.array(A)

# save group-level matrices:
h = h5py.File('/nobackup/kocher1/bayrak/hcp_embed/sulc_468.h5', 'w')
h.create_dataset('sulc', data=D)
h.close()

h = h5py.File('/nobackup/kocher1/bayrak/hcp_embed/embedding_468.h5', 'w')
h.create_dataset('embedding', data=E)
h.close()


# Correlate two datasets
C = []
for i in range(np.shape(E)[1]):
	C.append(np.cov(E.T[0][i],D.T[i])[0][1])
	print i
C = np.array(C)

# Vizualize data:
data = np.zeros(32492)
data[ind] = C
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=180)
plt.show()
plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=0)
plt.show()

  
