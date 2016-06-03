import sys, h5py, os
import pandas as pd
import numpy as np
import scipy
import scipy.spatial as sp
from scipy import io
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
sys.path.append(os.path.expanduser('~/devel/mapalign/'))
from mapalign import embed, dist, align
import nibabel as nib
import nibabel.gifti
sys.path.append(os.path.expanduser('~/devel/brainsurfacescripts'))
from plotting import plot_surf_stat_map, _get_plot_stat_map_params

#from nibabel import gifti 
#surf = gifti.giftiio.read('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii')
#vertices = np.array(surf.darrays[0].data, dtype=np.float64)
#triangles = np.array(surf.darrays[1].data, dtype=np.int32)

surfmL = nib.freesurfer.read_geometry('/home/raid/bayrak/devel/topography/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf')

bla = '/nobackup/kocher1/bayrak/data/Q1-Q6_R440.L.midthickness.32k_fs_LR.surf.gii'