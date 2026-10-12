# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.628; linear fit slope 1.940, intercept -8.74 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.362 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.4 (backward rho 0.535). **Flags:** forward Spearman rho 0.628 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0232 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges)

theta = 35.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.51, 10: 0.25, 30: 0.15; random cross-trajectory pairs 0.0010. 61004 landing states, 0.16 without any match, mean 2.5 matches each. Uncapped out-degree median 12 (max 48), cap None, walk = forward; 105 nodes without an outgoing edge, 112 without an incoming edge; 0.12 of edges have offset 0. Identification cost of kept edges median 30.77; stitch cost = critic (added median 20.28, p90 33.00). Passing cross-trajectory pairs: XY distance median 0.59, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. **Flags:** 105 nodes have no outgoing data edge.

## D. Edges

24396 edges. Cost p50 31.7, p90 51.2, p99 61.8, max 65.9. Out-degree 0/12.2/48 (min/mean/max), in-degree 0/12.2/50. Same-trajectory edges 0.023, of which forward 0.612; forward cost / true Delta median 0.14; 225 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 61.8 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 225 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

190 strongly connected components, largest 0.861 of N; 145 weakly connected component(s). **Flags:** largest SCC 0.861 < 0.95; 145 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.64 (p10 0.20, p90 0.96), hops median 7, max edge cost on path median 30.7; 77 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.998, cost median 176.3, forward vs backward Pearson 0.5544803734085786, median |log(fwd/bwd)| 0.27. Evaluation tasks: task 1 cost 361, 22 hops; task 2 cost 436, 30 hops; task 3 cost 226, 20 hops; task 4 cost 278, 15 hops; task 5 cost 172, 9 hops. **Flags:** 77 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6258 | 0.827 | 61.8 | 0.0232 | 0.998 | 0.86 | 0.0000 |
| 1000 | 10 | 6258 | 0.827 | 61.8 | 0.0232 | 1.000 | 0.83 | 0.0000 |
| 1000 | 20 | 6258 | 0.827 | 61.8 | 0.0232 | 1.000 | 0.78 | 0.0000 |
| 2000 | 5 | 24396 | 0.861 | 61.8 | 0.0232 | 0.994 | 0.66 | 0.0000 |
| 2000 | 10 | 24396 | 0.861 | 61.8 | 0.0232 | 1.000 | 0.64 | 0.0000 |
| 2000 | 20 | 24396 | 0.861 | 61.8 | 0.0232 | 1.000 | 0.64 | 0.0000 |
| 5000 | 5 | 149306 | 0.868 | 62.0 | 0.0252 | 0.980 | 0.43 | 0.0000 |
| 5000 | 10 | 149306 | 0.868 | 62.0 | 0.0252 | 0.988 | 0.43 | 0.0000 |
| 5000 | 20 | 149306 | 0.868 | 62.0 | 0.0252 | 1.000 | 0.43 | 0.0000 |
