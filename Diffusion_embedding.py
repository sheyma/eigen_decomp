
import sys, numpy as np, h5py 
import os
sys.path.append("utils_py/mapalign")
sys.path.append(os.path.expanduser('~/devel/mapalign'))
import embed

A = h5py.File('/ptmp/sbayrak/test_daniel/matrix_hcp_cortex_lh.mat','r') 
L = A.get('matrix') 
L = np.array(L)
#cortex = A.get('cortex') 
#cortex = np.array(cortex)

keep = list(np.where(sum(L) != 0))

embedding, result = embed.compute_diffusion_map(L[keep].T[keep].T, alpha=0.5, n_components=5, diffusion_time=0,
                          skip_checks=False, overwrite=False)

print result['lambdas']
print "embedding done!"


out_pfrx = "/ptmp/sbayrak/test_daniel_"
out_prec = "%g"
np.savetxt(out_pfrx + "embedding_01.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_pfrx + "lambdas_01.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_pfrx + "vectors_01.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
