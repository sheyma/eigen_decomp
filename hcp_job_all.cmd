#!/bin/bash
# My first script

echo "Hello World!"

function today {
echo "Today's date is:"
date +"%A, %B %-d, %Y"
}

today

cd /ptmp/sbayrak/hcp/

# generating arrays filled with subject id's (or directories)
# sbj_ignore for the ones with missing data
# sbj_cool for the ones with complete data (4-times *.nii files)  

declare -a sbj_ignore
i=1
declare -a sbj_cool
j=1

for subject in *; do
	count=$(ls $subject | wc -l); 
	if test "$count" != "4"; then
		sbj_ignore[$((i++))]=$subject
	else
		sbj_cool[$((j++))]=$subject
	fi 
done

# start jobs 

cd /u/sbayrak/devel/eigen_decomp

for subject in ${sbj_cool[*]}; do
	
	if test -f /ptmp/sbayrak/hcp_prep_out/${subject}_hcp_prep_out.csv; then
		echo "${subject} is already prepared"
	else
		job_file=tmp_jobs/tmp_file_${subject}.cmd
		cat hcp_job.cmd | sed "s/%SUBJ_ID%/$subject/g" > "$job_file"
	fi	
done
