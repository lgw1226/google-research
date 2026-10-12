# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.709; linear fit slope 1.562, intercept -4.16 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.435 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.622). **Flags:** forward Spearman rho 0.709 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.0262 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 11.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.50, 10: 0.18, 30: 0.07; random cross-trajectory pairs 0.0052. 122108 landing states, 0.01 without any match, mean 10.8 matches each. Uncapped out-degree median 75 (max 189), cap None, walk = both; 0 nodes without an outgoing edge, 2 without an incoming edge; 0.07 of edges have offset 0. Identification cost of kept edges median 6.93; stitch cost = critic (added median 2.04, p90 8.98). Passing cross-trajectory pairs: XY distance median 0.61, 0.000 beyond 4 units; pairs within 2 units pass at 0.17. No thresholds crossed.

## D. Edges

155557 edges. Cost p50 17.0, p90 32.0, p99 39.7, max 42.0. Out-degree 6/77.8/189 (min/mean/max), in-degree 0/77.8/193. Same-trajectory edges 0.003, of which forward 0.619; forward cost / true Delta median 0.13; 189 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 39.7 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 1415 in-degree hubs with in-degree > 5k (max 193); suspected wormhole attractors; 189 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

4 strongly connected components, largest 0.999 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.18 (p10 0.04, p90 0.31), hops median 39, max edge cost on path median 5.0; 431 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 37.5, forward vs backward Pearson 0.8796531854803578, median |log(fwd/bwd)| 0.18. Evaluation tasks: task 1 cost 94, 107 hops; task 2 cost 121, 143 hops; task 3 cost 98, 94 hops; task 4 cost 93, 75 hops; task 5 cost 97, 130 hops. **Flags:** 431 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 41044 | 0.999 | 39.4 | 0.0261 | 1.000 | 0.31 | 0.0000 |
| 1000 | 10 | 41044 | 0.999 | 39.4 | 0.0261 | 1.000 | 0.31 | 0.0000 |
| 1000 | 20 | 41044 | 0.999 | 39.4 | 0.0261 | 1.000 | 0.31 | 0.0000 |
| 2000 | 5 | 155557 | 0.999 | 39.7 | 0.0262 | 1.000 | 0.19 | 0.0000 |
| 2000 | 10 | 155557 | 0.999 | 39.7 | 0.0262 | 1.000 | 0.18 | 0.0000 |
| 2000 | 20 | 155557 | 0.999 | 39.7 | 0.0262 | 1.000 | 0.19 | 0.0000 |
| 5000 | 5 | 1018258 | 1.000 | 39.7 | 0.0249 | 1.000 | 0.05 | 0.0000 |
| 5000 | 10 | 1018258 | 1.000 | 39.7 | 0.0249 | 1.000 | 0.05 | 0.0000 |
| 5000 | 20 | 1018258 | 1.000 | 39.7 | 0.0249 | 1.000 | 0.05 | 0.0000 |
