# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0279 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). Full sweep: 1005000 dataset states, 0.022 assigned (nearest cost over all states median 28.6, p90 46.3); 11668 runs of median length 1, 7229 label switches. Entry hop median 5.0, exit hop median 5.7. Identification (hop) cost of kept edges median 8.98, p90 9.85, max 10.0; hop XY distance median 0.33, p90 0.79, 0.000 beyond 4 units. Uncapped out-degree median 2 (max 26), cap None; 276 nodes without an outgoing edge, 348 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 9.35, p90 16.44). **Flags:** 276 nodes have no outgoing data edge.

## D. Edges

5995 edges. Cost p50 44.0, p90 108.8, p99 168.3, max 212.1. Out-degree 0/3.0/26 (min/mean/max), in-degree 0/3.0/26. Same-trajectory edges 0.040, of which forward 0.950; forward cost / true Delta median 1.00; 10 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 18 (0.0030), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 168.3 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 10 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

845 strongly connected components, largest 0.534 of N; 76 weakly connected component(s). **Flags:** largest SCC 0.534 < 0.95; 76 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.968, path cost / Delta median 1.15 (p10 0.67, p90 2.01), hops median 1, max edge cost on path median 108.1; 6 wormhole suspects (ratio < 0.3). Query connection: nearest, 788 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 0.784, cost median 304.2, forward vs backward Pearson 0.3671552081807875, median |log(fwd/bwd)| 0.4229060519290504. Evaluation tasks: task 1 cost 579, 17 hops; task 2 cost 593, 18 hops; task 3 cost 474, 12 hops; task 4 cost 558, 11 hops; task 5 no path. **Flags:** 6 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 1 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 2127 | 0.087 | 176.8 | 0.0197 | 0.812 | 1.09 | 0.0052 |
| 2000 | 10 | 5995 | 0.534 | 168.3 | 0.0279 | 0.968 | 1.15 | 0.0030 |
| 5000 | 10 | 19274 | 0.732 | 131.1 | 0.0451 | 1.000 | 1.08 | 0.0019 |
