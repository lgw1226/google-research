# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

Critic undershoot on held-out pairs it would identify (symmetric cost <= cap 10, 11921 pairs): true offset minus critic cost median 10.8, p90 24.6, p99 28.9, max 29.9 steps.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.1719 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.172 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). Full sweep: 1005000 dataset states, 0.966 assigned (nearest cost over all states median 0.4, p90 5.2); 731633 runs of median length 1, 726633 label switches. Entry hop median 0.3, exit hop median 0.3. Identification (hop) cost of kept edges median 0.11, p90 3.22, max 10.0; per-node 90th-percentile radii: exit median 0.9 (p10 0.1, p90 6.6), entry median 0.7 (p10 0.1, p90 5.8); hop XY distance median 0.03, p90 0.27, 0.000 beyond 4 units. Uncapped out-degree median 19 (max 63), cap None; 0 nodes without an outgoing edge, 1 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 0.74, p90 7.70). No thresholds crossed.

## D. Edges

43947 edges. Cost p50 1.7, p90 9.0, p99 17.3, max 53.4. Out-degree 1/22.0/63 (min/mean/max), in-degree 0/22.0/66. Same-trajectory edges 0.006, of which forward 0.492; forward cost / true Delta median 0.08; 104 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** min degree < k without tau (bug); 75 in-degree hubs with in-degree > 5k (max 66); suspected wormhole attractors; 104 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

2 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.52 (p10 0.17, p90 0.89), hops median 11, max edge cost on path median 12.3; 91 wormhole suspects (ratio < 0.3). Against the maze lower bound (speed 0.28 units/step): path cost / LB median 2.46 (p10 1.81), data Delta / LB median 4.54, 0 paths below LB. Query connection: nearest, 61 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 168.3, forward vs backward Pearson 0.991517824461048, median |log(fwd/bwd)| 0.0468259404792198. Evaluation tasks: task 1 cost 387, 41 hops; task 2 cost 448, 57 hops; task 3 cost 308, 47 hops; task 4 cost 329, 42 hops; task 5 cost 382, 41 hops. **Flags:** 91 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 13985 | 0.999 | 29.9 | 0.1288 | 1.000 | 0.57 | 0.0000 |
| 2000 | 10 | 43947 | 1.000 | 17.3 | 0.1719 | 1.000 | 0.52 | 0.0000 |
| 5000 | 10 | 160711 | 0.999 | 11.3 | 0.1786 | 1.000 | 0.43 | 0.0000 |
