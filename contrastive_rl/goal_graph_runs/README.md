# Goal-graph runs (all four OGBench large mazes per folder)

Every folder has `<dataset>/{graph.npz, metrics.json, summary.md, sweep.csv, plots/, log.txt}`.
Encoders: `runs/` and `runs_gamma0.9/` trained their own; everything from `runs_g0.9_d0/` on
reuses `runs_g0.9_d0/<dataset>/encoders.pkl` (gamma 0.9, offset_min 0).

| folder | graph | edge cost | notes |
|---|---|---|---|
| runs | critic k-NN, gamma 0.99, offsets >= 1 | critic | spec defaults; negative costs, hubs, wall crossings |
| runs_gamma0.9 | critic k-NN, gamma 0.9, offsets >= 1 | critic | calibration linear to 30 steps |
| runs_g0.9_d0 | critic k-NN, gamma 0.9, offsets >= 0, in+out edges | critic | encoders reused below |
| runs_g0.9_d0_in | same, incoming edges only | critic | fragments stitch graphs |
| runs_g0.9_d0_data | walk fwd, theta mutual test, k cap | data offset only | free merges, zero path costs |
| runs_g0.9_d0_data_sc | walk fwd, theta, k cap | offset + critic hop | |
| runs_g0.9_d0_data_fwd_unc | walk fwd, theta, uncapped | offset + critic hop | |
| runs_g0.9_d0_data_both | walk fwd+bwd, theta, k cap | offset + critic hop | cap by cheapest is harmful |
| runs_g0.9_d0_data_both_unc | walk fwd+bwd, theta, uncapped | offset + critic hop | best theta graph |
| runs_g0.9_d0_data_both_unc_mq | same, mutual query connection (fallback) | offset + critic hop | fallback hid coverage gaps |
| runs_g0.9_d0_data_nearest | walk fwd+bwd, nearest-node identification, query nearest | offset + critic hop | first nearest variant |
| runs_g0.9_d0_data_nearest_qc | same, query k cheapest | offset + critic hop | |
| runs_g0.9_d0_data_near_walk_i10 | walk, nearest, cap 10, degree-aware query | offset + critic hop | cap 10 collapses antmaze |
| runs_g0.9_d0_data_near_sweep_i10 | trajectory sweep, cap 10 | data steps + critic hops | no dangling nodes (pointmaze) |
| runs_g0.9_d0_data_near_sweep_i30 | trajectory sweep, cap 30 | data steps + critic hops | no dangling nodes (antmaze) |
| runs_g0.9_d0_data_sweep_pure | sweep, cap 10/30 | data steps only | shortest, underestimates |
| runs_g0.9_d0_data_sweep_cap | sweep, cap 10/30 | cap + data steps + cap | **conservative prototype**; 0 below lower bound |
| runs_g0.9_d0_data_sweep_q90 | sweep, cap 10/30 | per-node q90 radius + data steps + q90 | cluster-size aware; shrinks with N |

Comparison tables: `runs_g0.9_d0_data_nearest/comparison.txt`, `runs_g0.9_d0_data_near_sweep_i10/comparison.txt`,
`runs_g0.9_d0_data_sweep_cap/comparison.txt`, `runs_g0.9_d0_data_sweep_q90/comparison.txt`
(regenerate with `python goal_graph/compare_nearest2.py` from `contrastive_rl/`).
