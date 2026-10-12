# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0242 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta). 122108 landing states over walk = both, horizon 30. Fraction whose nearest node is still their own node, by offset: 1: 0.92, 5: 0.33, 10: 0.16, 30: 0.10. Identification (hop) cost of kept edges median 26.87, p90 41.54, max 135.5; hop XY distance median 0.67, p90 1.44, 0.002 beyond 4 units. Uncapped out-degree median 12 (max 35), cap None; 95 nodes without an outgoing edge, 85 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 18.20, p90 35.93). No thresholds crossed.

## D. Edges

22765 edges. Cost p50 34.2, p90 56.3, p99 77.8, max 151.4. Out-degree 0/11.4/35 (min/mean/max), in-degree 0/11.4/33. Same-trajectory edges 0.022, of which forward 0.647; forward cost / true Delta median 0.30; 187 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 11 (0.0005), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 10 (0.0004), hop cost median 67.0. **Flags:** edge cost p99 77.8 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 187 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

185 strongly connected components, largest 0.869 of N; 101 weakly connected component(s). **Flags:** largest SCC 0.869 < 0.95; 101 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.63 (p10 0.11, p90 0.89), hops median 6, max edge cost on path median 29.0; 95 wormhole suspects (ratio < 0.3). Query connection: cheapest. Random cross-trajectory node pairs (499): reachability 0.992, cost median 174.0, forward vs backward Pearson 0.49687160055016477, median |log(fwd/bwd)| 0.31. Evaluation tasks: task 1 cost 357, 19 hops; task 2 cost 294, 15 hops; task 3 cost 257, 18 hops; task 4 cost 182, 7 hops; task 5 cost 273, 10 hops. **Flags:** 95 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 8778 | 0.882 | 90.1 | 0.0182 | 1.000 | 0.71 | 0.0007 |
| 2000 | 10 | 22765 | 0.869 | 77.8 | 0.0242 | 1.000 | 0.63 | 0.0005 |
| 5000 | 10 | 82739 | 0.869 | 65.7 | 0.0378 | 1.000 | 0.58 | 0.0001 |
