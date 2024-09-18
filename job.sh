#!/bin/bash 
#SBATCH --account=def-durandau
#SBATCH --job-name=back
#SBATCH --cpus-per-task=12
#SBATCH --time=0-23:00
#SBATCH --array=1
#SBATCH --mem=68G
#SBATCH --mail-user=huiyi.wang@mail.mcgill.ca
#SBATCH --mail-type=ALL

export PYTHONPATH="$PYTHONPATH:/home/cheryl16/projects/def-durandau/cheryl16/MyoBack"

cd /home/cheryl16/projects/def-durandau/cheryl16/MyoBack

module load StdEnv/2023
module load gcc opencv/4.9.0 cuda/12.2 python/3.10 mpi4py mujoco/3.1.6

source /home/cheryl16/py310/bin/activate

export MUJOCO_GL="egl"
export PYOPENGL_PLATFORM="egl"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

wandb offline

parallel -j 5 python train_back.py --group 'myoback_1' --num_envs 8 --learning_rate 0.0002 --clip_range 0.1 --seed ::: {6..10} 