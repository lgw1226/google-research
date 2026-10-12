# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0. Costs in steps.

## A. Encoder health

Trained 275000 steps (B = 256). Held-out loss 0.0110, top-1 accuracy 0.331 (chance 0.0039); train loss 0.0108, accuracy 0.332. Mean positive logit -1.62 vs negative -14.52. Clipped positives 0.044. Row normalization over 500 held-out states: CV 0.36, std of log mean exp 0.34. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.329; linear fit slope 0.168, intercept -0.14 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.157 on raw pairs). Delta_rel = 20; the binned median is within 20% of the fit for Delta in [1.0, 20.0]. Backward minus forward cost median 0.8 (backward rho 0.250). **Flags:** forward Spearman rho 0.329 < 0.8.

## C. Cost matrix

Negative fraction 0.0035 of off-diagonal entries and 0.4266 of selected edges (min raw cost -14.4). diag(M) median -1.16 (p1 -2.17, p99 1.88), 33 outliers with |z| > 3. Pearson(C, C^T) = 0.675. **Flags:** negative fraction (selected edges) 0.427 > 3%; 33 diagonal outliers (|z|>3) > 1% of nodes.

## D. Edges

28620 edges. Cost p50 0.2, p90 9.7, p99 30.1, max 60.7. Out-degree 10/14.3/42 (min/mean/max), in-degree 10/14.3/53. Same-trajectory edges 0.006, of which forward 0.556; forward cost / true Delta median 0.01; 80 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 30.1 > Delta_rel 20 (consider enabling tau); 1 in-degree hubs with in-degree > 5k (max 53); suspected wormhole attractors; 80 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

26 strongly connected components, largest 0.845 of N; 2 weakly connected component(s). **Flags:** largest SCC 0.845 < 0.95; 2 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [40, 200]): success 0.924, path cost / Delta median 0.19 (p10 0.01, p90 0.52), hops median 13, max edge cost on path median 9.3; 320 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (499): reachability 0.840, cost median 80.6, forward vs backward Pearson 0.43665976085338376, median |log(fwd/bwd)| 0.40. Evaluation tasks: task 1 cost 209, 53 hops; task 2 no path; task 3 cost 197, 62 hops; task 4 no path; task 5 cost 179, 33 hops. **Flags:** held-out path success 0.924 < 0.95; 320 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 2 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 7176 | 0.757 | 30.6 | 0.4037 | 0.882 | 0.29 | 0.0003 |
| 1000 | 10 | 13406 | 1.000 | 49.2 | 0.2515 | 1.000 | 0.24 | 0.0007 |
| 1000 | 20 | 25429 | 1.000 | 63.4 | 0.1359 | 1.000 | 0.24 | 0.0045 |
| 2000 | 5 | 15446 | 0.325 | 18.6 | 0.5858 | 0.622 | 0.15 | 0.0000 |
| 2000 | 10 | 28620 | 0.845 | 30.1 | 0.4266 | 0.924 | 0.19 | 0.0000 |
| 2000 | 20 | 53072 | 1.000 | 45.6 | 0.2616 | 1.000 | 0.17 | 0.0002 |
| 5000 | 5 | 42138 | 0.209 | 8.0 | 0.7732 | 0.612 | 0.08 | 0.0000 |
| 5000 | 10 | 78087 | 0.669 | 13.0 | 0.6476 | 0.838 | 0.09 | 0.0001 |
| 5000 | 20 | 144779 | 0.937 | 21.9 | 0.4831 | 0.982 | 0.07 | 0.0001 |
