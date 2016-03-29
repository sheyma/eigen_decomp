import numpy as np
import h5py
from scipy import stats
import mne
import pylab as plt

path = '/nobackup/kocher1/bayrak/math_anxiety/'
f = h5py.File(path + 'Data_BT1_align.h5', 'r')

list_UP = list(f.keys())
       
G_MA = f[list_UP[0]]
G_NMA = f[list_UP[1]]

list_lower = list(G_MA.keys())
list_check = list(G_NMA.keys())

if list_lower != list_check:
    raise ValueError('keys are not identical in both groups')    

    
for key in list_lower:
    # e.g. key = 'alpha1'
    
    f_tmp = h5py.File(path + 'ttest_BT1_' + key + '.h5', 'w')
    f_tmp = h5py.File(path + 'ttest_BT1_' + key + '.h5', 'r+')

    
    comps =  G_MA[key].shape[2]   
         
    for comp in range(0, comps):
        
        G1 = np.array(G_MA[key])[:,:, comp]
        G2 = np.array(G_NMA[key])[:,:, comp]
        print G1.shape, G2.shape
        # ttest of two independent samples        
        [t, p] = stats.ttest_ind(G1, G2, axis=0)
        # FDR correction on p-values
        alpha = 0.05
        reject, p_fdr = mne.stats.fdr_correction(p, alpha, method='indep')

        # set non-significatn t-statistics to 0
        t_fdr = np.copy(t)
        for i in range(0, t.shape[0]):
            if not reject[i]:
                t_fdr[i] = 0

        if comp !=9:
            string = '0'+ str(comp + 1)
        elif comp == 9:
            string = str(comp + 1)
        
        group_comp = f_tmp.create_group(string)
        group_comp.create_dataset('t', data=t)                
        group_comp.create_dataset('p', data=p)
        group_comp.create_dataset('rej_fdr', data=reject)
        group_comp.create_dataset('p_fdr', data=p_fdr)        
        group_comp.create_dataset('t_fdr', data=t_fdr)
        
    f_tmp.close()
    
## plot x'th (aligned) component over subjects
#D = np.array(f['MA_BT1']['alpha1'])
#x = 0
#D = D[:,:, x]
#X, Y=np.meshgrid(range(D.shape[0]+1),range(D.shape[1]+1))
#im = plt.pcolormesh(Y,X,D.transpose(), cmap='jet')
#plt.colorbar(im, orientation='vertical')
#plt.show()
#
## plot t_stats and p_values of x'th component over subjects
#A = h5py.File(path + 'ttest_gamma.h5', 'r')
#AT = np.array(A['01']['t'])
#AP = np.array(A['01']['p'])
#AT_fdr = np.array(A['01']['t_fdr'])
#
#plt.figure() 
#plt.plot(AP, 'or', label='p-values')    
#plt.plot(AT_fdr, 'oy', label='t_signif')    
#plt.legend()
#plt.show()