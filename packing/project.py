"""Projections: everything a reader sees is generated from the ledger. Never type a number by hand.

    python -m packing.project   # regenerates JOURNAL.md, campaign REPORT.md files, README.md,
                                # site/data.json and paper/numbers.tex from the ledger
"""
import glob, json, os
from . import analyze

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _load():
    from .ledger import open_ledger
    rt, G = open_ledger()
    campaigns = {o.data['cid']: o.data for o in G.objects('campaign')}
    cells = [o.data for o in G.objects('cell')]
    findings = [o.data for o in G.objects('finding')]
    return campaigns, cells, findings


def _h2h_block(cells, cid):
    cc = [c for c in cells if c['campaign'] == cid]
    methods = sorted({c['method'] for c in cc})
    out = []
    if 'harden' in methods:
        for m in methods:
            if m == 'harden':
                continue
            r = analyze.head_to_head(cc, 'harden', m)
            out.append((m, r))
    return out


def _fmt_L(x):
    return '%.6f' % x if x is not None else '—'


def report(campaigns, cells, cid):
    c = campaigns[cid]
    cc = [x for x in cells if x['campaign'] == cid]
    L = [f'# {cid}: {c.get("title", "")}', '',
         '*Generated from the ledger by `packing/project.py`. Do not edit.*', '',
         f'**Question.** {c.get("question", "")}', '',
         f'**Hypothesis.** {c.get("hypothesis", "")}', '',
         f'**Decision rule.** {c.get("decision_rule", "")}', '',
         f'**Status.** {c.get("status", "planned")}' + (f' — **decision:** {c["decision"]}' if c.get('decision') else ''), '',
         '## Head-to-head (best legalised container size per instance)', '']
    for m, r in _h2h_block(cells, cid):
        L.append(f'- harden vs {m}: **{r["a_wins"]} vs {r["b_wins"]}**, {r["ties"]} ties (two-sided p = {r["p"]:.4g})')
    L.append('')
    L.append('| instance | ' + ' | '.join(sorted({x['method'] for x in cc})) + ' |')
    L.append('|---|---|' + '--|' * (len({x['method'] for x in cc}) - 1))
    insts = sorted({(x['family'], x['n']) for x in cc})
    methods = sorted({x['method'] for x in cc})
    for fam, n in insts:
        row = [f'{fam} n={n}']
        for m in methods:
            hit = [x for x in cc if x['family'] == fam and x['n'] == n and x['method'] == m]
            row.append(_fmt_L(hit[0]['best_L']) + (f' ({hit[0]["runs"]} runs)' if hit else ''))
        L.append('| ' + ' | '.join(row) + ' |')
    L.append('')
    return '\n'.join(L)


def journal(campaigns, cells, findings):
    L = ['# Research journal', '',
         'Every entry below is generated from the ledger. Findings link to the cells that support them.', '']
    for cid in sorted(campaigns):
        c = campaigns[cid]
        L.append(f'## {cid}: {c.get("title", "")}')
        L.append(f'Status: {c.get("status", "planned")}' + (f' — {c["decision"]}' if c.get('decision') else ''))
        for m, r in _h2h_block(cells, cid):
            L.append(f'- harden vs {m}: {r["a_wins"]} vs {r["b_wins"]}, {r["ties"]} ties (p = {r["p"]:.4g})')
        L.append('')
    if findings:
        L.append('## Findings')
        for f in findings:
            ev = (' (evidence: ' + ', '.join(f.get('evidence', [])) + ')') if f.get('evidence') else ''
            L.append(f'- {f["text"]}{ev} [{f.get("campaign", "")} {f.get("date", "")}]')
        L.append('')
    return '\n'.join(L)


def readme(campaigns, cells):
    L = ['# When does hardening help?', '',
         'A follow-up to [soft-to-rigid](https://yoheinakajima.github.io/soft-to-rigid/): can we predict *where*',
         'the soft-to-rigid packing search helps, and *why*? Every number below is generated from the ledger.', '',
         '| campaign | question | status | harden vs rigid |', '|---|---|---|---|']
    for cid in sorted(campaigns):
        c = campaigns[cid]
        h2h = [r for m, r in _h2h_block(cells, cid) if m == 'rigid']
        s = f'{h2h[0]["a_wins"]}–{h2h[0]["b_wins"]} ({h2h[0]["ties"]} ties, p={h2h[0]["p"]:.3g})' if h2h else '—'
        L.append(f'| {cid} | {c.get("question", "")[:80]} | {c.get("status", "")} | {s} |')
    L.append('')
    return '\n'.join(L)


def site_data(campaigns, cells, findings):
    fams = {}
    for fn in glob.glob(os.path.join(ROOT, 'catalog', '*.json')):
        f = json.load(open(fn))
        name = os.path.basename(fn)[:-5]
        fams[name] = {'title': f['title'], 'piece': f['piece'], 'container': f['container'],
                      'has_records': bool(f.get('records'))}
    cells_out = []
    for c in cells:
        rep = os.path.join('campaigns', c['campaign'], 'replays',
                            f"{c['family']}_n{c['n']}_{c['method']}_B{c['budget']}_{c['config']}.json".replace('/', '-'))
        cells_out.append({k: c[k] for k in ('campaign', 'family', 'n', 'method', 'budget', 'config', 'runs', 'best_L', 'ms_mean', 'evals_mean')} | {'replay': rep if os.path.exists(os.path.join(ROOT, rep)) else None})
    return {'families': fams,
            'campaigns': [{'id': cid, **{k: c.get(k) for k in ('title', 'question', 'hypothesis', 'decision_rule', 'status', 'decision')}} for cid, c in sorted(campaigns.items())],
            'cells': cells_out,
            'findings': findings}


def paper_numbers(campaigns, cells):
    L = ['% Generated by packing/project.py. Do not edit.']
    for cid in sorted(campaigns):
        for m, r in _h2h_block(cells, cid):
            tag = cid.replace('-', '').upper() + m.upper().replace('-', '')
            L.append(f'\\newcommand{{\\hvr{tag}}}{{{r["a_wins"]} vs {r["b_wins"]}, {r["ties"]} ties}}')
            L.append(f'\\newcommand{{\\hvp{tag}}}{{{r["p"]:.4g}}}')
    return '\n'.join(L) + '\n'


def main():
    campaigns, cells, findings = _load()
    with open(os.path.join(ROOT, 'JOURNAL.md'), 'w') as f:
        f.write(journal(campaigns, cells, findings))
    with open(os.path.join(ROOT, 'README.md'), 'w') as f:
        f.write(readme(campaigns, cells))
    for cid in campaigns:
        with open(os.path.join(ROOT, 'campaigns', cid, 'REPORT.md'), 'w') as f:
            f.write(report(campaigns, cells, cid))
    os.makedirs(os.path.join(ROOT, 'site'), exist_ok=True)
    with open(os.path.join(ROOT, 'site', 'data.json'), 'w') as f:
        json.dump(site_data(campaigns, cells, findings), f)
    os.makedirs(os.path.join(ROOT, 'paper'), exist_ok=True)
    with open(os.path.join(ROOT, 'paper', 'numbers.tex'), 'w') as f:
        f.write(paper_numbers(campaigns, cells))
    print(f'projected: {len(campaigns)} campaigns, {len(cells)} cells, {len(findings)} findings')


if __name__ == '__main__':
    main()
