# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.680; linear fit slope 2.312, intercept -8.81 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.408 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 35.1 (backward rho 0.501). **Flags:** forward Spearman rho 0.680 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0241 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 40.15 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.53, 10: 0.27, 30: 0.10; random cross-trajectory pairs 0.0010. 114716 landing states, 0.12 without any match, mean 3.6 matches each. Uncapped out-degree median 23 (max 73), cap 10, walk = both; 40 nodes without an outgoing edge, 72 without an incoming edge; 0.07 of edges have offset 0. Identification cost of kept edges median 32.47; stitch cost = critic (added median 11.09, p90 26.96). Passing cross-trajectory pairs: XY distance median 0.65, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. No thresholds crossed.

## D. Edges

18882 edges. Cost p50 20.8, p90 35.7, p99 53.3, max 70.1. Out-degree 0/9.4/10 (min/mean/max), in-degree 0/9.4/38. Same-trajectory edges 0.011, of which forward 0.750; forward cost / true Delta median 0.53; 67 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 53.3 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 67 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

128 strongly connected components, largest 0.924 of N; 30 weakly connected component(s). **Flags:** largest SCC 0.924 < 0.95; 30 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.56 (p10 0.35, p90 0.87), hops median 6, max edge cost on path median 26.3; 24 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 144.6, forward vs backward Pearson 0.5759928005161746, median |log(fwd/bwd)| 0.26. Evaluation tasks: task 1 cost 301, 23 hops; task 2 cost 158, 7 hops; task 3 cost 209, 24 hops; task 4 cost 143, 8 hops; task 5 cost 318, 22 hops. **Flags:** 24 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4726 | 0.877 | 56.3 | 0.0273 | 0.990 | 0.75 | 0.0000 |
| 1000 | 10 | 8492 | 0.931 | 62.0 | 0.0164 | 1.000 | 0.72 | 0.0000 |
| 1000 | 20 | 11682 | 0.936 | 66.2 | 0.0120 | 1.000 | 0.71 | 0.0000 |
| 2000 | 5 | 9646 | 0.890 | 42.8 | 0.0436 | 1.000 | 0.59 | 0.0000 |
| 2000 | 10 | 18882 | 0.924 | 53.3 | 0.0241 | 1.000 | 0.56 | 0.0000 |
| 2000 | 20 | 34272 | 0.938 | 62.4 | 0.0142 | 1.000 | 0.54 | 0.0000 |
| 5000 | 5 | 24488 | 0.894 | 27.9 | 0.0913 | 0.996 | 0.38 | 0.0000 |
| 5000 | 10 | 48770 | 0.943 | 36.9 | 0.0526 | 1.000 | 0.36 | 0.0000 |
| 5000 | 20 | 96587 | 0.955 | 48.6 | 0.0290 | 1.000 | 0.36 | 0.0000 |
