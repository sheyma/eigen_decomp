import h5py
import numpy as np
import csv
import matplotlib.pylab as plt
from scipy.ndimage.filters import gaussian_filter1d

path = '/ptmp/sbayrak/tmp/'
subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

random_int = np.random.permutation(len(subject_list))[0]
subject_id = subject_list[random_int] 
subject_id = ''.join(subject_id)
print "chosen HCP subject : ", subject_id

# take the first (aligned) component of a random subject
aligned_all = h5py.File(path + '468_alignments.h5', 'r')
tmp = aligned_all[subject_id]['aligned']
tmp = np.array(tmp)
tmp = tmp[:,0]


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

window = 'bartlett'
plt.figure(1); plt.plot(tmp, 'b');
plt.title(window)
window_lengths = [0.005, 0.01, 0.02, 0.03, 0.04]     
colors = 'rgcyk'
j = 0;
for i in window_lengths:
    window_len = i * len(tmp)
    TMP = smooth(tmp, window_len, window)
    plt.plot(TMP, colors[j], label=str(i))
    j += 1    
    print window_len    
    
plt.legend()
plt.show()