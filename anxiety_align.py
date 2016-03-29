import numpy as np
import h5py
import sys, os
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import align

path = '/nobackup/kocher1/bayrak/math_anxiety/'
#path = '/home/sheyma/tmp/mano_data/'
k = h5py.File(path + 'Data_BT1_embed.h5', 'r')

k_new = h5py.File(path + 'Data_BT1_align.h5', 'w')
k_new = h5py.File(path + 'Data_BT1_align.h5', 'r+')

list_UP = list(k.keys())

for KEY in list_UP: 

    group_UP = k_new.create_group(KEY)
    E = k[KEY]    
    list_LOW = list(E.keys())

    for key in list_LOW:

        
        embeddings = np.array(E[key]['embedding'])        
        realigned, xfms = align.iterative_alignment(embeddings, n_iters=1000)
        realigned = np.array(realigned)
        print KEY, key, embeddings.shape, realigned.shape
        group_UP.create_dataset(key, data=realigned)

k_new.close()
