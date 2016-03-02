# construct design matrix
import numpy as np
import pandas as pd
from pandas.core.index import Int64Index

path = '/home/sheyma/tmp/'
filename = 'sustained_attention_task.csv'

# construct the DataFrame (df)
# data is indexed by the 'Subject' column 
df = pd.read_csv(path + filename, index_col = 'Subject', 
                        header = 0)

subjects = df.index
heads = list(df.columns.values)
dtype_ = df.dtypes

# get subject indices which have NaN entries
mask=False
for col in df.columns: mask = mask | df[col].isnull()
subjects_null = np.array(df[mask].index)

# get full original subject list
A = pd.read_csv(path + 'subject_list.csv',  index_col=False, header=None)
A = np.array(A)
A = A.reshape(len(A))

# check if any of subjects_null is in original subject list
for j in subjects_null:
    for i in A:
        if int(i) == int(j):
            print i

C = []
subjects_cool = Int64Index(A)
for subject in subjects_cool:   
    for head in heads: 
        # check if a subject has any NaN value
        if pd.isnull(df.loc[subject, head]) == True:
            break
    C.append( np.array(df.loc[subject]) )
C = np.array(C)
            
df_new = pd.DataFrame(C)
df_new.to_csv(path + 'design_matrix02.csv', sep=',', index=False, 
              header=False)
             
# construct a contrast matrix
con = np.eye(C.shape[1], dtype='int')   
np.savetxt(path + 'contrast_matrix02.csv', con, delimiter=',',
           fmt='%d',)