import numpy as np
import h5py
import sys, os
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed

# convert -v5 to -v7.3 on MATLAB like following:
# load('Data_BT1.mat');
# save('copyData_BT1.mat', '-v7.3')
path = '/home/sheyma/tmp/mano_data/'
h = h5py.File(path + 'Data_BT1_v73.mat', 'r')

list_UP = list(h.keys())

h_new = h5py.File(path + 'Data_BT1_embed.h5', 'w')
h_new = h5py.File(path + 'Data_BT1_embed.h5', 'r+')

for KEY in list_UP:
    L = h[KEY]
    print L
    group_UP = h_new.create_group(KEY)
   
    list_lower = list(L.keys())
    print list_lower
    
    for key in list_lower:
        print "create group: ", key
        grp = group_UP.create_group(key)
        tmp = np.array(L[key])
        
        embeddings = []
        lambdas = []	
        vectors = []    
        
        for i in range(0, tmp.shape[0]):
            embedding, results = embed.compute_diffusion_map(tmp[i,:,:], 
                                                             n_components=10)
            embeddings.append(embedding)
            lambdas.append(results['lambdas'])
            vectors.append(results['vectors'])        
        
        embeddings = np.array(embeddings)  	
        lambdas = np.array(lambdas)
        vectors = np.array(vectors)    
        grp.create_dataset('embedding', data=embeddings)
        grp.create_dataset('lambdas', data=lambdas)
        grp.create_dataset('vectors', data=vectors[:,:,1:tmp.shape[0]])

h_new.close()


