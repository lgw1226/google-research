import json, os
DS = ['pointmaze-large-navigate-v0', 'pointmaze-large-stitch-v0', 'antmaze-large-navigate-v0', 'antmaze-large-stitch-v0']
ROOTS = [('critic', 'goal_graph_runs/runs_g0.9_d0'), ('theta,unc', 'goal_graph_runs/runs_g0.9_d0_data_both_unc'), ('theta,mq', 'goal_graph_runs/runs_g0.9_d0_data_both_unc_mq'),
         ('near,qc', 'goal_graph_runs/runs_g0.9_d0_data_nearest_qc'), ('near,qn', 'goal_graph_runs/runs_g0.9_d0_data_nearest')]
def load(root, ds):
    p = f'{root}/{ds}/metrics.json'
    return json.load(open(p)) if os.path.exists(p) else None
print('nearest identification stats:')
for ds in DS:
    m = load('goal_graph_runs/runs_g0.9_d0_data_nearest', ds)
    if m is None: print('  ', ds, 'missing'); continue
    ci = m['C_identification']; sr = ci['self_match_rate_by_offset']; hs = m['D_edges'].get('identification_hop_shortcuts', {})
    print(f"  {ds:28s} self@1/3/5/10/30 {sr[1]:.2f}/{sr[3]:.2f}/{sr[5]:.2f}/{sr[10]:.2f}/{sr[30]:.2f} | hop cost p10/50/90/max {ci['identification_cost']['p10']:.1f}/{ci['identification_cost']['p50']:.1f}/{ci['identification_cost']['p90']:.1f}/{ci['identification_cost']['max']:.0f} | hop xy p50/p90/max {ci['ident_xy_dist']['p50']:.2f}/{ci['ident_xy_dist']['p90']:.2f}/{ci['ident_xy_dist']['max']:.1f} >4: {ci['ident_xy_gt_4_count']} | hop wall-cross {hs.get('n_shortcut_edges')} ({hs.get('shortcut_fraction', 0):.4f}) | outdeg p50/max {ci['out_degree_uncapped']['p50']:.0f}/{ci['out_degree_uncapped']['max']:.0f} no-out {ci['nodes_without_out_edge']} no-in {ci['nodes_without_in_edge']} | stitch added p50/p90 {ci['stitch_cost_added']['p50']:.1f}/{ci['stitch_cost_added']['p90']:.1f}")
print()
print(f"{'dataset':28s} {'graph':9s} {'edges':>6s} {'p50':>5s} {'p90':>5s} {'p99':>5s} {'outdeg min/mean/max':>19s} {'indeg max':>9s} {'short':>6s} {'SCC':>5s} {'WCC':>3s} {'succ':>5s} {'ratio p10/50/90':>15s} {'hops':>4s} {'maxE':>5s} {'worm':>4s} {'fb':>3s} tasks")
for ds in DS:
    for name, root in ROOTS:
        m = load(root, ds)
        if m is None: print(f"{ds:28s} {name:9s} missing"); continue
        d, e, f = m['D_edges'], m['E_connectivity'], m['F_paths']
        ho = f['heldout_same_traj']; r = ho['cost_over_delta']; sc = d.get('maze_shortcuts', {})
        tasks = ' '.join(('%.0f' % t['cost']) if t['success'] else 'X' for t in f['eval_tasks']['tasks'])
        fb = f.get('n_query_fallback', '-')
        print(f"{ds:28s} {name:9s} {d['n_edges']:6d} {d['cost']['p50']:5.1f} {d['cost']['p90']:5.1f} {d['cost']['p99']:5.1f} {d['out_degree']['min']:6d}/{d['out_degree']['mean']:5.1f}/{d['out_degree']['max']:<6d} {d['in_degree']['max']:9d} {sc.get('shortcut_fraction', float('nan')):6.4f} {e['largest_scc_fraction']:5.3f} {e['n_wcc']:3d} {ho['success_rate']:5.3f} {r['p10']:4.2f}/{r['p50']:4.2f}/{r['p90']:4.2f} {ho['hops']['p50']:4.0f} {ho['max_edge_cost_on_path']['p50']:5.1f} {ho['n_wormhole_suspects']:4d} {str(fb):>3s} {tasks}")
print()
print('N sweep (edges / largest SCC / path success / median ratio / shortcut frac):')
for ds in DS:
    for name, root in ROOTS:
        m = load(root, ds)
        if m is None: continue
        sw = [r for r in m['G_sweep'] if r['k'] == 10]
        print(f"  {ds:28s} {name:9s} " + '  '.join(f"N{r['N']}: {r['n_edges']}/{r['largest_scc_fraction']:.2f}/{r['path_success']:.2f}/{r['median_path_ratio']:.2f}/{r.get('shortcut_fraction', float('nan')):.4f}" for r in sw))
