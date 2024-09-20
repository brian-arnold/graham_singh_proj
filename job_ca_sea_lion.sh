#!/bin/bash
#SBATCH -J ca_sea_lion
#SBATCH -o .//out.ca_sea_lion
#SBATCH -e .//err.ca_sea_lion
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH -t 1400
#SBATCH --mem=20000
source /home/bjarnold/miniforge3/etc/profile.d/conda.sh
conda activate blast
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/ca_sea_lion/data/GCF_009762305.2/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > ca_sea_lion_fwd.out
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/ca_sea_lion/data/GCF_009762305.2/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > ca_sea_lion_frev.out
