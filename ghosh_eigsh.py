__author__ = 'santra ghosh'

from sklearn.utils.arpack import eigsh
# eigsh => re-released scipy.sparse.linalg.eigsh
from pylab import *
import numpy as np

# where conn is a symmetrical connectivity matrix:
def DoFiedler(conn):
    # prep for embedding
    K = (conn + 1) / 2.
    # axis=1 meaning operating over rows
    v = np.sqrt(np.sum(K, axis=1))
    A = K/(v[:, None] * v[None, :])
    del K
    A = np.squeeze(A * [A > 0])
    print "ASze" , np.shape(A)
    # diffusion embedding (original value of n_components_embedding=5)
    n_components_embedding = matrix_rank(A, tol=None)/2
    print "n_comp" , n_components_embedding
    # k must be < rank(A)
    lambdas, vectors = eigsh(A, k=n_components_embedding)
    del A
    print  "lambda_before", lambdas
    # sorting eigenvalues and -vectors in descending order
    lambdas = lambdas[::-1]
    print "lambda_aft", lambdas
    vectors = vectors[:, ::-1]
    psi = vectors/vectors[:, 0][:, None]
    # begin from second largest eigenvalue and ?
    lambdas = lambdas[1:] / (1 - lambdas[1:])
    embedding = psi[:, 1:(n_components_embedding + 1)] * lambdas[:n_components_embedding][None, :]
    #print "embedding" , embedding
    return embedding

def symmetrize(matrix):
    return matrix + matrix.T - np.diag(matrix.diagonal())


A = np.random.randn(12,12)
A = symmetrize(A)
B = DoFiedler(A)
