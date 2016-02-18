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
parser.add_argument("subject_dirs",nargs="+")
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)

args = parser.parse_args()

filenames = np.array(args.subject_dirs)

for i in range(0, len(filenames)):
    print "do loop %d/%d, %s" % (i+1, len(filenames), filenames[i])
print "loading data - loop done"


f = 'ptmp/sbayrak/franz_data/LI00000031/matrix.pkl'
m = pickle.load((open(f)))['correlation']

m += 1.0
m /= 2.0

embedding, result = embed.compute_diffusion_map(m , n_components=10)

h = h5py.File(f, 'w')
h.create_dataset('embedding', data = embedding)
h.create_dataset('result', data = result)
h.close()

