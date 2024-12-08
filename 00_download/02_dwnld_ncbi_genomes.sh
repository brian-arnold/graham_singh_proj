source /home/bjarnold/miniforge3/etc/profile.d/conda.sh
conda activate ncbi

#####
# taxids
# harbor seal: "Phoca vitulina"
# california sea lion: "Zalophus californianus"
# northern elephant seal: "Mirounga angustirostris"

# command line tool to download genome: `mamba install -c conda-forge ncbi-datasets-cli``
# see `datasets download genome taxon --help` for more options
#####

DEST_DIR=/scratch/gpfs/bjarnold/Graham/ncbi_data

#####
# harbor seal command
#####
datasets download genome taxon "Phoca vitulina" \
--assembly-level scaffold \
--assembly-source refseq \
--include genome,cds,rna,protein,gtf

unzip ncbi_dataset.zip
mv ncbi_dataset/ harbor_seal
rm ncbi_dataset.zip
mv harbor_seal $DEST_DIR

#####
# california sea lion command
#####
datasets download genome taxon "Zalophus californianus" \
--assembly-level chromosome \
--assembly-source refseq \
--include genome,cds,rna,protein,gtf

unzip ncbi_dataset.zip
mv ncbi_dataset/ ca_sea_lion
rm ncbi_dataset.zip
mv ca_sea_lion $DEST_DIR

#####
# northern elephant seal command
#####
datasets download genome taxon "Mirounga angustirostris" \
--assembly-level scaffold \
--assembly-source refseq \
--include genome,cds,rna,protein,gtf

unzip ncbi_dataset.zip
mv ncbi_dataset/ northern_elephant_seal
rm ncbi_dataset.zip
mv northern_elephant_seal $DEST_DIR

#####
# southern elephant seal command
#####
datasets download genome taxon "Mirounga leonina" \
--assembly-level scaffold \
--assembly-source refseq \
--include genome,cds,rna,protein,gtf

unzip ncbi_dataset.zip
mv ncbi_dataset/ southern_elephant_seal
rm ncbi_dataset.zip
mv southern_elephant_seal $DEST_DIR

#####
# humans
#####
datasets download genome taxon "Homo sapiens" \
--assembly-level chromosome \
--assembly-source refseq \
--include protein

unzip ncbi_dataset.zip
mv ncbi_dataset/ humans
rm ncbi_dataset.zip
mv humans $DEST_DIR


#####
# canine
#####
datasets download genome taxon "Canis" \
--assembly-level chromosome \
--assembly-source refseq \
--include protein

unzip ncbi_dataset.zip
mv ncbi_dataset/ canine
rm ncbi_dataset.zip
mv canine $DEST_DIR