#!/bin/bash
# gamma 0.9, offset_min 0: train once per dataset (edge_mode both), then reuse the
# encoders for edge_mode in. Outputs: goal_graph_runs/runs_g0.9_d0/<ds> (both), goal_graph_runs/runs_g0.9_d0_in/<ds> (in).
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
DS="pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0"
for ds in $DS; do
  mkdir -p goal_graph_runs/runs_g0.9_d0/$ds
  $PY -m goal_graph.run --dataset $ds --out_root goal_graph_runs/runs_g0.9_d0 --gamma 0.9 --offset_min 0 --edge_mode both > goal_graph_runs/runs_g0.9_d0/$ds/stdout.txt 2>&1 &
done
wait
for ds in $DS; do
  mkdir -p goal_graph_runs/runs_g0.9_d0_in/$ds
  $PY -m goal_graph.run --dataset $ds --out_root goal_graph_runs/runs_g0.9_d0_in --gamma 0.9 --offset_min 0 --edge_mode in --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > goal_graph_runs/runs_g0.9_d0_in/$ds/stdout.txt 2>&1 &
done
wait
echo COMPARE_DONE
