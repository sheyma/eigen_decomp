import numpy as np
import h5py
from scipy import stats
import pylab as plt

path = '/home/sheyma/tmp/mano_data/'
f = h5py.File(path + 'Data_BT1_align.h5', 'r')

f_new = h5py.File(path + 'Data_BT1_tstats1.h5', 'w')
f_new = h5py.File(path + 'Data_BT1_tstats1.h5', 'r+')

list_UP = list(f.keys())
popmean = 0

for KEY in list_UP:
    group_UP = f_new.create_group(KEY)
       
    L = f[KEY]
    list_lower = list(L.keys())
    
    for key in list_lower:
       
        t_stats = []
        p_values = []
        tmp = np.array(L[key])
        
        for i in range(0, tmp.shape[2]):
        
            # get i'th component over subjects
            # (rows,columns) = (subjects,values)
            tmp_subjects = tmp[:,:,i]
            # Ttest for values between subjects
            # axis=0 refers to the columns (values)            
            [t, p] = stats.ttest_1samp(tmp_subjects, popmean, axis=0)
            t_stats.append(t)
            p_values.append(p)

        # t_stats = (number of components, t-values)
        # P_ = (number of components, t-values)
        t_stats = np.array(t_stats)
        p_values = np.array(p_values)            
       
        group_LOW = group_UP.create_group(key)       
        group_LOW.create_dataset('t_stats', data=t_stats)
        group_LOW.create_dataset('p_values', data=p_values)

f_new.close()    


# plot x'th (aligned) component over subjects
D = np.array(f['MA_BT1']['alpha1'])
x = 0
D = D[:,:, x]
X,Y=np.meshgrid(range(D.shape[0]+1),range(D.shape[1]+1))
im = plt.pcolormesh(Y,X,D.transpose(), cmap='jet')
plt.colorbar(im, orientation='vertical')
plt.show()


# plot t_stats and p_values of x'th component over subjects
A = h5py.File(path + 'Data_BT1_tstats1.h5', 'r')
AT = np.array(A['MA_BT1']['alpha1']['t_stats'])
AP = np.array(A['MA_BT1']['alpha1']['p_values'])
x = 0
t_stats_component = AT[x, :]
p_values_component = AP[x, :]
length = len(t_stats_component)

plt.figure()
plt.plot(np.arange(0, length, 1), t_stats_component, 'o', label='t-values')    
plt.plot(np.arange(0, length, 1), p_values_component, 'o', label='p-values')    
plt.legend()
plt.show()