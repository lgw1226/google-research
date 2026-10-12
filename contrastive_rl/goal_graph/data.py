"""Dataset loading and trajectory bookkeeping for OGBench datasets."""
import numpy as np


def load(dataset_name):
  import ogbench  # pylint: disable=g-import-not-at-top
  env, train_ds, val_ds = ogbench.make_env_and_datasets(
      dataset_name, compact_dataset=False)
  return env, train_ds, val_ds


def to_trajectories(ds):
  """Split a flat OGBench dataset into trajectories (each of length T+1)."""
  ends = np.where(ds['terminals'] == 1)[0]
  starts = np.concatenate([[0], ends[:-1] + 1])
  return [np.concatenate([ds['observations'][a:b + 1],
                          ds['next_observations'][b:b + 1]])
          for a, b in zip(starts, ends)]


class FlatTrajs:
  """Trajectories stored as one flat state array with (traj_id, t) metadata."""

  def __init__(self, trajs):
    self.n_traj = len(trajs)
    self.states = np.concatenate(trajs).astype(np.float32)
    self.lens = np.array([len(t) for t in trajs])          # T + 1 states
    self.traj_id = np.repeat(np.arange(self.n_traj), self.lens)
    self.t = np.concatenate([np.arange(l) for l in self.lens])
    self.starts = np.concatenate([[0], np.cumsum(self.lens)[:-1]])
    self.ends = self.starts + self.lens - 1               # flat index of s_T
    self.traj_end = self.ends[self.traj_id]               # per flat index
    # Flat indices with at least one future step (t < T); uniform sampling over
    # these equals picking a trajectory proportional to its length then t < T.
    self.valid_idx = np.where(np.arange(len(self.states)) < self.traj_end)[0]

  @property
  def max_T(self):
    return int(self.lens.max() - 1)

  def __len__(self):
    return len(self.states)
