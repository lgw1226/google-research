# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.628; linear fit slope 1.940, intercept -8.74 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.362 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.4 (backward rho 0.535). **Flags:** forward Spearman rho 0.628 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0173 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges)

theta = 35.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.51, 10: 0.25, 30: 0.15; random cross-trajectory pairs 0.0010. 122108 landing states, 0.16 without any match, mean 2.5 matches each. Uncapped out-degree median 17 (max 65), cap None, walk = both; 86 nodes without an outgoing edge, 88 without an incoming edge; 0.05 of edges have offset 0. Identification cost of kept edges median 30.77; stitch cost = critic (added median 18.17, p90 32.52). Passing cross-trajectory pairs: XY distance median 0.59, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. No thresholds crossed.

## D. Edges

35835 edges. Cost p50 31.3, p90 51.5, p99 62.2, max 65.9. Out-degree 0/17.9/65 (min/mean/max), in-degree 0/17.9/59. Same-trajectory edges 0.017, of which forward 0.610; forward cost / true Delta median 0.13; 256 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 62.2 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 14 in-degree hubs with in-degree > 5k (max 59); suspected wormhole attractors; 256 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

172 strongly connected components, largest 0.868 of N; 121 weakly connected component(s). **Flags:** largest SCC 0.868 < 0.95; 121 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 0.998, path cost / Delta median 0.64 (p10 0.20, p90 1.05), hops median 9, max edge cost on path median 29.6; 71 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.758, cost median 140.2, forward vs backward Pearson 0.5105374273139676, median |log(fwd/bwd)| 0.30. Evaluation tasks: task 1 cost 279, 27 hops; task 2 cost 324, 37 hops; task 3 cost 218, 20 hops; task 4 cost 196, 8 hops; task 5 cost 167, 14 hops. **Flags:** 71 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 9372 | 0.871 | 62.3 | 0.0174 | 0.994 | 0.80 | 0.0000 |
| 1000 | 10 | 9372 | 0.871 | 62.3 | 0.0174 | 0.996 | 0.79 | 0.0000 |
| 1000 | 20 | 9372 | 0.871 | 62.3 | 0.0174 | 0.996 | 0.78 | 0.0000 |
| 2000 | 5 | 35835 | 0.868 | 62.2 | 0.0173 | 0.996 | 0.66 | 0.0000 |
| 2000 | 10 | 35835 | 0.868 | 62.2 | 0.0173 | 0.998 | 0.64 | 0.0000 |
| 2000 | 20 | 35835 | 0.868 | 62.2 | 0.0173 | 0.998 | 0.65 | 0.0000 |
| 5000 | 5 | 220111 | 0.869 | 62.2 | 0.0187 | 0.994 | 0.45 | 0.0000 |
| 5000 | 10 | 220111 | 0.869 | 62.2 | 0.0187 | 0.994 | 0.45 | 0.0000 |
| 5000 | 20 | 220111 | 0.869 | 62.2 | 0.0187 | 0.996 | 0.45 | 0.0000 |
