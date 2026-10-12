# pointmaze-large-stitch-v0: goal graph summary

N = 2000, k = 10, gamma = 0.9, tau = None, d = 64, seed = 0, edge mode = both, offset_min = 0, graph mode = data. Costs in steps.

## A. Encoder health

Trained 360000 steps (B = 256). Held-out loss 0.0107, top-1 accuracy 0.368 (chance 0.0039); train loss 0.0105, accuracy 0.367. Mean positive logit -1.55 vs negative -14.48. Clipped positives 0.041. Row normalization over 500 held-out states: CV 0.35, std of log mean exp 0.33. No thresholds crossed.

## B. Calibration

Forward cost vs Delta on 20000 held-out pairs, Delta in [1, 30]: Spearman rho 0.301; linear fit slope 0.265, intercept 0.01 (fit to binned medians, Delta <= 10; R2 1.000 on medians, -0.099 on raw pairs). Delta_rel = 30; the binned median is within 20% of the fit for Delta in [1.0, 30.0]. Backward minus forward cost median 0.9 (backward rho 0.244). **Flags:** forward Spearman rho 0.301 < 0.8.

## C. Cost matrix

Negative fraction 0.0022 of off-diagonal entries and 0.3479 of selected edges (min raw cost -16.0). diag(M) median -1.09 (p1 -2.26, p99 2.06), 29 outliers with |z| > 3. Pearson(C, C^T) = 0.624. **Flags:** negative fraction (selected edges) 0.348 > 3%; 29 diagonal outliers (|z|>3) > 1% of nodes.

## C2. Node identification (data-cost edges)

theta = 8.00 steps chosen so that 90% of held-out pairs 1-3 steps apart pass. Pass rate by offset: 0: 1.00, 5: 0.70, 10: 0.55, 30: 0.46; random cross-trajectory pairs 0.0110. 114716 landing states, 0.04 without any match, mean 22.0 matches each. Uncapped out-degree median 45 (max 131), cap 10, walk = both; 0 nodes without an outgoing edge, 37 without an incoming edge; 0.62 of edges have offset 0. Identification cost of kept edges median 1.30; stitch cost = critic (added median 0.00, p90 2.29). Passing cross-trajectory pairs: XY distance median 0.17, 0.000 beyond 4 units; pairs within 2 units pass at 0.39. **Flags:** cross-trajectory random pairs pass the identification test at rate 0.0110 > 1%; pairs 30 steps apart still pass at rate 0.46.

## D. Edges

19909 edges. Cost p50 0.5, p90 8.2, p99 20.7, max 37.6. Out-degree 3/10.0/10 (min/mean/max), in-degree 0/10.0/39. Same-trajectory edges 0.006, of which forward 0.568; forward cost / true Delta median 0.04; 52 with cost < 0.5 Delta. Maze shortcut edges (cross walls): 0 (0.0000), 0 of them cheaper than Delta_rel. **Flags:** min degree < k without tau (bug); 52 same-trajectory forward edges with cost < 0.5*Delta.

## E. Connectivity

214 strongly connected components, largest 0.461 of N; 3 weakly connected component(s). **Flags:** largest SCC 0.461 < 0.95; 3 weakly connected components > 1.

## F. Paths

Held-out same-trajectory queries (500, Delta in [60, 200]): success 0.918, path cost / Delta median 0.23 (p10 0.01, p90 0.50), hops median 15, max edge cost on path median 8.0; 314 wormhole suspects (ratio < 0.3). Random cross-trajectory node pairs (500): reachability 0.494, cost median 89.0, forward vs backward Pearson 0.8725211531987416, median |log(fwd/bwd)| 0.19. Evaluation tasks: task 1 cost 201, 58 hops; task 2 no path; task 3 cost 211, 59 hops; task 4 no path; task 5 no path. **Flags:** held-out path success 0.918 < 0.95; 314 held-out queries with path cost / Delta < 0.3 (wormhole suspects); 3 of 5 evaluation tasks have no path.

## G. Sensitivity (N x k)

| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5 | 4981 | 0.141 | 23.0 | 0.3120 | 0.616 | 0.22 | 0.0000 |
| 1000 | 10 | 9687 | 0.594 | 28.6 | 0.1903 | 0.958 | 0.27 | 0.0000 |
| 1000 | 20 | 17023 | 0.760 | 32.5 | 0.1104 | 0.988 | 0.26 | 0.0000 |
| 2000 | 5 | 9991 | 0.115 | 13.2 | 0.4799 | 0.576 | 0.18 | 0.0000 |
| 2000 | 10 | 19909 | 0.461 | 20.7 | 0.3479 | 0.918 | 0.23 | 0.0000 |
| 2000 | 20 | 39085 | 0.554 | 28.5 | 0.2150 | 0.970 | 0.21 | 0.0000 |
| 5000 | 5 | 25000 | 0.125 | 6.0 | 0.6460 | 0.436 | 0.09 | 0.0000 |
| 5000 | 10 | 49996 | 0.443 | 9.6 | 0.5236 | 0.882 | 0.11 | 0.0000 |
| 5000 | 20 | 99865 | 0.578 | 16.0 | 0.3844 | 0.964 | 0.10 | 0.0000 |
