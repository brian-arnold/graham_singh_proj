- `00a_download_data.sh` downloaded the original fastq files, and `00b_verify_download.py` verified that the downloaded local files were of the same size as the remote ones on the server. Using MD5 checksums would have been nice but these weren't available. 
    - The file sizes on the remote server can be found here: `/scratch/gpfs/bjarnold/Graham/data_10X/file_sizes_server.txt`

- `01_dwnload_cellranger.sh` is the command that was used to download cellranger.

- `02_dwnld_ncbi_genomes.sh` is a script with various commands that were used to download assemblies and other files from NCBI. If you want to download data from only 1 of these species you can comment out various lines.
    - The NCBI command line tool was used to perform these downloads and was installed via `mamba install -c conda-forge ncbi-datasets-cli`
    - the `datasets` command downloads a file called `ncbi_dataset.zip`, which is decompressed and renamed via commands in `02_dwnld_ncbi_genomes.sh`
    - while we don't analyze southern elephant seal data, we downlaoded data from this species to use the mitochondrial scaffold for the northern elephant seal. 
    - data was also downloaded for humans and canine for references

- `03_make_hybrid_assembly_for_northern_elephant_seal.py` is a script that was used to create a hybrid data for the northern elephant seal. Specifically, it creates a fasta file of the genome assembly, a protein fasta file, and a gtf file using the northern elephant seal for autosomal scaffolds and genes and the southern elephant seal for mitochondrial scaffold and genes. This was done because the Northern elephant seal asembly does not have a mitochondrial scaffold.