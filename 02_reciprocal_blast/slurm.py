# functions shared across multiple scripts

import sys
import gzip
import re
import os
from subprocess import Popen,PIPE


def create_job_script(name:str, outDir:str, tasks:int, cpuPerTask:int, time:int, mem:int, command:str) -> str:
	# create a job script for slurm
	outFile = open('job_%s.sh' % name , 'w')
	o = outDir + "/out." + str(name)
	e = outDir + "/err." + str(name)
	print("#!/bin/bash", file=outFile)
	print("#SBATCH -J "+ str(name), file=outFile)
	print("#SBATCH -o " + o, file=outFile)
	print("#SBATCH -e " + e, file=outFile)
	print("#SBATCH --ntasks=" + str(tasks), file=outFile)
	print("#SBATCH --cpus-per-task=" + str(cpuPerTask), file=outFile)
	print("#SBATCH -t " + str(time), file=outFile)
	print("#SBATCH --mem=" + str(mem), file=outFile)
	print(command, file=outFile)
	outFile.close()
	jobId = sbatch_submit(outFile.name)
	print(jobId)
	os.system("mv job_" + str(name) + ".sh " + outDir)
	return(jobId)

def sbatch_submit(filename:str) -> str:	
	# submit the job to slurm
	proc = Popen('sbatch %s'%filename,shell=True,stdout=PIPE,stderr=PIPE)
	stdout,stderr = proc.communicate()
	stdout = stdout.decode("utf-8","ignore")
	stdout = stdout.strip()
	stdout = stdout.strip('Submitted batch job ')
	return(stdout)




