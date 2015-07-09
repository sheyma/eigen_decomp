#----sample batch script--------
#@ shell = /bin/bash
#@ jobname = hello_hydra
#@ initialdir = /u/sbayrak/devel/eigen_decomp
#@ input = $(initialdir)/random_mtx.dat
#@ error = job.err.$(jobid)
#@ output = job.out.$(jobid)
#@ job_type = parallel
#@ node_usage = not_shared
#@ node = 32
#@ resources = ConsumableCpus(1)
#@ wall_clock_limit = 00:50:00
#@ notification = complete
#@ notify_user = $(user)@rzg.mpg.de
#@ queue

# runt the program

cd /ptmp/${USER}/
poe /u/${USER}/myprog > prog.out

