# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.709; linear fit slope 1.562, intercept -4.16 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.435 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.622). **Flags:** forward Spearman rho 0.709 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1872 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.187 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 11.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.50, 10: 0.18, 30: 0.07; random cross-trajectory pairs 0.0052. 61004 landing states, 0.01 without any match, mean 10.8 matches each. Uncapped out-degree median 50 (max 133), cap 10; 0 nodes without an outgoing edge; 0.49 of edges have offset 0. Identification cost of kept edges median 4.80; stitch cost = critic (added median 0.71, p90 4.58). Passing cross-trajectory pairs: XY distance median 0.61, 0.000 beyond 4 units; pairs within 2 units pass at 0.17. No thresholds crossed.

## D. Edges

19764 edges. Cost p50 2.8, p90 8.2, p99 17.4, max 41.9. Out-degree 2/9.9/10 (min/mean/max), in-degree 0/9.9/25. Same-trajectory edges 0.011, of which forward 0.555; forward cost / true Delta median 0.01; 107 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 107 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

20 strongly connected components, largest 0.981 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.22 (p10 0.04, p90 0.39), hops median 38, max edge cost on path median 6.0; 354 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 46.6, forward vs backward Pearson 0.808983652032681, median |log(fwd/bwd)| 0.22. Evaluation tasks: task 1 cost 131, 115 hops; task 2 cost 125, 138 hops; task 3 cost 120, 71 hops; task 4 cost 123, 63 hops; task 5 cost 119, 69 hops. **Flags:** 354 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4931 | 0.684 | 20.0 | 0.1967 | 0.804 | 0.37 | 0.0000 |
| 1000 | 10 | 9644 | 0.962 | 29.0 | 0.1062 | 1.000 | 0.37 | 0.0000 |
| 1000 | 20 | 17507 | 0.980 | 36.1 | 0.0588 | 1.000 | 0.36 | 0.0000 |
| 2000 | 5 | 9981 | 0.765 | 10.3 | 0.3206 | 0.902 | 0.24 | 0.0000 |
| 2000 | 10 | 19764 | 0.981 | 17.4 | 0.1872 | 1.000 | 0.22 | 0.0000 |
| 2000 | 20 | 38329 | 0.993 | 28.0 | 0.1016 | 1.000 | 0.22 | 0.0000 |
| 5000 | 5 | 25000 | 0.765 | 5.0 | 0.5729 | 0.850 | 0.06 | 0.0000 |
| 5000 | 10 | 49973 | 0.956 | 8.0 | 0.3858 | 0.980 | 0.05 | 0.0000 |
| 5000 | 20 | 99445 | 0.999 | 14.0 | 0.2277 | 1.000 | 0.05 | 0.0000 |
