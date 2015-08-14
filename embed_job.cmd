# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = job.$(jobid).err
# @ output = job.$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(4)
# @ node_resources = ConsumableMemory(55gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 24:00:00
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

/usr/bin/time -v python /u/${USER}/devel/eigen_decomp/test_embed.py /ptmp/sbayrak/hcp_prep_out/100307_hcp_prep_out.csv

