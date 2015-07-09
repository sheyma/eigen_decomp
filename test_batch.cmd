# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = job.err.$(jobid)
# @ output = job.out.$(jobid)
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 32
# @ tasks_per_node = 16
# @ resources = ConsumableCpus(1)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 24:00:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

# run the program

cd /ptmp/${USER}/
poe /u/${USER}/myprog > prog.out