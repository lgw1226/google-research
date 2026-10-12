# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.301; linear fit slope 0.265, intercept 0.01 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.099 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.244). **Flags:** forward Spearman rho 0.301 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.2236 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.224 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 8.00 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.70, 10: 0.55, 30: 0.46; random cross-trajectory pairs 0.0110. 57188 landing states, 0.03 without any match, mean 23.2 matches each. Uncapped out-degree median 36 (max 117), cap 10; 0 nodes without an outgoing edge; 0.73 of edges have offset 0. Identification cost of kept edges median 1.28; stitch cost = none. Passing cross-trajectory pairs: XY distance median 0.17, 0.000 beyond 4 units; pairs within 2 units pass at 0.39. **Flags:** cross-trajectory random pairs pass the identification test at rate 0.0110 > 1%; pairs 30 steps apart still pass at rate 0.46.

## D. Edges

19778 edges. Cost p50 0.0, p90 8.0, p99 22.0, max 30.0. Out-degree 1/9.9/10 (min/mean/max), in-degree 0/9.9/24. Same-trajectory edges 0.006, of which forward 0.600; forward cost / true Delta median 0.00; 58 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 58 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

83 strongly connected components, largest 0.406 of N; 3 weakly connected component(s). **Flags:** largest SCC 0.406 < 0.95; 3 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.920, path cost / Delta median 0.14 (p10 0.00, p90 0.36), hops median 17, max edge cost on path median 8.0; 391 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.470, cost median 54.0, forward vs backward Pearson 0.7823151751048523, median |log(fwd/bwd)| 0.25. Evaluation tasks: task 1 no path; task 2 no path; task 3 cost 140, 62 hops; task 4 no path; task 5 cost 138, 46 hops. **Flags:** held-out path success 0.920 < 0.95; 391 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 3 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4929 | 0.088 | 23.0 | 0.2075 | 0.582 | 0.18 | 0.0000 |
| 1000 | 10 | 9237 | 0.350 | 28.0 | 0.1640 | 0.866 | 0.21 | 0.0000 |
| 1000 | 20 | 15033 | 0.405 | 29.0 | 0.1218 | 0.958 | 0.22 | 0.0000 |
| 2000 | 5 | 9978 | 0.113 | 14.0 | 0.2667 | 0.560 | 0.10 | 0.0000 |
| 2000 | 10 | 19778 | 0.406 | 22.0 | 0.2236 | 0.920 | 0.14 | 0.0000 |
| 2000 | 20 | 37416 | 0.568 | 28.0 | 0.1795 | 0.974 | 0.12 | 0.0000 |
| 5000 | 5 | 24999 | 0.118 | 6.0 | 0.3061 | 0.556 | 0.03 | 0.0000 |
| 5000 | 10 | 49981 | 0.468 | 11.0 | 0.2821 | 0.902 | 0.02 | 0.0000 |
| 5000 | 20 | 99577 | 0.663 | 18.0 | 0.2420 | 0.964 | 0.02 | 0.0000 |
