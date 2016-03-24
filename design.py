# construct design matrix
import numpy as np
import pandas as pd
from pandas.core.index import Int64Index

path = '/nobackup/kocher1/bayrak/palm_data/'
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

# get target subject indices
path01 = '/nobackup/kocher1/bayrak/data/'
A = pd.read_csv(path01 + 'subject_list.csv',
                index_col=False, header=None)
A = np.array(A)
A = A.reshape(len(A))

# check if any of subjects_null is in target subjects
for j in subjects_null:
    for i in A:
        if int(i) == int(j):
            print i

C = []
subjects_cool = Int64Index(A)
# check if a subject has any NaN entry
if not pd.isnull(df.loc[subjects_cool, heads]).any().any():
    C = df.loc[subjects_cool, heads]
C = np.array(C)

# construct design matrices separately
Ones = np.ones(C.shape[0])
for i in range(0, C.shape[1]):
    D = []    
    D.append(Ones)
    # subtract the mean of column 
    D.append(C[:,i] - np.mean(C[:,i]))
    D = np.array(D).T    
    df_new = pd.DataFrame(D)
    df_new.to_csv(path + 'design_matrix_' + str(i+1) + '.csv',
                  sep = ',', index=False, header=False) 
    print i

# construct a contrast matrix
con = np.eye(2, dtype='int')   
np.savetxt(path + 'contrast_matrix.csv', con, delimiter=',',
           fmt='%d',)

# construct design matrix as combination of DataFrame columns
C = []
subjects_cool = Int64Index(A)
heads_cool = [heads[6], heads[7]]
# check if any of the entries is NaN
if not pd.isnull(df.loc[subjects_cool, heads_cool]).any().any():
    C = df.loc[subjects_cool, heads_cool]  
C = np.array(C)           

for i in range(0, C.shape[1]):
    C[:,i] = C[:,i] - np.mean(C[:,i])

df_new = pd.DataFrame(C)
df_new.to_csv(path + 'design_matrix_SCPTs.csv', sep=',', index=False,
              header=False)
