#!/bin/zsh
#SBATCH --job-name=evaluation_sweep
#SBATCH --account=cocoflops
#SBATCH --partition=cocoflops
#SBATCH --nodelist=cocoflops1
#SBATCH --array=0-19
#SBATCH --nice=1000
#SBATCH --output=slurm-output/eval_sweep_%a.log
#SBATCH --error=slurm-output/eval_sweep_%a.log
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=6:00:00

# Add your SLURM directives and options here

# Load any necessary modules
source ~/.zshrc

# Change to the working directory
cd ~/reasoning-in-chains

conda activate reasoning-chains
python scripts/model_evaluation_sweep.py ${SLURM_ARRAY_TASK_ID}
