import h5py
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

#tmp = np.array(h5py.File('/home/sheyma/tmp/embedding_672756.h5', 'r').get('embedding'))
tmp = np.array(h5py.File('/home/raid/bayrak/tmp/embeddings_full_901038.h5', 'r').get('embedding'))

tmp = tmp[0:278,0]



def smooth(x, window_len=11, window='hanning'):
    """smooth 1D data using a window with requested size.

    window_len : int, odd number
    
    Reference :  http://scipy-cookbook.readthedocs.org/items/SignalSmooth.html
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "choose a proper windowing function..."

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

    y=np.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len/2-1)+1:-(window_len/2)]

    
TMP = smooth(tmp, window_len = 5, window='blackman')
plt.figure(2); plt.plot(tmp, 'b'); 
plt.plot(TMP, 'k', label='window_len=5')
plt.title('blackman window - 50 data points')
plt.legend()