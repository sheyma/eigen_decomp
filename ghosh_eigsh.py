__author__ = 'santra ghosh'

from sklearn.utils.arpack import eigsh
# eigsh => re-released scipy.sparse.linalg.eigsh
from pylab import *
import numpy as np

# diffusion map corrdiantes : DoFiedler
# where conn is a symmetrical connectivity matrix:
def DoFiedler(conn):
    # prep for embedding
    # K : matrix of similarities
    K = (conn + 1) / 2.
    # axis=1 meaning operating over rows, "row sum's of K"
    v = np.sqrt(np.sum(K, axis=1))
    # make a random walk on data, D is diagonal matrix
    D = v[:, None] * v[None, :]
    # row-normalization of K gives transition matrix A => A = D^-1 * K
    A = K/D
    del K
    A = np.squeeze(A * [A > 0])
    # diffusion embedding (original value of n_components_embedding=5)
    n_components_embedding = matrix_rank(A) / 2
    # k must be < rank(A)
    lambdas, vectors = eigsh(A, k=n_components_embedding)
    del A
    # sorting eigenvalues and -vectors in descending order
    lambdas = lambdas[::-1]
    vectors = vectors[:, ::-1]
    psi = vectors/vectors[:, 0][:, None]
    # begin from second largest eigenvalue and
    lambdas = lambdas[1:] / (1 - lambdas[1:])
    embedding = psi[:, 1:(n_components_embedding + 1)] * lambdas[:n_components_embedding][None, :]
    return embedding

# symmetrizing a matrix
def symmetry(a):
    return a + a.T - np.diag(a.diagonal())

tmp = np.random.randn(12, 12)
tmp = symmetry(tmp)
B = DoFiedler(tmp)
