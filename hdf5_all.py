import h5py
import numpy as np
import pandas as pd

pathway = '/ptmp/sbayrak/tmp/'

# get subject list
subfile = pd.read_csv(pathway + 'subject_list.csv', header=None)

# get all embeddings as array
E = np.array(h5py.File(pathway + 'embeddings_full_468.h5', 'r').get('embedding'))
# get all realignments as array
A = np.array(h5py.File(pathway + 'realigned_full_n10_468.h5', 'r').get('aligned'))
# get sulc as array
S=np.array(h5py.File(pathway + 'sulc_full_468.h5', 'r').get('sulc'))

f = h5py.File(pathway + '468_embeddings.h5', 'w')
f = h5py.File(pathway + '468_embeddings.h5', 'r+')

g = h5py.File(pathway + '468_alignments.h5', 'w')
g = h5py.File(pathway + '468_alignments.h5', 'r+')

h = h5py.File(pathway + '468_sulcs.h5', 'w')
h = h5py.File(pathway + '468_sulcs.h5', 'r+')

for index, row in subfile.iterrows():
	group_E = f.create_group( str(row[0]) )
        group_E.create_dataset('embedding', data = E[index])

	group_A = g.create_group( str(row[0]) )
        group_A.create_dataset('aligned', data = A[index])

	group_S = h.create_group( str(row[0]) )
        group_S.create_dataset('sulc', data = S[index])

f.close()
g.close()
h.close()

k = h5py.File(pathway + '468_eas.h5', 'w')
k = h5py.File(pathway + '468_eas.h5', 'r+')

for index, row in subfile.iterrows():
        group = k.create_group( str(row[0]) )
        group.create_dataset('embedding', data = E[index])
        group.create_dataset('aligned', data = A[index])
	group.create_dataset('sulc', data = S[index])

k.close()

tmp = h5py.File(pathway + '468_eas.h5', 'r')

for name in tmp:
    print tmp[name], tmp[name].keys()


