- `config.py` stores information on the paths to the input protein fasta files that will be used for blast. It also stores the names of the blast databases that will be created by the downstream steps.

- `00_makeblastdb.sh` is a bash script that runs the `00_makeblastdb.py` python script, which makes a blast database from the input protein fasta file. This script imports `config.py` to get the paths to the input files.

- `01_blastp.py` is a python script that submits a blastp job to the cluster and runs reciprocal blasts between a given target species and the human reference. One SLURM job is submitted per sea-diving mammal species, and each of the reciprocal blasts are run in serial within each job.

- `02_reciprocal_best_hits.py` parses the blastp output to find proteins that have recirprocal best blast hits. This script creates a file called `rbbh_gene.csv` that contains all the reciprocal best blast hits.