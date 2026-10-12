#!/bin/bash
# Recompute graph + metrics A-G from saved encoders (no retraining), all four datasets.
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
for ds in pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0; do
  $PY -m goal_graph.run --dataset $ds --load_encoders goal_graph_runs/runs/$ds/encoders.pkl "$@" > goal_graph_runs/runs/$ds/stdout_metrics.txt 2>&1 &
done
wait
