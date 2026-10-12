"""Fixed-node, data-cost edges.

Nodes are the same uniformly sampled dataset states as in the critic-cost graph.
For every node we walk forward along its own trajectory for up to `horizon`
steps.  Each landing state s_f (offset delta from the node) is compared with
every node s_j through a mutual test on the contrastive critic:

    c(s_f -> s_j) <= theta   and   c(s_j -> s_f) <= theta,

with c the column-referenced cost in steps (same definition as the critic
graph).  A passing pair means "s_f and s_j are the same place", so we add the
edge node -> j with cost delta, the true number of steps the data took.  The
critic only answers the yes/no identification question; it never sets a cost.
theta is calibrated on held-out same-trajectory pairs.

identify='nearest' replaces the threshold: every landing state identifies with
its single nearest node under the symmetric cost max(c(s_f -> s_j), c(s_j -> s_f)).
The edge is always created and the identification hop is always charged, so a
far identification is expensive rather than rejected.  No theta is needed.
"""
import jax
import jax.numpy as jnp
import numpy as np

from goal_graph import metrics as met


def _q(x, qs=(10, 50, 90)):
  x = np.asarray(x, dtype=np.float64)
  return {f'p{q}': float(np.percentile(x, q)) for q in qs} | dict(mean=float(x.mean()), max=float(x.max()))


def pair_costs_sym(enc, a, b, scale):
  """Forward c(a -> b), backward c(b -> a) for aligned state arrays (n, D)."""
  pa, qa = enc.embed(a)
  pb, qb = enc.embed(b)
  m_aa = np.sum(pa * qa, 1)
  m_bb = np.sum(pb * qb, 1)
  fwd = (m_bb - np.sum(pa * qb, 1)) / scale
  bwd = (m_aa - np.sum(pb * qa, 1)) / scale
  return fwd, bwd


def calibrate_theta(enc, heldout_flat, scale, cfg, rng, xy_dims=None):
  """theta = the `merge_tpr` quantile of the symmetric cost over held-out
  same-trajectory pairs with offset in [1, merge_delta]."""
  d_max = int(min(cfg['data_horizon'], heldout_flat.max_T))
  i, j, delta = met.sample_same_traj_pairs(heldout_flat, cfg['calib_pairs'], 0, d_max, rng)
  fwd, bwd = pair_costs_sym(enc, heldout_flat.states[i], heldout_flat.states[j], scale)
  sym = np.maximum(fwd, bwd)
  pos = (delta >= 1) & (delta <= cfg['merge_delta'])
  theta = float(np.quantile(sym[pos], cfg['merge_tpr']))
  by_offset = [float(np.mean(sym[delta == d] <= theta)) if np.any(delta == d) else None
               for d in range(d_max + 1)]
  far = delta >= 5 * cfg['merge_delta']
  # Cross-trajectory negatives (held-out).
  n = cfg['calib_pairs']
  a = rng.integers(0, len(heldout_flat), n)
  b = rng.integers(0, len(heldout_flat), n)
  keep = heldout_flat.traj_id[a] != heldout_flat.traj_id[b]
  f2, b2 = pair_costs_sym(enc, heldout_flat.states[a[keep]], heldout_flat.states[b[keep]], scale)
  pass2 = np.maximum(f2, b2) <= theta
  cross = float(pass2.mean())
  xy_info = {}
  if xy_dims:
    d = np.linalg.norm(heldout_flat.states[a[keep]][:, xy_dims] - heldout_flat.states[b[keep]][:, xy_dims], axis=1)
    xy_info = dict(cross_pass_xy_dist=_q(d[pass2]) if pass2.any() else None,
                   cross_all_xy_dist=_q(d),
                   cross_pass_frac_xy_gt_4=float(np.mean(d[pass2] > 4)) if pass2.any() else None,
                   cross_pass_xy_gt_4_count=int(np.sum(d[pass2] > 4)),
                   cross_pairs_within_2_units_pass_rate=float(np.mean(pass2[d < 2])) if np.any(d < 2) else None)
  flags = []
  if xy_info.get('cross_pass_frac_xy_gt_4') and xy_info['cross_pass_frac_xy_gt_4'] > 0.05:
    flags.append(f"{xy_info['cross_pass_frac_xy_gt_4']:.2f} of passing cross-trajectory pairs are "
                 f"> 4 XY units apart (false identifications)")
  if cross > 0.01:
    flags.append(f'cross-trajectory random pairs pass the identification test at rate {cross:.4f} > 1%')
  if by_offset[-1] is not None and by_offset[-1] > 0.2:
    flags.append(f'pairs {d_max} steps apart still pass at rate {by_offset[-1]:.2f}')
  return dict(theta=theta, merge_delta=cfg['merge_delta'], merge_tpr=cfg['merge_tpr'],
              horizon=d_max, pass_rate_by_offset=by_offset,
              far_pairs_pass_rate=float(np.mean(sym[far] <= theta)) if far.any() else None,
              cross_traj_pass_rate=cross, n_pairs=int(len(delta)),
              sym_cost_positives=_q(sym[pos]), **xy_info, flags=flags)


def _walk_matches(enc, train_flat, node_idx, Phi, Psi, diag_M, scale, theta,
                  horizon, direction, chunk, identify='mutual', ident_max=None):
  """Mutual-test matches between walked states and nodes.

  direction 'forward': walked state = delta steps after node i; a match with
  node j yields candidate edge i -> j, stitch hop = c(walked -> s_j).
  direction 'backward': walked state = delta steps before node j; a match with
  node i yields candidate edge i -> j, stitch hop = c(s_i -> walked).
  identify='nearest': the match is the argmin of the symmetric cost (no theta).
  Returns (i, j, delta, ident_cost, stitch_cost, landing_idx, n_match_per_walked_state).
  """
  n = len(node_idx)
  if direction == 'forward':
    room = train_flat.traj_end[node_idx] - node_idx
  else:
    room = node_idx - train_flat.starts[train_flat.traj_id[node_idx]]
  n_walk = np.minimum(horizon, room) + 1                         # deltas 0..H
  w_node = np.repeat(np.arange(n), n_walk)
  w_delta = np.concatenate([np.arange(m) for m in n_walk])
  w_idx = node_idx[w_node] + (w_delta if direction == 'forward' else -w_delta)
  phi_w, psi_w = enc.embed(train_flat.states[w_idx])
  m_ww = np.sum(phi_w * psi_w, 1)
  Phi_j, Psi_j, diag_j = jnp.asarray(Phi), jnp.asarray(Psi), jnp.asarray(diag_M)

  @jax.jit
  def match(pw, qw, mw):
    c_w2n = (diag_j[None, :] - pw @ Psi_j.T) / scale             # walked -> node
    c_n2w = (mw[:, None] - qw @ Phi_j.T) / scale                 # node -> walked
    sym = jnp.maximum(c_w2n, c_n2w)
    if identify == 'nearest':
      ok = jax.nn.one_hot(jnp.argmin(sym, 1), sym.shape[1], dtype=bool)
      if ident_max is not None:                         # no identification beyond ident_max
        ok = ok & (sym.min(1) <= ident_max)[:, None]
    else:
      ok = (c_w2n <= theta) & (c_n2w <= theta)
    stitch = c_w2n if direction == 'forward' else c_n2w
    return ok, sym, stitch

  parts, n_match = [], np.zeros(len(w_idx), np.int32)
  for a in range(0, len(w_idx), chunk):
    ok, sym, st = match(jnp.asarray(phi_w[a:a + chunk]), jnp.asarray(psi_w[a:a + chunk]),
                        jnp.asarray(m_ww[a:a + chunk]))
    ok, sym, st = np.asarray(ok), np.asarray(sym), np.asarray(st)
    n_match[a:a + chunk] = ok.sum(1)
    wi, nj = np.nonzero(ok)
    own = w_node[a + wi]
    if direction == 'forward':
      parts.append((own, nj, w_delta[a + wi], sym[wi, nj], st[wi, nj], w_idx[a + wi]))
    else:
      parts.append((nj, own, w_delta[a + wi], sym[wi, nj], st[wi, nj], w_idx[a + wi]))
  i, j, delta, ident, st, widx = [np.concatenate(p) for p in zip(*parts)]
  return i, j, delta, ident, st, widx, n_match


def build_data_edges(enc, train_flat, node_idx, Phi, Psi, diag_M, scale, theta,
                     horizon, k_cap, eps, stitch_cost='critic', walk='both',
                     chunk=4096, identify='mutual', xy_dims=None, ident_max=None):
  """Returns rows, cols, weights (data offset [+ stitch hop], >= eps), stats, hops.

  hops: per kept edge, the identification hop (landing state index, matched
  node, direction 0=forward/1=backward, hop cost) for wall-crossing checks.
  """
  n = len(node_idx)
  dirs = ['forward', 'backward'] if walk == 'both' else [walk]
  res = [_walk_matches(enc, train_flat, node_idx, Phi, Psi, diag_M, scale, theta,
                       horizon, d, chunk, identify, ident_max) for d in dirs]
  i, j, delta, ident, st, widx = [np.concatenate([r[c] for r in res]) for c in range(6)]
  wdir = np.concatenate([np.full(len(r[0]), 1 if d == 'backward' else 0) for r, d in zip(res, dirs)])
  n_match = np.concatenate([r[6] for r in res])
  # Nearest mode: how often does a landing delta steps away still identify
  # with its own node?  (a node-density diagnostic)
  self_by_offset = None
  if identify == 'nearest':
    self_by_offset = [float(np.mean((i == j)[delta == d])) if np.any(delta == d) else None
                      for d in range(int(delta.max()) + 1)]
  keep = i != j
  i, j, delta, ident, st = i[keep], j[keep], delta[keep], ident[keep], st[keep]
  widx, wdir = widx[keep], wdir[keep]
  # Edge cost: the data offset, plus (optionally) the critic's estimate of the
  # one stitching hop (walked state <-> node), clipped at 0.
  cost = delta.astype(np.float64) + (np.maximum(st, 0.0) if stitch_cost == 'critic' else 0.0)
  # One edge per (i, j): the cheapest, ties broken by identification cost.
  order = np.lexsort((ident, cost, j, i))
  i, j, delta, ident, cost, st, widx, wdir = [x[order] for x in (i, j, delta, ident, cost, st, widx, wdir)]
  first = np.ones(len(i), bool)
  first[1:] = (i[1:] != i[:-1]) | (j[1:] != j[:-1])
  i, j, delta, ident, cost, st, widx, wdir = [x[first] for x in (i, j, delta, ident, cost, st, widx, wdir)]
  outdeg_uncapped = np.bincount(i, minlength=n)
  if k_cap is not None:
    order = np.lexsort((ident, cost, i))
    i, j, delta, ident, cost, st, widx, wdir = [x[order] for x in (i, j, delta, ident, cost, st, widx, wdir)]
    start = np.searchsorted(i, np.arange(n))
    rank = np.arange(len(i)) - start[i]
    keep = rank < k_cap
    i, j, delta, ident, cost, st, widx, wdir = [x[keep] for x in (i, j, delta, ident, cost, st, widx, wdir)]
  weights = np.maximum(cost, eps)
  hop_node = np.where(wdir == 0, j, i)              # the node the landing identified with
  hops = dict(landing_idx=widx, node=hop_node, direction=wdir, cost=st)
  xy_info = {}
  if xy_dims is not None and len(i):
    dxy = np.linalg.norm(train_flat.states[widx][:, xy_dims]
                         - train_flat.states[node_idx[hop_node]][:, xy_dims], axis=1)
    xy_info = dict(ident_xy_dist=_q(dxy), ident_xy_gt_4_count=int(np.sum(dxy > 4)),
                   ident_xy_gt_4_frac=float(np.mean(dxy > 4)))
  stats = dict(n_landings=int(len(n_match)), walk=walk,
               matches_per_landing=_q(n_match),
               frac_landings_without_match=float(np.mean(n_match == 0)),
               nodes_without_out_edge=int(np.sum(np.bincount(i, minlength=n) == 0)),
               nodes_without_in_edge=int(np.sum(np.bincount(j, minlength=n) == 0)),
               out_degree_uncapped=_q(outdeg_uncapped), k_cap=k_cap,
               frac_edges_delta0=float(np.mean(delta == 0)), stitch_cost=stitch_cost,
               stitch_cost_added=_q(weights - delta) if stitch_cost == 'critic' else None,
               edge_offset=_q(delta), identification_cost=_q(ident), identify=identify,
               ident_max=ident_max, self_match_rate_by_offset=self_by_offset, **xy_info)
  return i, j, weights, stats, hops


def _project_states(enc, states, Phi, Psi, diag_M, scale, chunk):
  """Nearest node (symmetric cost) of every state.

  Returns label, sym cost at the label, hop_out = c(state -> node), hop_in =
  c(node -> state)."""
  phi, psi = enc.embed(states)
  m = np.sum(phi * psi, 1)
  Phi_j, Psi_j, diag_j = jnp.asarray(Phi), jnp.asarray(Psi), jnp.asarray(diag_M)

  @jax.jit
  def nearest(pw, qw, mw):
    c_w2n = (diag_j[None, :] - pw @ Psi_j.T) / scale
    c_n2w = (mw[:, None] - qw @ Phi_j.T) / scale
    sym = jnp.maximum(c_w2n, c_n2w)
    j = jnp.argmin(sym, 1)
    r = jnp.arange(pw.shape[0])
    return j, sym[r, j], c_w2n[r, j], c_n2w[r, j]

  out = [[], [], [], []]
  for a in range(0, len(states), chunk):
    res = nearest(jnp.asarray(phi[a:a + chunk]), jnp.asarray(psi[a:a + chunk]), jnp.asarray(m[a:a + chunk]))
    for o, r in zip(out, res):
      o.append(np.asarray(r))
  return [np.concatenate(o) for o in out]


def build_sweep_edges(enc, train_flat, node_idx, Phi, Psi, diag_M, scale, ident_max, eps,
                      stitch_cost='critic', chunk=4096, xy_dims=None, entry='best',
                      radius=None, radius_q=None):
  """Full-dataset sweep: project every training state onto its nearest node
  (symmetric cost <= ident_max, else unassigned), then walk each trajectory in
  time.  Whenever the label switches from node a to node b, add edge a -> b with

      cost = c(a -> s_u) + (t_b - t_u) + c(s_t_b -> b),

  where s_u is the state in a's run that minimises c(a -> s_u) - t_u (the best
  entry point), t_b is the first state of b's run, and the middle term is the
  true number of dataset steps.  Unassigned states in between are "in transit":
  the data path through them is real, so they count in the step term.  Every
  node is its own nearest node, so a node always has an out-edge unless it is the
  last label of its trajectory, and an in-edge unless it is the first.

  entry='first': s_u is the first state of a's run instead, so with
  stitch_cost='none' the cost is purely t_b - t_a (first entry to first entry)
  and sums telescope exactly to the data time along any chain; the critic then
  sets no cost at all, only the node assignment.

  radius=r: conservative costing.  Both hop terms are the constant r (the
  identification cap: every cluster state is within r critic-steps of its node
  in both directions), entry is 'first', so

      cost = r + (t_b_first - t_a_first) + r.

  The critic then only decides cluster membership; the data sets the step
  count; the per-hop overhead 2r is an upper bound on the entry/exit hops if the
  critic's error within the cap is zero (a margin would cover that error).

  radius_q=q (e.g. 90): per-node radii instead of the constant: the exit
  radius of node a is the q-th percentile of c(a -> s) over the states s in a's
  cluster, the entry radius of node b the q-th percentile of c(s -> b) over b's
  cluster.  cost = r_exit[a] + data steps + r_entry[b].  Returns the per-node
  radii in `hops['radius_exit']`, `hops['radius_entry']` for the planner.
  """
  if radius is not None or radius_q is not None:
    entry = 'first'
  n = len(node_idx)
  label, symc, hop_out, hop_in = _project_states(enc, train_flat.states, Phi, Psi, diag_M, scale, chunk)
  nearest_all = symc.copy()
  if ident_max is not None:
    label = np.where(symc <= ident_max, label, -1)
  label[node_idx] = np.arange(n)                    # the nodes themselves (guards ties)
  hop_in[node_idx] = 0.0; hop_out[node_idx] = 0.0; symc[node_idx] = 0.0
  hop_in, hop_out = np.maximum(hop_in, 0.0), np.maximum(hop_out, 0.0)
  r_exit = r_entry = None
  if radius_q is not None:
    # per-node percentile of the critic hop over the cluster's states (nodes excluded)
    assigned = np.nonzero(label >= 0)[0]
    order = assigned[np.argsort(label[assigned], kind='stable')]
    bounds = np.searchsorted(label[order], np.arange(n + 1))
    r_exit, r_entry = np.zeros(n), np.zeros(n)
    for a_ in range(n):
      seg = order[bounds[a_]:bounds[a_ + 1]]
      seg = seg[seg != node_idx[a_]]
      if len(seg):
        r_exit[a_] = np.percentile(hop_in[seg], radius_q)    # c(node -> state)
        r_entry[a_] = np.percentile(hop_out[seg], radius_q)  # c(state -> node)
    hop_in, hop_out = r_exit[np.maximum(label, 0)], r_entry[np.maximum(label, 0)]
  elif radius is not None:
    hop_in, hop_out = np.full_like(hop_in, radius), np.full_like(hop_out, radius)
  elif stitch_cost == 'none':
    hop_in, hop_out = np.zeros_like(hop_in), np.zeros_like(hop_out)
  idx = np.nonzero(label >= 0)[0]                   # assigned states, in dataset order
  traj, lab, t = train_flat.traj_id[idx], label[idx], train_flat.t[idx]
  new = np.ones(len(idx), bool)
  new[1:] = (traj[1:] != traj[:-1]) | (lab[1:] != lab[:-1])
  run_id = np.cumsum(new) - 1
  run_first = np.nonzero(new)[0]
  # best entry point of each run: argmin over its states of c(a -> s_u) - t_u
  v = hop_in[idx] - t
  order = np.lexsort((v, run_id))
  first_sorted = np.ones(len(order), bool); first_sorted[1:] = run_id[order][1:] != run_id[order][:-1]
  u_star = order[first_sorted]                      # one per run, in run order
  run_traj, run_lab = traj[run_first], lab[run_first]
  sw = np.nonzero(run_traj[1:] == run_traj[:-1])[0]  # run r -> r + 1 on the same trajectory
  a, b = run_lab[sw], run_lab[sw + 1]
  entry, exit_ = (u_star if entry == 'best' else run_first)[sw], run_first[sw + 1]
  delta = (t[exit_] - t[entry]).astype(np.float64)
  h_in, h_out = hop_in[idx[entry]], hop_out[idx[exit_]]
  cost = h_in + delta + h_out
  ident = np.maximum(symc[idx[entry]], symc[idx[exit_]])
  n_switch = len(a)
  # dedupe: cheapest per (a, b)
  order = np.lexsort((ident, cost, b, a))
  a, b, delta, ident, cost, h_in, h_out, entry, exit_ = [x[order] for x in (a, b, delta, ident, cost, h_in, h_out, entry, exit_)]
  first = np.ones(len(a), bool); first[1:] = (a[1:] != a[:-1]) | (b[1:] != b[:-1])
  a, b, delta, ident, cost, h_in, h_out, entry, exit_ = [x[first] for x in (a, b, delta, ident, cost, h_in, h_out, entry, exit_)]
  weights = np.maximum(cost, eps)
  hops = dict(landing_idx=np.concatenate([idx[entry], idx[exit_]]),
              node=np.concatenate([a, b]),
              direction=np.concatenate([np.ones(len(a), int), np.zeros(len(b), int)]),
              cost=np.concatenate([h_in, h_out]), radius_exit=r_exit, radius_entry=r_entry)
  run_len = np.diff(np.append(run_first, len(idx)))
  xy_info = {}
  if xy_dims is not None and len(a):
    dxy = np.linalg.norm(train_flat.states[hops['landing_idx']][:, xy_dims]
                         - train_flat.states[node_idx[hops['node']]][:, xy_dims], axis=1)
    xy_info = dict(ident_xy_dist=_q(dxy), ident_xy_gt_4_count=int(np.sum(dxy > 4)),
                   ident_xy_gt_4_frac=float(np.mean(dxy > 4)))
  hist, edges = np.histogram(np.clip(nearest_all, 0, 100), bins=50, range=(0, 100))
  outdeg = np.bincount(a, minlength=n)
  stats = dict(n_landings=int(len(train_flat.states)), walk='sweep', ident_max=ident_max, entry=entry,
               radius=radius, radius_q=radius_q,
               radius_exit_per_node=_q(r_exit) if r_exit is not None else None,
               radius_entry_per_node=_q(r_entry) if r_entry is not None else None,
               frac_states_assigned=float(np.mean(label >= 0)),
               nearest_cost_all_states=_q(nearest_all),
               nearest_cost_hist=dict(counts=hist.tolist(), edges=edges.tolist()),
               n_runs=int(len(run_first)), run_length=_q(run_len), n_label_switches=int(n_switch),
               matches_per_landing=None, frac_landings_without_match=float(np.mean(label < 0)),
               nodes_without_out_edge=int(np.sum(outdeg == 0)),
               nodes_without_in_edge=int(np.sum(np.bincount(b, minlength=n) == 0)),
               out_degree_uncapped=_q(outdeg), k_cap=None,
               frac_edges_delta0=float(np.mean(delta == 0)) if len(delta) else 0.0,
               stitch_cost=stitch_cost,
               stitch_cost_added=_q(h_in + h_out) if (stitch_cost == 'critic' or radius is not None or radius_q is not None) else None,
               entry_hop_cost=_q(h_in), exit_hop_cost=_q(h_out),
               edge_offset=_q(delta), identification_cost=_q(ident), identify='nearest',
               self_match_rate_by_offset=None, **xy_info)
  return a, b, weights, stats, hops
