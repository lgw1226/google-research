#!/bin/bash
# Runs the full pipeline on the four OGBench large-maze datasets (GPU 3).
# Usage: goal_graph/run_all.sh [OUT_ROOT] [extra run.py args...]   (default OUT_ROOT=goal_graph_runs/runs)
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
OUT=${1:-goal_graph_runs/runs}; shift
for ds in pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0; do
  mkdir -p $OUT/$ds
  $PY -m goal_graph.run --dataset $ds --out_root $OUT "$@" > $OUT/$ds/stdout.txt 2>&1 &
done
wait
