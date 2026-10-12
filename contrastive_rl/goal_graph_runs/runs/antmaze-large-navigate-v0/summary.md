# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.99, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 240000 steps (B = 256). Held-out loss 0.0189, top-1 accuracy 0.205 (chance 0.0039); train loss 0.0153, accuracy 0.295. Mean positive logit -2.92 vs negative -9.21. Clipped positives 0.095. Row normalization over 500 held-out states: CV 1.21, std of log mean exp 1.23. **Flags:** row-normalization CV 1.21 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 300]: Spearman rho 0.608; linear fit slope 1.773, intercept -35.81 (fit to binned medians, Delta <= 100; R2 0.988 on medians, 0.284 on raw pairs). Delta_rel = 5; the binned median is within 20% of the fit for Delta in [41.0, 300.0]. Backward minus forward cost median 286.4 (backward rho 0.300). **Flags:** binned median leaves the linear fit at the SHORT end: linear only for Delta in [41, 300] (cost ~ 0 or negative below); Delta_rel=0 below floor 5; using floor (calibration breaks at short horizons); forward Spearman rho 0.608 < 0.8.

## C. Cost matrix

Negative fraction 0.0088 of off-diagonal entries and 0.6517 of selected edges (min raw cost -322.1). diag(M) median -2.08 (p1 -4.11, p99 3.87), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.689. **Flags:** negative fraction (selected edges) 0.652 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

32565 edges. Cost p50 0.0, p90 494.3, p99 784.2, max 1098.9. Out-degree 10/16.3/43 (min/mean/max), in-degree 10/16.3/147. Same-trajectory edges 0.018, of which forward 0.600; forward cost / true Delta median 0.00; 274 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 246 (0.0076), 102 of them cheaper than Delta_rel. **Flags:** edge cost p99 784.2 > Delta_rel 5 (consider enabling tau); 50 in-degree hubs with in-degree > 5k (max 147); suspected wormhole attractors; 274 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [10, 50]): success 1.000, path cost / Delta median 0.00 (p10 0.00, p90 1.55), hops median 1, max edge cost on path median 0.0; 395 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 0.0, forward vs backward Pearson 0.8791674484505111, median |log(fwd/bwd)| 0.69. Evaluation tasks: task 1 cost 58, 8 hops; task 2 cost 0, 9 hops; task 3 cost 23, 13 hops; task 4 cost 0, 9 hops; task 5 cost 53, 13 hops. **Flags:** 395 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 8303 | 1.000 | 802.4 | 0.6716 | 1.000 | 0.00 | 0.0076 |
| 1000 | 10 | 15374 | 1.000 | 876.6 | 0.5119 | 1.000 | 0.00 | 0.0122 |
| 1000 | 20 | 29173 | 1.000 | 955.4 | 0.3148 | 1.000 | 0.00 | 0.0231 |
| 2000 | 5 | 17371 | 0.988 | 706.2 | 0.7609 | 1.000 | 0.00 | 0.0052 |
| 2000 | 10 | 32565 | 1.000 | 784.2 | 0.6517 | 1.000 | 0.00 | 0.0076 |
| 2000 | 20 | 61096 | 1.000 | 864.5 | 0.4863 | 1.000 | 0.00 | 0.0113 |
| 5000 | 5 | 45660 | 0.972 | 576.4 | 0.8621 | 1.000 | 0.00 | 0.0046 |
| 5000 | 10 | 88050 | 0.998 | 670.6 | 0.8040 | 1.000 | 0.00 | 0.0063 |
| 5000 | 20 | 166396 | 1.000 | 752.7 | 0.7092 | 1.000 | 0.00 | 0.0073 |
