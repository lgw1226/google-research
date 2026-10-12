# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.701; linear fit slope 1.565, intercept -4.42 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.422 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.620). **Flags:** forward Spearman rho 0.701 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.0495 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.050 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta). 122108 landing states over walk = both, horizon 30. Fraction whose nearest node is still their own node, by offset: 1: 0.40, 5: 0.04, 10: 0.01, 30: 0.01. Identification (hop) cost of kept edges median 1.28, p90 4.29, max 33.3; hop XY distance median 0.16, p90 0.43, 0.000 beyond 4 units. Uncapped out-degree median 26 (max 64), cap None; 0 nodes without an outgoing edge, 3 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 0.40, p90 2.51). No thresholds crossed.

## D. Edges

52030 edges. Cost p50 16.0, p90 28.4, p99 32.6, max 55.5. Out-degree 3/26.0/64 (min/mean/max), in-degree 0/26.0/65. Same-trajectory edges 0.006, of which forward 0.692; forward cost / true Delta median 0.62; 101 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 32.6 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 32 in-degree hubs with in-degree > 5k (max 65); suspected wormhole attractors; 101 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

5 strongly connected components, largest 0.998 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.49 (p10 0.13, p90 0.71), hops median 23, max edge cost on path median 9.2; 143 wormhole suspects (ratio < 0.3). Query connection: nearest. Random cross-trajectory node pairs (499): reachability 0.996, cost median 90.7, forward vs backward Pearson 0.9824172027612141, median |log(fwd/bwd)| 0.07. Evaluation tasks: task 1 cost 214, 68 hops; task 2 no path; task 3 cost 213, 49 hops; task 4 cost 230, 41 hops; task 5 cost 243, 66 hops. **Flags:** 143 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 1 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 19099 | 1.000 | 36.0 | 0.0436 | 1.000 | 0.52 | 0.0000 |
| 2000 | 10 | 52030 | 0.998 | 32.6 | 0.0495 | 1.000 | 0.49 | 0.0000 |
| 5000 | 10 | 189906 | 1.000 | 31.1 | 0.0607 | 1.000 | 0.48 | 0.0000 |
