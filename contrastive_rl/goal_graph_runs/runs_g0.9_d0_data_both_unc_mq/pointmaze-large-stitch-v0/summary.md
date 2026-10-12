# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.301; linear fit slope 0.265, intercept 0.01 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.099 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.244). **Flags:** forward Spearman rho 0.301 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.0968 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.097 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 8.00 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.70, 10: 0.55, 30: 0.46; random cross-trajectory pairs 0.0110. 114716 landing states, 0.04 without any match, mean 22.0 matches each. Uncapped out-degree median 45 (max 131), cap None, walk = both; 0 nodes without an outgoing edge, 10 without an incoming edge; 0.31 of edges have offset 0. Identification cost of kept edges median 1.77; stitch cost = critic (added median 0.51, p90 3.94). Passing cross-trajectory pairs: XY distance median 0.17, 0.000 beyond 4 units; pairs within 2 units pass at 0.39. **Flags:** cross-trajectory random pairs pass the identification test at rate 0.0110 > 1%; pairs 30 steps apart still pass at rate 0.46.

## D. Edges

90137 edges. Cost p50 3.6, p90 26.8, p99 34.3, max 38.0. Out-degree 3/45.1/131 (min/mean/max), in-degree 0/45.1/142. Same-trajectory edges 0.004, of which forward 0.637; forward cost / true Delta median 0.12; 181 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 34.3 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 836 in-degree hubs with in-degree > 5k (max 142); suspected wormhole attractors; 181 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

12 strongly connected components, largest 0.993 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.22 (p10 0.01, p90 0.38), hops median 15, max edge cost on path median 9.0; 380 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.996, cost median 82.7, forward vs backward Pearson 0.9288546043530401, median |log(fwd/bwd)| 0.15. Evaluation tasks: task 1 cost 184, 59 hops; task 2 cost 215, 84 hops; task 3 cost 161, 64 hops; task 4 cost 161, 48 hops; task 5 cost 161, 43 hops. **Flags:** 380 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 23345 | 0.969 | 34.4 | 0.0807 | 0.994 | 0.27 | 0.0000 |
| 1000 | 10 | 23345 | 0.969 | 34.4 | 0.0807 | 0.994 | 0.27 | 0.0000 |
| 1000 | 20 | 23345 | 0.969 | 34.4 | 0.0807 | 0.994 | 0.27 | 0.0000 |
| 2000 | 5 | 90137 | 0.993 | 34.3 | 0.0968 | 0.998 | 0.21 | 0.0000 |
| 2000 | 10 | 90137 | 0.993 | 34.3 | 0.0968 | 1.000 | 0.22 | 0.0000 |
| 2000 | 20 | 90137 | 0.993 | 34.3 | 0.0968 | 1.000 | 0.21 | 0.0000 |
| 5000 | 5 | 570840 | 0.998 | 34.3 | 0.0888 | 1.000 | 0.11 | 0.0000 |
| 5000 | 10 | 570840 | 0.998 | 34.3 | 0.0888 | 1.000 | 0.11 | 0.0000 |
| 5000 | 20 | 570840 | 0.998 | 34.3 | 0.0888 | 1.000 | 0.11 | 0.0000 |
