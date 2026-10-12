# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.701; linear fit slope 1.565, intercept -4.42 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.422 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.620). **Flags:** forward Spearman rho 0.701 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1678 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.168 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

24717 edges. Cost p50 3.7, p90 12.5, p99 29.3, max 122.6. Out-degree 10/12.4/27 (min/mean/max), in-degree 10/12.4/28. Same-trajectory edges 0.009, of which forward 0.513; forward cost / true Delta median 0.00; 102 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 3 (0.0001), 1 of them cheaper than Delta_rel. **Flags:** 102 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.22 (p10 0.04, p90 0.40), hops median 38, max edge cost on path median 6.6; 362 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 46.9, forward vs backward Pearson 0.6565444428281273, median |log(fwd/bwd)| 0.29. Evaluation tasks: task 1 cost 114, 110 hops; task 2 cost 110, 115 hops; task 3 cost 102, 96 hops; task 4 cost 92, 72 hops; task 5 cost 124, 127 hops. **Flags:** 362 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 6382 | 1.000 | 35.2 | 0.1708 | 1.000 | 0.38 | 0.0000 |
| 1000 | 10 | 12410 | 1.000 | 48.4 | 0.0880 | 1.000 | 0.37 | 0.0002 |
| 1000 | 20 | 24423 | 1.000 | 60.3 | 0.0447 | 1.000 | 0.36 | 0.0008 |
| 2000 | 5 | 13068 | 0.969 | 18.7 | 0.3071 | 0.988 | 0.22 | 0.0000 |
| 2000 | 10 | 24717 | 1.000 | 29.3 | 0.1678 | 1.000 | 0.22 | 0.0001 |
| 2000 | 20 | 48652 | 1.000 | 43.8 | 0.0853 | 1.000 | 0.22 | 0.0002 |
| 5000 | 5 | 35543 | 0.935 | 8.2 | 0.5761 | 0.954 | 0.06 | 0.0000 |
| 5000 | 10 | 64706 | 0.990 | 13.4 | 0.3795 | 0.992 | 0.06 | 0.0000 |
| 5000 | 20 | 121917 | 1.000 | 23.7 | 0.2100 | 1.000 | 0.06 | 0.0000 |
