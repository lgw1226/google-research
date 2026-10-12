"""Contrastive state/goal encoders trained with a binary NCE loss (JAX/Flax)."""
import csv
import os
import pickle
import time

import flax.linen as nn
import jax
import jax.numpy as jnp
import numpy as np
import optax


class MLP(nn.Module):
  hidden: tuple
  out: int

  @nn.compact
  def __call__(self, x):
    for h in self.hidden:
      x = nn.relu(nn.Dense(h)(x))
    return nn.Dense(self.out)(x)


class Encoders:
  """Separate phi (state) and psi (goal) MLPs with input standardization."""

  def __init__(self, obs_dim, dim=64, hidden=(512, 512), mean=None, std=None):
    self.obs_dim, self.dim, self.hidden = obs_dim, dim, tuple(hidden)
    self.phi_net = MLP(self.hidden, dim)
    self.psi_net = MLP(self.hidden, dim)
    self.mean = np.zeros(obs_dim, np.float32) if mean is None else mean
    self.std = np.ones(obs_dim, np.float32) if std is None else std
    self.params = None

  def init(self, key):
    k1, k2 = jax.random.split(key)
    x = jnp.zeros((1, self.obs_dim))
    self.params = {'phi': self.phi_net.init(k1, x), 'psi': self.psi_net.init(k2, x)}
    return self.params

  def _norm(self, x):
    return (x - self.mean) / self.std

  def phi_apply(self, params, x):
    return self.phi_net.apply(params['phi'], self._norm(x))

  def psi_apply(self, params, x):
    return self.psi_net.apply(params['psi'], self._norm(x))

  def embed(self, x, chunk=65536):
    """Returns (Phi, Psi) as float32 numpy arrays, computed in chunks."""
    phi_fn = jax.jit(lambda p, s: self.phi_apply(p, s))
    psi_fn = jax.jit(lambda p, s: self.psi_apply(p, s))
    phis, psis = [], []
    for a in range(0, len(x), chunk):
      xb = jnp.asarray(x[a:a + chunk])
      phis.append(np.asarray(phi_fn(self.params, xb)))
      psis.append(np.asarray(psi_fn(self.params, xb)))
    return np.concatenate(phis), np.concatenate(psis)

  def save(self, path):
    with open(path, 'wb') as f:
      pickle.dump(dict(obs_dim=self.obs_dim, dim=self.dim, hidden=self.hidden,
                       mean=self.mean, std=self.std,
                       params=jax.device_get(self.params)), f)

  @classmethod
  def load(cls, path):
    with open(path, 'rb') as f:
      d = pickle.load(f)
    enc = cls(d['obs_dim'], d['dim'], d['hidden'], d['mean'], d['std'])
    enc.params = d['params']
    return enc


def critic_loss(enc, params, s, g):
  phi = enc.phi_apply(params, s)                       # (B, d)
  psi = enc.psi_apply(params, g)                       # (B, d)
  logits = phi @ psi.T                                 # (B, B)
  b = logits.shape[0]
  labels = jnp.eye(b)
  loss = optax.sigmoid_binary_cross_entropy(logits, labels).mean()
  diag = jnp.diag(logits)
  acc = jnp.mean(jnp.argmax(logits, axis=1) == jnp.arange(b))
  neg_mean = (logits.sum() - diag.sum()) / (b * (b - 1))
  metrics = dict(loss=loss, acc=acc, pos_logit=diag.mean(), neg_logit=neg_mean)
  return loss, metrics


def make_sampler(enc, states, valid_idx, traj_end, batch_size, gamma, offset_min=0):
  """Samples (s, s_{t+delta}) pairs on device.

  delta = offset_min + Geometric(1 - gamma) on {0, 1, ...}, i.e. with offset_min=0
  P(delta = k) = (1 - gamma) gamma^k for k >= 0 (the pair (s, s) is a positive
  with probability 1 - gamma); with offset_min=1 the support is {1, 2, ...}.
  """
  states = jnp.asarray(states)
  valid_idx = jnp.asarray(valid_idx)
  traj_end = jnp.asarray(traj_end)
  log_gamma = float(np.log(gamma))

  def sample(key):
    k1, k2 = jax.random.split(key)
    i = valid_idx[jax.random.randint(k1, (batch_size,), 0, len(valid_idx))]
    u = jax.random.uniform(k2, (batch_size,), minval=1e-12, maxval=1.0)
    delta = offset_min + jnp.floor(jnp.log(u) / log_gamma).astype(jnp.int32)
    end = traj_end[i]
    clipped = (i + delta) > end
    j = jnp.minimum(i + delta, end)                   # 'clip' episode-end handling
    return states[i], states[j], clipped.mean()
  del enc
  return sample


def train(enc, train_flat, heldout_flat, cfg, out_dir, log):
  """Trains phi/psi. Returns (log rows, final held-out metrics)."""
  gamma, B = cfg['gamma'], cfg['batch_size']
  key = jax.random.PRNGKey(cfg['seed'])
  key, k_init, k_ho = jax.random.split(key, 3)
  enc.init(k_init)
  tx = optax.adam(cfg['lr'])
  opt_state = tx.init(enc.params)

  sample_train = make_sampler(enc, train_flat.states, train_flat.valid_idx,
                              train_flat.traj_end, B, gamma, cfg['offset_min'])
  sample_ho = make_sampler(enc, heldout_flat.states, heldout_flat.valid_idx,
                           heldout_flat.traj_end, B, gamma, cfg['offset_min'])
  # Fixed held-out batches.
  ho_keys = jax.random.split(k_ho, cfg['heldout_batches'])
  ho_s, ho_g, _ = jax.vmap(sample_ho)(ho_keys)

  n_inner = cfg['inner_steps']

  @jax.jit
  def train_chunk(params, opt_state, key):
    def step(carry, k):
      params, opt_state = carry
      s, g, clipped = sample_train(k)
      (loss, m), grads = jax.value_and_grad(critic_loss, argnums=1,
                                            has_aux=True)(enc, params, s, g)
      updates, opt_state = tx.update(grads, opt_state, params)
      params = optax.apply_updates(params, updates)
      m['clipped_frac'] = clipped
      return (params, opt_state), m
    (params, opt_state), ms = jax.lax.scan(step, (params, opt_state),
                                           jax.random.split(key, n_inner))
    return params, opt_state, jax.tree_util.tree_map(jnp.mean, ms)

  @jax.jit
  def eval_heldout(params):
    _, ms = jax.vmap(lambda s, g: critic_loss(enc, params, s, g))(ho_s, ho_g)
    return jax.tree_util.tree_map(jnp.mean, ms)

  rows = []
  best_acc, best_step, step = -1.0, 0, 0
  patience_left = cfg['patience']
  t0 = time.time()
  params, train_m = enc.params, None
  while step < cfg['steps']:
    key, k = jax.random.split(key)
    params, opt_state, train_m = train_chunk(params, opt_state, k)
    step += n_inner
    if step % cfg['eval_every'] == 0 or step >= cfg['steps']:
      ho = eval_heldout(params)
      train_m, ho = jax.device_get((train_m, ho))
      row = dict(step=step, time=time.time() - t0,
                 **{f'train_{k}': float(v) for k, v in train_m.items()},
                 **{f'heldout_{k}': float(v) for k, v in ho.items()})
      rows.append(row)
      log(f"step {step:7d} | train loss {row['train_loss']:.4f} acc "
          f"{row['train_acc']:.3f} | heldout loss {row['heldout_loss']:.4f} "
          f"acc {row['heldout_acc']:.3f} | pos {row['heldout_pos_logit']:.2f} "
          f"neg {row['heldout_neg_logit']:.2f} | clipped "
          f"{row['train_clipped_frac']:.3f} | {row['time']:.0f}s")
      if row['heldout_acc'] > best_acc + cfg['min_delta']:
        best_acc, best_step, patience_left = row['heldout_acc'], step, cfg['patience']
      else:
        patience_left -= 1
      if patience_left <= 0 and step >= cfg['min_steps']:
        log(f'early stop at {step}: held-out acc plateaued '
            f'(best {best_acc:.3f} at step {best_step})')
        break
  enc.params = params
  enc.save(os.path.join(out_dir, 'encoders.pkl'))
  with open(os.path.join(out_dir, 'train_log.csv'), 'w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
  return rows, rows[-1]
