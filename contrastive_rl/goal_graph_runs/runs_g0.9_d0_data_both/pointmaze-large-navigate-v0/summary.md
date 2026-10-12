# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.709; linear fit slope 1.562, intercept -4.16 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.435 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.622). **Flags:** forward Spearman rho 0.709 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1914 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.191 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 11.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.50, 10: 0.18, 30: 0.07; random cross-trajectory pairs 0.0052. 122108 landing states, 0.01 without any match, mean 10.8 matches each. Uncapped out-degree median 75 (max 189), cap 10, walk = both; 0 nodes without an outgoing edge, 12 without an incoming edge; 0.38 of edges have offset 0. Identification cost of kept edges median 4.54; stitch cost = critic (added median 0.28, p90 3.05). Passing cross-trajectory pairs: XY distance median 0.61, 0.000 beyond 4 units; pairs within 2 units pass at 0.17. No thresholds crossed.

## D. Edges

19969 edges. Cost p50 2.1, p90 6.9, p99 14.5, max 40.3. Out-degree 6/10.0/10 (min/mean/max), in-degree 0/10.0/26. Same-trajectory edges 0.011, of which forward 0.562; forward cost / true Delta median 0.00; 114 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 114 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

19 strongly connected components, largest 0.986 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.18 (p10 0.04, p90 0.32), hops median 39, max edge cost on path median 5.0; 428 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 38.1, forward vs backward Pearson 0.8319941825106136, median |log(fwd/bwd)| 0.19. Evaluation tasks: task 1 cost 98, 111 hops; task 2 cost 93, 140 hops; task 3 cost 187, 96 hops; task 4 cost 101, 74 hops; task 5 cost 90, 127 hops. **Flags:** 428 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4975 | 0.924 | 17.6 | 0.2008 | 0.974 | 0.32 | 0.0000 |
| 1000 | 10 | 9841 | 0.974 | 24.0 | 0.1080 | 1.000 | 0.30 | 0.0000 |
| 1000 | 20 | 18962 | 0.991 | 34.0 | 0.0566 | 1.000 | 0.30 | 0.0000 |
| 2000 | 5 | 10000 | 0.691 | 8.5 | 0.3241 | 0.834 | 0.19 | 0.0000 |
| 2000 | 10 | 19969 | 0.986 | 14.5 | 0.1914 | 1.000 | 0.18 | 0.0000 |
| 2000 | 20 | 39382 | 0.999 | 24.8 | 0.1026 | 1.000 | 0.19 | 0.0000 |
| 5000 | 5 | 25000 | 0.738 | 3.8 | 0.5749 | 0.824 | 0.05 | 0.0000 |
| 5000 | 10 | 50000 | 0.958 | 6.2 | 0.3903 | 0.980 | 0.05 | 0.0000 |
| 5000 | 20 | 99996 | 0.999 | 11.7 | 0.2333 | 1.000 | 0.05 | 0.0000 |
