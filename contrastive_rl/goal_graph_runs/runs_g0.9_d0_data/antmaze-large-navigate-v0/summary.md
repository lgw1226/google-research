# antmaze-large-navigate-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 430000 steps (B = 256). Held-out loss 0.0096, top-1 accuracy 0.747 (chance 0.0039); train loss 0.0056, accuracy 0.807. Mean positive logit 0.74 vs negative -22.45. Clipped positives 0.008. Row normalization over 500 held-out states: CV 1.18, std of log mean exp 1.54. **Flags:** row-normalization CV 1.18 > 1 (poor calibration).

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.628; linear fit slope 1.940, intercept -8.74 (fit to binned medians, Delta <= 10; R2 1.000 on medians, 0.362 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 41.4 (backward rho 0.535). **Flags:** forward Spearman rho 0.628 < 0.8.

## C. Cost matrix

Negative fraction 0.0002 of off-diagonal entries and 0.0320 of selected edges (min raw cost -33.9). diag(M) median 1.46 (p1 -1.00, p99 5.06), 11 outliers with |z| > 3. Pearson(C, C^T) = 0.490. **Flags:** negative fraction (selected edges) 0.032 > 3%.

## C2. Node identification (data-cost edges)

theta = 35.99 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.51, 10: 0.25, 30: 0.15; random cross-trajectory pairs 0.0010. 61004 landing states, 0.16 without any match, mean 2.5 matches each. Uncapped out-degree median 12 (max 48), cap 10; 105 nodes without an outgoing edge; 0.27 of edges have offset 0. Identification cost of kept edges median 31.59; stitch cost = none. Passing cross-trajectory pairs: XY distance median 0.59, 0.000 beyond 4 units; pairs within 2 units pass at 0.04. **Flags:** 105 nodes have no outgoing data edge.

## D. Edges

15953 edges. Cost p50 5.0, p90 21.0, p99 29.0, max 30.0. Out-degree 0/8.0/10 (min/mean/max), in-degree 0/8.0/32. Same-trajectory edges 0.030, of which forward 0.584; forward cost / true Delta median 0.00; 232 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 232 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

198 strongly connected components, largest 0.857 of N; 146 weakly connected component(s). **Flags:** largest SCC 0.857 < 0.95; 146 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 300]): success 1.000, path cost / Delta median 0.19 (p10 0.05, p90 0.44), hops median 19, max edge cost on path median 14.9; 381 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.998, cost median 30.0, forward vs backward Pearson 0.8749922485972546, median |log(fwd/bwd)| 0.36. Evaluation tasks: task 1 cost 63, 79 hops; task 2 cost 71, 96 hops; task 3 cost 72, 61 hops; task 4 cost 117, 41 hops; task 5 cost 89, 81 hops. **Flags:** 381 held-out queries with path cost / Delta < 0.3 (wormhole suspects).

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 3838 | 0.800 | 29.0 | 0.0331 | 0.998 | 0.44 | 0.0000 |
| 1000 | 10 | 5694 | 0.826 | 30.0 | 0.0251 | 1.000 | 0.42 | 0.0000 |
| 1000 | 20 | 6250 | 0.827 | 30.0 | 0.0232 | 1.000 | 0.41 | 0.0000 |
| 2000 | 5 | 8812 | 0.821 | 26.0 | 0.0439 | 0.990 | 0.21 | 0.0000 |
| 2000 | 10 | 15953 | 0.857 | 29.0 | 0.0320 | 1.000 | 0.19 | 0.0000 |
| 2000 | 20 | 22788 | 0.861 | 30.0 | 0.0245 | 1.000 | 0.19 | 0.0000 |
| 5000 | 5 | 23430 | 0.816 | 16.0 | 0.0616 | 0.978 | 0.05 | 0.0000 |
| 5000 | 10 | 44979 | 0.855 | 23.0 | 0.0512 | 0.988 | 0.05 | 0.0000 |
| 5000 | 20 | 84417 | 0.864 | 28.0 | 0.0381 | 1.000 | 0.05 | 0.0000 |
