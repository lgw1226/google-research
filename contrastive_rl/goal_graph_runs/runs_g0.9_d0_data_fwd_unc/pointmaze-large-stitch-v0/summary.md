# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.301; linear fit slope 0.265, intercept 0.01 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.099 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.244). **Flags:** forward Spearman rho 0.301 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.1201 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.120 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 8.00 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.70, 10: 0.55, 30: 0.46; random cross-trajectory pairs 0.0110. 57188 landing states, 0.03 without any match, mean 23.2 matches each. Uncapped out-degree median 36 (max 117), cap None, walk = forward; 0 nodes without an outgoing edge, 12 without an incoming edge; 0.45 of edges have offset 0. Identification cost of kept edges median 1.60; stitch cost = critic (added median 0.60, p90 3.63). Passing cross-trajectory pairs: XY distance median 0.17, 0.000 beyond 4 units; pairs within 2 units pass at 0.39. **Flags:** cross-trajectory random pairs pass the identification test at rate 0.0110 > 1%; pairs 30 steps apart still pass at rate 0.46.

## D. Edges

71533 edges. Cost p50 2.0, p90 24.1, p99 33.2, max 38.0. Out-degree 1/35.8/117 (min/mean/max), in-degree 0/35.8/84. Same-trajectory edges 0.005, of which forward 0.636; forward cost / true Delta median 0.14; 180 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 33.2 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 614 in-degree hubs with in-degree > 5k (max 84); suspected wormhole attractors; 180 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

24 strongly connected components, largest 0.904 of N; 2 weakly connected component(s). **Flags:** largest SCC 0.904 < 0.95; 2 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.990, path cost / Delta median 0.25 (p10 0.02, p90 0.46), hops median 14, max edge cost on path median 11.7; 303 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.914, cost median 104.7, forward vs backward Pearson 0.8843248700739512, median |log(fwd/bwd)| 0.18. Evaluation tasks: task 1 cost 204, 47 hops; task 2 cost 249, 81 hops; task 3 cost 172, 51 hops; task 4 cost 191, 45 hops; task 5 cost 165, 30 hops. **Flags:** 303 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 18261 | 0.815 | 33.7 | 0.1010 | 0.970 | 0.31 | 0.0000 |
| 1000 | 10 | 18261 | 0.815 | 33.7 | 0.1010 | 0.984 | 0.31 | 0.0000 |
| 1000 | 20 | 18261 | 0.815 | 33.7 | 0.1010 | 0.998 | 0.31 | 0.0000 |
| 2000 | 5 | 71533 | 0.904 | 33.2 | 0.1201 | 0.974 | 0.25 | 0.0000 |
| 2000 | 10 | 71533 | 0.904 | 33.2 | 0.1201 | 0.990 | 0.25 | 0.0000 |
| 2000 | 20 | 71533 | 0.904 | 33.2 | 0.1201 | 0.994 | 0.25 | 0.0000 |
| 5000 | 5 | 453295 | 0.991 | 33.1 | 0.1102 | 0.996 | 0.13 | 0.0000 |
| 5000 | 10 | 453295 | 0.991 | 33.1 | 0.1102 | 0.996 | 0.13 | 0.0000 |
| 5000 | 20 | 453295 | 0.991 | 33.1 | 0.1102 | 1.000 | 0.13 | 0.0000 |
