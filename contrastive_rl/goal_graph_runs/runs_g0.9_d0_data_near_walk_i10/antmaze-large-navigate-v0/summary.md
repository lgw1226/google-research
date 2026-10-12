# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.1303 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. **Flags:** negative fraction (selected edges) 0.130 > 3%.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). 122108 landing states over walk = both, horizon 30, 0.83 without identification. Fraction whose nearest node is still their own node, by offset: 1: 0.94, 5: 0.63, 10: 0.56, 30: 0.54. Identification (hop) cost of kept edges median 7.91, p90 9.70, max 10.0; hop XY distance median 0.33, p90 0.82, 0.000 beyond 4 units. Uncapped out-degree median 0 (max 6), cap None; 1029 nodes without an outgoing edge, 1014 without an incoming edge; 0.01 of edges have offset 0; stitch cost = critic (added median 5.10, p90 9.18). **Flags:** 1029 nodes have no outgoing data edge.

## D. Edges

1520 edges. Cost p50 17.8, p90 32.5, p99 38.0, max 40.0. Out-degree 0/0.8/6 (min/mean/max), in-degree 0/0.8/9. Same-trajectory edges 0.219, of which forward 0.700; forward cost / true Delta median 0.45; 118 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 38.0 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 118 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1879 strongly connected components, largest 0.004 of N; 861 weakly connected component(s). **Flags:** largest SCC 0.004 < 0.95; 861 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 0.162, path cost / Delta median 0.06 (p10 0.00, p90 0.86), hops median 1, max edge cost on path median 13.0; 67 wormhole suspects (ratio < 0.3). Query connection: nearest, 1255 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.006, cost median 21.3, forward vs backward Pearson None, median |log(fwd/bwd)| 0.4567471108344119. Evaluation tasks: task 1 no path; task 2 no path; task 3 no path; task 4 no path; task 5 no path. **Flags:** held-out path success 0.162 < 0.95; 67 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 5 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 378 | 0.003 | 38.1 | 0.1243 | 0.136 | 0.08 | 0.0000 |
| 2000 | 10 | 1520 | 0.004 | 38.0 | 0.1303 | 0.162 | 0.06 | 0.0000 |
| 5000 | 10 | 8964 | 0.270 | 38.2 | 0.1243 | 0.572 | 1.55 | 0.0000 |
