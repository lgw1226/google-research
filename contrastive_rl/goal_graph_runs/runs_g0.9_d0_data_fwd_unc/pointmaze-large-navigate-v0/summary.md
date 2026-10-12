# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.709; linear fit slope 1.562, intercept -4.16 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.435 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.622). **Flags:** forward Spearman rho 0.709 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.0380 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.038 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 11.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.50, 10: 0.18, 30: 0.07; random cross-trajectory pairs 0.0052. 61004 landing states, 0.01 without any match, mean 10.8 matches each. Uncapped out-degree median 50 (max 133), cap None, walk = forward; 0 nodes without an outgoing edge, 2 without an incoming edge; 0.15 of edges have offset 0. Identification cost of kept edges median 6.97; stitch cost = critic (added median 2.51, p90 9.43). Passing cross-trajectory pairs: XY distance median 0.61, 0.000 beyond 4 units; pairs within 2 units pass at 0.17. No thresholds crossed.

## D. Edges

103493 edges. Cost p50 15.5, p90 31.5, p99 39.6, max 42.0. Out-degree 2/51.7/133 (min/mean/max), in-degree 0/51.7/148. Same-trajectory edges 0.004, of which forward 0.653; forward cost / true Delta median 0.29; 145 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 39.6 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 892 in-degree hubs with in-degree > 5k (max 148); suspected wormhole attractors; 145 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

5 strongly connected components, largest 0.994 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.22 (p10 0.04, p90 0.38), hops median 36, max edge cost on path median 6.0; 367 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 44.6, forward vs backward Pearson 0.8487902766164644, median |log(fwd/bwd)| 0.21. Evaluation tasks: task 1 cost 115, 112 hops; task 2 cost 100, 130 hops; task 3 cost 110, 72 hops; task 4 cost 122, 63 hops; task 5 cost 132, 112 hops. **Flags:** 367 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 27208 | 0.980 | 39.4 | 0.0380 | 0.998 | 0.36 | 0.0000 |
| 1000 | 10 | 27208 | 0.980 | 39.4 | 0.0380 | 1.000 | 0.36 | 0.0000 |
| 1000 | 20 | 27208 | 0.980 | 39.4 | 0.0380 | 1.000 | 0.36 | 0.0000 |
| 2000 | 5 | 103493 | 0.994 | 39.6 | 0.0380 | 1.000 | 0.22 | 0.0000 |
| 2000 | 10 | 103493 | 0.994 | 39.6 | 0.0380 | 1.000 | 0.22 | 0.0000 |
| 2000 | 20 | 103493 | 0.994 | 39.6 | 0.0380 | 1.000 | 0.22 | 0.0000 |
| 5000 | 5 | 675555 | 1.000 | 39.6 | 0.0360 | 1.000 | 0.05 | 0.0000 |
| 5000 | 10 | 675555 | 1.000 | 39.6 | 0.0360 | 1.000 | 0.05 | 0.0000 |
| 5000 | 20 | 675555 | 1.000 | 39.6 | 0.0360 | 1.000 | 0.05 | 0.0000 |
