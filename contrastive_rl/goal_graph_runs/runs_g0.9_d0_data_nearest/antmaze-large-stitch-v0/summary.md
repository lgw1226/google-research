# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0181 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges, nearest node)

Each landing state identifies with its nearest node under the symmetric cost (no theta). 114716 landing states over walk = both, horizon 30. Fraction whose nearest node is still their own node, by offset: 1: 0.91, 5: 0.28, 10: 0.12, 30: 0.05. Identification (hop) cost of kept edges median 27.55, p90 43.15, max 160.8; hop XY distance median 0.66, p90 1.42, 0.004 beyond 4 units. Uncapped out-degree median 12 (max 33), cap None; 44 nodes without an outgoing edge, 46 without an incoming edge; 0.00 of edges have offset 0; stitch cost = critic (added median 20.04, p90 37.60). No thresholds crossed.

## D. Edges

24739 edges. Cost p50 35.2, p90 57.3, p99 87.6, max 188.8. Out-degree 0/12.4/33 (min/mean/max), in-degree 0/12.4/38. Same-trajectory edges 0.009, of which forward 0.754; forward cost / true Delta median 0.75; 32 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 40 (0.0016), 0 of them cheaper than Delta_rel. Identification hops crossing walls: 43 (0.0017), hop cost median 89.4. **Flags:** edge cost p99 87.6 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 32 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

114 strongly connected components, largest 0.940 of N; 25 weakly connected component(s). **Flags:** largest SCC 0.940 < 0.95; 25 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.996, path cost / Delta median 0.99 (p10 0.62, p90 1.53), hops median 6, max edge cost on path median 43.5; 6 wormhole suspects (ratio < 0.3). Query connection: nearest. Random cross-trajectory node pairs (499): reachability 0.940, cost median 185.9, forward vs backward Pearson 0.6855352051931572, median |log(fwd/bwd)| 0.22. Evaluation tasks: task 1 cost 387, 20 hops; task 2 cost 408, 11 hops; task 3 cost 380, 20 hops; task 4 cost 321, 13 hops; task 5 cost 428, 22 hops. **Flags:** 6 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 10 | 9268 | 0.951 | 102.3 | 0.0141 | 1.000 | 1.08 | 0.0024 |
| 2000 | 10 | 24739 | 0.940 | 87.6 | 0.0181 | 0.996 | 0.99 | 0.0016 |
| 5000 | 10 | 86492 | 0.957 | 69.8 | 0.0268 | 0.998 | 0.91 | 0.0007 |
