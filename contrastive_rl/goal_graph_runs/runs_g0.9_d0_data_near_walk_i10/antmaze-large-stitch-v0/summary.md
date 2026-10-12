# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0877 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** negative fraction (selected edges) 0.088 > 3%; 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). 114716 landing states over walk = both, horizon 30, 0.91 without identification. Fraction whose nearest node is still their own node, by offset: 1: 0.97, 5: 0.59, 10: 0.48, 30: 0.38. Identification (hop) cost of kept edges median 8.21, p90 9.72, max 10.0; hop XY distance median 0.35, p90 0.80, 0.000 beyond 4 units. Uncapped out-degree median 0 (max 9), cap None; 1146 nodes without an outgoing edge, 1194 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 5.76, p90 9.32). **Flags:** 1146 nodes have no outgoing data edge.

## D. Edges

1174 edges. Cost p50 20.0, p90 33.2, p99 38.9, max 39.8. Out-degree 0/0.6/9 (min/mean/max), in-degree 0/0.6/6. Same-trajectory edges 0.113, of which forward 0.947; forward cost / true Delta median 0.95; 7 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 38.9 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 7 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1966 strongly connected components, largest 0.003 of N; 974 weakly connected component(s). **Flags:** largest SCC 0.003 < 0.95; 974 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.052, path cost / Delta median 0.70 (p10 0.21, p90 1.38), hops median 2, max edge cost on path median 35.0; 6 wormhole suspects (ratio < 0.3). Query connection: nearest, 1304 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.006, cost median 35.2, forward vs backward Pearson None, median |log(fwd/bwd)| 0.8196691525992326. Evaluation tasks: task 1 no path; task 2 no path; task 3 no path; task 4 no path; task 5 no path. **Flags:** held-out path success 0.052 < 0.95; 6 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 5 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 308 | 0.002 | 37.8 | 0.0390 | 0.050 | 0.62 | 0.0000 |
| 2000 | 10 | 1174 | 0.003 | 38.9 | 0.0877 | 0.052 | 0.70 | 0.0000 |
| 5000 | 10 | 6877 | 0.009 | 38.4 | 0.0839 | 0.210 | 1.45 | 0.0000 |
