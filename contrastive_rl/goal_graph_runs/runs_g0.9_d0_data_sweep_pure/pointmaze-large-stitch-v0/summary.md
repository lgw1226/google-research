# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.1719 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.172 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). Full sweep: 1005000 dataset states, 0.966 assigned (nearest cost over all states median 0.4, p90 5.2); 731633 runs of median length 1, 726633 label switches. Entry hop median 0.0, exit hop median 0.0. Identification (hop) cost of kept edges median 0.11, p90 3.22, max 10.0; hop XY distance median 0.03, p90 0.27, 0.000 beyond 4 units. Uncapped out-degree median 19 (max 63), cap None; 0 nodes without an outgoing edge, 1 without an incoming edge; 0.00 of edges have offset 0; stitch cost = none. No thresholds crossed.

## D. Edges

43947 edges. Cost p50 1.0, p90 1.0, p99 6.0, max 38.0. Out-degree 1/22.0/63 (min/mean/max), in-degree 0/22.0/66. Same-trajectory edges 0.006, of which forward 0.492; forward cost / true Delta median 0.04; 119 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** min degree < k without tau (bug); 75 in-degree hubs with in-degree > 5k (max 66); suspected wormhole attractors; 119 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

2 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.08 (p10 0.03, p90 0.15), hops median 12, max edge cost on path median 1.7; 493 wormhole suspects (ratio < 0.3). Query connection: nearest, 61 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 21.0, forward vs backward Pearson 0.9884248086802596, median |log(fwd/bwd)| 0.04256042035857183. Evaluation tasks: task 1 cost 83, 43 hops; task 2 cost 94, 50 hops; task 3 cost 90, 40 hops; task 4 cost 85, 41 hops; task 5 cost 116, 46 hops. **Flags:** 493 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 13985 | 0.999 | 17.2 | 0.1288 | 1.000 | 0.08 | 0.0000 |
| 2000 | 10 | 43947 | 1.000 | 6.0 | 0.1719 | 1.000 | 0.08 | 0.0000 |
| 5000 | 10 | 160711 | 0.999 | 2.0 | 0.1786 | 1.000 | 0.09 | 0.0000 |
