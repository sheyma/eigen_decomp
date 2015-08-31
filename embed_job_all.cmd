#!/bin/bash
# My first script

echo "Hello World!"

function today {
echo "Today's date is:"
date +"%A, %B %-d, %Y"
}

today

j=1;
for prepout in /ptmp/sbayrak/hcp_prep_out/*_hcp_prep_out.csv; do 
	subject=$(basename "$prepout" _hcp_prep_out.csv)
	
	if test -f /ptmp/sbayrak/embed_out/${subject}_embed_out.csv; then
		echo "subject $subject is already embedded"
		echo $((j++))
	else
		
		path="/u/sbayrak/devel/eigen_decomp/"
		
		job_file=${path}tmp_jobs_embed/tmp_file_embed_${subject}.cmd
		cat ${path}embed_job.cmd | sed "s/%SUBJ_ID%/${subject}_hcp_prep_out.csv/g" > "$job_file"
		chmod +x ${job_file}
	fi
done
