#!/bin/bash

## define job template in variable JOB_TEMPLATE ###########

read -r -d '' JOB_TEMPLATE <<'EOF'
# @ shell=/bin/bash
#
# Sample script for LoadLeveler
#
# @ error = /ptmp/sbayrak/hcp_job_stat/job_test_embed_%SUBJ_ID%_$(jobid).err
# @ output = /ptmp/sbayrak/hcp_job_stat/job_test_embed_%SUBJ_ID%_$(jobid).out
# @ job_type = parallel
# @ node_usage= not_shared
# @ node = 1
# @ tasks_per_node = 1
# @ resources = ConsumableCpus(16)
# @ node_resources = ConsumableMemory(90gb)
# @ network.MPI = sn_all,not_shared,us
# @ wall_clock_limit = 00:15:00
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

/usr/bin/time -v python ${HOME}/devel/eigen_decomp/test_embed.py /ptmp/sbayrak/hcp/%SUBJ_ID%
EOF
## end define JOB_TEMPLATE ################################


rm -f tmp_jobs/*

for d in /ptmp/sbayrak/hcp/*; do
	subject=$(basename "$d")
	count=$(ls $d | wc -l); 
	if test "$count" = "4"; then
		job_file=tmp_jobs/job_${subject}.cmd
		echo "$JOB_TEMPLATE" | sed "s/%SUBJ_ID%/$subject/g" > "$job_file"
	fi
done

