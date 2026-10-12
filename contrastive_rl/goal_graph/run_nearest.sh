#!/bin/bash
# Nearest-node identification (no theta), both walks, uncapped, stitch cost = critic,
# from goal_graph_runs/runs_g0.9_d0 encoders:
#   goal_graph_runs/runs_g0.9_d0_data_nearest/     query connect = nearest (single nearest node each side)
#   goal_graph_runs/runs_g0.9_d0_data_nearest_qc/  query connect = cheapest (k cheapest critic edges)
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
DS="pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0"
for cfg in "nearest nearest" "nearest_qc cheapest"; do
  set -- $cfg; out=goal_graph_runs/runs_g0.9_d0_data_$1; qc=$2
  for ds in $DS; do
    mkdir -p $out/$ds
    $PY -m goal_graph.run --dataset $ds --out_root $out --gamma 0.9 --offset_min 0 --graph_mode data \
      --identify nearest --query_connect $qc --data_walk both --data_uncapped --stitch_cost critic \
      --sweep_k 10 --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > $out/$ds/stdout.txt 2>&1 &
  done
  wait
done
echo NEAREST_DONE
