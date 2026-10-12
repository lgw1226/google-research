# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.622; linear fit slope 1.967, intercept -8.59 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.347 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.5 (backward rho 0.534). **Flags:** forward Spearman rho 0.622 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0289 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. No thresholds crossed.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta, capped at ident_max = 10 steps). Full sweep: 1001000 dataset states, 0.075 assigned (nearest cost over all states median 27.3, p90 47.1); 16964 runs of median length 1, 15965 label switches. Entry hop median 5.1, exit hop median 5.8. Identification (hop) cost of kept edges median 9.02, p90 9.86, max 10.0; hop XY distance median 0.34, p90 0.81, 0.000 beyond 4 units. Uncapped out-degree median 3 (max 30), cap None; 108 nodes without an outgoing edge, 49 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 9.60, p90 16.52). **Flags:** 108 nodes have no outgoing data edge.

## D. Edges

9215 edges. Cost p50 58.8, p90 178.6, p99 353.5, max 689.3. Out-degree 0/4.6/30 (min/mean/max), in-degree 0/4.6/28. Same-trajectory edges 0.060, of which forward 0.766; forward cost / true Delta median 0.92; 146 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 559 (0.0607), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 0 (0.0000). **Flags:** edge cost p99 353.5 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 146 same-trajectory forward edges with cost < 0.5*Delta; 559 edges (0.061) are maze shortcuts (BFS cells >> XY distance, i.e. cross walls); their cost median 198.0.

## E. Connectivity

242 strongly connected components, largest 0.838 of N; 16 weakly connected component(s). **Flags:** largest SCC 0.838 < 0.95; 16 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.93 (p10 0.12, p90 1.50), hops median 1, max edge cost on path median 128.8; 77 wormhole suspects (ratio < 0.3). Query connection: nearest, 589 queries with a start/goal hop beyond ident_max. Random cross-trajectory node pairs (499): reachability 1.000, cost median 212.9, forward vs backward Pearson 0.5083117491027869, median |log(fwd/bwd)| 0.2634414378675302. Evaluation tasks: task 1 cost 395, 1 hops; task 2 cost 328, 1 hops; task 3 cost 106, 1 hops; task 4 cost 292, 1 hops; task 5 cost 440, 1 hops. **Flags:** 77 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 4115 | 0.809 | 578.5 | 0.0146 | 1.000 | 0.97 | 0.1380 |
| 2000 | 10 | 9215 | 0.838 | 353.5 | 0.0289 | 1.000 | 0.93 | 0.0607 |
| 5000 | 10 | 24196 | 0.845 | 163.8 | 0.0564 | 1.000 | 0.91 | 0.0083 |
