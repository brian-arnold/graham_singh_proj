#!/bin/bash
#SBATCH -J template
#SBATCH -o out
#SBATCH -e err
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=30        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=2G         # memory per cpu-core (4G is default)
#SBATCH --time 1-00:00:00        # DAYS-HOURS:MINUTES:SECONDS

source /home/bjarnold/miniforge3/etc/profile.d/conda.sh
conda activate snakemake_latest

# snakemake --snakefile Snakefile --cores 30 --rerun-incomplete --latency-wait 20

snakemake --profile ./profiles/slurm

# snakemake --executor slurm \
# --default-resources "time='20:00:00'" slurm_partition=cpu slurm_account=cs \
# --jobs 10

# --default-resources time=10 \
# --default-resources time=1-00:00:00 \
# slurm_account=cs

# snakemake --executor cluster-generic \
# --default-resources "time='20:00:00'" \
# --jobs 10
