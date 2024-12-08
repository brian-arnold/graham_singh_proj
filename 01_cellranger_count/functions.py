#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
from collections import defaultdict
import pandas as pd

def parse_sample_sheet(sample_sheet : str) -> dict:
    """
    Parse the sample sheet and return a dictionary with the sample name as key
    and the sample genome as value
    """
    samples_2_genome = defaultdict(dict)
    df = pd.read_csv(sample_sheet, sep='\t')
    data_dir = set()
    for i,r in df.iterrows():
        sample = r['sample']
        genome = r['genome']
        assert os.path.isdir(genome), f"Genome directory {genome} does not exist"
        assert os.path.isfile(r['R1']), f"R1 file {r['R1']} does not exist"
        assert os.path.isfile(r['R2']), f"R2 file {r['R2']} does not exist"
        assert os.path.isfile(r['I1']), f"I1 file {r['I1']} does not exist"
        assert os.path.isfile(r['I2']), f"I2 file {r['I2']} does not exist"

        samples_2_genome[sample] = genome

        data_dir.add(os.path.dirname(r['R1']))
    # use the directory of the first file as the data directory, but here we assume all data files are in the same directory
    assert len(data_dir) == 1, f"Multiple data directories found: {data_dir}"

    return samples_2_genome, data_dir.pop()
