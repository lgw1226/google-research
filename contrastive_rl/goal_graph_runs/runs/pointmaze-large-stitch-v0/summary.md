# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.99, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 280000 steps (B = 256). Held-out loss 0.0147, top-1 accuracy 0.160 (chance 0.0039); train loss 0.0145, accuracy 0.166. Mean positive logit -2.67 vs negative -11.96. Clipped positives 0.425. Row normalization over 500 held-out states: CV 0.40, std of log mean exp 0.39. **Flags:** clipped positive fraction 0.43 > 0.3 (consider resampling Delta or smaller gamma).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 200]: Spearman rho 0.666; linear fit slope 2.593, intercept -38.98 (fit to binned medians, Delta <= 100; R2 0.949 on medians, 0.355 on raw pairs). Delta_rel = 5; the binned median is within 20% of the fit for Delta in [51.0, 160.0]. Backward minus forward cost median 177.7 (backward rho 0.691). **Flags:** binned median leaves the linear fit at the SHORT end: linear only for Delta in [51, 160] (cost ~ 0 or negative below); Delta_rel=0 below floor 5; using floor (calibration breaks at short horizons); forward Spearman rho 0.666 < 0.8.

## C. Cost matrix

Negative fraction 0.0068 of off-diagonal entries and 0.6744 of selected edges (min raw cost -239.5). diag(M) median -1.90 (p1 -2.86, p99 0.08), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.736. **Flags:** negative fraction (selected edges) 0.674 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

30738 edges. Cost p50 0.0, p90 24.9, p99 129.3, max 690.1. Out-degree 10/15.4/48 (min/mean/max), in-degree 10/15.4/62. Same-trajectory edges 0.006, of which forward 0.571; forward cost / true Delta median 0.00; 76 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 12 (0.0004), 4 of them cheaper than Delta_rel. **Flags:** edge cost p99 129.3 > Delta_rel 5 (consider enabling tau); 3 in-degree hubs with in-degree > 5k (max 62); suspected wormhole attractors; 76 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

237 strongly connected components, largest 0.644 of N; 1 weakly connected component(s). **Flags:** largest SCC 0.644 < 0.95.

## F. Paths

Held-out same-trajectory queries (500, Delta in [10, 50]): success 1.000, path cost / Delta median 0.21 (p10 0.00, p90 4.70), hops median 1, max edge cost on path median 4.5; 270 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 0.711, cost median 115.4, forward vs backward Pearson 0.21663230560306337, median |log(fwd/bwd)| 1.04. Evaluation tasks: task 1 cost 370, 18 hops; task 2 no path; task 3 cost 265, 32 hops; task 4 no path; task 5 cost 182, 17 hops. **Flags:** 270 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 2 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 7678 | 0.445 | 127.5 | 0.6727 | 0.976 | 0.22 | 0.0003 |
| 1000 | 10 | 13852 | 0.881 | 254.9 | 0.4685 | 1.000 | 0.23 | 0.0012 |
| 1000 | 20 | 25984 | 1.000 | 373.9 | 0.2634 | 1.000 | 0.23 | 0.0026 |
| 2000 | 5 | 17031 | 0.375 | 61.5 | 0.8133 | 0.998 | 0.27 | 0.0002 |
| 2000 | 10 | 30738 | 0.644 | 129.3 | 0.6744 | 1.000 | 0.21 | 0.0004 |
| 2000 | 20 | 54745 | 0.918 | 222.9 | 0.4697 | 1.000 | 0.17 | 0.0010 |
| 5000 | 5 | 46205 | 0.355 | 22.2 | 0.9291 | 0.998 | 0.10 | 0.0002 |
| 5000 | 10 | 86664 | 0.468 | 39.5 | 0.8621 | 1.000 | 0.06 | 0.0003 |
| 5000 | 20 | 157709 | 0.730 | 77.3 | 0.7356 | 1.000 | 0.05 | 0.0003 |
