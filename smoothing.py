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

#path = '/home/sheyma/tmp/'
path = '/ptmp/sbayrak/tmp'

surface_data = path + 'data_surface.h5'
hemisphere = 'full'
surface_type = 'inflated'
n, vertices, triangles = get_surface(surface_data, hemisphere, surface_type)


subject_list = []
with open(path + 'subject_list.csv', 'rb') as f:
    reader = csv.reader(f);
    subject_list = list(reader);

DATA = h5py.File(path + '468_alignments.h5', 'r')

window = 'gaussian'
window_percent = 0.0005
components = np.arange(0, 10, 1)

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


#data = np.zeros(len(vertices))
#data[n] = tmp_smooth
#
#plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)    
#
#data[n] = A[:,9]
#plt = plotting.plot_surf_stat_map(vertices, triangles, stat_map=data, cmap='jet', azim=0)    
#
#    
#import matplotlib.pyplot as plt
#window = 'gaussian'
#plt.figure(1); plt.plot(tmp, 'b');
#plt.title(window)
#window_perc = [0.00025, 0.0005, 0.0010, 0.0025, 0.0050 ]     
#colors = 'rgcyk'
#j = 0;
#for i in window_perc:
#    window_len = i * len(tmp)
#    TMP = smooth(tmp, window_len, window)
#    plt.plot(TMP, colors[j], label=str(i))
#    j += 1    
#    print window_len        
#plt.legend()
#plt.show()


