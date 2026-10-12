# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = in, offset_min = 0. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.685; linear fit slope 2.325, intercept -9.02 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.414 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 34.8 (backward rho 0.507). **Flags:** forward Spearman rho 0.685 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0257 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

20000 edges. Cost p50 29.3, p90 56.5, p99 112.6, max 246.9. Out-degree 0/10.0/34 (min/mean/max), in-degree 10/10.0/10. Same-trajectory edges 0.009, of which forward 0.674; forward cost / true Delta median 0.77; 44 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 156 (0.0078), 5 of them cheaper than Delta_rel. **Flags:** edge cost p99 112.6 > Delta_rel 30 (consider enabling tau); 13 nodes have out-degree 0 (incoming-only edges); 44 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

38 strongly connected components, largest 0.967 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.59 (p10 0.34, p90 0.91), hops median 6, max edge cost on path median 30.9; 35 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 1.000, cost median 148.7, forward vs backward Pearson 0.43688693237391346, median |log(fwd/bwd)| 0.25. Evaluation tasks: task 1 cost 299, 24 hops; task 2 cost 181, 7 hops; task 3 cost 193, 17 hops; task 4 cost 243, 16 hops; task 5 cost 160, 7 hops. **Flags:** 35 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 5000 | 0.967 | 115.2 | 0.0284 | 1.000 | 0.85 | 0.0070 |
| 1000 | 10 | 10000 | 0.984 | 132.9 | 0.0142 | 1.000 | 0.77 | 0.0132 |
| 1000 | 20 | 20000 | 0.993 | 147.1 | 0.0071 | 1.000 | 0.74 | 0.0282 |
| 2000 | 5 | 10000 | 0.949 | 101.1 | 0.0498 | 1.000 | 0.67 | 0.0051 |
| 2000 | 10 | 20000 | 0.967 | 112.6 | 0.0257 | 1.000 | 0.59 | 0.0078 |
| 2000 | 20 | 40000 | 0.992 | 127.1 | 0.0129 | 1.000 | 0.58 | 0.0135 |
| 5000 | 5 | 25000 | 0.955 | 83.5 | 0.1131 | 1.000 | 0.42 | 0.0016 |
| 5000 | 10 | 50000 | 0.981 | 95.9 | 0.0601 | 1.000 | 0.38 | 0.0024 |
| 5000 | 20 | 100000 | 0.991 | 107.8 | 0.0305 | 1.000 | 0.36 | 0.0041 |
