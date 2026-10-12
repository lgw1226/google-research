#!/bin/bash
# Nearest-node identification with an identification cap and degree-aware query connection
# (nearest node that has an out-edge for the start / an in-edge for the goal), from
# goal_graph_runs/runs_g0.9_d0 encoders:
#   goal_graph_runs/runs_g0.9_d0_data_near_walk_i10/   walk both (horizon 30), ident_max 10
#   goal_graph_runs/runs_g0.9_d0_data_near_sweep_i10/  full trajectory sweep, ident_max 10
#   goal_graph_runs/runs_g0.9_d0_data_near_sweep_i30/  full trajectory sweep, ident_max 30
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
DS="pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0"
for cfg in "near_walk_i10 --data_walk both --ident_max 10" "near_sweep_i10 --data_walk sweep --ident_max 10" "near_sweep_i30 --data_walk sweep --ident_max 30"; do
  set -- $cfg; out=goal_graph_runs/runs_g0.9_d0_data_$1; shift
  for ds in $DS; do
    mkdir -p $out/$ds
    $PY -m goal_graph.run --dataset $ds --out_root $out --gamma 0.9 --offset_min 0 --graph_mode data \
      --identify nearest --query_connect nearest --data_uncapped --stitch_cost critic "$@" \
      --sweep_k 10 --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > $out/$ds/stdout.txt 2>&1 &
  done
  wait
done
echo NEAREST2_DONE
