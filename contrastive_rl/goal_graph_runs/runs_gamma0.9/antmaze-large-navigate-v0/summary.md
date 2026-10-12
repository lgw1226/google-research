# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0093, top-1 accuracy 0.728 (chance 0.0039); train loss 0.0058, accuracy 0.797. Mean positive logit 0.57 vs negative -23.04. Clipped positives 0.009. Row normalization over 500 held-out states: CV 0.98, std of log mean exp 1.58. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.638; linear fit slope 1.492, intercept -11.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.365 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 43.4 (backward rho 0.525). **Flags:** forward Spearman rho 0.638 < 0.8.

## C. Cost matrix

Negative fraction 0.0006 of off-diagonal entries and 0.0905 of selected edges (min raw cost -61.5). diag(M) median 0.57 (p1 -2.28, p99 5.14), 22 outliers with |z| > 3. Pearson(C, C^T) = 0.463. **Flags:** negative fraction (selected edges) 0.091 > 3%; 22 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

27392 edges. Cost p50 20.3, p90 76.4, p99 109.4, max 143.1. Out-degree 10/13.7/31 (min/mean/max), in-degree 10/13.7/74. Same-trajectory edges 0.020, of which forward 0.574; forward cost / true Delta median 0.06; 255 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 277 (0.0101), 8 of them cheaper than Delta_rel. **Flags:** edge cost p99 109.4 > Delta_rel 30 (consider enabling tau); 9 in-degree hubs with in-degree > 5k (max 74); suspected wormhole attractors; 255 same-trajectory forward edges with cost < 0.5*Delta; 277 edges (0.010) are maze shortcuts (BFS cells >> XY distance, i.e. cross walls); their cost median 87.4.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.14 (p10 0.01, p90 0.39), hops median 10, max edge cost on path median 12.5; 416 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 39.4, forward vs backward Pearson 0.6854828408366457, median |log(fwd/bwd)| 0.50. Evaluation tasks: task 1 cost 104, 30 hops; task 2 cost 81, 35 hops; task 3 cost 36, 23 hops; task 4 cost 122, 51 hops; task 5 cost 114, 30 hops. **Flags:** 416 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 7024 | 1.000 | 108.7 | 0.0884 | 1.000 | 0.31 | 0.0054 |
| 1000 | 10 | 13436 | 1.000 | 119.8 | 0.0462 | 1.000 | 0.31 | 0.0125 |
| 1000 | 20 | 26057 | 1.000 | 133.5 | 0.0238 | 1.000 | 0.31 | 0.0344 |
| 2000 | 5 | 14256 | 0.997 | 98.3 | 0.1733 | 1.000 | 0.15 | 0.0059 |
| 2000 | 10 | 27392 | 1.000 | 109.4 | 0.0905 | 1.000 | 0.14 | 0.0101 |
| 2000 | 20 | 53258 | 1.000 | 121.2 | 0.0466 | 1.000 | 0.14 | 0.0158 |
| 5000 | 5 | 36796 | 0.985 | 76.9 | 0.3755 | 1.000 | 0.02 | 0.0033 |
| 5000 | 10 | 70114 | 1.000 | 87.9 | 0.2101 | 1.000 | 0.02 | 0.0057 |
| 5000 | 20 | 135832 | 1.000 | 100.0 | 0.1089 | 1.000 | 0.02 | 0.0079 |
