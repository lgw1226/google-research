"""Full pipeline: train encoders, build graph, compute metrics A-G, plots.

Usage (from contrastive_rl/):
  python -m goal_graph.run --dataset pointmaze-large-navigate-v0
"""
import argparse
import csv
import json
import os
import sys
import time

import numpy as np

from goal_graph import data as data_lib
from goal_graph import data_edges
from goal_graph import encoders as enc_lib
from goal_graph import graph as graph_lib
from goal_graph import metrics as met
from goal_graph import plots


def parse_args(argv=None):
  p = argparse.ArgumentParser()
  p.add_argument('--dataset', default='pointmaze-large-navigate-v0')
  p.add_argument('--out_root', default='runs')
  p.add_argument('--gamma', type=float, default=0.9)
  p.add_argument('--dim', type=int, default=64)
  p.add_argument('--hidden', default='512,512')
  p.add_argument('--batch_size', type=int, default=256)
  p.add_argument('--steps', type=int, default=500_000)
  p.add_argument('--lr', type=float, default=3e-4)
  p.add_argument('--inner_steps', type=int, default=100)
  p.add_argument('--eval_every', type=int, default=5000)
  p.add_argument('--heldout_batches', type=int, default=50)
  p.add_argument('--patience', type=int, default=20, help='evals without held-out acc gain')
  p.add_argument('--min_delta', type=float, default=0.005)
  p.add_argument('--min_steps', type=int, default=100_000)
  p.add_argument('--n_nodes', type=int, default=2000)
  p.add_argument('--k', type=int, default=10)
  p.add_argument('--edge_mode', default='both', choices=['both', 'in', 'out'],
                 help="'in' keeps only the k cheapest incoming (column-wise) edges per node")
  p.add_argument('--graph_mode', default='critic', choices=['critic', 'data'],
                 help="'data': edges from trajectory walks with true offsets as costs, "
                      "nodes identified by a mutual critic test")
  p.add_argument('--data_horizon', type=int, default=30, help='max forward walk (steps)')
  p.add_argument('--merge_delta', type=int, default=3, help='offsets <= this count as "same place"')
  p.add_argument('--merge_tpr', type=float, default=0.9, help='pass rate target on those pairs')
  p.add_argument('--data_uncapped', action='store_true', help='keep all matched edges (no k cap)')
  p.add_argument('--query_connect', default='cheapest', choices=['cheapest', 'mutual', 'nearest'],
                 help="'mutual': connect query start/goal only to nodes passing the "
                      "identification test (fallback: k cheapest); 'nearest': the single "
                      "nearest node by symmetric cost")
  p.add_argument('--identify', default='mutual', choices=['mutual', 'nearest'],
                 help="data edges: 'mutual' = both-direction threshold theta; 'nearest' = each "
                      "landing identifies with its nearest node (no theta, hop always charged)")
  p.add_argument('--data_walk', default='both', choices=['forward', 'backward', 'both', 'sweep'],
                 help='data edges: walk each node forward (edges out of it), backward '
                      "(edges into it), both, or 'sweep': project every dataset state onto "
                      'its nearest node and add an edge at every label switch along each '
                      'trajectory (nearest identification only, no horizon)')
  p.add_argument('--sweep_radius', default='critic', choices=['critic', 'cap', 'q90'],
                 help="sweep: entry/exit hop cost per edge: 'critic' (per-segment critic hops, "
                      "or none with --stitch_cost none) or 'cap' (constant = --ident_max both "
                      "sides, also for start/goal connection; no critic cost anywhere) or 'q90' "
                      "(per-node 90th percentile of the critic hop over the node's cluster)")
  p.add_argument('--sweep_entry', default='best', choices=['best', 'first'],
                 help="sweep: entry point of a run: 'best' (min critic hop - t) or 'first' "
                      "(first state; with --stitch_cost none the cost is pure data time)")
  p.add_argument('--ident_max', type=float, default=None,
                 help='nearest identification: no identification if the symmetric cost to the '
                      'nearest node exceeds this (steps); the critic then never licenses a '
                      'hop longer than this')
  p.add_argument('--stitch_cost', default='critic', choices=['none', 'critic'],
                 help="data edges: 'critic' adds the critic's landing->node cost to the offset")
  p.add_argument('--offset_min', type=int, default=0,
                 help='smallest positive offset: 0 includes (s, s) pairs with prob 1-gamma')
  p.add_argument('--tau', type=float, default=None)
  p.add_argument('--eps', type=float, default=1e-6)
  p.add_argument('--seed', type=int, default=0)
  p.add_argument('--calib_pairs', type=int, default=20000)
  p.add_argument('--calib_bin_width', type=int, default=10)
  p.add_argument('--calib_fit_max_delta', type=int, default=0, help='0 = 1/(1-gamma)')
  p.add_argument('--delta_rel_min', type=float, default=5)
  p.add_argument('--path_queries', type=int, default=500)
  p.add_argument('--random_queries', type=int, default=500)
  p.add_argument('--row_norm_states', type=int, default=500)
  p.add_argument('--sweep_N', default='1000,2000,5000')
  p.add_argument('--sweep_k', default='5,10,20')
  p.add_argument('--xy_dims', default='0,1', help="'pca' for PCA of psi")
  p.add_argument('--load_encoders', default=None, help='skip training; load pickle')
  return p.parse_args(argv)


def to_py(o):
  if isinstance(o, dict):
    return {k: to_py(v) for k, v in o.items()}
  if isinstance(o, (list, tuple)):
    return [to_py(v) for v in o]
  if isinstance(o, (np.floating, np.integer)):
    return o.item()
  if isinstance(o, np.ndarray):
    return o.tolist()
  if isinstance(o, float) and not np.isfinite(o):
    return None
  return o


def _qq(x, qs=(50, 90, 99)):
  x = np.asarray(x, dtype=np.float64)
  return {f'p{q}': float(np.percentile(x, q)) for q in qs} | dict(max=float(x.max()), mean=float(x.mean()))


def build(enc, train_flat, N, k, tau, eps, scale, seed, mode='both',
          graph_mode='critic', data_cfg=None):
  S, node_traj, node_t, node_idx = graph_lib.sample_nodes(train_flat, N, seed)
  Phi, Psi = enc.embed(S)
  M, diag_M, C_raw, C = graph_lib.cost_matrix(Phi, Psi, scale, eps)
  stats, hops = None, None
  if graph_mode == 'critic':
    rows, cols = graph_lib.select_edges(C, k, tau, mode)
    weights = C[rows, cols]
  else:
    if data_cfg['walk'] == 'sweep':
      rows, cols, weights, stats, hops = data_edges.build_sweep_edges(
          enc, train_flat, node_idx, Phi, Psi, diag_M, scale, data_cfg['ident_max'], eps,
          data_cfg['stitch_cost'], xy_dims=data_cfg['xy_dims'], entry=data_cfg.get('sweep_entry', 'best'),
          radius=data_cfg.get('radius'), radius_q=data_cfg.get('radius_q'))
    else:
      rows, cols, weights, stats, hops = data_edges.build_data_edges(
          enc, train_flat, node_idx, Phi, Psi, diag_M, scale, data_cfg['theta'],
          data_cfg['horizon'], None if data_cfg['uncapped'] else k, eps, data_cfg['stitch_cost'],
          data_cfg['walk'], identify=data_cfg['identify'], xy_dims=data_cfg['xy_dims'],
          ident_max=data_cfg['ident_max'])
  G = graph_lib.build_graph(rows, cols, weights, N)
  qcost = None
  if data_cfg:
    if data_cfg.get('radius_q') is not None:
      qcost = (hops['radius_entry'], hops['radius_exit'])
    else:
      qcost = data_cfg.get('radius')
  planner = graph_lib.Planner(rows, cols, weights, Phi, Psi, diag_M, scale, k, eps,
                              data_cfg.get('query_theta') if data_cfg else None,
                              data_cfg.get('query_connect', 'cheapest') if data_cfg else 'cheapest',
                              data_cfg.get('ident_max') if data_cfg else None, qcost)
  return dict(S=S, node_traj=node_traj, node_t=node_t, node_idx=node_idx,
              Phi=Phi, Psi=Psi, M=M, diag_M=diag_M, C_raw=C_raw, C=C,
              rows=rows, cols=cols, weights=weights, G=G, planner=planner,
              data_stats=stats, hops=hops)


def hop_shortcuts(env, train_flat, node_xy, hops, xy_dims, delta_rel):
  """Wall-crossing check on the identification hops (landing state <-> node)."""
  if hops is None or xy_dims == 'pca' or len(hops['node']) == 0:
    return None
  d = [int(x) for x in xy_dims.split(',')]
  n = len(node_xy)
  land_xy = train_flat.states[hops['landing_idx']][:, d]
  e = np.arange(len(hops['node']))
  rows = np.where(hops['direction'] == 0, n + e, hops['node'])
  cols = np.where(hops['direction'] == 0, hops['node'], n + e)
  ms = met.maze_shortcut_metrics(env, np.concatenate([node_xy, land_xy]), rows, cols,
                                 np.maximum(hops['cost'], 0.0), delta_rel)
  if ms is not None:
    ms['flags'] = [f'identification hops: {f}' for f in ms['flags']]
  return ms


def main(argv=None):
  args = parse_args(argv)
  cfg = vars(args).copy()
  out_dir = os.path.join(args.out_root, args.dataset)
  plot_dir = os.path.join(out_dir, 'plots')
  os.makedirs(plot_dir, exist_ok=True)
  logf = open(os.path.join(out_dir, 'log.txt'), 'a')

  def log(msg):
    line = f'[{time.strftime("%H:%M:%S")}] {msg}'
    print(line, flush=True); logf.write(line + '\n'); logf.flush()

  log(f'config: {json.dumps(cfg)}')
  env, train_ds, val_ds = data_lib.load(args.dataset)
  train_flat = data_lib.FlatTrajs(data_lib.to_trajectories(train_ds))
  heldout_flat = data_lib.FlatTrajs(data_lib.to_trajectories(val_ds))
  log(f'train: {train_flat.n_traj} trajs, {len(train_flat)} states, max T '
      f'{train_flat.max_T}; held-out: {heldout_flat.n_traj} trajs, '
      f'{len(heldout_flat)} states')
  obs_dim = train_flat.states.shape[1]
  scale = -np.log(args.gamma)
  rng = np.random.default_rng(args.seed)

  # ---------------------------------------------------------------- 1. train
  if args.load_encoders:
    enc = enc_lib.Encoders.load(args.load_encoders)
    train_rows = list(csv.DictReader(open(os.path.join(
        os.path.dirname(args.load_encoders), 'train_log.csv'))))
    train_rows = [{k: float(v) for k, v in r.items()} for r in train_rows]
    final = train_rows[-1]
  else:
    mean = train_flat.states.mean(0)
    std = train_flat.states.std(0) + 1e-6
    enc = enc_lib.Encoders(obs_dim, args.dim,
                           tuple(int(h) for h in args.hidden.split(',')),
                           mean.astype(np.float32), std.astype(np.float32))
    tcfg = dict(gamma=args.gamma, batch_size=args.batch_size, seed=args.seed,
                lr=args.lr, steps=args.steps, inner_steps=args.inner_steps,
                eval_every=args.eval_every, heldout_batches=args.heldout_batches,
                offset_min=args.offset_min,
                patience=args.patience, min_delta=args.min_delta,
                min_steps=args.min_steps)
    train_rows, final = enc_lib.train(enc, train_flat, heldout_flat, tcfg,
                                      out_dir, log)
  plots.training(train_rows, os.path.join(plot_dir, '6_training_curves.png'))

  metrics = {'config': cfg, 'dataset': dict(
      n_train_traj=train_flat.n_traj, n_heldout_traj=heldout_flat.n_traj,
      traj_len=train_flat.max_T, obs_dim=obs_dim)}

  # ---------------------------------------------------------- 2-5. the graph
  N, k = args.n_nodes, args.k
  xyd_list = None if args.xy_dims == 'pca' else [int(x) for x in args.xy_dims.split(',')]
  data_cfg, ident = None, None
  if args.graph_mode == 'data':
    xyd = None if args.xy_dims == 'pca' else [int(x) for x in args.xy_dims.split(',')]
    if args.data_walk == 'sweep' and args.identify != 'nearest':
      raise SystemExit('--data_walk sweep requires --identify nearest')
    if args.sweep_radius != 'critic' and (args.data_walk != 'sweep' or args.ident_max is None):
      raise SystemExit('--sweep_radius cap/q90 requires --data_walk sweep and --ident_max')
    if args.identify == 'nearest':
      ident = dict(identify='nearest', theta=None, horizon=int(min(args.data_horizon, train_flat.max_T)),
                   flags=[])
      log(f'identification: nearest node by symmetric cost (no theta), ident_max={args.ident_max}, '
          f'walk={args.data_walk}')
    else:
      ident = data_edges.calibrate_theta(enc, heldout_flat, scale, cfg, rng, xyd)
      log(f"identification: theta={ident['theta']:.3f} steps, pass by offset "
          f"{[None if x is None else round(x, 2) for x in ident['pass_rate_by_offset'][:8]]}..., "
          f"cross-traj {ident['cross_traj_pass_rate']:.4f}")
    data_cfg = dict(theta=ident['theta'], horizon=ident['horizon'], uncapped=args.data_uncapped,
                    stitch_cost=args.stitch_cost, walk=args.data_walk, identify=args.identify,
                    xy_dims=xyd, query_connect=args.query_connect, ident_max=args.ident_max,
                    sweep_entry=args.sweep_entry,
                    radius=(args.ident_max if args.sweep_radius == 'cap' else None),
                    radius_q=(90.0 if args.sweep_radius == 'q90' else None),
                    query_theta=ident['theta'] if args.query_connect == 'mutual' else None)
  g = build(enc, train_flat, N, k, args.tau, args.eps, scale, args.seed, args.edge_mode,
            args.graph_mode, data_cfg)
  log(f'graph: N={N} k={k} edges={len(g["rows"])}')
  np.savez(os.path.join(out_dir, 'graph.npz'), S=g['S'],
           node_traj_id=g['node_traj'], node_t=g['node_t'],
           node_flat_idx=g['node_idx'], Phi=g['Phi'], Psi=g['Psi'],
           diag_M=g['diag_M'], rows=g['rows'], cols=g['cols'],
           weights=g['weights'], config=json.dumps(cfg),
           input_mean=enc.mean, input_std=enc.std)

  # ------------------------------------------------------ A. encoder health
  a = dict(heldout_loss=final['heldout_loss'], heldout_acc=final['heldout_acc'],
           train_loss=final['train_loss'], train_acc=final['train_acc'],
           heldout_pos_logit=final['heldout_pos_logit'],
           heldout_neg_logit=final['heldout_neg_logit'],
           chance_acc=1 / args.batch_size, train_steps=int(final['step']),
           clipped_positive_fraction=final['train_clipped_frac'],
           row_normalization=met.row_normalization(
               enc, heldout_flat, g['Psi'], args.row_norm_states, args.seed))
  a['flags'] = list(a['row_normalization'].pop('flags'))
  if a['heldout_acc'] < 5 / args.batch_size:
    a['flags'].append(f'held-out top-1 acc {a["heldout_acc"]:.3f} < 5/B')
  if a['train_acc'] - a['heldout_acc'] > 0.1:
    a['flags'].append(f'train/held-out acc gap {a["train_acc"] - a["heldout_acc"]:.3f} > 0.1')
  if a['clipped_positive_fraction'] > 0.3:
    a['flags'].append(f'clipped positive fraction {a["clipped_positive_fraction"]:.2f} > 0.3 '
                      '(consider resampling Delta or smaller gamma)')
  metrics['A_encoder'] = a
  log(f'A: {a}')

  # --------------------------------------------------------- B. calibration
  b, (cal_delta, cal_fwd, cal_bwd) = met.calibration(enc, heldout_flat, cfg, scale, rng)
  delta_rel = b['delta_rel']
  metrics['B_calibration'] = b
  log(f'B: rho={b["forward_spearman"]:.3f} fit={b["fit"]} Delta_rel={delta_rel}')
  plots.calibration(b, os.path.join(plot_dir, '1_cost_vs_delta.png'))
  np.savez(os.path.join(out_dir, 'calibration_pairs.npz'), delta=cal_delta,
           forward=cal_fwd, backward=cal_bwd)
  if args.ident_max is not None:
    # How much the critic undershoots the true offset on pairs it would identify
    # (symmetric cost <= cap): the margin a conservative radius would need.
    sym = np.maximum(cal_fwd, cal_bwd)
    within = (sym <= args.ident_max) & (cal_delta >= 1)
    und = cal_delta[within] - sym[within]
    b['undershoot_within_cap'] = dict(
        cap=args.ident_max, n_pairs=int(within.sum()),
        delta_minus_sym=_qq(und, (50, 90, 99)) if within.any() else None,
        delta_minus_fwd=_qq(cal_delta[within] - cal_fwd[within], (50, 90, 99)) if within.any() else None,
        frac_pairs_within_cap_by_offset=[float(np.mean(within[cal_delta == d])) if np.any(cal_delta == d) else None
                                         for d in range(0, int(min(2 * args.ident_max, cal_delta.max())) + 1)])
    log(f"undershoot within cap: {b['undershoot_within_cap']['delta_minus_sym']}")

  # --------------------------------------------------------- C. cost matrix
  c = met.cost_matrix_metrics(g['M'], g['diag_M'], g['C_raw'], g['rows'], g['cols'])
  metrics['C_cost_matrix'] = c
  log(f'C: {c}')
  if ident is not None:
    ident.update(g['data_stats'])
    if ident['nodes_without_out_edge'] > 0.05 * N:
      ident['flags'].append(f"{ident['nodes_without_out_edge']} nodes have no outgoing data edge")
    metrics['C_identification'] = ident
    log(f'C identification: {ident}')
    plots.identification(ident, os.path.join(plot_dir, '7_identification.png'))

  # --------------------------------------------------------------- D. edges
  d, (outdeg, indeg) = met.edge_metrics(g['rows'], g['cols'], g['weights'],
                                        g['node_traj'], g['node_t'], N, k,
                                        delta_rel, args.tau, args.edge_mode)
  xy, xy_note = plots.node_positions(g['S'], g['Psi'], args.xy_dims)
  if args.xy_dims != 'pca':
    ms = met.maze_shortcut_metrics(env, xy, g['rows'], g['cols'], g['weights'], delta_rel)
    if ms is not None:
      d['maze_shortcuts'] = ms
      d['flags'] += ms.pop('flags')
    hs = hop_shortcuts(env, train_flat, xy, g.get('hops'), args.xy_dims, delta_rel)
    if hs is not None:
      d['identification_hop_shortcuts'] = hs
      d['flags'] += hs.pop('flags')
  metrics['D_edges'] = d
  log(f'D: {d}')
  plots.edge_costs(g['weights'], delta_rel, os.path.join(plot_dir, '2_edge_costs.png'))
  plots.degrees(outdeg, indeg, k, os.path.join(plot_dir, '3_degrees.png'))

  # -------------------------------------------------------- E. connectivity
  e = met.connectivity_metrics(g['G'])
  metrics['E_connectivity'] = e
  log(f'E: {e}')

  # --------------------------------------------------------------- F. paths
  lb_fn = met.maze_lower_bound(env, train_flat, xyd_list) if args.xy_dims != 'pca' else None
  f_ho, raw_ho = met.heldout_path_queries(g['planner'], enc, heldout_flat, cfg,
                                          delta_rel, rng, lb_fn, xyd_list)
  f_rand, raw_rand = met.random_queries(g['planner'], enc, g['S'], g['node_traj'],
                                        args.random_queries, rng)
  f_task, raw_task = met.eval_task_queries(g['planner'], enc, env)
  metrics['F_paths'] = dict(heldout_same_traj=f_ho, random_cross_traj=f_rand,
                            eval_tasks=f_task, query_connect=args.query_connect,
                            n_query_fallback=g['planner'].n_fallback,
                            n_query_far=g['planner'].n_query_far,
                            flags=f_ho['flags'] + f_rand['flags'] + f_task['flags'])
  log(f'F held-out: {f_ho}')
  log(f'F random: {f_rand}')
  log(f'F tasks: {f_task}')
  plots.path_ratio(raw_ho['ratio'], os.path.join(plot_dir, '5_path_cost_ratio.png'))

  walls = plots.maze_walls(env)
  task_paths = []
  for t, r in enumerate(raw_task['results']):
    s_xy = plots.node_positions(raw_task['starts'][t:t + 1], None, args.xy_dims)[0][0] if args.xy_dims != 'pca' else None
    g_xy = plots.node_positions(raw_task['goals'][t:t + 1], None, args.xy_dims)[0][0] if args.xy_dims != 'pca' else None
    if args.xy_dims == 'pca':  # project query embeddings like the nodes
      continue
    inner = [i for i in r['path'] if i < N]
    lab = f"task {t + 1}: " + (f"cost {r['cost']:.0f}, {len(r['path']) - 1} hops" if r['success'] else 'NO PATH')
    task_paths.append(dict(start_xy=s_xy, goal_xy=g_xy,
                           node_xy=xy[inner] if r['success'] else None, label=lab))
  plots.overlay(xy, g['rows'], g['cols'], g['weights'], walls, task_paths,
                f'{args.dataset}: N={N}, k={k}, {len(g["rows"])} edges ({xy_note})',
                os.path.join(plot_dir, '4_graph_overlay.png'))
  worm = plots.wormhole_triage(raw_ho, g['S'], xy, heldout_flat, args.xy_dims,
                               walls, os.path.join(out_dir, 'wormholes'))
  metrics['F_paths']['wormhole_triage'] = worm

  # ----------------------------------------------------------- G. sweep
  sweep = []
  for n_sw in [int(x) for x in args.sweep_N.split(',')]:
    for k_sw in [int(x) for x in args.sweep_k.split(',')]:
      if n_sw == N and k_sw == k:
        gs, es, cs, ds, fs = g, e, c, d, f_ho
      else:
        gs = build(enc, train_flat, n_sw, k_sw, args.tau, args.eps, scale, args.seed,
                   args.edge_mode, args.graph_mode, data_cfg)
        es = met.connectivity_metrics(gs['G'])
        cs = met.cost_matrix_metrics(gs['M'], gs['diag_M'], gs['C_raw'], gs['rows'], gs['cols'])
        ds, _ = met.edge_metrics(gs['rows'], gs['cols'], gs['weights'], gs['node_traj'],
                                 gs['node_t'], n_sw, k_sw, delta_rel, args.tau, args.edge_mode)
        fs, _ = met.heldout_path_queries(gs['planner'], enc, heldout_flat, cfg,
                                         delta_rel, np.random.default_rng(args.seed + 7), lb_fn, xyd_list)
        if args.xy_dims != 'pca':
          ms = met.maze_shortcut_metrics(env, plots.node_positions(gs['S'], gs['Psi'], args.xy_dims)[0],
                                         gs['rows'], gs['cols'], gs['weights'], delta_rel)
          if ms is not None:
            ds['maze_shortcuts'] = ms
      row = dict(N=n_sw, k=k_sw, n_edges=len(gs['rows']),
                 largest_scc_fraction=es['largest_scc_fraction'],
                 n_wcc=es['n_wcc'], edge_p99=ds['cost']['p99'],
                 negative_fraction_edges=cs['negative_fraction_edges'],
                 negative_fraction_all=cs['negative_fraction_all'],
                 path_success=fs['success_rate'],
                 median_path_ratio=fs['cost_over_delta']['p50'] if fs['cost_over_delta'] else None,
                 wormhole_suspects=fs['n_wormhole_suspects'],
                 shortcut_fraction=ds.get('maze_shortcuts', {}).get('shortcut_fraction'))
      sweep.append(row)
      log(f'G: {row}')
  with open(os.path.join(out_dir, 'sweep.csv'), 'w') as fh:
    w = csv.DictWriter(fh, fieldnames=list(sweep[0].keys()))
    w.writeheader(); w.writerows(sweep)
  metrics['G_sweep'] = sweep

  with open(os.path.join(out_dir, 'metrics.json'), 'w') as fh:
    json.dump(to_py(metrics), fh, indent=1)
  write_summary(metrics, out_dir, args)
  log('done')


def write_summary(m, out_dir, args):
  a, b, c, d, e, f = (m['A_encoder'], m['B_calibration'], m['C_cost_matrix'],
                      m['D_edges'], m['E_connectivity'], m['F_paths'])
  def flags(x):
    return ' **Flags:** ' + '; '.join(x['flags']) + '.' if x['flags'] else ' No thresholds crossed.'
  rn = a['row_normalization']
  ho = f['heldout_same_traj']; rq = f['random_cross_traj']; tk = f['eval_tasks']
  sw = m['G_sweep']
  ci = m.get('C_identification')
  lines = [f'# {args.dataset}: goal graph summary', '',
           f'N = {args.n_nodes}, k = {args.k}, gamma = {args.gamma}, tau = {args.tau}, '
           f'd = {args.dim}, seed = {args.seed}, edge mode = {args.edge_mode}, offset_min = '
           f'{args.offset_min}, graph mode = {args.graph_mode}. Costs in steps.', '',
           '## A. Encoder health', '',
           f"Trained {a['train_steps']} steps (B = {args.batch_size}). Held-out loss "
           f"{a['heldout_loss']:.4f}, top-1 accuracy {a['heldout_acc']:.3f} (chance "
           f"{a['chance_acc']:.4f}); train loss {a['train_loss']:.4f}, accuracy "
           f"{a['train_acc']:.3f}. Mean positive logit {a['heldout_pos_logit']:.2f} vs "
           f"negative {a['heldout_neg_logit']:.2f}. Clipped positives "
           f"{a['clipped_positive_fraction']:.3f}. Row normalization over {rn['n_states']} "
           f"held-out states: CV {rn['cv']:.2f}, std of log mean exp {rn['log_mean_exp_std']:.2f}."
           + flags(a), '',
           '## B. Calibration', '',
           f"Forward cost vs Delta on {b['n_pairs']} held-out pairs, Delta in [1, {b['delta_max']}]: "
           f"Spearman rho {b['forward_spearman']:.3f}; linear fit slope {b['fit']['slope']:.3f}, "
           f"intercept {b['fit']['intercept']:.2f} (fit to binned medians, Delta <= {b['fit']['max_delta']}; "
           f"R2 {b['fit']['r2']:.3f} on medians, {b['fit']['r2_pairs']:.3f} on raw pairs). Delta_rel = "
           f"{b['delta_rel']:.0f}; the binned median is within 20% of the fit for Delta in "
           f"{b['linear_range']}. Backward minus forward cost median "
           f"{b['backward_minus_forward_median']:.1f} (backward rho {b['backward_spearman']:.3f})."
           + flags(b), '',
           ] + ([f"Critic undershoot on held-out pairs it would identify (symmetric cost <= cap "
                 f"{b['undershoot_within_cap']['cap']:.0f}, {b['undershoot_within_cap']['n_pairs']} pairs): "
                 f"true offset minus critic cost median {b['undershoot_within_cap']['delta_minus_sym']['p50']:.1f}, "
                 f"p90 {b['undershoot_within_cap']['delta_minus_sym']['p90']:.1f}, p99 "
                 f"{b['undershoot_within_cap']['delta_minus_sym']['p99']:.1f}, max "
                 f"{b['undershoot_within_cap']['delta_minus_sym']['max']:.1f} steps.", '']
                if b.get('undershoot_within_cap') and b['undershoot_within_cap']['delta_minus_sym'] else []) + [
           '## C. Cost matrix', '',
           f"Negative fraction {c['negative_fraction_all']:.4f} of off-diagonal entries and "
           f"{c['negative_fraction_edges']:.4f} of selected edges (min raw cost "
           f"{c['negative_min_cost']:.1f}). diag(M) median {c['diag_M']['p50']:.2f} "
           f"(p1 {c['diag_M']['p1']:.2f}, p99 {c['diag_M']['p99']:.2f}), {c['diag_outliers_z3']} "
           f"outliers with |z| > 3. Pearson(C, C^T) = {c['asymmetry_pearson']:.3f}." + flags(c), '',
           ] + ([
           '## C2. Node identification (data-cost edges, nearest node)', '',
           f"Each landing state identifies with its nearest node under the symmetric cost (no theta"
           + (f", capped at ident_max = {ci['ident_max']:.0f} steps" if ci.get('ident_max') is not None else '') + '). '
           + (f"Full sweep: {ci['n_landings']} dataset states, {ci['frac_states_assigned']:.3f} assigned "
              f"(nearest cost over all states median {ci['nearest_cost_all_states']['p50']:.1f}, p90 "
              f"{ci['nearest_cost_all_states']['p90']:.1f}); {ci['n_runs']} runs of median length "
              f"{ci['run_length']['p50']:.0f}, {ci['n_label_switches']} label switches. Entry hop median "
              f"{ci['entry_hop_cost']['p50']:.1f}, exit hop median {ci['exit_hop_cost']['p50']:.1f}. "
              if ci['walk'] == 'sweep' else
              f"{ci['n_landings']} landing states over walk = {ci['walk']}, horizon {ci['horizon']}, "
              f"{ci['frac_landings_without_match']:.2f} without identification. "
              f"Fraction whose nearest node is still their own node, by offset: 1: "
              f"{ci['self_match_rate_by_offset'][1]:.2f}, 5: {ci['self_match_rate_by_offset'][5]:.2f}, "
              f"10: {ci['self_match_rate_by_offset'][10]:.2f}, {ci['horizon']}: "
              f"{ci['self_match_rate_by_offset'][-1]:.2f}. ")
           + f"Identification (hop) cost of kept edges "
           f"median {ci['identification_cost']['p50']:.2f}, p90 {ci['identification_cost']['p90']:.2f}, "
           f"max {ci['identification_cost']['max']:.1f}"
           + (f"; entry/exit radius = cap = {ci['radius']:.0f} steps each (no critic cost)" if ci.get('radius') is not None else '')
           + (f"; per-node {ci['radius_q']:.0f}th-percentile radii: exit median {ci['radius_exit_per_node']['p50']:.1f} "
              f"(p10 {ci['radius_exit_per_node']['p10']:.1f}, p90 {ci['radius_exit_per_node']['p90']:.1f}), entry median "
              f"{ci['radius_entry_per_node']['p50']:.1f} (p10 {ci['radius_entry_per_node']['p10']:.1f}, p90 "
              f"{ci['radius_entry_per_node']['p90']:.1f})" if ci.get('radius_q') is not None else '')
           + (f"; hop XY distance median {ci['ident_xy_dist']['p50']:.2f}, p90 {ci['ident_xy_dist']['p90']:.2f}, "
              f"{ci['ident_xy_gt_4_frac']:.3f} beyond 4 units" if ci.get('ident_xy_dist') else '')
           + f". Uncapped out-degree median {ci['out_degree_uncapped']['p50']:.0f} (max "
           f"{ci['out_degree_uncapped']['max']:.0f}), cap {ci['k_cap']}; {ci['nodes_without_out_edge']} "
           f"nodes without an outgoing edge, {ci['nodes_without_in_edge']} without an incoming edge; "
           f"{ci['frac_edges_delta0']:.2f} of edges have offset 0; stitch cost = {ci['stitch_cost']}"
           + (f" (added median {ci['stitch_cost_added']['p50']:.2f}, p90 {ci['stitch_cost_added']['p90']:.2f})"
              if ci['stitch_cost_added'] else '') + '.' + flags(ci), ''] if ci and ci.get('identify') == 'nearest' else []) + ([
           '## C2. Node identification (data-cost edges)', '',
           f"theta = {ci['theta']:.2f} steps chosen so that {ci['merge_tpr']:.0%} of held-out pairs "
           f"1-{ci['merge_delta']} steps apart pass. Pass rate by offset: 0: "
           f"{ci['pass_rate_by_offset'][0]:.2f}, 5: {ci['pass_rate_by_offset'][5]:.2f}, 10: "
           f"{ci['pass_rate_by_offset'][10]:.2f}, {ci['horizon']}: {ci['pass_rate_by_offset'][-1]:.2f}; "
           f"random cross-trajectory pairs {ci['cross_traj_pass_rate']:.4f}. {ci['n_landings']} landing "
           f"states, {ci['frac_landings_without_match']:.2f} without any match, mean "
           f"{ci['matches_per_landing']['mean']:.1f} matches each. Uncapped out-degree median "
           f"{ci['out_degree_uncapped']['p50']:.0f} (max {ci['out_degree_uncapped']['max']:.0f}), cap "
           f"{ci['k_cap']}, walk = {ci['walk']}; {ci['nodes_without_out_edge']} nodes without an outgoing "
           f"edge, {ci['nodes_without_in_edge']} without an incoming edge; "
           f"{ci['frac_edges_delta0']:.2f} of edges have offset 0. Identification cost of kept edges "
           f"median {ci['identification_cost']['p50']:.2f}; stitch cost = {ci['stitch_cost']}"
           + (f" (added median {ci['stitch_cost_added']['p50']:.2f}, p90 {ci['stitch_cost_added']['p90']:.2f})"
              if ci['stitch_cost_added'] else '') + '.'
           + (f" Passing cross-trajectory pairs: XY distance median {ci['cross_pass_xy_dist']['p50']:.2f}, "
              f"{ci['cross_pass_frac_xy_gt_4']:.3f} beyond 4 units; pairs within 2 units pass at "
              f"{ci['cross_pairs_within_2_units_pass_rate']:.2f}." if ci.get('cross_pass_xy_dist') else '')
           + flags(ci), ''] if ci and ci.get('identify') != 'nearest' else []) + [
           '## D. Edges', '',
           f"{d['n_edges']} edges. Cost p50 {d['cost']['p50']:.1f}, p90 {d['cost']['p90']:.1f}, "
           f"p99 {d['cost']['p99']:.1f}, max {d['cost']['max']:.1f}. Out-degree "
           f"{d['out_degree']['min']}/{d['out_degree']['mean']:.1f}/{d['out_degree']['max']} "
           f"(min/mean/max), in-degree {d['in_degree']['min']}/{d['in_degree']['mean']:.1f}/"
           f"{d['in_degree']['max']}. Same-trajectory edges {d['same_traj_fraction']:.3f}"
           + (f", of which forward {d['same_traj_forward_fraction']:.3f}; forward cost / true "
              f"Delta median {d['same_traj_forward_cost_over_delta']['p50']:.2f}; "
              f"{d['same_traj_cheap_forward_edges']} with cost < 0.5 Delta."
              if d['same_traj_forward_fraction'] is not None else '.')
           + (f" Maze shortcut edges (cross walls): {d['maze_shortcuts']['n_shortcut_edges']} "
              f"({d['maze_shortcuts']['shortcut_fraction']:.4f}), "
              f"{d['maze_shortcuts']['shortcut_cheaper_than_delta_rel']} of them cheaper than Delta_rel."
              if 'maze_shortcuts' in d else '')
           + (f" Identification hops crossing walls: {d['identification_hop_shortcuts']['n_shortcut_edges']} "
              f"({d['identification_hop_shortcuts']['shortcut_fraction']:.4f})"
              + (f", hop cost median {d['identification_hop_shortcuts']['shortcut_cost']['p50']:.1f}"
                 if d['identification_hop_shortcuts']['shortcut_cost'] else '') + '.'
              if 'identification_hop_shortcuts' in d else '') + flags(d), '',
           '## E. Connectivity', '',
           f"{e['n_scc']} strongly connected components, largest {e['largest_scc_fraction']:.3f} "
           f"of N; {e['n_wcc']} weakly connected component(s)." + flags(e), '',
           '## F. Paths', '',
           f"Held-out same-trajectory queries ({ho['n']}, Delta in {ho['delta_range']}): success "
           f"{ho['success_rate']:.3f}"
           + (f", path cost / Delta median {ho['cost_over_delta']['p50']:.2f} (p10 "
              f"{ho['cost_over_delta']['p10']:.2f}, p90 {ho['cost_over_delta']['p90']:.2f}), hops "
              f"median {ho['hops']['p50']:.0f}, max edge cost on path median "
              f"{ho['max_edge_cost_on_path']['p50']:.1f}" if ho['cost_over_delta'] else '')
           + f"; {ho['n_wormhole_suspects']} wormhole suspects (ratio < 0.3)"
           + (f". Against the maze lower bound (speed {ho['lower_bound']['speed_units_per_step']:.2f} units/step): "
              f"path cost / LB median {ho['lower_bound']['cost_over_lb']['p50']:.2f} (p10 "
              f"{ho['lower_bound']['cost_over_lb']['p10']:.2f}), data Delta / LB median "
              f"{ho['lower_bound']['delta_over_lb']['p50']:.2f}, {ho['lower_bound']['n_below_lb']} paths below LB"
              if ho.get('lower_bound') and ho['lower_bound']['cost_over_lb'] else '')
           + ". Query connection: "
           f"{f.get('query_connect', 'cheapest')}"
           + (f", {f['n_query_fallback']} queries fell back to the k cheapest critic edges"
              if f.get('query_connect') == 'mutual' else '')
           + (f", {f['n_query_far']} queries with a start/goal hop beyond ident_max"
              if f.get('query_connect') == 'nearest' and f.get('n_query_far') is not None else '')
           + '. Random cross-'
           f"trajectory node pairs ({rq['n']}): reachability {rq['reachability']:.3f}"
           + (f", cost median {rq['cost']['p50']:.1f}, forward vs backward Pearson "
              f"{rq['fwd_bwd_pearson']}, median |log(fwd/bwd)| {rq['fwd_over_bwd_abs_log_median']}"
              if rq['cost'] else '')
           + '. Evaluation tasks: ' + '; '.join(
               f"task {t['task_id']} " + (f"cost {t['cost']:.0f}, {t['hops']} hops"
                                          if t['success'] else 'no path') for t in tk['tasks'])
           + '.' + flags(f), '',
           '## G. Sensitivity (N x k)', '',
           '| N | k | edges | largest SCC | edge p99 | neg. frac (edges) | path success | median ratio | shortcut frac |',
           '|---|---|---|---|---|---|---|---|---|']
  for r in sw:
    ratio = '-' if r['median_path_ratio'] is None else f"{r['median_path_ratio']:.2f}"
    sc = '-' if r['shortcut_fraction'] is None else f"{r['shortcut_fraction']:.4f}"
    lines.append(f"| {r['N']} | {r['k']} | {r['n_edges']} | {r['largest_scc_fraction']:.3f} | "
                 f"{r['edge_p99']:.1f} | {r['negative_fraction_edges']:.4f} | "
                 f"{r['path_success']:.3f} | {ratio} | "
                 f"{sc} |")
  with open(os.path.join(out_dir, 'summary.md'), 'w') as fh:
    fh.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
  main(sys.argv[1:])
