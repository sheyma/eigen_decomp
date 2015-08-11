import numpy as np
import sys

satra_path = sys.path.append('/home/raid/bayrak/devel/mapalign/mapalign')

import embed

tmp_mtx = np.random.randint(1, 10, (8000, 8000)) / float(100)
tmp_mtx += tmp_mtx.T - np.diag(tmp_mtx.diagonal())

print tmp_mtx.shape
#np.savetxt('test_matrix.csv', tmp_mtx, fmt='%5.5e', delimiter='\t', newline='\n')


#csv = np.loadtxt('test_matrix.csv')

#print csv

embedding, result = embed.compute_diffusion_map(tmp_mtx, alpha=0, n_components=5, diffusion_time=0)



# data_path = '/a/documents/connectome/_all'
# subject = '../q5/965771/MNINonLinear/T1w.nii.gz'
#
# example_filename = os.path.join(data_path, subject)
# img = nib.load(example_filename)
#
# print "class of data: ", type(img)
# print "shape of data: ", img.shape
# print "type of data: ", img.get_data_dtype()
#
# img_new = img.get_data()
#
# def show_slices(slices):
#     fig, axes = pl.subplots(1, len(slices))
#     for i, slice in enumerate(slices):
#         print slice.shape
#         axes[i].imshow(slice.T, cmap='gray', origin="lower")
#
# # sclices are numpy arrays
# slice_0 = img_new[:, 10, :]
# slice_1 = img_new[:, 50, :]
# slice_2 = img_new[:, 70, :]
#
# show_slices([slice_0, slice_1, slice_2])
# pl.suptitle("bla")
# #pl.show()

