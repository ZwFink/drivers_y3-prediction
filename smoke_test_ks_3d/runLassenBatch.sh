#! /bin/bash
#BSUB -nnodes 1
#BSUB -G uiuc
#BSUB -W 90
#BSUB -J pred_smoke
#BSUB -o charm_odf1_4pes_redo.txt
#BSUB -e charm_odf1_4pes_redo.txt

module load gcc/8.3.1
module load spectrum-mpi

source ~/.bashrc
conda deactivate
conda activate /usr/WS2/fink12/drivers_y3-prediction_charm/emirge/miniforge3/envs/mirgeDriver_retry_with_charm

export PYOPENCL_CTX="port:tesla"
#export PYOPENCL_CTX="0:2"
jsrun_cmd="jsrun -g 1 -a 1 -n 4"
export XDG_CACHE_ROOT="/tmp/$USER/xdg-scratch"
export POCL_CACHE_ROOT="/tmp/$USER/pocl-cache"
$jsrun_cmd js_task_info

# Create the mesh for a small, simple test (size==mesh spacing)
#if [[ ! -f "data/actii.msh" ]]; then
#  cd data
#  ./mkmsh --size=5 --link  # will not overwrite existing actii.msh
#  cd ../
#fi

#$jsrun_cmd bash -c 'POCL_CACHE_DIR=$POCL_CACHE_ROOT/$OMPI_COMM_WORLD_RANK XDG_CACHE_HOME=$XDG_CACHE_ROOT/$OMPI_COMM_WORLD_RANK python -O -u -m mpi4py ./driver.py -i run_params.yaml --log --lazy > mirge-1.out'
#jsrun -g 1 -a 1 -n 4 bash -c 'POCL_CACHE_DIR=$POCL_CACHE_ROOT/$OMPI_COMM_WORLD_RANK XDG_CACHE_HOME=$XDG_CACHE_ROOT/$OMPI_COMM_WORLD_RANK python3 -m mpi4py ./driver.py -i run_params.yaml --lazy'
jsrun -g 1 -a 1 -n 4 bash -c 'POCL_CACHE_DIR=$POCL_CACHE_ROOT/$OMPI_COMM_WORLD_RANK XDG_CACHE_HOME=$XDG_CACHE_ROOT/$OMPI_COMM_WORLD_RANK python3 -O ./driver.py -i run_params.yaml --lazy'
