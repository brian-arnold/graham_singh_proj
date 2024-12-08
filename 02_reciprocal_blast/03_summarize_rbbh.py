#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
from collections import defaultdict
import pandas as pd

def main():

  df = pd.read_csv('rbbh_gene.csv')

  print(f'Number of rows: {len(df)}')
  print(f'Number of unique harbor_seal genes: {len(df.harbor_seal.unique())}')
  print(f'Number of unique reference genes: {len(df.reference.unique())}')
  print(f'Number of unique ca_sea_lion genes: {len(df.ca_sea_lion.unique())}')
  print(f'Number of unique northern_elephant_seal genes: {len(df.northern_elephant_seal.unique())}')
  print(f'Number of unique reference_gene_symbol genes: {len(df.reference_gene_symbol.unique())}')

  # get rows in df which have duplicate values in reference_gene_symbol column
  dup_rows = df[df.duplicated(subset='reference_gene_symbol', keep=False)]
  print(dup_rows.head())

if __name__ == '__main__':
  main()
