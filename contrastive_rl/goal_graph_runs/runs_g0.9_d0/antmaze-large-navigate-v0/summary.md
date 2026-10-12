# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0236 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## D. Edges

27037 edges. Cost p50 30.0, p90 80.7, p99 109.0, max 150.4. Out-degree 10/13.5/29 (min/mean/max), in-degree 10/13.5/54. Same-trajectory edges 0.020, of which forward 0.564; forward cost / true Delta median 0.08; 232 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 282 (0.0104), 3 of them cheaper than Delta_rel. **Flags:** edge cost p99 109.0 > Delta_rel 30 (consider enabling tau); 1 in-degree hubs with in-degree > 5k (max 54); suspected wormhole attractors; 232 same-trajectory forward edges with cost < 0.5*Delta; 282 edges (0.010) are maze shortcuts (BFS cells >> XY distance, i.e. cross walls); their cost median 89.5.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.47 (p10 0.11, p90 0.78), hops median 7, max edge cost on path median 27.7; 108 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 133.6, forward vs backward Pearson 0.4261627861645381, median |log(fwd/bwd)| 0.32. Evaluation tasks: task 1 cost 248, 17 hops; task 2 cost 278, 11 hops; task 3 cost 117, 1 hops; task 4 cost 196, 8 hops; task 5 cost 170, 11 hops. **Flags:** 108 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6912 | 1.000 | 106.9 | 0.0245 | 1.000 | 0.68 | 0.0068 |
| 1000 | 10 | 13295 | 1.000 | 118.2 | 0.0127 | 1.000 | 0.65 | 0.0148 |
| 1000 | 20 | 25942 | 1.000 | 132.6 | 0.0065 | 1.000 | 0.64 | 0.0358 |
| 2000 | 5 | 13934 | 0.996 | 98.0 | 0.0459 | 1.000 | 0.50 | 0.0074 |
| 2000 | 10 | 27037 | 1.000 | 109.0 | 0.0236 | 1.000 | 0.47 | 0.0104 |
| 2000 | 20 | 52798 | 1.000 | 120.8 | 0.0121 | 1.000 | 0.47 | 0.0176 |
| 5000 | 5 | 35862 | 0.990 | 80.5 | 0.1192 | 1.000 | 0.26 | 0.0035 |
| 5000 | 10 | 68930 | 1.000 | 90.3 | 0.0622 | 1.000 | 0.25 | 0.0058 |
| 5000 | 20 | 133812 | 1.000 | 100.4 | 0.0320 | 1.000 | 0.25 | 0.0087 |
