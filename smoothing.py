import h5py
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d


def smooth(x, window_len=11, window='hanning'):
    """smooth 1D data using a window with requested size.

    window_len : int, odd number, choose as [1, 4]% of the sample size
    
    Reference :  http://scipy-cookbook.readthedocs.org/items/SignalSmooth.html
    http://stackoverflow.com/questions/25216382/gaussian-filter-in-scipy
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman', 'gaussian']:
        raise ValueError, "choose a proper windowing function..."

    if window =='gaussian':
        sigma = int( ((window_len -1)/2 -0.5)/4.0) +1
        y = gaussian_filter1d(x, sigma, order=0)
        
    else:    

        s = np.r_[ x[window_len-1:0:-1], x, x[-1:-window_len:-1] ]
    
        if window == 'flat': 
            # np.ones : moving average method
            w=np.ones(window_len, 'd')
        else:
            # np.hanning : the Hanning window to smooth values; the cosine bell
            # np.hamming : the Hamming window to smooth values; the cosine bell
            # np.bartlett : the Bartlett window; triangular window
            # np.blackman : the Blackman window; narrower cosine bell
            w=eval('np.'+window+'(window_len)')
    
        y = np.convolve(w/w.sum(), s, mode='valid')
        y = y[(window_len/2-1)+1:-(window_len/2)]

    return y

def choose_random_subject(subject_list):
    random_int = np.random.permutation(len(subject_list))[0]
    subject_id = subject_list[random_int] 
    subject_id = ''.join(subject_id)
    print "chosen HCP subject : ", subject_id
    return subject_id

#path = '/home/sheyma/tmp/'
path = '/ptmp/sbayrak/tmp/'

subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

# load data to be smoothed
DATA = h5py.File(path + '468_alignments.h5', 'r')

window = 'gaussian'
window_percent = 0.00025
components = np.arange(0, 10, 1)

# open  hdf5 file to save smoothed data
f = h5py.File(path + 'test.h5', 'w')
f = h5py.File(path + 'test.h5', 'r+')

for subject_id in subject_list:
    subject_id = ''.join(subject_id)
    print subject_id
    A = []
    tmp = DATA[subject_id]['aligned']
    tmp = np.array(tmp)    
    for component in components:        
        tmp_column= tmp[:, component]
        window_len = len(tmp_column) * window_percent
        tmp_smooth = smooth(tmp_column, window_len, window)
        A.append(tmp_smooth)   
    A = np.transpose(np.array(A))
    group_id = f.create_group(subject_id)
    group_id.create_dataset('smooth', data = A)
    del tmp_column, tmp_smooth   
    
f.close()

# chose subject_id randomly     
subject_id = choose_random_subject(subject_list)
tmp = np.array(DATA[subject_id]['aligned'])    
component = 0
tmp = tmp[:, component]

window = 'gaussian'
plt.figure(1); plt.plot(tmp, 'b');
plt.title(window)
window_perc = [0.00025, 0.0005, 0.0010, 0.0025, 0.0050 ]     
colors = 'rgcyk'
j = 0;
for i in window_perc:
    window_len = i * len(tmp)
    TMP = smooth(tmp, window_len, window)
    plt.plot(TMP, colors[j], label=str(i))
    j += 1    
    print window_len        
plt.legend()
plt.show()
