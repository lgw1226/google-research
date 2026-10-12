# pointmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 375000 steps (B = 256). Held-out loss 0.0122, top-1 accuracy 0.385 (chance 0.0039); train loss 0.0119, accuracy 0.405. Mean positive logit -1.94 vs negative -13.25. Clipped positives 0.008. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.30. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.709; linear fit slope 1.562, intercept -4.16 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.435 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 7.4 (backward rho 0.622). **Flags:** forward Spearman rho 0.709 < 0.8.

## C. Cost matrix

Negative fraction 0.0010 of off-diagonal entries and 0.1586 of selected edges (min raw cost -15.7). diag(M) median -0.87 (p1 -1.94, p99 1.43), 21 outliers with |z| > 3. Pearson(C, C^T) = 0.801. **Flags:** negative fraction (selected edges) 0.159 > 3%; 21 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 11.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.50, 10: 0.18, 30: 0.07; random cross-trajectory pairs 0.0052. 61004 landing states, 0.01 without any match, mean 10.8 matches each. Uncapped out-degree median 50 (max 133), cap 10; 0 nodes without an outgoing edge; 0.76 of edges have offset 0. Identification cost of kept edges median 6.26; stitch cost = none. Passing cross-trajectory pairs: XY distance median 0.61, 0.000 beyond 4 units; pairs within 2 units pass at 0.17. No thresholds crossed.

## D. Edges

19764 edges. Cost p50 0.0, p90 4.0, p99 14.0, max 30.0. Out-degree 2/9.9/10 (min/mean/max), in-degree 0/9.9/23. Same-trajectory edges 0.011, of which forward 0.529; forward cost / true Delta median 0.00; 115 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 115 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

14 strongly connected components, largest 0.976 of N; 1 weakly connected component(s). No thresholds crossed.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 0.996, path cost / Delta median 0.00 (p10 0.00, p90 0.03), hops median 30, max edge cost on path median 0.9; 498 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.992, cost median 0.0, forward vs backward Pearson 0.2424256594309852, median |log(fwd/bwd)| 0.29. Evaluation tasks: task 1 cost 20, 75 hops; task 2 cost 35, 85 hops; task 3 cost 4, 56 hops; task 4 cost 17, 61 hops; task 5 cost 27, 63 hops. **Flags:** 498 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4931 | 0.286 | 16.0 | 0.1562 | 0.534 | 0.07 | 0.0000 |
| 1000 | 10 | 9644 | 0.963 | 25.0 | 0.1011 | 1.000 | 0.07 | 0.0000 |
| 1000 | 20 | 17507 | 0.980 | 29.0 | 0.0587 | 1.000 | 0.07 | 0.0000 |
| 2000 | 5 | 9981 | 0.631 | 7.0 | 0.2131 | 0.722 | 0.02 | 0.0000 |
| 2000 | 10 | 19764 | 0.976 | 14.0 | 0.1586 | 0.996 | 0.00 | 0.0000 |
| 2000 | 20 | 38329 | 0.993 | 24.0 | 0.0988 | 1.000 | 0.01 | 0.0000 |
| 5000 | 5 | 25000 | 0.804 | 1.0 | 0.2652 | 0.826 | 0.00 | 0.0000 |
| 5000 | 10 | 49973 | 0.969 | 5.0 | 0.2330 | 0.992 | 0.00 | 0.0000 |
| 5000 | 20 | 99445 | 0.999 | 11.0 | 0.1839 | 1.000 | 0.00 | 0.0000 |
