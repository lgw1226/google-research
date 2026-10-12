# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = in, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.3548 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.355 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

20000 edges. Cost p50 0.4, p90 13.2, p99 36.2, max 63.9. Out-degree 0/10.0/34 (min/mean/max), in-degree 10/10.0/10. Same-trajectory edges 0.006, of which forward 0.531; forward cost / true Delta median 0.01; 60 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 4 (0.0002), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 36.2 > Delta_rel 30 (consider enabling tau); 62 nodes have out-degree 0 (incoming-only edges); 60 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

238 strongly connected components, largest 0.630 of N; 2 weakly connected component(s). **Flags:** largest SCC 0.630 < 0.95; 2 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.760, path cost / Delta median 0.29 (p10 0.02, p90 0.60), hops median 15, max edge cost on path median 13.0; 197 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 0.669, cost median 114.1, forward vs backward Pearson 0.7332334123711204, median |log(fwd/bwd)| 0.33. Evaluation tasks: task 1 cost 282, 48 hops; task 2 no path; task 3 no path; task 4 cost 138, 6 hops; task 5 no path. **Flags:** held-out path success 0.760 < 0.95; 197 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 3 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 5000 | 0.344 | 36.6 | 0.3220 | 0.652 | 0.35 | 0.0002 |
| 1000 | 10 | 10000 | 0.828 | 52.6 | 0.1879 | 0.836 | 0.37 | 0.0008 |
| 1000 | 20 | 20000 | 1.000 | 70.5 | 0.0966 | 1.000 | 0.33 | 0.0050 |
| 2000 | 5 | 10000 | 0.156 | 25.1 | 0.5049 | 0.476 | 0.27 | 0.0000 |
| 2000 | 10 | 20000 | 0.630 | 36.2 | 0.3548 | 0.760 | 0.29 | 0.0002 |
| 2000 | 20 | 40000 | 0.894 | 51.7 | 0.2126 | 0.942 | 0.27 | 0.0005 |
| 5000 | 5 | 25000 | 0.202 | 13.7 | 0.7068 | 0.642 | 0.19 | 0.0000 |
| 5000 | 10 | 50000 | 0.567 | 19.4 | 0.5649 | 0.832 | 0.14 | 0.0000 |
| 5000 | 20 | 100000 | 0.883 | 29.0 | 0.4012 | 0.966 | 0.11 | 0.0001 |
