import numpy as np
import sys
import os
import scipy
import sklearn
import csv
print "aaaa scipy", scipy.__version__
print "bbbb numpy", np.__version__
print "ccccc sklearn", sklearn.__version__

satra_path = sys.path.append('/u/sbayrak/devel/mapalign/mapalign')
import embed 

subject = sys.argv[1]
# e.g. /ptmp/sbayrak/hcp_prep_out/100307......

out_path = '/ptmp/sbayrak/embed_out'
# set as local output directory (HYDRA)

# a replacement for numpy.loadtxt() which used 5 times more memory than needed
def load_matrix(file):
    n = -1
    with open(file, 'r') as f:
        reader = csv.reader(f,'excel-tab')
        for i, row in enumerate(reader):
            if n < 0:
                n = len(row)
                b = np.zeros((n,n))
            b[i,:] = np.array(row)
    return b

L = load_matrix(subject)

def save_output(subject, embed_matrix):
    out_dir = os.path.join(out_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = os.path.basename(subject[27:33]) + '_embed_out.csv'
    print filename
    out_file = os.path.join(out_dir, filename)
    # %.e = Floating point exponential format (lowercase)
    np.savetxt(out_file, embed_matrix, fmt='%5.5e', delimiter='\t', newline='\n')
    return out_file

embedding, result = embed.compute_diffusion_map(L, alpha=0, n_components=5, 
diffusion_time=0, skip_checks=True, overwrite=True)

save_output(subject, embedding)

print result['lambdas']

