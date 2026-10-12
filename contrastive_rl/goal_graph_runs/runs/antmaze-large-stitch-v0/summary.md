# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.99, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 185000 steps (B = 256). Held-out loss 0.0143, top-1 accuracy 0.242 (chance 0.0039); train loss 0.0124, accuracy 0.343. Mean positive logit -2.49 vs negative -17.48. Clipped positives 0.429. Row normalization over 500 held-out states: CV 14.10, std of log mean exp 0.82. **Flags:** row-normalization CV 14.10 > 1 (poor calibration); train/held-out acc gap 0.101 > 0.1; clipped positive fraction 0.43 > 0.3 (consider resampling Delta or smaller gamma).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 200]: Spearman rho 0.571; linear fit slope 2.803, intercept -20.22 (fit to binned medians, Delta <= 100; R2 0.997 on medians, 0.201 on raw pairs). Delta_rel = 5; the binned median is within 20% of the fit for Delta in [11.0, 150.0]. Backward minus forward cost median 640.8 (backward rho 0.570). **Flags:** binned median leaves the linear fit at the SHORT end: linear only for Delta in [11, 150] (cost ~ 0 or negative below); Delta_rel=0 below floor 5; using floor (calibration breaks at short horizons); forward Spearman rho 0.571 < 0.8; forward binned median is not monotone.

## C. Cost matrix

Negative fraction 0.0045 of off-diagonal entries and 0.5103 of selected edges (min raw cost -484.6). diag(M) median -1.49 (p1 -3.59, p99 2.92), 34 outliers with |z| > 3. Pearson(C, C^T) = 0.512. **Flags:** negative fraction (selected edges) 0.510 > 3%; 34 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

30051 edges. Cost p50 0.0, p90 136.3, p99 629.1, max 1386.4. Out-degree 10/15.0/48 (min/mean/max), in-degree 10/15.0/101. Same-trajectory edges 0.007, of which forward 0.725; forward cost / true Delta median 0.00; 91 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 131 (0.0044), 42 of them cheaper than Delta_rel. **Flags:** edge cost p99 629.1 > Delta_rel 5 (consider enabling tau); 18 in-degree hubs with in-degree > 5k (max 101); suspected wormhole attractors; 91 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [10, 50]): success 1.000, path cost / Delta median 0.00 (p10 0.00, p90 2.27), hops median 2, max edge cost on path median 0.0; 358 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 0.0, forward vs backward Pearson 0.6010985382537136, median |log(fwd/bwd)| 1.01. Evaluation tasks: task 1 cost 0, 7 hops; task 2 cost 0, 9 hops; task 3 cost 94, 8 hops; task 4 cost 62, 7 hops; task 5 cost 60, 7 hops. **Flags:** 358 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 7544 | 1.000 | 605.3 | 0.5027 | 1.000 | 0.00 | 0.0038 |
| 1000 | 10 | 14063 | 1.000 | 667.4 | 0.3191 | 1.000 | 0.00 | 0.0054 |
| 1000 | 20 | 27116 | 1.000 | 764.2 | 0.1719 | 1.000 | 0.00 | 0.0116 |
| 2000 | 5 | 16454 | 1.000 | 548.3 | 0.6809 | 1.000 | 0.00 | 0.0035 |
| 2000 | 10 | 30051 | 1.000 | 629.1 | 0.5103 | 1.000 | 0.00 | 0.0044 |
| 2000 | 20 | 56087 | 1.000 | 711.2 | 0.3116 | 1.000 | 0.00 | 0.0066 |
| 5000 | 5 | 44825 | 1.000 | 412.1 | 0.8431 | 1.000 | 0.00 | 0.0029 |
| 5000 | 10 | 83707 | 1.000 | 493.8 | 0.7431 | 1.000 | 0.00 | 0.0032 |
| 5000 | 20 | 153136 | 1.000 | 573.1 | 0.5786 | 1.000 | 0.00 | 0.0037 |
