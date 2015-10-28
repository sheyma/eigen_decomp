import sys
import os
import matplotlib.pylab as pl

sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import hcp_util

cnt_files = 4
subject = '/tmp/sbayrak/hcp/907656'
N_first = 0
N_cnt = 100

K_norm = hcp_util.t_series(subject, cnt_files=cnt_files, N_first=N_first, N_cnt=N_cnt)

K_none = hcp_util.t_series(subject,
             template = None,
             cnt_files=4,
             N_cnt=N_cnt,
             N_first=N_first,
             subject_path=None,
             dtype=None,
             normalize=False)
pl.figure(1); 
pl.plot(K_norm)

pl.figure(2);
pl.plot(K_none)


