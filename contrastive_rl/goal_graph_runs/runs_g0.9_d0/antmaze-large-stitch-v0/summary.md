# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0190 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

27101 edges. Cost p50 31.3, p90 56.7, p99 110.4, max 246.9. Out-degree 10/13.6/35 (min/mean/max), in-degree 10/13.6/59. Same-trajectory edges 0.008, of which forward 0.647; forward cost / true Delta median 0.83; 45 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 246 (0.0091), 6 of them cheaper than Delta_rel. **Flags:** edge cost p99 110.4 > Delta_rel 30 (consider enabling tau); 4 in-degree hubs with in-degree > 5k (max 59); suspected wormhole attractors; 45 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.57 (p10 0.34, p90 0.90), hops median 6, max edge cost on path median 30.8; 35 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 142.6, forward vs backward Pearson 0.46358357872616246, median |log(fwd/bwd)| 0.25. Evaluation tasks: task 1 cost 248, 19 hops; task 2 cost 186, 9 hops; task 3 cost 182, 17 hops; task 4 cost 214, 12 hops; task 5 cost 166, 7 hops. **Flags:** 35 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6819 | 1.000 | 109.6 | 0.0208 | 1.000 | 0.79 | 0.0089 |
| 1000 | 10 | 13053 | 1.000 | 122.9 | 0.0109 | 1.000 | 0.76 | 0.0185 |
| 1000 | 20 | 25282 | 1.000 | 142.0 | 0.0056 | 1.000 | 0.73 | 0.0375 |
| 2000 | 5 | 14116 | 1.000 | 98.7 | 0.0365 | 1.000 | 0.64 | 0.0052 |
| 2000 | 10 | 27101 | 1.000 | 110.4 | 0.0190 | 1.000 | 0.57 | 0.0091 |
| 2000 | 20 | 52322 | 1.000 | 123.9 | 0.0098 | 1.000 | 0.58 | 0.0174 |
| 5000 | 5 | 36233 | 1.000 | 82.3 | 0.0845 | 1.000 | 0.40 | 0.0017 |
| 5000 | 10 | 69365 | 1.000 | 94.0 | 0.0441 | 1.000 | 0.37 | 0.0028 |
| 5000 | 20 | 133395 | 1.000 | 104.9 | 0.0230 | 1.000 | 0.36 | 0.0055 |
