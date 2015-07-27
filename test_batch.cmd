# @ shell=!/bin/bash
#
# Sample script for LoadLeveler
#
# @ initialdir = /u/sbayrak/devel/eigen_decomp
# @ error = job.err.$(jobid)
# @ output = job.out.$(jobid)
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(1)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 24:00:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

# run the program

cd /ptmp/${USER}/
poe /u/${USER}/devel/eigen_decomp/test_batch.cmd > prog.out
python /u/sbayrak/devel/eigen_decomp/hcp_prep.py