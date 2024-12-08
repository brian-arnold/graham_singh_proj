#!/usr/bin/python -tt

"""
"""
from collections import defaultdict
from config import query_species_protein_fastas
import pandas as pd
from Bio import Entrez
Entrez.email = "bs_email@gmail.com"  # Replace with your email
import re

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

def recprocal_best_hits_dict_method(df_fwd:pd.DataFrame, df_rev:pd.DataFrame) -> int:
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


def fetch_gene_symbols(accessions:list) -> list:
  """
  Use Entrez.efetch to fetch gene symbols for a list of protein accession numbers.
  Unfortunately, you can only fetch 10k records at a time, so we need to chunk the list
  to get gene symbols in batches.
  """
  
  def chunk_list(full_list:list, chunk_size:int) -> list:
      """Split the list into sublists of given size."""
      return [full_list[i:(i+chunk_size)] for i in range(0, len(full_list), chunk_size)]
  
  chunked_list = chunk_list(accessions, 9000)
  gene_names = []
  mito = []
  # Fetch gene symbols for each chunk to avoid hitting the 10k limit
  for sub_list in chunked_list:
    ids = ",".join(sub_list)
    handle = Entrez.efetch(db="protein", id=ids, rettype="gb", retmode="text")
    records = handle.read().split('//')
    handle.close()
    records = records[:-1]  # Remove the last empty record
    for i,rec in enumerate(records):

      gene = re.findall(r"/gene=\"(.*?)\"", rec)
      assert len(gene) == 1, f'Expected 1 gene symbol, got {len(gene)}'
      gene_names.append(gene[0])

      is_mito = re.findall(r"organelle=\"mitochondrion\"", rec, re.IGNORECASE)
      mito.append(len(is_mito) > 0)


  assert len(accessions) == len(gene_names), f'Number of accessions {len(accessions)} does not match number of symbols {len(gene_names)}'
  return gene_names, mito
  

def main():

  species_list = query_species_protein_fastas.keys()


  dfs = []
  for i, species in enumerate(species_list):
    print(f'Processing {species}')
    df_fwd = convert_blastout_to_df(f'blast_out/{species}_fwd.out')
    df_rev = convert_blastout_to_df(f'blast_out/{species}_rev.out')

    # Add in gene annotations before finding reciprocal best hits to see which genes are dropping out (e.g. mitochondrial genes)
    df_rev['reference_gene_symbol'], df_rev['is_mito'] = fetch_gene_symbols(df_rev['qseqid'])

    # join table where sseqid in df_fwd is qseqid in df_rev
    df_rbbh = pd.merge(df_fwd, df_rev[['qseqid', 'sseqid', 'reference_gene_symbol', 'is_mito']],
                        how='outer',
                        left_on='sseqid', 
                        right_on='qseqid')
    # df_rbbh.to_csv('rbbh_outer_merge.csv', index=False)

    # Filter out non-reciprocal hits
    df_rbbh = df_rbbh.loc[df_rbbh.qseqid_x == df_rbbh.sseqid_y]

    df_rbbh = df_rbbh.groupby(['qseqid_x', 'sseqid_x']).max()
    # remove hierarchy of columns from groupby statement
    df_rbbh = df_rbbh.reset_index()
    print(f'Number of RBBH from df method, {species}:', len(df_rbbh))

    df_rbbh.rename(columns={'qseqid_x': species, 'sseqid_x': 'reference'}, inplace=True)
    dfs.append(df_rbbh[[species, 'reference']])

  # Merge all the dataframes
  df_rbb = dfs[0]
  for i, df in enumerate(dfs[1:]):
    df_rbb = df_rbb.merge(df, how='inner', on='reference')

  print(len(df_rbb))
  print(df_rbb.head(3)) 
  # df_rbb.to_csv('rbbh_orig.csv', index=False)

  # Fetch gene symbols
  df_rbb['reference_gene_symbol'], df_rbb['is_mt'] = fetch_gene_symbols(df_rbb['reference'])
  df_rbb.to_csv('rbbh_gene.csv', index=False)


if __name__ == '__main__':
  main()
