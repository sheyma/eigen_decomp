# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/sbayrak/fisher/fisher_$(jobid).err
# @ output = /ptmp/sbayrak/fisher/fisher_$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(16)
# @ node_resources = ConsumableMemory(80gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 22:00:00
# @ notification = complete
# @ notify_user = $(user)@rzg.mpg.de
# @ queue

echo "#### begin env"
echo "job started at: `date +"%F %T"`"
echo "hostname: `hostname -f`"
cpus="`cat /proc/cpuinfo | grep "physical id" | wc -l`"
echo "number of CPUs: $cpus"
free
ulimit -a
env | sort
echo "#### end env"

# here we go
cd /ptmp/sbayrak || exit 1
subject_dirs="$(for i in /ptmp/sbayrak/hcp/*; do count=`ls $i| wc -l `; if test $count = 4 ; then echo $i; fi ;done)" || exit 1
echo "command started at: `date +"%F %T"`"
/usr/bin/time -v -o /dev/stdout -a python -u ${HOME}/devel/eigen_decomp/corr_fisher.py $subject_dirs

ret=$?
echo "job ended at: `date +"%F %T"`, exit code $ret"
exit $ret
