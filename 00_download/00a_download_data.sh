#!/bin/bash
#SBATCH -J download
#SBATCH -o out
#SBATCH -e err
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=10G         # memory per cpu-core (4G is default)
#SBATCH --time 1-00:00:00        # DAYS-HOURS:MINUTES:SECONDS

# This bash script was run on a detatched screen on the cluster to download the 10X data

# data link specified in the email from Guilin
DATA_LINK='http://fcb.ycga.yale.edu:3010/cMaZuBaKFBP0Ygrh2ubrWr5mn7xa55w/20240821_ccc7_22G7Y5LT4_RQ25573_5p'
BASE_DIR=/scratch/gpfs/bjarnold/Graham
OUT_DIR=${BASE_DIR}/data_10X

wget -e robots=off -r -nH ${DATA_LINK} --directory-prefix ${OUT_DIR}
