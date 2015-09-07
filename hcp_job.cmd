# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/sbayrak/hcp_job_stat/job.$(jobid).err
# @ output = /ptmp/sbayrak/hcp_job_stat/job.$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(16)
# @ node_resources = ConsumableMemory(120gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 01:30:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

export OMP_NUM_THREADS=16

echo "#### begin env"
hostname -f
free
ulimit -a
env | sort
echo "#### end env"

# here we go

/usr/bin/time -v poe python /u/${USER}/devel/eigen_decomp/hcp_prep.py /ptmp/sbayrak/hcp/%SUBJ_ID%
