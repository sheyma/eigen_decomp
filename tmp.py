import sys
import os
import matplotlib.pylab as pl
import numpy as np

import hcp_corr

cnt_files = 4
subject = '/var/tmp/hcp/907656'


N_first = 0
N_cnt = None

#K_norm = hcp_corr.t_series(subject, cnt_files=cnt_files, N_first=N_first, N_cnt=N_cnt)

K_none = hcp_corr.t_series(subject,
             template = None,
             cnt_files=4,
             N_cnt=N_cnt,
             N_first=N_first,
             subject_path=None,
             dtype=None,
             normalize=True)
print K_none.shape

n = K_none.shape[0]
m = K_none.shape[1]

pl.figure(2); 
for i in range(500, 550 ):
    pl.plot(K_none[i,:])
pl.title('907656')
pl.xlabel('t')
pl.ylabel('node (first 50)')
#pl.figure(2);
#pl.plot(K_none)

A = np.random.randn(500, 500)

A = np.corrcoef(A)

A = A.flatten()

ten_percent = 0.1
dbins = 0.01
bins = np.arange(-1, 1+dbins, dbins)
x, bins = np.histogram(A, bins)

pl.hist(A, bins)

# find out threshold value for top 10 percent
back_sum = 0
for idx in range(x.shape[0]-1, -1, -1):
    back_sum += x[idx]/float(x.sum())
    if back_sum >= ten_percent:
        thr = bins[idx]
        print "top-10percent threshold Seyma:", 
pl.show()
A = np.random.randn(60, 60)

A = np.corrcoef(A)

A = A.flatten()

ten_percent = 0.1
dbins = 0.01
bins = np.arange(-1, 1+dbins, dbins)
x, bins = np.histogram(A, bins)
# find out threshold value for top 10 percent
back_sum = 0
for idx in range(x.shape[0]-1, -1, -1):
    back_sum += x[idx]/float(x.sum())
    if back_sum >= ten_percent:
        thr = bins[idx]
        print "top-10percent threshold:", thr
        break
 
np.percentile(A, 90)


 
THR = np.percentile(A, 100*(1-ten_percent))
print "top-10 percent threshold Sabine: ", THR
