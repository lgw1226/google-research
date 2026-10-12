# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = in, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.701; linear fit slope 1.565, intercept -4.42 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.422 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.620). **Flags:** forward Spearman rho 0.701 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.2030 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.203 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

20000 edges. Cost p50 2.9, p90 11.6, p99 29.7, max 122.6. Out-degree 1/10.0/26 (min/mean/max), in-degree 10/10.0/10. Same-trajectory edges 0.011, of which forward 0.514; forward cost / true Delta median 0.00; 101 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 1 (0.0001), 0 of them cheaper than Delta_rel. **Flags:** 101 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

1 strongly connected components, largest 1.000 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.23 (p10 0.04, p90 0.42), hops median 38, max edge cost on path median 6.5; 351 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 47.8, forward vs backward Pearson 0.6402312996258275, median |log(fwd/bwd)| 0.28. Evaluation tasks: task 1 cost 109, 1 hops; task 2 cost 140, 117 hops; task 3 cost 88, 95 hops; task 4 cost 119, 76 hops; task 5 cost 127, 118 hops. **Flags:** 351 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 5000 | 0.930 | 36.6 | 0.2112 | 0.992 | 0.41 | 0.0000 |
| 1000 | 10 | 10000 | 0.993 | 49.4 | 0.1092 | 1.000 | 0.37 | 0.0002 |
| 1000 | 20 | 20000 | 1.000 | 61.1 | 0.0546 | 1.000 | 0.36 | 0.0009 |
| 2000 | 5 | 10000 | 0.834 | 20.4 | 0.3538 | 0.918 | 0.27 | 0.0000 |
| 2000 | 10 | 20000 | 1.000 | 29.7 | 0.2030 | 1.000 | 0.23 | 0.0001 |
| 2000 | 20 | 40000 | 1.000 | 44.9 | 0.1037 | 1.000 | 0.22 | 0.0002 |
| 5000 | 5 | 25000 | 0.717 | 9.3 | 0.6069 | 0.794 | 0.08 | 0.0000 |
| 5000 | 10 | 50000 | 0.947 | 14.3 | 0.4277 | 0.978 | 0.06 | 0.0000 |
| 5000 | 20 | 100000 | 1.000 | 23.3 | 0.2496 | 1.000 | 0.06 | 0.0000 |
