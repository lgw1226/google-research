# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = in, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0319 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. **Flags:** negative fraction (selected edges) 0.032 > 3%.

## D. Edges

20000 edges. Cost p50 27.6, p90 71.8, p99 110.0, max 150.4. Out-degree 0/10.0/29 (min/mean/max), in-degree 10/10.0/10. Same-trajectory edges 0.025, of which forward 0.577; forward cost / true Delta median 0.07; 227 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 177 (0.0089), 2 of them cheaper than Delta_rel. **Flags:** edge cost p99 110.0 > Delta_rel 30 (consider enabling tau); 5 nodes have out-degree 0 (incoming-only edges); 227 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

12 strongly connected components, largest 0.992 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.48 (p10 0.11, p90 0.80), hops median 7, max edge cost on path median 27.3; 107 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 136.4, forward vs backward Pearson 0.33880072722862703, median |log(fwd/bwd)| 0.32. Evaluation tasks: task 1 cost 270, 23 hops; task 2 cost 220, 9 hops; task 3 cost 122, 21 hops; task 4 cost 169, 16 hops; task 5 cost 186, 13 hops. **Flags:** 107 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 5000 | 0.862 | 106.3 | 0.0338 | 1.000 | 0.70 | 0.0048 |
| 1000 | 10 | 10000 | 0.986 | 116.2 | 0.0169 | 1.000 | 0.66 | 0.0092 |
| 1000 | 20 | 20000 | 0.999 | 129.3 | 0.0084 | 1.000 | 0.64 | 0.0251 |
| 2000 | 5 | 10000 | 0.860 | 98.5 | 0.0631 | 1.000 | 0.52 | 0.0060 |
| 2000 | 10 | 20000 | 0.992 | 110.0 | 0.0319 | 1.000 | 0.48 | 0.0089 |
| 2000 | 20 | 40000 | 0.997 | 120.2 | 0.0160 | 1.000 | 0.48 | 0.0136 |
| 5000 | 5 | 25000 | 0.851 | 81.3 | 0.1505 | 0.998 | 0.30 | 0.0031 |
| 5000 | 10 | 50000 | 0.985 | 91.1 | 0.0828 | 1.000 | 0.26 | 0.0048 |
| 5000 | 20 | 100000 | 0.997 | 100.4 | 0.0426 | 1.000 | 0.25 | 0.0075 |
