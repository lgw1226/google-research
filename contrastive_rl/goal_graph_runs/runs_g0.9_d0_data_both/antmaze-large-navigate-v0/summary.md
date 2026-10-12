# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.628; linear fit slope 1.940, intercept -8.74 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.362 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.4 (backward rho 0.535). **Flags:** forward Spearman rho 0.628 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0335 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. **Flags:** negative fraction (selected edges) 0.033 > 3%.

## C2. Node identification (data-cost edges)

theta = 35.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.51, 10: 0.25, 30: 0.15; random cross-trajectory pairs 0.0010. 122108 landing states, 0.16 without any match, mean 2.5 matches each. Uncapped out-degree median 17 (max 65), cap 10, walk = both; 86 nodes without an outgoing edge, 96 without an incoming edge; 0.08 of edges have offset 0. Identification cost of kept edges median 29.49; stitch cost = critic (added median 10.49, p90 26.14). Passing cross-trajectory pairs: XY distance median 0.59, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. No thresholds crossed.

## D. Edges

17118 edges. Cost p50 21.1, p90 35.9, p99 53.9, max 65.2. Out-degree 0/8.6/10 (min/mean/max), in-degree 0/8.6/31. Same-trajectory edges 0.029, of which forward 0.612; forward cost / true Delta median 0.09; 221 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 53.9 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 221 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

179 strongly connected components, largest 0.864 of N; 124 weakly connected component(s). **Flags:** largest SCC 0.864 < 0.95; 124 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.54 (p10 0.16, p90 0.81), hops median 8, max edge cost on path median 26.0; 93 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.998, cost median 147.0, forward vs backward Pearson 0.5398404569099113, median |log(fwd/bwd)| 0.28. Evaluation tasks: task 1 cost 294, 31 hops; task 2 cost 300, 27 hops; task 3 cost 191, 19 hops; task 4 cost 228, 23 hops; task 5 cost 210, 20 hops. **Flags:** 93 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4205 | 0.855 | 55.9 | 0.0347 | 0.998 | 0.73 | 0.0000 |
| 1000 | 10 | 7125 | 0.870 | 60.3 | 0.0220 | 1.000 | 0.70 | 0.0000 |
| 1000 | 20 | 9125 | 0.871 | 62.0 | 0.0178 | 1.000 | 0.68 | 0.0000 |
| 2000 | 5 | 8976 | 0.836 | 42.6 | 0.0589 | 0.992 | 0.58 | 0.0000 |
| 2000 | 10 | 17118 | 0.864 | 53.9 | 0.0335 | 1.000 | 0.54 | 0.0000 |
| 2000 | 20 | 28742 | 0.868 | 60.3 | 0.0211 | 1.000 | 0.54 | 0.0000 |
| 5000 | 5 | 23624 | 0.824 | 34.0 | 0.1195 | 0.990 | 0.35 | 0.0000 |
| 5000 | 10 | 45537 | 0.864 | 39.4 | 0.0732 | 0.992 | 0.34 | 0.0000 |
| 5000 | 20 | 87742 | 0.868 | 49.6 | 0.0423 | 1.000 | 0.34 | 0.0000 |
