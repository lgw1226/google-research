"""Node sampling, cost matrix, edge selection, graph building, and planning."""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra


def sample_nodes(flat, n_nodes, seed):
  rng = np.random.default_rng(seed)
  idx = rng.choice(len(flat), size=n_nodes, replace=False)
  idx.sort()
  return flat.states[idx], flat.traj_id[idx], flat.t[idx], idx


def cost_matrix(Phi, Psi, scale, eps):
  """Returns M, diag_M, C_raw (unclipped, steps), C (clipped, inf diagonal)."""
  M = Phi.astype(np.float64) @ Psi.astype(np.float64).T   # M[i, j] = phi_i . psi_j
  diag_M = np.diag(M).copy()
  C_raw = (diag_M[None, :] - M) / scale                   # cost(i -> j)
  C = np.maximum(C_raw, eps)
  np.fill_diagonal(C, np.inf)
  return M, diag_M, C_raw, C


def select_edges(C, k, tau=None, mode='both'):
  """mode: 'both' = union of k cheapest outgoing (row) and incoming (column)
  edges per node; 'in' = incoming (column-wise) only; 'out' = outgoing only."""
  n = C.shape[0]
  assert k < n and mode in ('both', 'in', 'out')
  rows, cols = [], []
  if mode in ('both', 'out'):
    out_idx = np.argpartition(C, k, axis=1)[:, :k]         # k cheapest outgoing
    rows.append(np.repeat(np.arange(n), k)); cols.append(out_idx.ravel())
  if mode in ('both', 'in'):
    in_idx = np.argpartition(C, k, axis=0)[:k, :]          # k cheapest incoming
    rows.append(in_idx.T.ravel()); cols.append(np.repeat(np.arange(n), k))
  rows, cols = np.concatenate(rows), np.concatenate(cols)
  key = np.unique(rows.astype(np.int64) * n + cols)
  rows, cols = key // n, key % n
  if tau is not None:
    keep = C[rows, cols] <= tau
    rows, cols = rows[keep], cols[keep]
  return rows, cols


def build_graph(rows, cols, weights, n):
  return sp.csr_matrix((weights, (rows, cols)), shape=(n, n))


class Planner:
  """Plans from a query state to a query goal through the node graph."""

  def __init__(self, rows, cols, weights, Phi, Psi, diag_M, scale, k, eps,
               theta=None, connect='cheapest', ident_max=None, query_cost=None):
    self.rows, self.cols, self.weights = rows, cols, weights
    self.n = Phi.shape[0]
    self.Phi, self.Psi, self.diag_M = Phi, Psi, diag_M
    self.scale, self.k, self.eps = scale, k, eps
    self.max_w = float(weights.max()) if len(weights) else 0.0
    self.theta = theta  # if set, connect queries only to nodes passing the mutual test
    self.connect = connect  # 'nearest': single nearest node by symmetric cost, no theta
    self.n_fallback = 0     # mutual mode: queries where nothing passed on either side
    self.ident_max = ident_max
    # if set: cost for start->node j and node i->goal, no direct edge.  Scalar, or a pair of
    # per-node arrays (entry radius for the start side, exit radius for the goal side).
    self.query_cost = query_cost
    self.n_query_far = 0    # nearest mode: queries whose start or goal hop exceeds ident_max
    self.has_out = np.bincount(rows, minlength=self.n) > 0   # eligible start-side nodes
    self.has_in = np.bincount(cols, minlength=self.n) > 0    # eligible goal-side nodes

  def plan(self, p0, q0, pg, qg):
    """p0 = phi(s0), q0 = psi(s0), pg = phi(g), qg = psi(g)."""
    n, k = self.n, self.k
    m_gg = float(pg @ qg)
    c_out = np.maximum((self.diag_M - self.Psi @ p0) / self.scale, self.eps)
    c_in = np.maximum((m_gg - self.Phi @ qg) / self.scale, self.eps)
    c_dir = (m_gg - p0 @ qg) / self.scale
    j = np.argpartition(c_out, k)[:k]
    i = np.argpartition(c_in, k)[:k]
    if self.theta is not None or self.connect == 'nearest':
      m_00 = float(p0 @ q0)
      c_out_rev = np.maximum((m_00 - self.Phi @ q0) / self.scale, self.eps)   # node j -> s0
      c_in_rev = np.maximum((self.diag_M - self.Psi @ pg) / self.scale, self.eps)  # g -> node i
    if self.connect == 'nearest':
      # nearest node (symmetric cost) that has an outgoing / incoming edge
      so = np.where(self.has_out, np.maximum(c_out, c_out_rev), np.inf)
      si = np.where(self.has_in, np.maximum(c_in, c_in_rev), np.inf)
      j = np.array([int(np.argmin(so))])
      i = np.array([int(np.argmin(si))])
      if self.ident_max is not None:
        self.n_query_far += int(so[j[0]] > self.ident_max or si[i[0]] > self.ident_max)
    elif self.theta is not None:
      jm = np.where((c_out <= self.theta) & (c_out_rev <= self.theta))[0]
      im = np.where((c_in <= self.theta) & (c_in_rev <= self.theta))[0]
      self.n_fallback += int(len(jm) == 0 or len(im) == 0)
      j = jm if len(jm) else j          # fall back to the k cheapest if nothing passes
      i = im if len(im) else i
    rows = [self.rows, np.full(len(j), n), i]
    cols = [self.cols, j, np.full(len(i), n + 1)]
    if self.query_cost is not None:
      if np.ndim(self.query_cost) == 0:
        ws = [self.weights, np.full(len(j), float(self.query_cost)), np.full(len(i), float(self.query_cost))]
      else:
        ws = [self.weights, self.query_cost[0][j], self.query_cost[1][i]]
    else:
      ws = [self.weights, c_out[j], c_in[i]]
    if self.query_cost is None and c_dir <= self.max_w:   # direct edge for short queries
      rows.append([n]); cols.append([n + 1]); ws.append([max(c_dir, self.eps)])
    G = sp.csr_matrix((np.concatenate(ws), (np.concatenate(rows),
                                            np.concatenate(cols))),
                      shape=(n + 2, n + 2))
    dist, pred = dijkstra(G, directed=True, indices=n, return_predecessors=True)
    cost = float(dist[n + 1])
    if not np.isfinite(cost):
      return dict(success=False, cost=np.inf, path=[], edge_costs=[])
    path = [n + 1]
    while path[-1] != n:
      path.append(int(pred[path[-1]]))
    path = path[::-1]
    edge_costs = [float(G[a, b]) for a, b in zip(path[:-1], path[1:])]
    return dict(success=True, cost=cost, path=path, edge_costs=edge_costs)
