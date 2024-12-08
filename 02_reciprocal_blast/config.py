#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
from collections import defaultdict

base_data_dir = '/scratch/gpfs/bjarnold/Graham/ncbi_data'

# location of the protein fasta files for each of the query species
query_species_protein_fastas = {'harbor_seal':f'{base_data_dir}/harbor_seal/data/GCF_004348235.1/protein.faa',
                                'ca_sea_lion':f'{base_data_dir}/ca_sea_lion/data/GCF_009762305.2/protein.faa',
                                'northern_elephant_seal':f'{base_data_dir}/northern_elephant_seal_hybrid/data/protein.fasta',
                                }

# location of the protein fasta file for the reference species
# reference_protein_fasta = f'{base_data_dir}/humans/data/GCF_000001405.40/protein.faa'
reference_protein_fasta = f'{base_data_dir}/canine/data/GCF_000002285.5/protein.faa'


# location of the blast databases that will get created
query_species_blast_dbs = {k:v.replace('protein.faa', 'blast_db') for k,v in query_species_protein_fastas.items()}
reference_blast_db = reference_protein_fasta.replace('protein.faa', 'blast_db')


for i in query_species_protein_fastas.values():
  assert os.path.exists(i), f"Error: {i} does not exist"