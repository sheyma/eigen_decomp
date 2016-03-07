#!/usr/bin/python
# run PALM...

import h5py
import csv
import pandas as pd
import numpy as np
import glob
import os
from subprocess import call
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--hem', default='LH', choices=['full','LH','RH'])
parser.add_argument('-i', '--input_file', type=str, required=True)
parser.add_argument('-s', '--surface_file', type=str, required=True)
parser.add_argument('-dm', '--design_matrix', type=str, required=True)
parser.add_argument('-cm', '--contrast_matrix', type=str, required=True)
parser.add_argument('-o', '--output_file', type=str, required=True)
args = parser.parse_args()

def choose_component(DATA, subject_id, mode, component = None):
    # choose all components of a given subject    
    A = DATA[subject_id][mode]    
    A = np.array(A)    
    # choose a specified component of a given subject
    if component != None:
        A = A[:, component]
    return A

def over_subjects(DATA, subject_list, mode, component):
   
    DATA_all = []
    for subject_id in subject_list:
        subject_id = ''.join(subject_id)
        subject_component = choose_component(DATA, subject_id, 
                                             mode, component)
        DATA_all.append(subject_component)
    
    return np.array(DATA_all)    

def save_csv(name, data):
    tmp = pd.DataFrame(data)
    return tmp.to_csv(name, header=False, index=False)


def mask_index(surf_data, surf_type, hem):
    tmp = h5py.File(surf_data, 'r')
    n = np.array(tmp[hem][surf_type]['indices'])   
    vertices = np.array(tmp[hem][surf_type]['vertices'])    
    return n, vertices


def get_csv(DATA, subject_list, mode, components, surf_data, surf_type,
            hem, path_out):

    n, vertices = mask_index(surf_data, surf_type, hem)
      
    for component in components:
        print "loop for component ", component + 1
        DATA_all = over_subjects(DATA, subject_list, mode, component)    

        if hem == 'LH':
            Data = DATA_all[:, 0:len(n)]
        elif hem == 'RH':
            n_LH, vertices_RH = mask_index(surf_data, surf_type, hem='LH')
            Data = DATA_all[:, len(n_LH): len(n_LH) + len(n)]
        elif hem == 'full':   
            Data = DATA_all        
        
        data  = np.zeros((len(subject_list), len(vertices)))
        
	data[:,n] = Data
        
        if component != 9:
            name = path_out+'Sdata_32492_'+ hem + '_0'+str(component+1)+'.csv'
        else :
            name = path_out+'Sdata_32492_'+ hem + '_'+str(component+1)+'.csv'
        
	save_csv(name, data)
    return        


def callPalm(input_file, surface_file, iteration, design_matrix,
             contrast_matrix, output_file):
                 
    retcode = call(["palm", "-i", input_file, "-s", surface_file,
                    "-n", str(iteration), "-approx",  "tail",  
                    "-o", output_file, "-zstat", "-fdr", 
                    "-d", design_matrix,  "-t",  contrast_matrix, 
                    "-corrcon", "-corrmod", "-T", "-tfce2D"])
    return retcode 
    

path_in = '/nobackup/kocher1/bayrak/tmp/'
path_out = '/nobackup/kocher1/bayrak/palm_results/'
path = '/nobackup/kocher1/bayrak/palm_data/'

surf_data =  path_in + 'data_surface.h5'
surf_type = 'midthickness'

DATA = h5py.File(path_in + '468_smoothing_new.h5', 'r')
mode = 'smooth'
components = np.arange(0,10,1)

subject_list = []
with open('data/subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);


hem=args.hem
#get_csv(DATA, subject_list, mode, components, surf_data, surf_type, hem ,path)

      
design_matrix = args.design_matrix
contrast_matrix = args.contrast_matrix
input_file = args.input_file
output_file = args.output_file
surface_file = args.surface_file

iteration = 500

return_code = callPalm(input_file, surface_file, iteration, 
                       design_matrix, contrast_matrix, output_file)

