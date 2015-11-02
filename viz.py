# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 23:36:09 2015

@author: bayrak
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 23:18:25 2015

@author: bayrak
"""


from nibabel import gifti
surf = gifti.giftiio.read('/nobackup/kocher1/bayrak/embed_out/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii')
vertices = np.array(surf.darrays[0].data, dtype=np.float64)
triangles = np.array(surf.darrays[1].data, dtype=np.int32)

import nibabel as nb
img = nb.load('/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
n = img.header.matrix.mims[1].brainModels[0].vertexIndices.indices

data = np.zeros(len(vertices))
import h5py
A = h5py.File('/nobackup/kocher1/bayrak/embed_out/LH_node_average.h5', 'r')
L = A.get('sum')

data[n] = L[20015]

data[n] = L[:][10015]

from mayavi import mlab

mlab.triangular_mesh(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles, scalars=data)

import numpy as np

b = np.loadtxt('/nobackup/kocher1/bayrak/embed_out/daniel_embedding.csv')


def vizData(a, n, num):
    data = np.zeros(len(vertices))
    data[n] = a[:,num]
    mlab.triangular_mesh(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles, scalars=data)
    
vizData(a,n,0)
