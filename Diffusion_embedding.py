
import sys, numpy as np, h5py 
import os
sys.path.append("utils_py/mapalign")
sys.path.append(os.path.expanduser('~/devel/mapalign'))
from mapalign import embed, dist, align

A = h5py.File('matrix_hcp_cortex_lh.mat','r') 
L = A.get('matrix') 
L = np.array(L)
cortex = A.get('cortex') 
cortex = np.array(cortex)

keep = list(np.where(sum(L) != 0))

embedding, result = embed.compute_diffusion_map(L[keep].T[keep].T, alpha=0.5, n_components=5, diffusion_time=0,
                          skip_checks=False, overwrite=False)

from scipy.io import savemat
savemat('embed_hcp_cortex.lh.mat',{'embedding': embedding, 'result': result, 'keep': keep})