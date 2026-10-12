# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

Critic undershoot on held-out pairs it would identify (symmetric cost <= cap 30, 4983 pairs): true offset minus critic cost median -4.9, p90 19.5, p99 28.7, max 30.0 steps.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0172 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 30 steps). Full sweep: 1001000 dataset states, 0.592 assigned (nearest cost over all states median 27.3, p90 47.1); 223328 runs of median length 2, 222328 label switches. Entry hop median 27.2, exit hop median 27.0. Identification (hop) cost of kept edges median 25.74, p90 29.35, max 30.0; per-node 90th-percentile radii: exit median 27.0 (p10 19.8, p90 28.2), entry median 26.9 (p10 20.3, p90 28.3); hop XY distance median 0.65, p90 1.38, 0.000 beyond 4 units. Uncapped out-degree median 15 (max 60), cap None; 63 nodes without an outgoing edge, 4 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 54.01, p90 55.89). No thresholds crossed.

## D. Edges

30394 edges. Cost p50 56.0, p90 67.0, p99 92.2, max 764.9. Out-degree 0/15.2/60 (min/mean/max), in-degree 0/15.2/55. Same-trajectory edges 0.016, of which forward 0.562; forward cost / true Delta median 0.42; 144 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 1 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 92.2 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 1 in-degree hubs with in-degree > 5k (max 55); suspected wormhole attractors; 144 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

149 strongly connected components, largest 0.872 of N; 1 weakly connected component(s). **Flags:** largest SCC 0.872 < 0.95.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 0.984, path cost / Delta median 2.12 (p10 0.48, p90 3.32), hops median 7, max edge cost on path median 73.6; 29 wormhole suspects (ratio < 0.3). Against the maze lower bound (speed 0.28 units/step): path cost / LB median 7.47 (p10 5.34), data Delta / LB median 3.30, 0 paths below LB. Query connection: nearest, 402 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.878, cost median 532.1, forward vs backward Pearson 0.8957261446283831, median |log(fwd/bwd)| 0.11254298279269008. Evaluation tasks: task 1 cost 1024, 16 hops; task 2 cost 1222, 20 hops; task 3 cost 882, 16 hops; task 4 cost 283, 6 hops; task 5 cost 982, 15 hops. **Flags:** 29 held-out queries with path cost / Delta < 0.3 (wormhole suspects); median path cost / Delta 2.12 >> 1.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 14058 | 0.887 | 129.8 | 0.0111 | 0.992 | 1.97 | 0.0003 |
| 2000 | 10 | 30394 | 0.872 | 92.2 | 0.0172 | 0.984 | 2.12 | 0.0000 |
| 5000 | 10 | 89333 | 0.872 | 66.5 | 0.0273 | 0.980 | 2.47 | 0.0000 |
