# antmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 395000 steps (B = 256). Held-out loss 0.0064, top-1 accuracy 0.769 (chance 0.0039); train loss 0.0057, accuracy 0.807. Mean positive logit 0.38 vs negative -25.86. Clipped positives 0.042. Row normalization over 500 held-out states: CV 1.15, std of log mean exp 0.82. **Flags:** row-normalization CV 1.15 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.680; linear fit slope 2.312, intercept -8.81 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.408 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 35.1 (backward rho 0.501). **Flags:** forward Spearman rho 0.680 < 0.8.

## C. Cost matrix

Negative fraction 0.0001 of off-diagonal entries and 0.0242 of selected edges (min raw cost -31.3). diag(M) median 1.56 (p1 -0.88, p99 5.76), 23 outliers with |z| > 3. Pearson(C, C^T) = 0.579. **Flags:** 23 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 40.15 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.53, 10: 0.27, 30: 0.10; random cross-trajectory pairs 0.0010. 57188 landing states, 0.10 without any match, mean 3.8 matches each. Uncapped out-degree median 16 (max 53), cap 10; 48 nodes without an outgoing edge; 0.15 of edges have offset 0. Identification cost of kept edges median 32.89; stitch cost = critic (added median 16.76, p90 32.42). Passing cross-trajectory pairs: XY distance median 0.65, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. No thresholds crossed.

## D. Edges

18043 edges. Cost p50 25.5, p90 40.8, p99 58.2, max 69.9. Out-degree 0/9.0/10 (min/mean/max), in-degree 0/9.0/41. Same-trajectory edges 0.012, of which forward 0.742; forward cost / true Delta median 0.63; 58 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** edge cost p99 58.2 > Delta_rel 30 (consider enabling tau); min degree < k without tau (bug); 58 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

143 strongly connected components, largest 0.915 of N; 49 weakly connected component(s). **Flags:** largest SCC 0.915 < 0.95; 49 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 1.000, path cost / Delta median 0.66 (p10 0.44, p90 1.04), hops median 6, max edge cost on path median 30.7; 15 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 1.000, cost median 188.3, forward vs backward Pearson 0.6423844266019115, median |log(fwd/bwd)| 0.24. Evaluation tasks: task 1 cost 398, 23 hops; task 2 cost 176, 7 hops; task 3 cost 181, 17 hops; task 4 cost 180, 9 hops; task 5 cost 235, 16 hops. **Flags:** 15 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4473 | 0.744 | 60.3 | 0.0262 | 0.978 | 0.90 | 0.0000 |
| 1000 | 10 | 7308 | 0.876 | 64.7 | 0.0172 | 1.000 | 0.84 | 0.0000 |
| 1000 | 20 | 8717 | 0.878 | 66.6 | 0.0145 | 1.000 | 0.80 | 0.0000 |
| 2000 | 5 | 9496 | 0.824 | 47.9 | 0.0422 | 0.996 | 0.71 | 0.0000 |
| 2000 | 10 | 18043 | 0.915 | 58.2 | 0.0242 | 1.000 | 0.66 | 0.0000 |
| 2000 | 20 | 29258 | 0.927 | 64.2 | 0.0155 | 1.000 | 0.64 | 0.0000 |
| 5000 | 5 | 24418 | 0.836 | 33.3 | 0.0859 | 0.996 | 0.48 | 0.0000 |
| 5000 | 10 | 48515 | 0.926 | 42.6 | 0.0490 | 1.000 | 0.45 | 0.0000 |
| 5000 | 20 | 94263 | 0.951 | 55.1 | 0.0274 | 1.000 | 0.45 | 0.0000 |
