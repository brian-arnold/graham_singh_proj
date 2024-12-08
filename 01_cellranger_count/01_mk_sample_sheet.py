#!/usr/bin/python -tt

"""
"""

import re
import sys
import os
import glob
from dataclasses import dataclass

@dataclass
class Sample:
    name: str
    R1: str
    R2: str
    I1: str
    I2: str
    genome: str

def get_sample_names(files):
    samples = []
    for f in files:
        f = os.path.basename(f)
        sample = f.split('_')[0:3]
        sample = '_'.join(sample)
        samples.append(sample)
    return samples

def main():

    BASE_DIR = '/scratch/gpfs/bjarnold/Graham'
    GENOME_DIR = f'{BASE_DIR}/genomes_10X'
    DATA_DIR = f'{BASE_DIR}/data_10X/cMaZuBaKFBP0Ygrh2ubrWr5mn7xa55w/20240821_ccc7_22G7Y5LT4_RQ25573_5p'

    files = glob.glob(f'{DATA_DIR}/*_R1_*')
    # files = [os.path.basename(f) for f in files]

    species_code_2_name = {'HS':'harbor_seal',
                           'CSL':'ca_sea_lion',
                           'ES':'northern_elephant_seal_hybrid',
                        #    'ES':'northern_elephant_seal',
                           }

    samples = get_sample_names(files)
    print("Samples:")
    print(samples)

    sample_sheet_info = []
    for samp in samples:
        # get the file in files list that contains the sample name
        R1 = [f for f in files if samp in f]
        assert len(R1) == 1, f"you have duplicate read files: {R1}"
        R1 = R1[0]
        # names of other files should be identical with exception of _R1_
        R2, I1, I2 = R1.replace('_R1_', '_R2_'), R1.replace('_R1_', '_I1_'), R1.replace('_R1_', '_I2_')

        # get species code
        species_code = samp.split('-')[0]
        species_name = species_code_2_name[species_code]
        genome = f'{GENOME_DIR}/{species_name}'

        sample_sheet_info.append(Sample(samp, R1, R2, I1, I2, genome))

    with open('sample_sheet.txt','w') as f:
        f.write('sample\tR1\tR2\tI1\tI2\tgenome\n')
        for s in sample_sheet_info:
            f.write(f'{s.name}\t{s.R1}\t{s.R2}\t{s.I1}\t{s.I2}\t{s.genome}\n')

if __name__ == '__main__':
  main()
