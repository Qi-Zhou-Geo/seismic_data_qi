#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=example          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

#SBATCH --output /your/path/to/output/output.txt
#SBATCH --error /your/path/to/output/error.txt

source /your/path/to/output/miniforge3/bin/activate
conda activate seismic

srun python /your/path/to/output/read_data_from_Glic.py
