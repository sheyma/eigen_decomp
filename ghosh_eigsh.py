__author__ = 'santra ghosh'

from sklearn.utils.arpack import eigsh
# eigsh => re-released scipy.sparse.linalg.eigsh
from pylab import *
import numpy as np

# diffusion map corrdiantes : DoFiedler
# where conn is a symmetrical connectivity matrix:
def DoFiedler(conn):
    # prep for embedding
    # K : matrix of similarities / Kernel matrix / Gram matrix
    # make conn non-negative, -1<since conn<1
    K = (conn + 1) / 2.
    # axis=1 meaning operating over rows, "row sum's of K"
    v = np.sqrt(np.sum(K, axis=1))
    # make a random walk on data, D is diagonal matrix
    D = v[:, None] * v[None, :]
    # row-normalization of K gives transition matrix A => A = D^-1 * K
    A = K/D
    del K
    A = np.squeeze(A * [A > 0])
    n_components_embedding = 5
    lambdas, vectors = eigsh(A, k=n_components_embedding)
    del A
    # sorting eigenvalues and -vectors in descending order
    lambdas = lambdas[::-1]
    vectors = vectors[:, ::-1]
    psi = vectors/vectors[:, 0][:, None]
    # begin from second largest eigenvalue and corr. eigenvector
    lambdas = lambdas[1:] / (1 - lambdas[1:])
    embedding = psi[:, 1:(n_components_embedding + 1)] * lambdas[:n_components_embedding][None, :]
    return embedding

# symmetrizing a matrix
def symmetry(a):
    return a + a.T - np.diag(a.diagonal())

tmp = np.random.randn(10, 10)
tmp = symmetry(tmp)
B = DoFiedler(tmp)
