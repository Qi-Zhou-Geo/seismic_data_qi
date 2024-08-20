#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=Qi_run          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

source /your/path/for/miniforge3/bin/activate
conda activate seismic

run python /your/python/file/path/test.py
