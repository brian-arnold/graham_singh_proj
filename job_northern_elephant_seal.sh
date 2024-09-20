#!/bin/bash
#SBATCH -J northern_elephant_seal
#SBATCH -o .//out.northern_elephant_seal
#SBATCH -e .//err.northern_elephant_seal
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH -t 1400
#SBATCH --mem=20000
source /home/bjarnold/miniforge3/etc/profile.d/conda.sh
conda activate blast
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/northern_elephant_seal/data/GCF_029215605.1/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > northern_elephant_seal_fwd.out
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/northern_elephant_seal/data/GCF_029215605.1/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > northern_elephant_seal_frev.out
