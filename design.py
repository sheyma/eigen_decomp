# construct desig matrix

import h5py
import pandas as pd

path = '/tmp/'
filename = 'sustained_attention_task.csv'

# data is originaly indexed by the 'Subject' column 
DataFrame = pd.read_csv(path + filename, index_col = 'Subject',
                   header = 0)
subjects = DataFrame.index
heads = list(DataFrame.columns.values)



subjects[0]
heads[0]

DataFrame.H[0]
DataFrame.loc[100307, 'FS_InterCranial_Vol']
for value in values:
    print value
    DataFrame.

DataFrame.'FS_InterCranial_Vol'
