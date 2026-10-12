# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.322; linear fit slope 0.246, intercept 0.04 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.119 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.251). **Flags:** forward Spearman rho 0.322 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.3022 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.302 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

27770 edges. Cost p50 0.5, p90 13.0, p99 34.9, max 63.9. Out-degree 10/13.9/36 (min/mean/max), in-degree 10/13.9/41. Same-trajectory edges 0.006, of which forward 0.538; forward cost / true Delta median 0.01; 79 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 4 (0.0001), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 34.9 > Delta_rel 30 (consider enabling tau); 79 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

11 strongly connected components, largest 0.915 of N; 2 weakly connected component(s). **Flags:** largest SCC 0.915 < 0.95; 2 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.976, path cost / Delta median 0.25 (p10 0.03, p90 0.58), hops median 15, max edge cost on path median 11.8; 282 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 0.910, cost median 115.2, forward vs backward Pearson 0.7080562773490429, median |log(fwd/bwd)| 0.33. Evaluation tasks: task 1 cost 276, 49 hops; task 2 cost 303, 89 hops; task 3 cost 168, 63 hops; task 4 cost 282, 60 hops; task 5 cost 227, 31 hops. **Flags:** 282 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6976 | 0.595 | 35.0 | 0.2691 | 0.892 | 0.33 | 0.0001 |
| 1000 | 10 | 13073 | 1.000 | 54.7 | 0.1480 | 1.000 | 0.33 | 0.0015 |
| 1000 | 20 | 25428 | 1.000 | 72.8 | 0.0761 | 1.000 | 0.32 | 0.0065 |
| 2000 | 5 | 14880 | 0.492 | 22.6 | 0.4670 | 0.774 | 0.25 | 0.0000 |
| 2000 | 10 | 27770 | 0.915 | 34.9 | 0.3022 | 0.976 | 0.25 | 0.0001 |
| 2000 | 20 | 52021 | 0.981 | 52.0 | 0.1693 | 0.996 | 0.25 | 0.0004 |
| 5000 | 5 | 40258 | 0.402 | 10.6 | 0.6872 | 0.784 | 0.13 | 0.0000 |
| 5000 | 10 | 74502 | 0.812 | 16.8 | 0.5279 | 0.924 | 0.11 | 0.0000 |
| 5000 | 20 | 139013 | 0.965 | 26.5 | 0.3486 | 0.992 | 0.11 | 0.0001 |
