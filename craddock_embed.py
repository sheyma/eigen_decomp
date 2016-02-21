import pickle
import os, sys
import numpy as np
import h5py
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed
import argparse

## parse command line arguments
parser = argparse.ArgumentParser()
# input prefix for subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("subject_dirs", nargs="+")
parser.add_argument('-o', '--outprfx', required=True)
args = parser.parse_args()

filenames = np.array(args.subject_dirs)

for i in range(0, len(filenames)):
    print "do loop %d/%d, %s" % (i+1, len(filenames), filenames[i])
    f_in = os.path.join(filenames[i], 'matrix.pkl')
    subject_id = os.path.basename(filenames[i])	
    f_out = os.path.join(args.outprfx, subject_id + '_embeddings.h5')		
    print f_out	
    m = pickle.load(open(f_in))['correlation']	
    m += 1.0
    m /= 2.0

    # set NaN entries to ='s    
    m[np.where(np.isnan(m) == True)] = 0
    ind = np.where(np.sum(m, axis=1) != 1)

    embedding, results = embed.compute_diffusion_map(m[ind].T[ind].T, 
                                                     n_components=10)	
    h = h5py.File(f_out, 'w')
    h.create_dataset('embedding', data = embedding)
    h.create_dataset('lambdas', data = results['lambdas'])
    h.create_dataset('vectors', data = results['vectors'])
    h.close()
  
print "loop done!"

