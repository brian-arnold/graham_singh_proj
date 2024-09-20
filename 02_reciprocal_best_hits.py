#!/usr/bin/python -tt

"""
"""
from collections import defaultdict
from config import query_species_protein_fastas
import pandas as pd
import sys


def convert_blastout_to_df(blast_out:str) -> pd.DataFrame:
  # Convert the blast output to a pandas dataframe without writing an intermediate file to disk
  # see here for an overview of output format and options: https://www.metagenomics.wiki/tools/blast/blastn-output-format-6
  columns = ['qseqid',
            'sseqid',
            'pident',
            'length',
            'mismatch',
            'gapopen',
            'qstart',
            'qend',
            'sstart',
            'send',
            'evalue',
            'bitscore',]
  
  df = pd.read_csv(blast_out, 
                   sep='\t', 
                   header=None, 
                   names=columns)
  
  df['norm_bitscore'] = df.bitscore / df.length

  return df

def recprocal_best_hits_dict_method(df_fwd, df_rev):
  # Use dictionaries to find reciprocal best hits
  # This is a sanity check, it should be equivalent to the pandas method below
  def blast_out_2_dict(df):
    # create dictionary of blast results: keys are query protein, values and subject protein
    blast = {}
    for i, row in df.iterrows():
      query = row['qseqid']
      subject = row['sseqid']
      # assert query not in blast, f'Query {query} already in blast dictionary'
      if query not in blast:
        blast[query] = subject

    return blast
  
  fwd_hits = blast_out_2_dict(df_fwd)
  rev_hits = blast_out_2_dict(df_rev)

  # Find reciprocal best hits
  rbbh = {}
  for query, subject in fwd_hits.items():
    if subject in rev_hits:
      if rev_hits[subject] == query:
        rbbh[query] = subject

  return len(rbbh.keys())

def main():

  species_list = query_species_protein_fastas.keys()

  for i, species in enumerate(species_list):
    # if i != 0:
    #   continue
    print(f'Processing {species}')
    df_fwd = convert_blastout_to_df(f'blast_out/{species}_fwd.out')
    df_rev = convert_blastout_to_df(f'blast_out/{species}_rev.out')

    # print(f'Number of RBBH from dict method, {species}:', recprocal_best_hits_dict_method(df_fwd, df_rev))

    # Merge forward and reverse results
    df_rbbh = pd.merge(df_fwd, df_rev[['qseqid', 'sseqid']],
                    how='outer',
                    left_on='sseqid', 
                    right_on='qseqid')

    # Filter out non-reciprocal hits
    df_rbbh = df_rbbh.loc[df_rbbh.qseqid_x == df_rbbh.sseqid_y]

    df_rbbh = df_rbbh.groupby(['qseqid_x', 'sseqid_x']).max()
    print(f'Number of RBBH from df method, {species}:', len(df_rbbh))
    print(df_rbbh.head(3))                                

if __name__ == '__main__':
  main()
