#!/usr/bin/python -tt

"""
"""

import subprocess
# import data structures containing the locations of the protein fasta files 
from config import query_species_protein_fastas, reference_protein_fasta
# import data structures containing the locations of the blast databases that will get created
from config import query_species_blast_dbs, reference_blast_db


def create_blast_db(protein_fasta:str, blast_db:str) -> int:
  # Create a blast database for a given protein fasta file and a name/location for the database

  command = ["makeblastdb", 
            "-in", protein_fasta,
            "-dbtype", "prot",
            "-out", blast_db,
            ]
  
  result = subprocess.run(command, capture_output=True, text=True)

  if result.returncode == 0:
    return 1
  else: 
    print("ERROR")
    print(result.stderr)
    return 0


def main():

  print(query_species_protein_fastas)

  # Create blast databases for each of the query species
  for species in query_species_protein_fastas:
    if create_blast_db(query_species_protein_fastas[species],query_species_blast_dbs[species]):
      print(f"Created blast db for {species}")
    else:
      print(f"Error creating blast db for {species}")
  
  # Create blast database for the reference species
  if create_blast_db(reference_protein_fasta, reference_blast_db):
    print(f"Created blast db for reference species")
  else:
    print(f"Error creating blast db for reference species")   

if __name__ == '__main__':
  main()
