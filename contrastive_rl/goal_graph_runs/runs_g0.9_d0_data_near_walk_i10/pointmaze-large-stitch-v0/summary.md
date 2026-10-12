# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.1407 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.141 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). 114716 landing states over walk = both, horizon 30, 0.02 without identification. Fraction whose nearest node is still their own node, by offset: 1: 0.26, 5: 0.05, 10: 0.02, 30: 0.02. Identification (hop) cost of kept edges median 0.24, p90 3.17, max 10.0; hop XY distance median 0.05, p90 0.39, 0.000 beyond 4 units. Uncapped out-degree median 21 (max 51), cap None; 0 nodes without an outgoing edge, 15 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 0.07, p90 1.62). No thresholds crossed.

## D. Edges

43770 edges. Cost p50 12.0, p90 26.8, p99 31.4, max 39.9. Out-degree 2/21.9/51 (min/mean/max), in-degree 0/21.9/57. Same-trajectory edges 0.007, of which forward 0.687; forward cost / true Delta median 0.53; 96 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 31.4 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 5 in-degree hubs with in-degree > 5k (max 57); suspected wormhole attractors; 96 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

20 strongly connected components, largest 0.989 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.998, path cost / Delta median 0.34 (p10 0.10, p90 0.58), hops median 11, max edge cost on path median 12.7; 189 wormhole suspects (ratio < 0.3). Query connection: nearest, 63 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.994, cost median 105.5, forward vs backward Pearson 0.9727974085965035, median |log(fwd/bwd)| 0.08870108421911815. Evaluation tasks: task 1 cost 255, 48 hops; task 2 no path; task 3 cost 202, 42 hops; task 4 cost 271, 37 hops; task 5 cost 275, 42 hops. **Flags:** 189 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 1 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 14399 | 0.967 | 32.8 | 0.1099 | 0.994 | 0.35 | 0.0000 |
| 2000 | 10 | 43770 | 0.989 | 31.4 | 0.1407 | 0.998 | 0.34 | 0.0000 |
| 5000 | 10 | 164126 | 0.996 | 30.5 | 0.1412 | 1.000 | 0.30 | 0.0000 |
