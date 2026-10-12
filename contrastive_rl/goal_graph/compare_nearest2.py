"""Compare the nearest-identification variants (python goal_graph/compare_nearest2.py)."""
import json, os
import numpy as np
DS = ['pointmaze-large-navigate-v0', 'pointmaze-large-stitch-v0', 'antmaze-large-navigate-v0', 'antmaze-large-stitch-v0']
ROOTS = [('critic', 'goal_graph_runs/runs_g0.9_d0'), ('theta,unc', 'goal_graph_runs/runs_g0.9_d0_data_both_unc'),
         ('near,walk', 'goal_graph_runs/runs_g0.9_d0_data_nearest'), ('walk,i10', 'goal_graph_runs/runs_g0.9_d0_data_near_walk_i10'),
         ('sweep,i10', 'goal_graph_runs/runs_g0.9_d0_data_near_sweep_i10'), ('sweep,i30', 'goal_graph_runs/runs_g0.9_d0_data_near_sweep_i30'),
         ('sweep,pure', 'goal_graph_runs/runs_g0.9_d0_data_sweep_pure'), ('sweep,cap', 'goal_graph_runs/runs_g0.9_d0_data_sweep_cap'),
         ('sweep,q90', 'goal_graph_runs/runs_g0.9_d0_data_sweep_q90')]
def load(root, ds):
    p = f'{root}/{ds}/metrics.json'
    return json.load(open(p)) if os.path.exists(p) else None
def isolated(root, ds):
    g = np.load(f'{root}/{ds}/graph.npz'); n = len(g['S'])
    o = np.bincount(g['rows'], minlength=n); i = np.bincount(g['cols'], minlength=n)
    return int(np.sum((o == 0) & (i == 0))), int(np.sum(o == 0)), int(np.sum(i == 0))
print('identification / dangling nodes:')
for ds in DS:
    for name, root in ROOTS[2:]:
        m = load(root, ds)
        if m is None: print(f"  {ds:28s} {name:9s} missing"); continue
        ci = m['C_identification']; hs = m['D_edges'].get('identification_hop_shortcuts', {}); iso = isolated(root, ds)
        rq = ci.get('radius_exit_per_node')
        extra = (f"radii exit p10/50/90 {rq['p10']:.1f}/{rq['p50']:.1f}/{rq['p90']:.1f} entry {ci['radius_entry_per_node']['p10']:.1f}/{ci['radius_entry_per_node']['p50']:.1f}/{ci['radius_entry_per_node']['p90']:.1f} | " if rq else '') + (f"assigned {ci['frac_states_assigned']:.3f} nearest-all p50/p90 {ci['nearest_cost_all_states']['p50']:.1f}/{ci['nearest_cost_all_states']['p90']:.1f} runs {ci['n_runs']} switches {ci['n_label_switches']}"
                 if ci['walk'] == 'sweep' else f"no-ident landings {ci['frac_landings_without_match']:.2f}")
        print(f"  {ds:28s} {name:9s} isolated/no-out/no-in {iso[0]}/{iso[1]}/{iso[2]} | hop cost p50/p90/max {ci['identification_cost']['p50']:.1f}/{ci['identification_cost']['p90']:.1f}/{ci['identification_cost']['max']:.0f} | hop xy p90/max {ci['ident_xy_dist']['p90']:.2f}/{ci['ident_xy_dist']['max']:.1f} | hop wall-cross {hs.get('n_shortcut_edges')} | stitch added p50 {(ci['stitch_cost_added'] or {}).get('p50', 0):.1f} | offset p50/p90/max {ci['edge_offset']['p50']:.0f}/{ci['edge_offset']['p90']:.0f}/{ci['edge_offset']['max']:.0f} | {extra}")
print()
print(f"{'dataset':28s} {'graph':10s} {'edges':>6s} {'p50':>5s} {'p90':>5s} {'p99':>6s} {'outdeg mean/max':>15s} {'SCC':>5s} {'WCC':>4s} {'succ':>5s} {'ratio p10/50/90':>15s} {'hops':>4s} {'maxE':>5s} {'worm':>4s} {'far':>4s} tasks")
for ds in DS:
    for name, root in ROOTS:
        m = load(root, ds)
        if m is None: print(f"{ds:28s} {name:9s} missing"); continue
        d, e, f = m['D_edges'], m['E_connectivity'], m['F_paths']
        ho = f['heldout_same_traj']; r = ho['cost_over_delta']
        tasks = ' '.join(('%.0f' % t['cost']) if t['success'] else 'X' for t in f['eval_tasks']['tasks'])
        far = f.get('n_query_far', '-')
        print(f"{ds:28s} {name:10s} {d['n_edges']:6d} {d['cost']['p50']:5.1f} {d['cost']['p90']:5.1f} {d['cost']['p99']:6.1f} {d['out_degree']['mean']:8.1f}/{d['out_degree']['max']:<6d} {e['largest_scc_fraction']:5.3f} {e['n_wcc']:4d} {ho['success_rate']:5.3f} {r['p10']:4.2f}/{r['p50']:4.2f}/{r['p90']:4.2f} {ho['hops']['p50']:4.0f} {ho['max_edge_cost_on_path']['p50']:5.1f} {ho['n_wormhole_suspects']:4d} {str(far):>4s} {tasks}")
print()
print('against the maze lower bound (held-out queries): path cost / LB p10/p50/p90, data Delta / LB p50, paths below LB (certain underestimates):')
for ds in DS:
    for name, root in ROOTS:
        m = load(root, ds)
        if m is None: continue
        lb = m['F_paths']['heldout_same_traj'].get('lower_bound')
        if not lb or not lb['cost_over_lb']: continue
        c = lb['cost_over_lb']
        print(f"  {ds:28s} {name:10s} cost/LB {c['p10']:.2f}/{c['p50']:.2f}/{c['p90']:.2f} | Delta/LB {lb['delta_over_lb']['p50']:.2f} | below LB {lb['n_below_lb']} ({lb['frac_below_lb']:.3f}) | speed {lb['speed_units_per_step']:.2f}")
print()
print('N sweep (edges / largest SCC / path success / median ratio):')
for ds in DS:
    for name, root in ROOTS:
        m = load(root, ds)
        if m is None: continue
        sw = [r for r in m['G_sweep'] if r['k'] == 10]
        print(f"  {ds:28s} {name:9s} " + '  '.join(f"N{r['N']}: {r['n_edges']}/{r['largest_scc_fraction']:.2f}/{r['path_success']:.2f}/{r['median_path_ratio']:.2f}" for r in sw))
