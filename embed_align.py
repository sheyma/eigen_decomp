# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:03:07 2015

@author: bayrak
"""

import os, argparse, sys, h5py, numpy as np, glob
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed, align
import hcp_corr

# Load all embedding variables across subjects as arrays:
embeddings = [] 
filelist = []
i = 1
for f in glob.glob('/nobackup/kocher1/bayrak/hcp_embed/embedding_*.h5'):
    d = np.array(h5py.File(f, 'r').get('embedding'))
    if (29696 == d.shape[0] and i < 11):
        embeddings.append(d)
        filelist.append(f)
        print os.path.basename(f)        
        #print d.shape[0]        
        i += 1
    #else: 
        #print "bad subject: ", os.path.basename(f)
        #os.path.basename(f)
        #print f
# Realign embeddings across subjects
realigned, xfms = align.iterative_alignment_with_coords(embeddings, 
                                                        coords=None, 
                                                        n_iters=1, 
                                                        n_samples=0.1, 
                                                        use_mean=False)





