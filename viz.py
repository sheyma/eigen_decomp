"""
load embedding components
load indices, triangles, vertices of surface
plot embedding component on brain template
"""

import numpy as np
import h5py 
import sys
import os
import pandas as pd
#sys.path.append(os.path.expanduser('/u/sbayrak/devel/brainsurfacescripts'))
sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))

import plotting
import argparse

## begin parse command line arguments
parser = argparse.ArgumentParser()
# data input prefix, e.g. /ptmp/sbayrak/
parser.add_argument('-hem', '--hemisphere', required=True)
# output prefix, e.g. /ptmp/sbayrak/hcp_embed_figures/
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp_embed/*
parser.add_argument("subject",nargs="+")
## end parse command line arguments
args = parser.parse_args()

if args.hemisphere == 'LH':
    file_name = '/ptmp/sbayrak/data_LH.h5'
elif args.hemisphere == 'RH':
    file_name = '/ptmp/sbayrak/data_RH.h5'
elif args.hemisphere == 'full':
    file_name = '/ptmp/sbayrak/data_full.h5'
    file_name = '/nobackup/kocher1/bayrak/data_full.h5'


# get surface data for corresponding hemisphere    

n = np.array(h5py.File(file_name, 'r').get('indices'))
vertices = np.array(h5py.File(file_name, 'r').get('vertices'))
triangles = np.array(h5py.File(file_name, 'r').get('triangles'))

data = np.zeros(len(vertices))

subfile = pd.read_csv('/NOBACKUP/bayrak/subject_list.csv', header=None)
A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/realigned_full_n10_468.h5', 'r')
A = np.array(A_init.get('aligned'))

A_init = h5py.File('/nobackup/kocher1/bayrak/tmp/RcovS_468.h5', 'r')
A = np.array(A_init.get('cov'))


for index, row in subfile.iterrows():
    print index, row[0]
    data[n] = A[index]
    plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    import matplotlib.pyplot as plt
    plt.title(index)
    plt.show()
    #plt.savefig(args.outprfx + index + '_000_jet.png')

# get embedding component
subject_list = np.array(args.subject)
N =len(subject_list)

print "n shape : ", np.shape(n)

for i in range(0, N):
    subject = subject_list[i]
    print "plot subject %d/%d, %s" % (i+1, N, subject)
    subject_basename = os.path.basename(subject)
    
    Lin = h5py.File(subject, 'r')
    L_embed = Lin.get('embedding')
    L_embed = np.array(L_embed)

    # ind = np.where(np.sum(L_embed, axis=1) != 1)
    # data[n[ind]] = L_embed[:,0]

    data[n] = L_embed[:,0] 

    plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)
    import matplotlib.pyplot as plt
    plt.title(subject_basename)
    #plt.show()
    plt.savefig(args.outprfx + subject_basename[:-3] + '_000_jet.png')


import nibabel as nb
from nibabel import gifti 
#surf = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii')
#surf_L = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.inflated.32k_fs_LR.surf.gii')
surf_L = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.very_inflated.32k_fs_LR.surf.gii')
#surf_R = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.R.inflated.32k_fs_LR.surf.gii')
surf_R = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.R.very_inflated.32k_fs_LR.surf.gii')
#surf = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.R.midthickness.32k_fs_LR.surf.gii')

v_left = np.array(surf_L.darrays[0].data, dtype=np.float64)
t_left = np.array(surf_L.darrays[1].data, dtype=np.int32)

v_right = np.array(surf_R.darrays[0].data, dtype=np.float64)
t_right = np.array(surf_R.darrays[1].data, dtype=np.int32)

#img = nb.load('/ptmp/sbayrak/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
img = nb.load('/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')

n_left = img.header.matrix.mims[1].brainModels[0].vertexIndices.indices
n_right = img.header.matrix.mims[1].brainModels[1].vertexIndices.indices

N = np.concatenate((n_left, n_right+32492))
triangles = np.concatenate((t_left, t_right+32492))
vertices = np.concatenate((v_left, v_right))


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

data = np.zeros(len(vertices))
data[N] = A
plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=180)




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
