"""Plots for the goal-graph diagnostics."""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # pylint: disable=g-import-not-at-top
from matplotlib.collections import LineCollection
import numpy as np


def calibration(cal, path):
  c = np.array(cal['bin_centers'])
  fig, ax = plt.subplots(figsize=(7, 4.5))
  for name, med, iqr, col in [('forward', cal['forward_median'], cal['forward_iqr'], 'C0'),
                              ('backward', cal['backward_median'], cal['backward_iqr'], 'C1')]:
    iqr = np.array(iqr)
    ax.plot(c, med, '-o', ms=3, color=col, label=f'{name} median')
    ax.fill_between(c, iqr[:, 0], iqr[:, 1], color=col, alpha=0.2)
  f = cal['fit']
  ax.plot(c, f['slope'] * c + f['intercept'], 'k--', lw=1,
          label=f"fit slope={f['slope']:.2f} int={f['intercept']:.1f} R2={f['r2']:.2f}")
  ax.plot(c, c, ':', color='gray', lw=1, label='cost = Delta')
  ax.axvline(cal['delta_rel'], color='r', ls='-.', label=f"Delta_rel={cal['delta_rel']:.0f}")
  ax.set_xlabel('Delta (steps)'); ax.set_ylabel('cost (steps)')
  ax.set_title(f"held-out same-trajectory cost vs Delta (rho={cal['forward_spearman']:.2f})")
  ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def edge_costs(weights, delta_rel, path):
  fig, ax = plt.subplots(figsize=(6, 4))
  ax.hist(weights, bins=80, color='C0')
  ax.axvline(delta_rel, color='r', ls='--', label=f'Delta_rel={delta_rel:.0f}')
  ax.set_xlabel('edge cost (steps)'); ax.set_ylabel('count'); ax.set_yscale('log')
  ax.set_title('selected edge costs'); ax.legend()
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def degrees(outdeg, indeg, k, path):
  fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
  for ax, d, name in zip(axes, [outdeg, indeg], ['out-degree', 'in-degree']):
    ax.hist(d, bins=np.arange(d.min(), d.max() + 2) - 0.5, color='C0')
    ax.axvline(k, color='r', ls='--', label=f'k={k}')
    ax.set_xlabel(name); ax.set_ylabel('nodes'); ax.set_yscale('log'); ax.legend()
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def maze_walls(env):
  u = env.unwrapped
  mm = getattr(u, 'maze_map', None)
  if mm is None:
    return []
  unit, ox, oy = u._maze_unit, u._offset_x, u._offset_y  # pylint: disable=protected-access
  return [(j * unit - ox - unit / 2, i * unit - oy - unit / 2, unit)
          for i in range(mm.shape[0]) for j in range(mm.shape[1]) if mm[i, j] == 1]


def node_positions(S, Psi, xy_dims):
  if xy_dims == 'pca':
    X = Psi - Psi.mean(0)
    _, _, vt = np.linalg.svd(X, full_matrices=False)
    return X @ vt[:2].T, 'PCA of psi (projection can make long edges look short)'
  d = [int(x) for x in xy_dims.split(',')]
  return S[:, d], f'state dims {d}'


def overlay(xy, rows, cols, weights, walls, paths, title, path, vmax=None):
  """paths: list of dict(start_xy, goal_xy, node_xy (hops,2), label)."""
  fig, ax = plt.subplots(figsize=(10, 7.5))
  for x, y, u in walls:
    ax.add_patch(plt.Rectangle((x, y), u, u, color='0.85', zorder=0))
  segs = np.stack([xy[rows], xy[cols]], axis=1)
  vmax = vmax or np.percentile(weights, 99)
  lc = LineCollection(segs, cmap='viridis', norm=plt.Normalize(0, vmax),
                      linewidths=0.4, alpha=0.5, zorder=1)
  lc.set_array(weights)
  ax.add_collection(lc)
  ax.scatter(xy[:, 0], xy[:, 1], s=2, c='k', zorder=2)
  fig.colorbar(lc, ax=ax, label='edge cost (steps)')
  for n, p in enumerate(paths):
    col = f'C{n % 10}'
    if p['node_xy'] is not None:
      pts = np.concatenate([p['start_xy'][None], p['node_xy'], p['goal_xy'][None]])
      ax.plot(pts[:, 0], pts[:, 1], '-', color=col, lw=2, zorder=3, label=p['label'])
    ax.plot(*p['start_xy'], marker='o', color=col, ms=9, mec='k', zorder=4)
    ax.plot(*p['goal_xy'], marker='*', color=col, ms=14, mec='k', zorder=4)
  ax.set_title(title); ax.set_aspect('equal'); ax.autoscale()
  ax.legend(fontsize=8, loc='upper left', bbox_to_anchor=(1.18, 1))
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def path_ratio(ratio, path):
  r = ratio[np.isfinite(ratio)]
  fig, ax = plt.subplots(figsize=(6, 4))
  ax.hist(r, bins=60, color='C0')
  ax.axvline(1.0, color='k', ls=':'); ax.axvline(0.3, color='r', ls='--', label='0.3 (wormhole)')
  ax.set_xlabel('path cost / true Delta'); ax.set_ylabel('queries')
  ax.set_title('held-out same-trajectory queries'); ax.legend()
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def training(rows, path):
  s = [r['step'] for r in rows]
  fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
  for key, ax in zip(['loss', 'acc'], axes):
    ax.plot(s, [r[f'train_{key}'] for r in rows], label='train')
    ax.plot(s, [r[f'heldout_{key}'] for r in rows], label='held-out')
    ax.set_xlabel('step'); ax.set_ylabel(key); ax.legend()
  axes[1].set_ylim(0, 1); axes[1].set_title('top-1 accuracy (chance = 1/B)')
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def wormhole_triage(raw, S, xy, heldout_flat, xy_dims, walls, out_dir):
  """Save endpoint states of every edge on each wormhole-suspect path."""
  os.makedirs(out_dir, exist_ok=True)
  n = len(S)
  summary = []
  for qi in np.where(raw['ratio'] < 0.3)[0]:
    r = raw['results'][qi]
    s0 = heldout_flat.states[raw['i'][qi]]
    g = heldout_flat.states[raw['j'][qi]]
    aug = np.concatenate([S, s0[None], g[None]])
    p = np.array(r['path'])
    ec = np.array(r['edge_costs'])
    order = np.argsort(ec)
    np.savez(os.path.join(out_dir, f'query_{qi:03d}.npz'),
             start=s0, goal=g, delta=raw['delta'][qi], path_cost=r['cost'],
             path_nodes=p, edge_costs=ec[order],
             edge_from=aug[p[:-1]][order], edge_to=aug[p[1:]][order])
    summary.append(dict(query=int(qi), delta=int(raw['delta'][qi]),
                        path_cost=float(r['cost']), hops=int(len(p) - 1),
                        cheapest_edge_cost=float(ec.min()),
                        cheapest_edge=[int(p[order[0]]), int(p[order[0] + 1])]))
    if xy_dims != 'pca':
      d = [int(x) for x in xy_dims.split(',')]
      pts = aug[p][:, d]
      fig, ax = plt.subplots(figsize=(8, 6))
      for x, y, u in walls:
        ax.add_patch(plt.Rectangle((x, y), u, u, color='0.85', zorder=0))
      ax.scatter(xy[:, 0], xy[:, 1], s=1, c='0.6', zorder=1)
      lc = LineCollection(np.stack([pts[:-1], pts[1:]], 1), cmap='viridis',
                          linewidths=2, zorder=2)
      lc.set_array(ec); ax.add_collection(lc); fig.colorbar(lc, label='edge cost')
      for a, b, c in zip(pts[:-1], pts[1:], ec):
        ax.annotate(f'{c:.1f}', (a + b) / 2, fontsize=6)
      ax.plot(*pts[0], 'o', color='C3', ms=9, mec='k'); ax.plot(*pts[-1], '*', color='C3', ms=14, mec='k')
      ax.set_aspect('equal'); ax.autoscale()
      ax.set_title(f'query {qi}: Delta={raw["delta"][qi]} path cost={r["cost"]:.1f} '
                   f'(ratio {r["cost"] / raw["delta"][qi]:.2f})')
      fig.tight_layout(); fig.savefig(os.path.join(out_dir, f'query_{qi:03d}.png'), dpi=120)
      plt.close(fig)
  del n
  return summary


def identification(ident, path):
  if ident.get('identify') == 'nearest':
    return identification_nearest(ident, path)
  pr = ident['pass_rate_by_offset']
  fig, ax = plt.subplots(figsize=(6, 4))
  ax.plot(range(len(pr)), [np.nan if x is None else x for x in pr], '-o', ms=3)
  ax.axhline(ident['cross_traj_pass_rate'], color='r', ls='--',
             label=f"cross-trajectory pairs ({ident['cross_traj_pass_rate']:.4f})")
  ax.axvline(ident['merge_delta'], color='k', ls=':', label=f"merge_delta={ident['merge_delta']}")
  ax.set_xlabel('true offset (steps, held-out same trajectory)')
  ax.set_ylabel('fraction passing mutual test'); ax.set_ylim(0, 1.02)
  ax.set_title(f"identification test, theta={ident['theta']:.2f} steps"); ax.legend()
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def identification_nearest(ident, path):
  sr = ident['self_match_rate_by_offset']
  fig, ax = plt.subplots(figsize=(6, 4))
  if sr is not None:
    ax.plot(range(len(sr)), [np.nan if x is None else x for x in sr], '-o', ms=3)
    ax.set_xlabel('offset of landing from its own node (steps)')
    ax.set_ylabel('fraction whose nearest node is its own'); ax.set_ylim(0, 1.02)
  else:
    h = ident['nearest_cost_hist']; e = np.array(h['edges'])
    ax.bar(e[:-1], h['counts'], width=np.diff(e), align='edge')
    ax.set_xlabel('symmetric cost to nearest node, all dataset states (steps, clipped at 100)')
    ax.set_ylabel('states')
  if ident.get('ident_max') is not None:
    ax.axvline(ident['ident_max'], color='r', ls='--', label=f"ident_max={ident['ident_max']}")
    ax.legend()
  ic = ident['identification_cost']
  ax.set_title(f"nearest-node identification; hop cost p50 {ic['p50']:.1f}, p90 {ic['p90']:.1f}")
  fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
