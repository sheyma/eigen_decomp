"""
1) load NKI data of corr matrices
1) manipulate negative values
2) diffusion embedding on corr matrices
"""
import nibabel as nb
import numpy as np
import sys
import os
import h5py
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed
import argparse
from sklearn.manifold.spectral_embedding_ import _graph_is_connected


# begin parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--abs', action='store_false')
#parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/nki_data/*
parser.add_argument("subject",nargs="+")
#
args = parser.parse_args()
# end parse command line arguments

subject_list = np.array(args.subject)

N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    subject_basename = os.path.basename(subject)
    print "do loop %d/%d, %s" % (i+1, N, subject)

    
    #name = '/scr/namibia1/Data/fsa4_corr/subs_243.nii'
    A = nb.load(subject)
    K = A.get_data()
    K = np.array(K)
    K = K[:,:,0]
    print type(K), K.shape

    if args.abs:
        K[np.where(K<0)] = 0 
        K[np.where(K==0)] = 1e-24
        
    #else:
    #    K[np.where(K < 0)] = 0     


    if not _graph_is_connected(K):
        raise ValueError('Graph is disconnected')


#    embedding, result = embed.compute_diffusion_map(K, 
#                                                   n_components=10,
#                                                   skip_checks=True)
#
#    name = 'embeddings_' + args.hem + '_' + subject_basename + '.h5'
#
#    outfile = os.path.join(args.outprfx, name)
# 
#    print "outfile : ", outfile
#    h = h5py.File(outfile , 'w')
#    print outfile
#    h.create_dataset('embedding', data=embedding)
#    h.create_dataset('lambdas', data=result['lambdas'])
#    h.create_dataset('vectors', data=result['vectors'])
#    h.close()

#print "loop done!"
