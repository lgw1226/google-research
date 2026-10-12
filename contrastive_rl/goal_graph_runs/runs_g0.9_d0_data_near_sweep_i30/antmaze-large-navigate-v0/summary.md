# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0172 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 30 steps). Full sweep: 1001000 dataset states, 0.592 assigned (nearest cost over all states median 27.3, p90 47.1); 223328 runs of median length 2, 222328 label switches. Entry hop median 12.6, exit hop median 15.6. Identification (hop) cost of kept edges median 25.93, p90 29.35, max 30.0; hop XY distance median 0.64, p90 1.36, 0.000 beyond 4 units. Uncapped out-degree median 15 (max 60), cap None; 63 nodes without an outgoing edge, 4 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 27.26, p90 47.00). No thresholds crossed.

## D. Edges

30394 edges. Cost p50 31.3, p90 52.8, p99 72.8, max 743.1. Out-degree 0/15.2/60 (min/mean/max), in-degree 0/15.2/55. Same-trajectory edges 0.016, of which forward 0.562; forward cost / true Delta median 0.13; 211 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 1 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 72.8 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 1 in-degree hubs with in-degree > 5k (max 55); suspected wormhole attractors; 211 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

149 strongly connected components, largest 0.872 of N; 1 weakly connected component(s). **Flags:** largest SCC 0.872 < 0.95.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.71 (p10 0.12, p90 1.14), hops median 9, max edge cost on path median 32.9; 79 wormhole suspects (ratio < 0.3). Query connection: nearest, 402 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 143.9, forward vs backward Pearson 0.6074488964677781, median |log(fwd/bwd)| 0.2817649023785802. Evaluation tasks: task 1 cost 296, 41 hops; task 2 cost 329, 38 hops; task 3 cost 156, 1 hops; task 4 cost 300, 1 hops; task 5 cost 287, 47 hops. **Flags:** 79 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 14058 | 0.887 | 109.2 | 0.0111 | 1.000 | 0.80 | 0.0003 |
| 2000 | 10 | 30394 | 0.872 | 72.8 | 0.0172 | 1.000 | 0.71 | 0.0000 |
| 5000 | 10 | 89333 | 0.872 | 58.4 | 0.0273 | 1.000 | 0.72 | 0.0000 |
