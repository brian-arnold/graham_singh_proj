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
  
  # result = subprocess.run(command, capture_output=True, text=True)

  # if result.returncode == 0:
  #   return result.stdout
  # else: 
  #   print("ERROR")
  #   print(result.stderr)
  #   return None
  return " ".join(command)

# def convert_blastout_to_df(blast_out:str) -> pd.DataFrame:
#   # Convert the blast output to a pandas dataframe without writing an intermediate file to disk
#   # see here for an overview of output format and options: https://www.metagenomics.wiki/tools/blast/blastn-output-format-6
#   columns = ['qseqid',
#             'sseqid',
#             'pident',
#             'length',
#             'mismatch',
#             'gapopen',
#             'qstart',
#             'qend',
#             'sstart',
#             'send',
#             'evalue',
#             'bitscore',]
#   df = pd.read_csv(StringIO(blast_out), 
#                    sep='\t', 
#                    header=None, 
#                    names=columns)
# 
#   return df

# def save_df_to_csv(df:pd.DataFrame, out_file:str) -> None:
#   df.to_csv(out_file, index=False)

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

  # Reciprocal blast part 1: blast the query species against the reference species
  # if blast_out_fwd := blast(query, reference_db, threads=threads):
  #   df_fwd = convert_blastout_to_df(blast_out_fwd)
  #   save_df_to_csv(df_fwd, './blast_fwd.csv')

  # Reciprocal blast part 2: blast the reference species against the query species
  # if blast_out_rev := blast(reference_db, query, threads=threads):
  #   df_rev = convert_blastout_to_df(blast_out_rev)
  #   save_df_to_csv(df_rev, './blast_rev.csv')



  # print(df_fwd.columns)
  # # Merge forward and reverse results
  # df_rbbh = pd.merge(df_fwd, df_rev[['qseqid', 'sseqid']],
  #                 how='outer',
  #                 left_on='sseqid', 
  #                 right_on='qseqid')

  # print(df_rbbh.columns)



if __name__ == '__main__':
  main()
