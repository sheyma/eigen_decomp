import h5py
import numpy as np
import csv

path = '/ptmp/sbayrak/tmp/'
path01 = '/ptmp/sbayrak/smoothing_new/'

subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

k = h5py.File(path + '468_smoothing_new.h5', 'w')
k = h5py.File(path + '468_smoothing_new.h5', 'r+')

for subject_id in subject_list:
    subject_id = ''.join(subject_id)
    print subject_id
    tmp_name = path01 + subject_id +'_smooth_59412.h5'    
    tmp = np.array(h5py.File(tmp_name, 'r')['smooth'])
    
    group_k = k.create_group(subject_id)
    group_k.create_dataset('smooth', data = tmp)

k.close()


#tmp = h5py.File(path + '468_smoothing.h5', 'r')

#for name in tmp:
#    print tmp[name], tmp[name].keys()


