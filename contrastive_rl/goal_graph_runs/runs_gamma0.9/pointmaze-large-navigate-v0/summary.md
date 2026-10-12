# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 320000 steps (B = 256). Held-out loss 0.0126, top-1 accuracy 0.336 (chance 0.0039); train loss 0.0124, accuracy 0.352. Mean positive logit -2.12 vs negative -13.39. Clipped positives 0.009. Row normalization over 500 held-out states: CV 0.33, std of log mean exp 0.32. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.710; linear fit slope 1.293, intercept -4.82 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.452 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.7 (backward rho 0.627). **Flags:** forward Spearman rho 0.710 < 0.8.

## C. Cost matrix

Negative fraction 0.0019 of off-diagonal entries and 0.2949 of selected edges (min raw cost -19.4). diag(M) median -1.19 (p1 -2.36, p99 1.05), 19 outliers with |z| > 3. Pearson(C, C^T) = 0.771. **Flags:** negative fraction (selected edges) 0.295 > 3%.

## D. Edges

25088 edges. Cost p50 1.8, p90 9.4, p99 25.9, max 118.7. Out-degree 10/12.5/24 (min/mean/max), in-degree 10/12.5/34. Same-trajectory edges 0.009, of which forward 0.538; forward cost / true Delta median 0.00; 110 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** 110 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.06 (p10 0.01, p90 0.14), hops median 32, max edge cost on path median 4.0; 497 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 14.5, forward vs backward Pearson 0.5387385722639499, median |log(fwd/bwd)| 0.46. Evaluation tasks: task 1 cost 30, 81 hops; task 2 cost 79, 95 hops; task 3 cost 127, 75 hops; task 4 cost 74, 85 hops; task 5 cost 73, 99 hops. **Flags:** 497 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6483 | 0.994 | 29.5 | 0.2989 | 0.998 | 0.14 | 0.0000 |
| 1000 | 10 | 12447 | 1.000 | 42.6 | 0.1620 | 1.000 | 0.13 | 0.0002 |
| 1000 | 20 | 24494 | 1.000 | 55.8 | 0.0827 | 1.000 | 0.13 | 0.0005 |
| 2000 | 5 | 13567 | 0.964 | 14.9 | 0.4813 | 0.986 | 0.07 | 0.0000 |
| 2000 | 10 | 25088 | 1.000 | 25.9 | 0.2949 | 1.000 | 0.06 | 0.0000 |
| 2000 | 20 | 48890 | 1.000 | 41.5 | 0.1550 | 1.000 | 0.06 | 0.0000 |
| 5000 | 5 | 38675 | 0.945 | 5.9 | 0.7486 | 0.968 | 0.02 | 0.0000 |
| 5000 | 10 | 68640 | 0.990 | 10.3 | 0.5824 | 0.996 | 0.02 | 0.0000 |
| 5000 | 20 | 125353 | 1.000 | 20.4 | 0.3678 | 1.000 | 0.02 | 0.0000 |
