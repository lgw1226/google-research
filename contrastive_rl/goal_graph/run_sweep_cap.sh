#!/bin/bash
# Conservative sweep: nearest identification capped (10 pointmaze / 30 antmaze), edge cost =
# cap + data steps (first entry of A to first entry of B) + cap; start/goal connect to the
# nearest node with edges at cost cap.  No critic cost anywhere.  Output: goal_graph_runs/runs_g0.9_d0_data_sweep_cap/
cd "$(dirname "$0")/.."
export MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 XLA_PYTHON_CLIENT_PREALLOCATE=false
PY=~/miniconda3/envs/off-gcrl/bin/python
out=goal_graph_runs/runs_g0.9_d0_data_sweep_cap
for cfg in "pointmaze-large-navigate-v0 10" "pointmaze-large-stitch-v0 10" "antmaze-large-navigate-v0 30" "antmaze-large-stitch-v0 30"; do
  set -- $cfg; ds=$1; im=$2
  mkdir -p $out/$ds
  $PY -m goal_graph.run --dataset $ds --out_root $out --gamma 0.9 --offset_min 0 --graph_mode data \
    --identify nearest --query_connect nearest --data_uncapped --data_walk sweep --sweep_radius cap \
    --ident_max $im --sweep_k 10 --load_encoders goal_graph_runs/runs_g0.9_d0/$ds/encoders.pkl > $out/$ds/stdout.txt 2>&1 &
done
wait
echo CAP_DONE
