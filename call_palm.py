# run PALM...

import h5py
import csv
import pandas as pd
import numpy as np
import glob
import os
from subprocess import call

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A

def get_surface(surface_data, hemisphere, surface_type):
    """
    surface_data = hdf5 formatted surface data
    hemisphere = 'LH', 'RH', or 'full'
    surface_type = 'midthickness', 'inflated', or 'very_inflated'
    """
    tmp = h5py.File(surface_data, 'r')
    indices = np.array( tmp[hemisphere][surface_type]['indices'] )
    vertices = np.array( tmp[hemisphere][surface_type]['vertices'] )    
    triangles = np.array( tmp[hemisphere][surface_type]['triangles'])
    
    return indices, vertices, triangles


def get_csv(DATA, subject_list, mode, components, n, n_LH, n_RH, vertices,
            vertices_LH, vertices_RH, path_out):
                
    for component in components:
        print "loop for component ", component + 1
    
        DATA_all = []
        
        for subject_id in subject_list:
            subject_id = ''.join(subject_id)
            subject_component = choose_component(DATA, subject_id, 
                                                 mode, component)
            DATA_all.append(subject_component)
        
        DATA_all = np.array(DATA_all)
        DATA_LH = DATA_all[:, 0:len(n_LH)]
        DATA_RH = DATA_all[:, len(n_LH):len(n_RH)+len(n_LH)]
        
        data_all = np.zeros((len(subject_list), len(vertices)))
        data_LH = np.zeros((len(subject_list), len(vertices_LH)))
        data_RH = np.zeros((len(subject_list), len(vertices_RH)))
        
        data_all[:, n] = DATA_all
        data_LH[:, n_LH] = DATA_LH
        data_RH[:, n_RH] = DATA_RH
        
        if component != 9:
            name_LH = path_out+'Sdata_32492_left_0'+str(component+1)+'.csv'    
            name_RH = path_out+'Sdata_32492_right_0'+str(component+1)+'.csv'
        else:
            name_LH = path_out+'Sdata_32492_left_'+str(component+1)+'.csv'    
            name_RH = path_out+'Sdata_32492_right_'+str(component+1)+'.csv'
            
        tmp_LH = pd.DataFrame(data_LH)
        tmp_LH.to_csv(name_LH, header=False, index=False)
        
        tmp_RH = pd.DataFrame(data_RH)
        tmp_RH.to_csv(name_RH, header=False, index=False)

    return


def callPalm(input_file, surface_file, iteration, design_matrix,
             contrast_matrix, output_file):
                 
    retcode = call(["palm", "-i", input_file, "-s", surface_file,
                    "-n", str(iteration), "-approx",  "tail",  
                    "-o", output_file, "-zstat", "-fdr", 
                    "-d", design_matrix,  "-t",  contrast_matrix, 
                    "-corrcon", "-corrmod", "-T", "-tfce2D"])
    return retcode 

surface_data = 'data/data_surface.h5'
surface_type = 'midthickness'

hemisphere = 'full'
n, vertices, triangles = get_surface(surface_data, 
                                     hemisphere, surface_type)
hemisphere = 'LH'
n_LH, vertices_LH, triangles_LH = get_surface(surface_data, 
                                              hemisphere, surface_type)
hemisphere = 'RH'
n_RH, vertices_RH, triangles_RH = get_surface(surface_data, 
                                              hemisphere, surface_type)

path_in = '/nobackup/kocher1/bayrak/tmp/'
path_out = '/nobackup/kocher1/bayrak/palm_results/'
path = '/nobackup/kocher1/bayrak/palm_data/'

DATA = h5py.File(path_in + '468_smoothing_new.h5', 'r')
mode = 'smooth'
components = np.arange(0,10,1)

subject_list = []
with open('data/subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

#get_csv(DATA, subject_list, mode, components, n, n_LH, n_RH, vertices,
#            vertices_LH, vertices_RH, path_out)

              
left_list = glob.glob(path + '*left*csv')
right_list = glob.glob(path + '*right*csv')

surface_file = path + 'lh.pial'
design_matrix = path + 'design_matrix.csv'
contrast_matrix = path + 'contrast.csv'
iteration = 5

for input_file in left_list:
    
    output_file = path_out + os.path.basename(input_file)[12:-4]
    return_code = callPalm(input_file, surface_file, iteration, design_matrix,
                           contrast_matrix, output_file)

    print input_file
    print "return code" , return_code

#sys.path.append(os.path.expanduser('/home/raid/bayrak/src/PALM'))
#os.system('./palm')

# load a certain component for each subject and save as .csv

#./palm -i ~/tmp/data_lh.csv -s ~/devel/topography/data/lh.pial -d ~/tmp/design_matrix.csv -t test.con -n 1000 -o myresults/second_run  -zstat -fdr -logp
#
#path = '/home/raid/bayrak/tmp/'
