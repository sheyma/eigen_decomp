# run PALM...

import sys, os
import csv

sys.path.append(os.path.expanduser('/home/raid/bayrak/src/PALM'))
os.system('./palm')

# load a certain component for each subject and save as .csv





./palm -i ~/tmp/data_lh.csv -s ~/devel/topography/data/lh.pial -d ~/tmp/design_matrix.csv -t test.con -n 1000 -o myresults/second_run  -zstat -fdr -logp

path = '/home/raid/bayrak/tmp/'

# read-in subject_list
subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);


# save out group level results...
tmp_list = []

# plot a component over all subjects
components = np.arange(0, 10, 1)
for component in components:
    #tmp = get_mean(DATA, subject_list, mode, component)
   
    tmp = get_cov(DATA, DATA_new, subject_list, mode, mode_new, 
                      comp=component, comp_new=None)    
    tmp_list.append(tmp)