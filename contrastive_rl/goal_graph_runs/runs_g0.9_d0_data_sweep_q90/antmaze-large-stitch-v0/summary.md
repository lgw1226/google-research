# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

Critic undershoot on held-out pairs it would identify (symmetric cost <= cap 30, 3385 pairs): true offset minus critic cost median -12.4, p90 1.4, p99 20.8, max 30.0 steps.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0120 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 30 steps). Full sweep: 1005000 dataset states, 0.553 assigned (nearest cost over all states median 28.6, p90 46.3); 246825 runs of median length 1, 241828 label switches. Entry hop median 27.4, exit hop median 27.2. Identification (hop) cost of kept edges median 25.93, p90 29.39, max 30.0; per-node 90th-percentile radii: exit median 27.4 (p10 25.5, p90 28.4), entry median 27.2 (p10 25.1, p90 28.5); hop XY distance median 0.61, p90 1.27, 0.000 beyond 4 units. Uncapped out-degree median 17 (max 52), cap None; 41 nodes without an outgoing edge, 29 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 54.53, p90 56.20). No thresholds crossed.

## D. Edges

35372 edges. Cost p50 56.4, p90 65.6, p99 88.0, max 192.0. Out-degree 0/17.7/52 (min/mean/max), in-degree 0/17.7/53. Same-trajectory edges 0.006, of which forward 0.583; forward cost / true Delta median 3.56; 1 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 88.0 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 2 in-degree hubs with in-degree > 5k (max 53); suspected wormhole attractors; 1 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

87 strongly connected components, largest 0.952 of N; 6 weakly connected component(s). **Flags:** 6 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 2.18 (p10 1.62, p90 3.35), hops median 6, max edge cost on path median 73.0; 0 wormhole suspects (ratio < 0.3). Against the maze lower bound (speed 0.27 units/step): path cost / LB median 8.36 (p10 6.48), data Delta / LB median 3.88, 0 paths below LB. Query connection: nearest, 402 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.982, cost median 543.4, forward vs backward Pearson 0.9535353956409289, median |log(fwd/bwd)| 0.08662462454857402. Evaluation tasks: task 1 cost 896, 14 hops; task 2 cost 618, 10 hops; task 3 cost 1122, 18 hops; task 4 cost 925, 17 hops; task 5 cost 991, 15 hops. **Flags:** median path cost / Delta 2.18 >> 1.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 15263 | 0.963 | 116.9 | 0.0087 | 1.000 | 1.92 | 0.0002 |
| 2000 | 10 | 35372 | 0.952 | 88.0 | 0.0120 | 1.000 | 2.18 | 0.0000 |
| 5000 | 10 | 105396 | 0.961 | 66.3 | 0.0183 | 1.000 | 2.37 | 0.0000 |
