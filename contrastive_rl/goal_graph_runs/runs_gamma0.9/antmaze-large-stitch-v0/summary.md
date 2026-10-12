# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 490000 steps (B = 256). Held-out loss 0.0066, top-1 accuracy 0.759 (chance 0.0039); train loss 0.0058, accuracy 0.795. Mean positive logit 0.23 vs negative -26.51. Clipped positives 0.043. Row normalization over 500 held-out states: CV 0.93, std of log mean exp 0.83. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.689; linear fit slope 2.176, intercept -15.17 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.425 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 37.4 (backward rho 0.482). **Flags:** forward Spearman rho 0.689 < 0.8.

## C. Cost matrix

Negative fraction 0.0004 of off-diagonal entries and 0.0600 of selected edges (min raw cost -115.8). diag(M) median 0.66 (p1 -2.12, p99 5.76), 32 outliers with |z| > 3. Pearson(C, C^T) = 0.595. **Flags:** negative fraction (selected edges) 0.060 > 3%; 32 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

27158 edges. Cost p50 23.2, p90 48.7, p99 106.0, max 233.4. Out-degree 10/13.6/33 (min/mean/max), in-degree 10/13.6/52. Same-trajectory edges 0.007, of which forward 0.663; forward cost / true Delta median 0.56; 62 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 280 (0.0103), 25 of them cheaper than Delta_rel. **Flags:** edge cost p99 106.0 > Delta_rel 30 (consider enabling tau); 1 in-degree hubs with in-degree > 5k (max 52); suspected wormhole attractors; 62 same-trajectory forward edges with cost < 0.5*Delta; 280 edges (0.010) are maze shortcuts (BFS cells >> XY distance, i.e. cross walls); their cost median 66.3.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.30 (p10 0.13, p90 0.60), hops median 7, max edge cost on path median 19.5; 247 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 64.6, forward vs backward Pearson 0.31514762790882395, median |log(fwd/bwd)| 0.36. Evaluation tasks: task 1 cost 159, 29 hops; task 2 cost 82, 22 hops; task 3 cost 109, 24 hops; task 4 cost 173, 25 hops; task 5 cost 130, 16 hops. **Flags:** 247 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6857 | 1.000 | 109.4 | 0.0629 | 1.000 | 0.54 | 0.0079 |
| 1000 | 10 | 13164 | 1.000 | 125.1 | 0.0327 | 1.000 | 0.52 | 0.0163 |
| 1000 | 20 | 25253 | 1.000 | 142.9 | 0.0171 | 1.000 | 0.51 | 0.0364 |
| 2000 | 5 | 14112 | 1.000 | 93.3 | 0.1154 | 1.000 | 0.32 | 0.0067 |
| 2000 | 10 | 27158 | 1.000 | 106.0 | 0.0600 | 1.000 | 0.30 | 0.0103 |
| 2000 | 20 | 52279 | 1.000 | 120.0 | 0.0312 | 1.000 | 0.30 | 0.0171 |
| 5000 | 5 | 36736 | 1.000 | 78.4 | 0.2767 | 1.000 | 0.08 | 0.0021 |
| 5000 | 10 | 69948 | 1.000 | 90.8 | 0.1486 | 1.000 | 0.08 | 0.0030 |
| 5000 | 20 | 134504 | 1.000 | 102.5 | 0.0773 | 1.000 | 0.08 | 0.0051 |
