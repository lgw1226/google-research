"""Diagnostics A-G for the contrastive goal graph."""
import numpy as np
from scipy import stats
from scipy.sparse.csgraph import connected_components


def _f(x):
  return float(x)


def _q(x, qs=(50, 90, 99)):
  x = np.asarray(x, dtype=np.float64)
  d = {f'p{q}': _f(np.percentile(x, q)) for q in qs}
  d['max'] = _f(x.max())
  d['min'] = _f(x.min())
  d['mean'] = _f(x.mean())
  return d


# ---------------------------------------------------------------- A. encoder
def row_normalization(enc, heldout_flat, Psi_nodes, n_states, seed):
  rng = np.random.default_rng(seed + 1)
  idx = rng.choice(len(heldout_flat), size=n_states, replace=False)
  phi, _ = enc.embed(heldout_flat.states[idx])
  logits = phi.astype(np.float64) @ Psi_nodes.astype(np.float64).T  # (n, N)
  log_mean = np.logaddexp.reduce(logits, axis=1) - np.log(logits.shape[1])
  shift = log_mean.max()
  v = np.exp(log_mean - shift)                                      # relative
  cv = _f(v.std() / v.mean())
  return dict(n_states=n_states, log_mean_exp_median=_f(np.median(log_mean)),
              log_mean_exp_std=_f(log_mean.std()), cv=cv,
              flags=[f'row-normalization CV {cv:.2f} > 1 (poor calibration)']
              if cv > 1.0 else [])


# ------------------------------------------------------------ B. calibration
def sample_same_traj_pairs(flat, n_pairs, delta_lo, delta_hi, rng):
  """Pairs (flat_i, flat_j) with j = i + delta on the same trajectory."""
  tid = rng.integers(0, flat.n_traj, size=n_pairs)
  T = flat.lens[tid] - 1
  hi = np.minimum(delta_hi, T)
  delta = rng.integers(delta_lo, hi + 1)
  t = rng.integers(0, T - delta + 1)
  i = flat.starts[tid] + t
  return i, i + delta, delta


def pair_costs(enc, flat, i, j, scale):
  """Forward cost s_i -> s_j and backward cost s_j -> s_i in steps."""
  phi_i, psi_i = enc.embed(flat.states[i])
  phi_j, psi_j = enc.embed(flat.states[j])
  m_jj = np.sum(phi_j * psi_j, axis=1)
  m_ii = np.sum(phi_i * psi_i, axis=1)
  fwd = (m_jj - np.sum(phi_i * psi_j, axis=1)) / scale
  bwd = (m_ii - np.sum(phi_j * psi_i, axis=1)) / scale
  return fwd, bwd


def calibration(enc, heldout_flat, cfg, scale, rng):
  gamma = cfg['gamma']
  d_max = int(min(round(3 / (1 - gamma)), heldout_flat.max_T))
  i, j, delta = sample_same_traj_pairs(heldout_flat, cfg['calib_pairs'], 1,
                                       d_max, rng)
  fwd, bwd = pair_costs(enc, heldout_flat, i, j, scale)
  width = cfg['calib_bin_width']
  edges = np.arange(1, d_max + width, width)
  edges[-1] = max(edges[-1], d_max + 1)
  centers, med_f, iqr_f, med_b, iqr_b, counts = [], [], [], [], [], []
  for a, b in zip(edges[:-1], edges[1:]):
    m = (delta >= a) & (delta < b)
    if m.sum() < 5:
      continue
    centers.append(_f(delta[m].mean()))
    counts.append(int(m.sum()))
    med_f.append(_f(np.median(fwd[m])))
    iqr_f.append([_f(np.percentile(fwd[m], 25)), _f(np.percentile(fwd[m], 75))])
    med_b.append(_f(np.median(bwd[m])))
    iqr_b.append([_f(np.percentile(bwd[m], 25)), _f(np.percentile(bwd[m], 75))])
  rho = _f(stats.spearmanr(delta, fwd).correlation)
  rho_b = _f(stats.spearmanr(delta, bwd).correlation)
  # Linear fit of the binned forward medians (count-weighted) over the intended
  # edge-length range; a raw-pair fit is dominated by the heavy upper tail.
  fit_max = cfg['calib_fit_max_delta'] or int(round(1 / (1 - gamma)))
  cc, mm, ww = np.array(centers), np.array(med_f), np.array(counts, float)
  fm = cc <= fit_max
  if fm.sum() < 2:
    fm[:2] = True
  slope, intercept = np.polyfit(cc[fm], mm[fm], 1, w=np.sqrt(ww[fm]))
  pred = slope * cc[fm] + intercept
  r2 = 1 - np.sum((mm[fm] - pred) ** 2) / max(np.sum((mm[fm] - mm[fm].mean()) ** 2), 1e-12)
  # Raw-pair R^2 of the same line (how noisy individual pairs are around it).
  pr = slope * delta + intercept
  r2_pairs = 1 - np.sum((fwd - pr) ** 2) / np.sum((fwd - fwd.mean()) ** 2)
  # Delta_rel: largest delta such that every bin up to it has its median within
  # +-20% of the linear fit (relative to max(|fit|, 1) to avoid blow-up near 0).
  within = []
  for c, m in zip(centers, med_f):
    fit = slope * c + intercept
    within.append(abs(m - fit) <= 0.2 * max(abs(fit), 1.0))
  d_rel = 0.0
  for c, w, (a, b) in zip(centers, within, zip(edges[:-1], edges[1:])):
    if not w:
      break
    d_rel = _f(min(b - 1, d_max))
  # Where the curve leaves the line at the long end (saturation onset): the
  # largest Delta such that its bin and all bins below it down to the first
  # in-tolerance bin are within 20% of the fit.
  d_lin_hi, first_ok = 0.0, None
  for idx, (w, (a, b)) in enumerate(zip(within, zip(edges[:-1], edges[1:]))):
    if w and first_ok is None:
      first_ok = idx
    if first_ok is not None:
      if not w:
        break
      d_lin_hi = _f(min(b - 1, d_max))
  d_lin_lo = _f(edges[first_ok]) if first_ok is not None else None
  flags = []
  if d_lin_lo is not None and d_lin_lo > 1:
    flags.append(f'binned median leaves the linear fit at the SHORT end: linear only for '
                 f'Delta in [{d_lin_lo:.0f}, {d_lin_hi:.0f}] (cost ~ 0 or negative below)')
  if d_rel < cfg['delta_rel_min']:
    flags.append(f'Delta_rel={d_rel:.0f} below floor {cfg["delta_rel_min"]}; '
                 f'using floor (calibration breaks at short horizons)')
    d_rel = float(cfg['delta_rel_min'])
  if rho < 0.8:
    flags.append(f'forward Spearman rho {rho:.3f} < 0.8')
  if not all(np.diff(med_f) >= -0.05 * np.maximum(np.abs(med_f[:-1]), 1)):
    flags.append('forward binned median is not monotone')
  return dict(delta_max=d_max, n_pairs=len(delta), bin_centers=centers,
              bin_counts=counts, forward_median=med_f, forward_iqr=iqr_f,
              backward_median=med_b, backward_iqr=iqr_b,
              forward_spearman=rho, backward_spearman=rho_b,
              fit=dict(slope=_f(slope), intercept=_f(intercept), r2=_f(r2),
                       r2_pairs=_f(r2_pairs), max_delta=int(fit_max)),
              bins_within_20pct=[bool(w) for w in within],
              delta_rel=d_rel, linear_range=[d_lin_lo, d_lin_hi],
              backward_minus_forward_median=_f(np.median(bwd - fwd)),
              flags=flags), (delta, fwd, bwd)


# ----------------------------------------------------------- C. cost matrix
def cost_matrix_metrics(M, diag_M, C_raw, rows, cols):
  n = M.shape[0]
  off = ~np.eye(n, dtype=bool)
  neg_all = _f(np.mean(C_raw[off] < 0))
  neg_edges = _f(np.mean(C_raw[rows, cols] < 0))
  z = (diag_M - diag_M.mean()) / diag_M.std()
  n_out = int(np.sum(np.abs(z) > 3))
  asym = _f(np.corrcoef(C_raw[off], C_raw.T[off])[0, 1])
  flags = []
  if neg_all > 0.03:
    flags.append(f'negative fraction (all off-diagonal) {neg_all:.3f} > 3%')
  if neg_edges > 0.03:
    flags.append(f'negative fraction (selected edges) {neg_edges:.3f} > 3%')
  if n_out > 0.01 * n:
    flags.append(f'{n_out} diagonal outliers (|z|>3) > 1% of nodes')
  if asym > 0.95:
    flags.append(f'C vs C^T Pearson {asym:.3f} > 0.95 (near-symmetric)')
  return dict(negative_fraction_all=neg_all, negative_fraction_edges=neg_edges,
              negative_min_cost=_f(C_raw[off].min()),
              diag_M=_q(diag_M, (1, 50, 99)), diag_M_std=_f(diag_M.std()),
              diag_outliers_z3=n_out, asymmetry_pearson=asym, flags=flags)


# ------------------------------------------------------------------ D. edges
def edge_metrics(rows, cols, weights, node_traj, node_t, n, k, delta_rel, tau,
                 mode='both'):
  wq = _q(weights)
  outdeg = np.bincount(rows, minlength=n)
  indeg = np.bincount(cols, minlength=n)
  same = node_traj[rows] == node_traj[cols]
  dt = (node_t[cols] - node_t[rows])[same]
  w_same = weights[same]
  fwd = dt > 0
  fwd_ratio = w_same[fwd] / dt[fwd]
  cheap = int(np.sum(fwd_ratio < 0.5))
  flags = []
  if wq['p99'] > delta_rel:
    flags.append(f'edge cost p99 {wq["p99"]:.1f} > Delta_rel {delta_rel:.0f}'
                 + ('' if tau else ' (consider enabling tau)'))
  if tau is None and ((mode in ('both', 'out') and outdeg.min() < k) or
                      (mode in ('both', 'in') and indeg.min() < k)):
    flags.append('min degree < k without tau (bug)')
  if mode == 'in' and outdeg.min() == 0:
    flags.append(f'{int(np.sum(outdeg == 0))} nodes have out-degree 0 (incoming-only edges)')
  hub = int(np.sum(indeg > 5 * k))
  if hub:
    flags.append(f'{hub} in-degree hubs with in-degree > 5k '
                 f'(max {indeg.max()}); suspected wormhole attractors')
  if cheap:
    flags.append(f'{cheap} same-trajectory forward edges with cost < 0.5*Delta')
  return dict(n_edges=int(len(rows)), cost=wq,
              out_degree=dict(min=int(outdeg.min()), mean=_f(outdeg.mean()),
                              max=int(outdeg.max())),
              in_degree=dict(min=int(indeg.min()), mean=_f(indeg.mean()),
                             max=int(indeg.max())),
              same_traj_fraction=_f(same.mean()),
              same_traj_forward_fraction=_f(fwd.mean()) if same.any() else None,
              same_traj_forward_cost_over_delta=_q(fwd_ratio, (10, 50, 90))
              if fwd.any() else None,
              same_traj_forward_abs_delta=_q(dt[fwd], (10, 50, 90)) if fwd.any() else None,
              same_traj_backward_cost=_q(w_same[~fwd], (10, 50, 90)) if (~fwd).any() else None,
              same_traj_cheap_forward_edges=cheap,
              flags=flags), (outdeg, indeg)


# ----------------------------------------------------------- E. connectivity
def connectivity_metrics(G):
  n = G.shape[0]
  n_scc, lab = connected_components(G, directed=True, connection='strong')
  largest = _f(np.bincount(lab).max() / n)
  n_wcc, _ = connected_components(G, directed=True, connection='weak')
  flags = []
  if largest < 0.95:
    flags.append(f'largest SCC {largest:.3f} < 0.95')
  if n_wcc > 1:
    flags.append(f'{n_wcc} weakly connected components > 1')
  return dict(n_scc=int(n_scc), largest_scc_fraction=largest, n_wcc=int(n_wcc),
              flags=flags)


# ------------------------------------------------------------------ F. paths
def run_queries(planner, enc, starts, goals):
  p0, q0 = enc.embed(starts)
  pg, qg = enc.embed(goals)
  return [planner.plan(p0[i], q0[i], pg[i], qg[i]) for i in range(len(starts))]


def maze_lower_bound(env, train_flat, xy_dims):
  """Approximate lower bound in steps on start -> goal cost from maze geometry:
  max(euclid, (bfs_cells - 1) * unit) / fastest per-step XY displacement in the data."""
  u = env.unwrapped
  if getattr(u, 'maze_map', None) is None or xy_dims is None:
    return None
  dist = maze_cell_distances(env)
  unit = u._maze_unit  # pylint: disable=protected-access
  xy = train_flat.states[:, xy_dims]
  same = train_flat.traj_id[1:] == train_flat.traj_id[:-1]
  step = np.linalg.norm(xy[1:] - xy[:-1], axis=1)[same]
  speed = float(np.percentile(step, 99))

  def lb(s_xy, g_xy):
    a, b = tuple(u.xy_to_ij(s_xy)), tuple(u.xy_to_ij(g_xy))
    cells = dist.get(a, {}).get(b, np.inf)
    d = max(float(np.linalg.norm(s_xy - g_xy)), (cells - 1) * unit)
    return d / speed
  lb.speed = speed
  return lb


def heldout_path_queries(planner, enc, heldout_flat, cfg, delta_rel, rng, lb_fn=None, xy_dims=None):
  T = heldout_flat.max_T
  lo = int(min(2 * delta_rel, T))
  hi = int(min(10 * delta_rel, T))
  if lo >= hi:
    lo = max(1, hi // 2)
  i, j, delta = sample_same_traj_pairs(heldout_flat, cfg['path_queries'], lo,
                                       hi, rng)
  res = run_queries(planner, enc, heldout_flat.states[i],
                    heldout_flat.states[j])
  succ = np.array([r['success'] for r in res])
  ratio = np.array([r['cost'] / d for r, d in zip(res, delta)])
  hops = np.array([len(r['path']) - 1 for r in res])
  maxe = np.array([max(r['edge_costs']) if r['success'] else np.nan for r in res])
  ok = succ
  flags = []
  sr = _f(succ.mean())
  if sr < 0.95:
    flags.append(f'held-out path success {sr:.3f} < 0.95')
  n_worm = int(np.sum(ratio[ok] < 0.3))
  if n_worm:
    flags.append(f'{n_worm} held-out queries with path cost / Delta < 0.3 '
                 f'(wormhole suspects)')
  med = _f(np.median(ratio[ok])) if ok.any() else None
  if med is not None and med > 1.5:
    flags.append(f'median path cost / Delta {med:.2f} >> 1')
  out = dict(n=len(delta), delta_range=[lo, hi], success_rate=sr,
             cost_over_delta=_q(ratio[ok], (10, 50, 90)) if ok.any() else None,
             hops=_q(hops[ok], (10, 50, 90)) if ok.any() else None,
             max_edge_cost_on_path=_q(maxe[ok], (50, 90, 99)) if ok.any() else None,
             n_wormhole_suspects=n_worm, flags=flags)
  raw = dict(i=i, j=j, delta=delta, results=res, ratio=ratio)
  if lb_fn is not None:
    sxy = heldout_flat.states[i][:, xy_dims]; gxy = heldout_flat.states[j][:, xy_dims]
    lb = np.array([lb_fn(a, b) for a, b in zip(sxy, gxy)])
    cost = np.array([r['cost'] for r in res])
    fin = ok & np.isfinite(lb) & (lb > 0)
    below = int(np.sum(cost[fin] < lb[fin]))
    out['lower_bound'] = dict(speed_units_per_step=float(lb_fn.speed),
                              cost_over_lb=_q(cost[fin] / lb[fin], (10, 50, 90)) if fin.any() else None,
                              delta_over_lb=_q(delta[fin] / lb[fin], (10, 50, 90)) if fin.any() else None,
                              n_below_lb=below, frac_below_lb=_f(below / max(fin.sum(), 1)))
    if below:
      flags.append(f'{below} planned paths cheaper than the maze lower bound (certain underestimates)')
    raw['lb'] = lb
  return out, raw


def random_queries(planner, enc, S, node_traj, n_queries, rng):
  n = len(S)
  a = rng.integers(0, n, size=n_queries)
  b = rng.integers(0, n, size=n_queries)
  keep = node_traj[a] != node_traj[b]
  a, b = a[keep], b[keep]
  fwd = run_queries(planner, enc, S[a], S[b])
  bwd = run_queries(planner, enc, S[b], S[a])
  cf = np.array([r['cost'] for r in fwd])
  cb = np.array([r['cost'] for r in bwd])
  both = np.isfinite(cf) & np.isfinite(cb)
  return dict(n=int(len(a)), reachability=_f(np.isfinite(cf).mean()),
              cost=_q(cf[np.isfinite(cf)], (10, 50, 90)) if np.isfinite(cf).any() else None,
              hops=_q([len(r['path']) - 1 for r in fwd if r['success']], (10, 50, 90)),
              fwd_bwd_pearson=_f(np.corrcoef(cf[both], cb[both])[0, 1]) if both.sum() > 2 else None,
              fwd_over_bwd_median=_f(np.median(cf[both] / cb[both])) if both.any() else None,
              fwd_over_bwd_abs_log_median=_f(np.median(np.abs(np.log(cf[both] / cb[both])))) if both.any() else None,
              flags=[]), dict(a=a, b=b, fwd=fwd, bwd=bwd)


def eval_task_queries(planner, enc, env, n_tasks=5):
  starts, goals = [], []
  for tid in range(1, n_tasks + 1):
    ob, info = env.reset(options=dict(task_id=tid))
    starts.append(np.asarray(ob, np.float32))
    goals.append(np.asarray(info['goal'], np.float32))
  starts, goals = np.stack(starts), np.stack(goals)
  res = run_queries(planner, enc, starts, goals)
  tasks = [dict(task_id=t + 1, success=bool(r['success']),
                cost=_f(r['cost']) if r['success'] else None,
                hops=len(r['path']) - 1 if r['success'] else None,
                max_edge_cost=_f(max(r['edge_costs'])) if r['success'] else None)
           for t, r in enumerate(res)]
  n_fail = sum(not t['success'] for t in tasks)
  flags = [f'{n_fail} of {n_tasks} evaluation tasks have no path'] if n_fail else []
  return dict(tasks=tasks, flags=flags), dict(starts=starts, goals=goals,
                                               results=res)


# ------------------------------------------------- maze-specific edge check
def maze_cell_distances(env):
  """All-pairs BFS distance (in cells) over the free cells of the maze."""
  from collections import deque
  u = env.unwrapped
  mm = np.asarray(u.maze_map)
  free = list(zip(*np.where(mm == 0)))
  dist = {}
  for src in free:
    d = {src: 0}
    q = deque([src])
    while q:
      i, j = q.popleft()
      for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= ni < mm.shape[0] and 0 <= nj < mm.shape[1] and mm[ni, nj] == 0 and (ni, nj) not in d:
          d[(ni, nj)] = d[(i, j)] + 1
          q.append((ni, nj))
    dist[src] = d
  return dist


def maze_shortcut_metrics(env, xy, rows, cols, weights, delta_rel):
  """Edges whose endpoints are much farther apart in the maze than in XY."""
  u = env.unwrapped
  if getattr(u, 'maze_map', None) is None:
    return None
  dist = maze_cell_distances(env)
  unit = u._maze_unit  # pylint: disable=protected-access
  cells = [tuple(u.xy_to_ij(p)) for p in xy]
  bfs = np.array([dist.get(cells[a], {}).get(cells[b], np.inf) for a, b in zip(rows, cols)])
  euclid = np.linalg.norm(xy[rows] - xy[cols], axis=1) / unit
  shortcut = bfs > np.ceil(euclid) + 1                # straight line needs ~ceil(euclid) cells
  frac = _f(shortcut.mean())
  flags = []
  if frac > 0.01:
    flags.append(f'{shortcut.sum()} edges ({frac:.3f}) are maze shortcuts (BFS cells >> XY '
                 f'distance, i.e. cross walls); their cost median '
                 f'{np.median(weights[shortcut]):.1f}')
  return dict(n_shortcut_edges=int(shortcut.sum()), shortcut_fraction=frac,
              shortcut_cost=_q(weights[shortcut], (10, 50, 90)) if shortcut.any() else None,
              shortcut_cheaper_than_delta_rel=int(np.sum(weights[shortcut] < delta_rel)),
              edge_bfs_cells=_q(bfs[np.isfinite(bfs)], (50, 90, 99)),
              flags=flags)
