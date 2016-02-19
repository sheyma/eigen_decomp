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
args = parser.parse_args()

filenames = np.array(args.subject_dirs)

for i in range(0, len(filenames)):
    print "do loop %d/%d, %s" % (i+1, len(filenames), filenames[i])
    f_in = os.path.join(filenames[i], 'matrix.pkl')
    f_out = os.path.join(filenames[i], 'embedding.h5')		
    m = pickle.load(open(f_in))['correlation']	
    m += 1.0
    m /= 2.0
    embedding, results = embed.compute_diffusion_map(m , 
  						    n_components=10)	
    h = h5py.File(f_out, 'w')
    h.create_dataset('embedding', data = embedding)
    h.create_dataset('lambdas', data = results['lambdas'])
    h.create_dataset('vectors', data = results['vectors'])
    h.close()
  
print "loop done!"

