#!/bin/bash
# Data-cost graphs (stitch cost = critic) from goal_graph_runs/runs_g0.9_d0 encoders:
#   goal_graph_runs/runs_g0.9_d0_data_fwd_unc/  forward walk, uncapped
#   goal_graph_runs/runs_g0.9_d0_data_both/     forward+backward walk, k cap
#   goal_graph_runs/runs_g0.9_d0_data_both_unc/ forward+backward walk, uncapped
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
for ds in pointmaze-large-navigate-v0 pointmaze-large-stitch-v0 antmaze-large-navigate-v0 antmaze-large-stitch-v0; do
  for cfg in "fwd_unc --data_walk forward --data_uncapped" "both --data_walk both" "both_unc --data_walk both --data_uncapped"; do
    set -- $cfg; out=goal_graph_runs/runs_g0.9_d0_data_$1; shift
    mkdir -p $out/$ds
    $PY -m goal_graph.run --dataset $ds --out_root $out --gamma 0.9 --offset_min 0 --graph_mode data \
      --stitch_cost critic "$@" --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > $out/$ds/stdout.txt 2>&1 &
  done
done
wait
echo DATA2_DONE
