# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.701; linear fit slope 1.565, intercept -4.42 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.422 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.620). **Flags:** forward Spearman rho 0.701 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1423 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.142 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 30 steps). Full sweep: 1001000 dataset states, 1.000 assigned (nearest cost over all states median 1.5, p90 5.3); 589950 runs of median length 1, 588950 label switches. Entry hop median 0.0, exit hop median 0.0. Identification (hop) cost of kept edges median 1.32, p90 4.80, max 29.5; hop XY distance median 0.13, p90 0.43, 0.000 beyond 4 units. Uncapped out-degree median 10 (max 28), cap None; 0 nodes without an outgoing edge, 1 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 0.29, p90 3.52). No thresholds crossed.

## D. Edges

20878 edges. Cost p50 1.3, p90 4.9, p99 15.9, max 51.1. Out-degree 1/10.4/28 (min/mean/max), in-degree 0/10.4/28. Same-trajectory edges 0.010, of which forward 0.502; forward cost / true Delta median 0.01; 99 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** min degree < k without tau (bug); 99 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

2 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.21 (p10 0.06, p90 0.33), hops median 28, max edge cost on path median 2.3; 390 wormhole suspects (ratio < 0.3). Query connection: nearest, 1 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 39.1, forward vs backward Pearson 0.9675376869134334, median |log(fwd/bwd)| 0.08037702015024988. Evaluation tasks: task 1 cost 85, 76 hops; task 2 cost 124, 103 hops; task 3 cost 87, 73 hops; task 4 cost 89, 62 hops; task 5 cost 137, 79 hops. **Flags:** 390 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 8653 | 1.000 | 29.0 | 0.1031 | 1.000 | 0.23 | 0.0000 |
| 2000 | 10 | 20878 | 1.000 | 15.9 | 0.1423 | 1.000 | 0.21 | 0.0000 |
| 5000 | 10 | 74605 | 1.000 | 7.5 | 0.1923 | 1.000 | 0.25 | 0.0000 |
