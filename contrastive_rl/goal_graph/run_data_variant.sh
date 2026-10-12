#!/bin/bash
# Data-cost graphs from the gamma 0.9 / offset_min 0 encoders in goal_graph_runs/runs_g0.9_d0/.
#   goal_graph_runs/runs_g0.9_d0_data/     : cost = data offset only (identified nodes merged for free)
#   goal_graph_runs/runs_g0.9_d0_data_sc/  : cost = data offset + critic landing->node cost
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
for ds in pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0; do
  for sc in none critic; do
    out=goal_graph_runs/runs_g0.9_d0_data; [ $sc = critic ] && out=goal_graph_runs/runs_g0.9_d0_data_sc
    mkdir -p $out/$ds
    $PY -m goal_graph.run --dataset $ds --out_root $out --gamma 0.9 --offset_min 0 --graph_mode data \
      --stitch_cost $sc --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > $out/$ds/stdout.txt 2>&1 &
  done
done
wait
echo DATA_DONE
