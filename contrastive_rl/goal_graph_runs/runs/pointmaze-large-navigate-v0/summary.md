# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.99, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 270000 steps (B = 256). Held-out loss 0.0218, top-1 accuracy 0.073 (chance 0.0039); train loss 0.0215, accuracy 0.083. Mean positive logit -4.47 vs negative -6.57. Clipped positives 0.098. Row normalization over 500 held-out states: CV 0.14, std of log mean exp 0.13. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 300]: Spearman rho 0.582; linear fit slope 1.891, intercept -10.33 (fit to binned medians, Delta <= 100; R2 0.997 on medians, 0.035 on raw pairs). Delta_rel = 5; the binned median is within 20% of the fit for Delta in [21.0, 200.0]. Backward minus forward cost median 40.1 (backward rho 0.391). **Flags:** binned median leaves the linear fit at the SHORT end: linear only for Delta in [21, 200] (cost ~ 0 or negative below); Delta_rel=0 below floor 5; using floor (calibration breaks at short horizons); forward Spearman rho 0.582 < 0.8.

## C. Cost matrix

Negative fraction 0.0132 of off-diagonal entries and 0.8327 of selected edges (min raw cost -163.4). diag(M) median -3.24 (p1 -4.37, p99 0.49), 56 outliers with |z| > 3. Pearson(C, C^T) = 0.552. **Flags:** negative fraction (selected edges) 0.833 > 3%; 56 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

33475 edges. Cost p50 0.0, p90 7.2, p99 178.5, max 804.3. Out-degree 10/16.7/65 (min/mean/max), in-degree 10/16.7/126. Same-trajectory edges 0.007, of which forward 0.599; forward cost / true Delta median 0.00; 133 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 96 (0.0029), 95 of them cheaper than Delta_rel. **Flags:** edge cost p99 178.5 > Delta_rel 5 (consider enabling tau); 21 in-degree hubs with in-degree > 5k (max 126); suspected wormhole attractors; 133 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

25 strongly connected components, largest 0.968 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [10, 50]): success 1.000, path cost / Delta median 0.00 (p10 0.00, p90 0.16), hops median 3, max edge cost on path median 0.0; 463 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 0.998, cost median 0.0, forward vs backward Pearson -0.04872280507202209, median |log(fwd/bwd)| 0.90. Evaluation tasks: task 1 cost 0, 12 hops; task 2 no path; task 3 cost 398, 20 hops; task 4 cost 416, 23 hops; task 5 cost 200, 27 hops. **Flags:** 463 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 1 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 8466 | 0.965 | 209.1 | 0.8365 | 0.996 | 0.00 | 0.0006 |
| 1000 | 10 | 15348 | 1.000 | 333.8 | 0.7060 | 1.000 | 0.00 | 0.0010 |
| 1000 | 20 | 27910 | 1.000 | 402.2 | 0.4902 | 1.000 | 0.00 | 0.0021 |
| 2000 | 5 | 17962 | 0.886 | 51.3 | 0.9109 | 0.990 | 0.00 | 0.0036 |
| 2000 | 10 | 33475 | 0.968 | 178.5 | 0.8327 | 1.000 | 0.00 | 0.0029 |
| 2000 | 20 | 60800 | 0.987 | 354.7 | 0.6871 | 1.000 | 0.00 | 0.0028 |
| 5000 | 5 | 47716 | 0.830 | 10.7 | 0.9686 | 0.936 | 0.00 | 0.0026 |
| 5000 | 10 | 91430 | 0.898 | 30.6 | 0.9379 | 0.986 | 0.00 | 0.0027 |
| 5000 | 20 | 171270 | 0.968 | 103.2 | 0.8766 | 1.000 | 0.00 | 0.0027 |
