#!/usr/bin/python -tt

"""
"""

# import subprocess
# import pandas as pd
# from io import StringIO

# import data structures containing the locations of the protein fasta files 
from config import query_species_protein_fastas, reference_protein_fasta
# import data structures containing the locations of the blast databases that will get created
from config import query_species_blast_dbs, reference_blast_db
# import functions to submit slurm jobs
from slurm import create_job_script


def blast_cmd(query:str, reference_db:str, out_name:str, threads:int=1, max_target_seqs:int=1) -> str:
  # Run blastp on the command line via subprocess
  command = ["blastp", 
            "-query", query,
            "-db", reference_db,
            "-outfmt", "6",
            "-num_threads", f"{threads}",
            "-max_target_seqs", f"{max_target_seqs}",
            ">", out_name]

  return " ".join(command)

def main():

  threads = 20
  runtime = 1400
  mem = 20000

  for species in query_species_protein_fastas:
    # create a job script for each query species
    fwd_blast = blast_cmd(query_species_protein_fastas[species], reference_blast_db, f"{species}_fwd.out", threads=threads)
    rev_blast = blast_cmd(reference_protein_fasta, query_species_blast_dbs[species], f"{species}_rev.out", threads=threads)
    cmd = "source /home/bjarnold/miniforge3/etc/profile.d/conda.sh\n"
    cmd += "conda activate blast\n"
    cmd += fwd_blast + '\n' + rev_blast
    job_id = create_job_script(name=species, 
                               outDir='./', 
                               tasks=1, 
                               cpuPerTask=threads, 
                               time=runtime, 
                               mem=mem, 
                               command=cmd)
    print(job_id)

if __name__ == '__main__':
  main()
