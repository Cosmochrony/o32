"""Summarise the per-prime rebuild JSON files into the O32 2.0 calibration table (LaTeX rows)."""
import json, glob, sys

def load(pattern):
    out = {}
    for f in sorted(glob.glob(pattern)):
        for q, rep in json.load(open(f)).items():
            out[int(q)] = rep
    return out

def fmt(x):
    """Value in units of 1e-3, as printed in the paper's table."""
    if x is None:
        return '---'
    return '0' if x == 0 else f'{x * 1e3:.2f}'

def cell(block):
    vals = [g['vr'] for g in block['groups'] if g['vr'] is not None]
    if not vals:
        return '---', '---', 0
    return fmt(sum(vals) / len(vals)), f'{fmt(min(vals))}--{fmt(max(vals))}', len(vals)

data = load(sys.argv[1] if len(sys.argv) > 1 else 'rebuild-q*.json')
for q in sorted(data):
    r = data[q]
    us = sorted({len(g['usable']) for k in ('colour_triplets', 'conjugate_pairs', 'arbitrary_triples')
                 if k in r for g in r[k]['groups']})
    row = [str(q), f"{min(us)}--{max(us)}" if us and min(us) != max(us) else (str(us[0]) if us else '0')]
    for k in ('colour_triplets', 'conjugate_pairs', 'arbitrary_triples'):
        if k in r:
            mean, rng, n = cell(r[k])
            row.append(f'{mean} ({rng})' if n > 1 else mean)
        else:
            row.append('---')
    print(' & '.join(row) + r' \\')
