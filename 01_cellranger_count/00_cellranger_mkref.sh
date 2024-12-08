#!/bin/bash
#SBATCH -J cellranger_mkref
#SBATCH -o out_cellranger_mkref
#SBATCH -e err_cellranger_mkref
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=20G         # memory per cpu-core (4G is default)
#SBATCH --time 1-00:00:00        # DAYS-HOURS:MINUTES:SECONDS

BASE_DIR=/scratch/gpfs/bjarnold/Graham


CR_DIR=${BASE_DIR}/cellranger/cellranger-8.0.1
NCBI_DATA_DIR=${BASE_DIR}/ncbi_data
WORK_DIR=${BASE_DIR}/genomes_10X
cd ${WORK_DIR}

# ###
# # harbor_seal
# ###
# REF_DIR=${NCBI_DATA_DIR}/harbor_seal/data/GCF_004348235.1

# ${CR_DIR}/cellranger \
# mkref \
# --genome=harbor_seal \
# --fasta ${REF_DIR}/GCF_004348235.1_GSC_HSeal_1.0_genomic.fna \
# --genes ${REF_DIR}/genomic.gtf \


# ###
# # ca_sea_lion
# ###
# REF_DIR=${NCBI_DATA_DIR}/ca_sea_lion/data/GCF_009762305.2

# ${CR_DIR}/cellranger \
# mkref \
# --genome=ca_sea_lion \
# --fasta ${REF_DIR}/GCF_009762305.2_mZalCal1.pri.v2_genomic.fna \
# --genes ${REF_DIR}/genomic.gtf \


# ###
# # northern_elephant_seal
# ###
# REF_DIR=${NCBI_DATA_DIR}/northern_elephant_seal/data/GCF_029215605.1

# ${CR_DIR}/cellranger \
# mkref \
# --genome=northern_elephant_seal \
# --fasta ${REF_DIR}/GCF_029215605.1_mMirAng1.0.hap1_genomic.fna \
# --genes ${REF_DIR}/genomic.gtf \


###
# northern_elephant_seal_hybrid
###
REF_DIR=${NCBI_DATA_DIR}/northern_elephant_seal_hybrid/data

${CR_DIR}/cellranger \
mkref \
--genome=northern_elephant_seal_hybrid \
--fasta ${REF_DIR}/hybrid_assembly.fasta \
--genes ${REF_DIR}/hybrid_assembly.gtf \