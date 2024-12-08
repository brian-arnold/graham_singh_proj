#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
from collections import defaultdict
from Bio import SeqIO


def create_hybrid_genome_fasta(NES_genome_file:str, SES_genome_file:str, SES_mitochondrial_scaff:str, hybrid_assembly_dir:str) -> None:
  # copy the northern elephant seal assembly to the hybrid assembly directory
  os.system(f'cp {NES_genome_file} {hybrid_assembly_dir}/hybrid_assembly.fasta')
  # Then append the mitochondrial scaffold from the southern elephant seal assembly
  # note hybrid assembly opened in append mode
  with open(SES_genome_file, "r") as SES_fasta, open(f'{hybrid_assembly_dir}/hybrid_assembly.fasta', "a") as hyb_fasta:
      for record in SeqIO.parse(SES_fasta, "fasta"):
          if record.id == SES_mitochondrial_scaff:
              SeqIO.write(record, hyb_fasta, "fasta")
              print(f"Scaffold '{SES_mitochondrial_scaff}' appended to {hyb_fasta}")
              return
      print(f"Scaffold '{SES_mitochondrial_scaff}' not found in {SES_genome_file}") 


def create_hybrid_gtf(NES_gtf_file:str, SES_gtf_file:str, SES_mitochondrial_scaff:str, hybrid_assembly_dir:str) -> None:
  # copy the northern elephant seal gtf to the hybrid assembly directory
  os.system(f'cp {NES_gtf_file} {hybrid_assembly_dir}/hybrid_assembly.gtf')
  # Then append the mitchondrial scaffold info from the southern elephant seal assembly
  with open(SES_gtf_file, "r") as SES_gtf, open(f'{hybrid_assembly_dir}/hybrid_assembly.gtf', "a") as hyb_gtf:
      cnt = 0
      for line in SES_gtf:
          if line.startswith(SES_mitochondrial_scaff):
              cnt+=1
              hyb_gtf.write(line)              
      print(f'Appended {cnt} lines from {SES_gtf_file} to {hyb_gtf}')
  return


def create_hybrid_protein_fasta(NES_protein_file:str, SES_protein_file:str, hybrid_assembly_dir:str) -> None:
  # copy the northern elephant seal protein fasta to the hybrid assembly directory
  os.system(f'cp {NES_protein_file} {hybrid_assembly_dir}/protein.fasta')
  # Then append the protein fasta from the southern elephant seal assembly
  with open(SES_protein_file, "r") as SES_protein, open(f'{hybrid_assembly_dir}/protein.fasta', "a") as hyb_protein:
      cnt = 0
      for record in SeqIO.parse(SES_protein, "fasta"):
          if '(mitochondrion)' in record.description:
            cnt += 1
            SeqIO.write(record, hyb_protein, "fasta")
      print(f"Added {cnt} entries to {hyb_protein}")
  return


def main():
  """
  This function creates a hybrid assembly that consists of the northern elephant seal assembly along
  with the mitochondrial scaffold from the southern elephant seal assembly. We create both a fasta file
  and a gtf file for the hybrid assembly. 
  """

  # NES = nourthern elephant seal
  # SES = southern elephant seal
  NES_dir = '/scratch/gpfs/bjarnold/Graham/ncbi_data/northern_elephant_seal/data/GCF_029215605.1'
  SES_dir = '/scratch/gpfs/bjarnold/Graham/ncbi_data/southern_elephant_seal/data/GCF_011800145.1'

  NES_genome_file = f'{NES_dir}/GCF_029215605.1_mMirAng1.0.hap1_genomic.fna'
  SES_genome_file = f'{SES_dir}/GCF_011800145.1_KU_Mleo_1.0_genomic.fna'

  NES_gtf_file, NES_protein_file = f'{NES_dir}/genomic.gtf', f'{NES_dir}/protein.faa'
  SES_gtf_file, SES_protein_file = f'{SES_dir}/genomic.gtf', f'{SES_dir}/protein.faa'

  SES_mitochondrial_scaff = 'NC_008422.1'

  hybrid_assembly_dir = '/scratch/gpfs/bjarnold/Graham/ncbi_data/northern_elephant_seal_hybrid/data'
  os.makedirs(hybrid_assembly_dir, exist_ok=True)

  # Create hybrid fasta file
  create_hybrid_genome_fasta(NES_genome_file, SES_genome_file, SES_mitochondrial_scaff, hybrid_assembly_dir)

  # Create hybrid gtf file
  create_hybrid_gtf(NES_gtf_file, SES_gtf_file, SES_mitochondrial_scaff, hybrid_assembly_dir)

  # create hybrid protein fasta file
  create_hybrid_protein_fasta(NES_protein_file, SES_protein_file, hybrid_assembly_dir)


if __name__ == '__main__':
  main()
