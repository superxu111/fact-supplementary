"""纯 CPU 秒级。
"""
import json, sys
import numpy as np
from scipy.stats import t as tdist

BASE = '.'
TOST = f'{BASE}/results/threshold-calibration/equivalence-bound-scan.json'
DELTAS = [0.005, 0.01, 0.02, 0.05]


def main():
    old = json.load(open(TOST))
    e6 = json.load(open(f'{BASE}/results/sampling-protocols/ranking-inference.json'))
    ap = {r['point']: r for r in e6['E2']['per_point'] if r['metric'] == 'ap_logon'}
    tcrit = float(tdist.ppf(0.95, 2))

    # 小样本自测：temporal_1
    obs1 = [x['obs_diff'] for x in ap['temporal_1']['per_seed']]
    m1 = float(np.mean(obs1)); h1 = tcrit * np.std(obs1, ddof=1) / np.sqrt(3)
    assert [round(m1 + h1, 5), round(m1 - h1, 5)] == [old['points']['temporal_1']['ci90'][1],
                                                      old['points']['temporal_1']['ci90'][0]], \
        f'小样本自测失败: [{m1 - h1:.5f},{m1 + h1:.5f}]'
    print(f'小样本自测过 temporal_1: CI=[{m1 - h1:.5f},{m1 + h1:.5f}] == 在案')

    points, mism = {}, []
    for p in sorted(ap):
        obs = [x['obs_diff'] for x in ap[p]['per_seed']]
        m = float(np.mean(obs)); h = tcrit * np.std(obs, ddof=1) / np.sqrt(3)
        lo, hi = m - h, m + h
        exc = [d for d in DELTAS if lo > -d]
        if old['points'][p]['obs_per_seed'] != obs or round(m, 5) != old['points'][p]['agg_obs'] \
                or [round(lo, 5), round(hi, 5)] != old['points'][p]['ci90'] \
                or exc != old['points'][p]['excludable_delta']:
            mism.append(p)
        points[p] = {'obs_per_seed': obs, 'agg_obs': round(m, 5), 'ci90': [round(lo, 5), round(hi, 5)],
                     'excludable_delta': exc, 'note': f'90%CI=[{lo:.5f},{hi:.5f}]'}
    assert not mism, f'重放与在案不一致: {mism}'
    n_exc01 = sum(1 for v in points.values() if 0.01 in v['excludable_delta'])
    n_exc005 = sum(1 for v in points.values() if 0.005 in v['excludable_delta'])
    lo_min = min(v['ci90'][0] for v in points.values())
    hi_max = max(v['ci90'][1] for v in points.values())
    assert n_exc01 == 6 and n_exc005 == 1, f'预登记枚举不符: Δ0.01 {n_exc01}/6, Δ0.005 {n_exc005}/6'
    conclusion = (f'扫描结果（registry stage 生产者补录重生成，判据与枚举未变）：6/6 点可排除 Δ=0.01 的 LOGON AP 劣势'
                  f'（起排除作用的是 CI 下界：6 点下界全部 >−0.01，最小下界 {lo_min:.5f}>−0.01；'
                  f'CI 上界为 {min(v["ci90"][1] for v in points.values()):.5f}–{hi_max:.5f}，不承担排除语义）；'
                  f'Δ=0.005 档仅 1/6 可排除（其余点 CI 下界 <−0.005，不能排除 0.5pp 级差异）——n=3 seed 下 '
                  f'LOGON AP 口径：数据可排除「≥1pp 劣势」但排不掉 0.5pp 级差异，等效性主张在 Δ<0.01 档不可判。'
                  f'论文对 AP 口径只写「未检出差异」、不写「非劣/等效」（红线④正向申报；C1 not-detectably-improve '
                  f'措辞与该扫描一致；本扫描为描述性事后分析，边界未预冻结，不构成确证性 TOST）。')
    out = {'exp': 'V-registry round-1：half1 LOGON AP 边界扫描式 TOST 描述（fix item 伴随；红线④正向申报素材）',
           'date': '2026-10-24',
           'producer': 'src/e14_tost_boundary_scan.py（registry stage/review fix：原交付无源，本脚本为补录生产者并注明 '
                       'post_hoc；输入=results/sampling-protocols/ranking-inference.json:E2.per_point[metric=ap_logon] 逐 seed '
                       'obs_diff，重放与原交付逐位一致）',
           'design_post_hoc': old['design_post_hoc'],
           'points': points,
           'superseded_conclusion': {'status': 'SUPERSEDES：原 conclusion 的「各点 90% CI 上界 |·|≤0.0096」为上下界'
                                               '笔误（起排除作用的是 CI 下界；原文保留）',
                                     'text': old['conclusion'], 'review_refs': 'review fix / registry round E14'},
           'conclusion': conclusion,
           'ci_bounds_range': {'ci_lower_min': round(lo_min, 5), 'ci_upper_max': round(hi_max, 5),
                               'note': '上界笔误更正依据（review fix）'}}
    with open(TOST, 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f'E14_DONE 重放逐位一致；Δ=0.01 排除 {n_exc01}/6、Δ=0.005 {n_exc005}/6；'
          f'下界范围 [{lo_min:.5f}, {max(v["ci90"][0] for v in points.values()):.5f}]、上界 {hi_max:.5f}')


if __name__ == '__main__':
    main()
