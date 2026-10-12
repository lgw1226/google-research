# Contrastive goal graph (OGBench large mazes)

Builds a directed, weighted graph over states sampled from an offline
goal-conditioned dataset, with edge costs from a contrastive state encoder phi
and goal encoder psi (binary NCE on (state, future-state) pairs), then reports
diagnostics A-G and plots. JAX/Flax for training, NumPy/SciPy for the graph.

```
conda activate off-gcrl          # has jax (GPU), flax, optax, ogbench, scipy
cd contrastive_rl
MUJOCO_GL=egl CUDA_VISIBLE_DEVICES=3 python -m goal_graph.run --dataset pointmaze-large-navigate-v0
goal_graph/run_all.sh            # all four datasets in parallel on GPU 3
```

All run folders live under `goal_graph_runs/` (see `goal_graph_runs/README.md` for an index).
Outputs under `goal_graph_runs/runs/<dataset>/`: `graph.npz`, `encoders.pkl`, `train_log.csv`,
`calibration_pairs.npz`, `metrics.json`, `sweep.csv`, `summary.md`, `plots/`,
`wormholes/` (endpoint states of every edge on paths with cost / Delta < 0.3),
`log.txt`.

Modules: `data.py` (trajectories), `encoders.py` (phi/psi MLPs, NCE training,
on-device geometric-offset sampling), `graph.py` (nodes, cost matrix, k-NN
edge selection, Dijkstra planner with query augmentation), `metrics.py`
(groups A-G), `plots.py`, `run.py` (driver; `--load_encoders` skips training).

Cost convention: `C[i, j] = (M[j, j] - M[i, j]) / (-log gamma)` in steps,
clipped at `eps = 1e-6`; negative fraction is logged before clipping.
Delta_rel is the largest Delta such that all calibration bins up to it have a
median within 20% of the linear fit (floored at `--delta_rel_min`).

## Findings from the first runs (2026-10-08)

- `goal_graph_runs/runs/` holds the spec defaults (gamma = 0.99). On all four datasets 51-83% of the
  *selected* edges have negative raw cost: the diagonal reference M_jj is exceeded by a
  median of 7-19 entries per column (positives use Delta >= 1 and the agent never stays
  put), so the k = 10 cheapest edges per node are exactly those entries. Edge costs are
  clipped to eps, path cost / Delta is ~0, and some paths cross maze walls.
- The calibration curve (plot 1) is flat/negative for Delta below ~20-50 steps and only
  then linear (slope 1.8-2.8), i.e. the critic is uninformative at the edge scale when
  1/(1 - gamma) = 100 >> the few-step edges.
- `goal_graph_runs/runs_gamma0.9/` repeats everything with gamma = 0.9 (1/(1 - gamma) = 10): linear
  from Delta = 1, Delta_rel = 30 (= range cap), negative edge fraction 6-43%, edge cost
  p99 26-109 steps, no wall-crossing edges in pointmaze, all 5 eval tasks reachable on
  3/4 datasets. Path costs are still compressed (ratio ~0.1-0.3).
- 2026-10-12: defaults changed to gamma = 0.9 and `--offset_min 0` (positives include
  (s, s) with probability 1 - gamma). `goal_graph_runs/runs_g0.9_d0/` (edge_mode both) and
  `goal_graph_runs/runs_g0.9_d0_in/` (incoming-only edges) share encoders. Delta = 0 cut the negative
  edge fraction to 2-30% and in-degree hubs to <= 59; incoming-only edges leave nodes
  with out-degree 0, fragment the stitch graphs (SCC 0.63 vs 0.92 on pointmaze-stitch)
  and do not change path costs, so `both` stays the default.
- 2026-10-12: `--graph_mode data` (goal_graph/data_edges.py) builds fixed-node, data-cost
  edges: walk each node along its trajectory (forward and/or backward, `--data_walk`,
  horizon `--data_horizon`), identify walked states with nodes by a mutual critic test
  with threshold theta calibrated on held-out pairs (`--merge_delta`, `--merge_tpr`),
  cost = true offset (+ critic stitch hop with `--stitch_cost critic`). `--data_uncapped`
  keeps all matched edges; `--query_connect mutual` applies the same test to query
  start/goal (falls back to k cheapest). Runs: goal_graph_runs/runs_g0.9_d0_data_{sc,fwd_unc,both,
  both_unc,both_unc_mq}/. Result: zero wall-crossing edges on all datasets (critic graphs
  had ~1% on antmaze); both-walk uncapped matches the critic graph's connectivity on
  pointmaze (SCC >= 0.99) but antmaze stays at 0.87-0.94 (velocity must match to
  identify); path ratios are unchanged on pointmaze (~0.2) and 0.55-0.70 on antmaze;
  the k cap by cheapest cost is harmful (offset-0 merges crowd out walking edges).
- 2026-10-12: `--identify nearest` (no theta): every landing state identifies with its
  single nearest node under the symmetric cost max(c(w->n), c(n->w)) and the hop is always
  charged (edge cost = offset + critic hop), so far identifications are expensive rather
  than rejected; `--query_connect nearest` connects query start/goal to their single
  nearest node the same way (no fallback). Diagnostics: self-match rate by offset
  (node-density check), hop cost / XY distance, and wall-crossing of the identification
  hops. Runs: goal_graph_runs/runs_g0.9_d0_data_nearest/ (query nearest), goal_graph_runs/runs_g0.9_d0_data_nearest_qc/
  (query k cheapest); `goal_graph/run_nearest.sh`. Result: 3x fewer edges than the theta graphs,
  held-out path cost / Delta 0.45-0.49 on pointmaze (theta: 0.17-0.22) and 0.86-0.99 on
  antmaze, and the ratio is stable over N = 1000..5000 (critic and theta graphs fall to
  0.05-0.1 at N = 5000); 0 wall-crossing hops on pointmaze, 10-43 (<0.2%) on antmaze, all
  charged 46-160 steps. Nearest query connection fails when the goal's nearest node has no
  incoming edge (nodes at trajectory starts): 1/5 tasks on the navigate datasets.
- 2026-10-12 (later): `--data_walk sweep` projects every dataset state onto its nearest node
  (cap `--ident_max`, states beyond it are unassigned "transit") and adds an edge at every
  label switch along each trajectory, which removes the dangling nodes (antmaze: 57 isolated
  -> 0 with cap 30). `--query_connect nearest` now picks the nearest node that has an
  out-edge (start) / in-edge (goal). Edge cost options: per-segment critic hops
  (`--sweep_radius critic`, default; cheapest-of-many bias returns, ratio ~0.2 on pointmaze),
  pure data time (`--sweep_entry first --stitch_cost none`, ratio 0.08-0.43, worst), or the
  conservative rule `--sweep_radius cap`: cost = cap + data steps + cap, start/goal hops =
  cap, no critic cost anywhere. Cap runs (goal_graph_runs/runs_g0.9_d0_data_sweep_cap/, cap 10 pointmaze /
  30 antmaze): 0 paths below the maze lower bound, wormhole suspects 0-20 (from 380-495),
  path cost / data length 1.3-2.4 and rising with N (more hops x 2 cap). `--ident_max 10` is
  too tight for antmaze (critic puts cluster states ~27 steps from their node). Metrics added:
  maze lower bound (B/F), critic undershoot within cap (B). Scripts: run_nearest2.sh,
  run_sweep_pure.sh, run_sweep_cap.sh, compare_nearest2.py.
- `--sweep_radius q90` (goal_graph_runs/runs_g0.9_d0_data_sweep_q90/, run_sweep_q90.sh): per-node radii =
  90th percentile of the critic hop over the node's cluster (exit node->state, entry
  state->node), start/goal connect at the node's radius. Pointmaze radii are 1-2.5 steps
  (cap 10), so path/data drops from 2.3/1.3 (cap) to 0.83/0.52; still 0 paths below the
  maze lower bound, but wormhole suspects rise (18->71, 3->91) and the ratio now falls with N
  (0.97 -> 0.65 at N=5000) because the critic's short-range hop estimates shrink with cluster
  size faster than they should (short-range undershoot). Antmaze radii ~27 ~ cap 30: no real
  change (2.38 -> 2.12).
