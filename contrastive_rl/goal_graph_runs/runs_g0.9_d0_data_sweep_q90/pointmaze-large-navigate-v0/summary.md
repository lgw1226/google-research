# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.701; linear fit slope 1.565, intercept -4.42 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.422 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.620). **Flags:** forward Spearman rho 0.701 < 0.8.

Critic undershoot on held-out pairs it would identify (symmetric cost <= cap 10, 3996 pairs): true offset minus critic cost median 0.2, p90 18.2, p99 27.4, max 30.0 steps.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1418 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.142 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). Full sweep: 1001000 dataset states, 0.978 assigned (nearest cost over all states median 1.5, p90 5.3); 585158 runs of median length 1, 584158 label switches. Entry hop median 2.2, exit hop median 2.1. Identification (hop) cost of kept edges median 1.07, p90 4.81, max 10.0; per-node 90th-percentile radii: exit median 2.5 (p10 0.7, p90 6.4), entry median 2.3 (p10 0.7, p90 5.7); hop XY distance median 0.14, p90 0.45, 0.000 beyond 4 units. Uncapped out-degree median 10 (max 28), cap None; 0 nodes without an outgoing edge, 2 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 4.65, p90 10.05). No thresholds crossed.

## D. Edges

21037 edges. Cost p50 5.7, p90 11.4, p99 18.1, max 40.3. Out-degree 1/10.5/28 (min/mean/max), in-degree 0/10.5/28. Same-trajectory edges 0.010, of which forward 0.502; forward cost / true Delta median 0.02; 82 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** min degree < k without tau (bug); 82 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

3 strongly connected components, largest 0.999 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.83 (p10 0.23, p90 1.28), hops median 23, max edge cost on path median 11.8; 71 wormhole suspects (ratio < 0.3). Against the maze lower bound (speed 0.28 units/step): path cost / LB median 2.31 (p10 1.81), data Delta / LB median 2.65, 0 paths below LB. Query connection: nearest, 27 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 171.2, forward vs backward Pearson 0.9971169067393648, median |log(fwd/bwd)| 0.02388533610432686. Evaluation tasks: task 1 cost 364, 64 hops; task 2 cost 410, 81 hops; task 3 cost 276, 45 hops; task 4 cost 304, 43 hops; task 5 cost 355, 69 hops. **Flags:** 71 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 9116 | 1.000 | 32.5 | 0.0994 | 1.000 | 0.97 | 0.0000 |
| 2000 | 10 | 21037 | 0.999 | 18.1 | 0.1418 | 1.000 | 0.83 | 0.0000 |
| 5000 | 10 | 74638 | 1.000 | 11.8 | 0.1923 | 1.000 | 0.65 | 0.0000 |
