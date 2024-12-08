This directory contains a snakemake workflow that runs cellranger. Since it's a single step/rule long, a simple python script probably would have sufficed, but I had grand ambitions of making everything into a single snakemake workflow before I realized that this was unecessary overengineering.


- `00_cellranger_mkref.sh` is a bash script that creates a reference genome for cellranger count. This script does this for each species in serial, since it doesn't take too much time to do so.

- `01_mk_sample_sheet.py` is a python script that creates a sample sheet that is used in a snakemake workflow to run cellranger count on all the samples. This sample sheet has 6 columns that include the sample name, the file paths of the forward and reverse reads (R1 and R2), the file paths of the index files (I1 and I2), and finally the full path to the reference genome created in the previous step.
    - This script produces a file called `sample_sheet.txt`.

- `02_run_snakemake.sh` is a bash script that runs the snakemake workflow specified in the `Snakefile`. This snakemake workflow essentially runs cellranger count on all the samples in parallel. 
    - the `Snakefile` contains the cellranger command. Throughout the process, I experimented with also adding `--include-introns true` and also using the `--force-cells` option with various numbers. However, we ultimately removed these. Regaring the use of `--force-cells`, we decided that it may be better to use all cells and experiment with thresholds in downstream analyses
