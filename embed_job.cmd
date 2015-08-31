# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/sbayrak/embed_job_stat/job.$(jobid).err
# @ output = /ptmp/sbayrak/embed_job_stat/job.$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(4)
# @ node_resources = ConsumableMemory(55gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 00:50:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

echo "#### begin env"
hostname -f
free
ulimit -a
env | sort
echo "#### end env"

# here we go

/usr/bin/time -v python /u/${USER}/devel/eigen_decomp/test_embed.py /ptmp/${USER}/hcp_prep_out/%SUBJ_ID%

