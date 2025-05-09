#!/bin/zsh
#SBATCH --job-name=train_all_transformers
#SBATCH --account=cocoflops
#SBATCH --partition=cocoflops
#SBATCH --nodelist=cocoflops1
#SBATCH --array=0-19
#SBATCH --nice=1000
#SBATCH --output=slurm-output/training_sweep_%a.out
#SBATCH --error=slurm-output/training_sweep_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00

source ~/.zshrc

cd ~/reasoning-in-chains

conda activate reasoning-chains
python scripts/model_training_sweep.py ${SLURM_ARRAY_TASK_ID}
