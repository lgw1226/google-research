# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.1724 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.172 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 30 steps). Full sweep: 1005000 dataset states, 0.997 assigned (nearest cost over all states median 0.4, p90 5.2); 739992 runs of median length 1, 734992 label switches. Entry hop median 0.0, exit hop median 0.0. Identification (hop) cost of kept edges median 0.18, p90 3.30, max 29.7; hop XY distance median 0.03, p90 0.25, 0.000 beyond 4 units. Uncapped out-degree median 19 (max 63), cap None; 0 nodes without an outgoing edge, 0 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 0.02, p90 1.53). No thresholds crossed.

## D. Edges

43784 edges. Cost p50 1.0, p90 2.8, p99 14.7, max 66.9. Out-degree 1/21.9/63 (min/mean/max), in-degree 1/21.9/65. Same-trajectory edges 0.006, of which forward 0.492; forward cost / true Delta median 0.04; 117 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** min degree < k without tau (bug); 74 in-degree hubs with in-degree > 5k (max 65); suspected wormhole attractors; 117 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.14 (p10 0.04, p90 0.27), hops median 15, max edge cost on path median 3.4; 465 wormhole suspects (ratio < 0.3). Query connection: nearest, 7 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 45.1, forward vs backward Pearson 0.875213956167234, median |log(fwd/bwd)| 0.2079391223234123. Evaluation tasks: task 1 cost 123, 68 hops; task 2 cost 155, 88 hops; task 3 cost 78, 60 hops; task 4 cost 145, 62 hops; task 5 cost 146, 78 hops. **Flags:** 465 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 13633 | 1.000 | 27.2 | 0.1315 | 1.000 | 0.16 | 0.0000 |
| 2000 | 10 | 43784 | 1.000 | 14.7 | 0.1724 | 1.000 | 0.14 | 0.0000 |
| 5000 | 10 | 160734 | 0.999 | 6.9 | 0.1786 | 1.000 | 0.14 | 0.0000 |
