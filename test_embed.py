import matplotlib.pyplot as pl
import numpy as np
import os
import nibabel as nib
import sys

satra_path = sys.path.append('/home/raid/bayrak/devel/mapalign/mapalign')

import embed

tmp_mtx = np.random.randint(1, 10, (10, 10)) / float(10)
tmp_mtx += tmp_mtx.T - np.diag(tmp_mtx.diagonal())

embed.compute_diffusion_map(tmp_mtx, alpha=0, n_components=5, diffusion_time=0)

data_path = '/a/documents/connectome/_all'
subject = '../q5/965771/MNINonLinear/T1w.nii.gz'

example_filename = os.path.join(data_path, subject)
img = nib.load(example_filename)

print "class of data: ", type(img)
print "shape of data: ", img.shape
print "type of data: ", img.get_data_dtype()

img_new = img.get_data()

def show_slices(slices):
    fig, axes = pl.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        print slice.shape
        axes[i].imshow(slice.T, cmap='gray', origin="lower")

# sclices are numpy arrays
slice_0 = img_new[:, 10, :]
slice_1 = img_new[:, 50, :]
slice_2 = img_new[:, 70, :]

show_slices([slice_0, slice_1, slice_2])
pl.suptitle("bla")
#pl.show()

