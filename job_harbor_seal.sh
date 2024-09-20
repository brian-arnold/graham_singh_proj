#!/bin/bash
#SBATCH -J harbor_seal
#SBATCH -o .//out.harbor_seal
#SBATCH -e .//err.harbor_seal
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH -t 1400
#SBATCH --mem=20000
source /home/bjarnold/miniforge3/etc/profile.d/conda.sh
conda activate blast
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/harbor_seal/data/GCF_004348235.1/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > harbor_seal_fwd.out
blastp -query /scratch/gpfs/bjarnold/Graham/ncbi_data/humans/data/GCF_000001405.40/protein.faa -db /scratch/gpfs/bjarnold/Graham/ncbi_data/harbor_seal/data/GCF_004348235.1/blast_db -outfmt 6 -num_threads 20 -max_target_seqs 1 > harbor_seal_frev.out
