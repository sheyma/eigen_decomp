import nibabel as nb
from nibabel import gifti
import numpy as np
import h5py 
import sys
import os
sys.path.append(os.path.expanduser('/u/sbayrak/devel/brainsurfacescripts'))
#sys.path.append(os.path.expanduser('/home/raid/bayrak/devel/brainsurfacescripts'))

import plotting
import argparse

## begin parse command line arguments
parser = argparse.ArgumentParser()

# output prefix, e.g. /ptmp/sbayrak/hcp_embed_figures/
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp_embed/*
parser.add_argument("subject",nargs="+")

args = parser.parse_args()
## end parse command line arguments

#surf = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.R.midthickness.32k_fs_LR.surf.gii')
surf = gifti.giftiio.read('/u/sbayrak/devel/topography/data/Q1-Q6_R440.R.midthickness.32k_fs_LR.surf.gii')

vertices = np.array(surf.darrays[0].data, dtype=np.float64)
triangles = np.array(surf.darrays[1].data, dtype=np.int32)

data = np.zeros(len(vertices))

# get the indices
img = nb.load('/ptmp/sbayrak/hcp/100307/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
#img = nb.load('/a/documents/connectome/_all/100307/MNINonLinear/Results/rfMRI_REST1_LR/rfMRI_REST1_LR_Atlas_hp2000_clean.dtseries.nii')
n = img.header.matrix.mims[1].brainModels[1].vertexIndices.indices

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

    ind = np.where(np.sum(L_embed, axis=1) != 1)
    data[n[ind]] = L_embed[:,0] 

    plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, azim=180)
    import matplotlib.pyplot as plt
    plt.title(subject_basename)
    #plt.show()
    plt.savefig(args.outprfx + subject_basename[:-3] + '.png')

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
