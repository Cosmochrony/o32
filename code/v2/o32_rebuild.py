"""O32 2.0 calibration rebuild (reads the O32 code, writes only to --out).

1. Reproduces each character's M-block mean profile with the O32 per-character seeds
   (base_seed + cidx*997 + c*7, characters = list(set(groups))) using the exact
   frequency-counting sigma, and compares it with code/results_o32*.npz.
2. Keeps per-block profiles and cumulative ranks, and defines the usable shells of a
   group as the shells n >= 1 at which no block of any member has reached rank q
   (so no shell is truncated by saturation or zero-padded).
3. On usable shells only, computes the normalised inter-group variance ratio
   vr(n) = Var_i(mean sigma_ci(n)) / <mean sigma_ci(n)^2>, with an unbiased (ddof=1)
   variance so groups of 2 and 3 are comparable, for: colour triplets (test primes),
   conjugate pairs (all primes), and arbitrary triples (all primes, null).
"""
import sys, json, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--code", required=True)
ap.add_argument("--primes", type=int, nargs="+", default=[29, 61, 101, 151, 211, 307])
ap.add_argument("--M", type=int, default=50)
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--n-null", type=int, default=12)
ap.add_argument("--null-seed", type=int, default=20261119)
ap.add_argument("--out", required=True)
a = ap.parse_args()
sys.path.insert(0, a.code)
import spectral_O12 as S
from sigma_freq import compute_block_capacity_freq as freq
import o32_triplet_pipeline as P

def char_blocks(c, q, shells, gens, n_max, M, base_seed, cidx):
    rng = np.random.default_rng(base_seed + cidx * 997 + c * 7)
    prof, rank = [], []
    for _ in range(M):
        sv, dr, sz, _ = freq(shells, P.sample_block(c, q, rng), q, gens, n_max=n_max)
        prof.append(sv); rank.append(np.cumsum(dr))
    return prof, rank

def pad(xs, L, v=0.0):
    return np.stack([np.concatenate([x, np.full(L - len(x), v)]) for x in xs])

def usable_shells(members, data, q, L):
    ok = np.ones(L, bool); ok[0] = False
    for c in members:
        R = pad(data[c][1], L, q)          # after a profile ends the rank is q
        ok &= np.all(R < q, axis=0)
    return np.nonzero(ok)[0]

def vr_on(members, means, idx):
    if len(idx) == 0:
        return None
    stk = np.stack([means[c][idx] for c in members])
    return float(np.mean(np.var(stk, 0, ddof=1) / np.mean(stk ** 2, 0)))

old = {}
for f in ("results_o32.npz", "results_o32_controls.npz"):
    try:
        old.update(dict(np.load(f"{a.code}/{f}", allow_pickle=True)))
    except FileNotFoundError:
        pass

report = {}
for q in a.primes:
    nrng = np.random.default_rng(a.null_seed + q)   # per-prime stream: independent of grouping
    omega = P.primitive_cube_root(q)
    is_test = omega is not None
    groups = P.find_colour_triplets(q, omega, 4) if is_test else P.find_conjugate_pairs(q, 4)
    chars = list({c for g in groups for c in g})
    gens = S.build_generators(q)
    shells = S.bfs_shells(None, None, gens, q, P.BFS_FRAC.get(q, 0.05))
    n_max = P.N_MAX_BLK.get(q, 60)
    data = {c: char_blocks(c, q, shells, gens, n_max, a.M, a.seed, i) for i, c in enumerate(chars)}
    # reproduction check against the stored campaign
    mism = []
    for c in chars:
        k = f"q{q}_sm_c{c}"
        if k in old:
            # the stored campaign truncated each character's mean to its shortest block profile
            Lmin = min(len(x) for x in data[c][0])
            m = np.mean([x[:Lmin] for x in data[c][0]], 0)
            o = np.asarray(old[k], float)
            mism.append(float(np.max(np.abs(m - o))) if len(m) == len(o) else float("inf"))
    # extra groups: conjugate pairs and arbitrary triples (fresh seeds; null controls)
    extra_pairs = [] if not is_test else P.find_conjugate_pairs(q, 4)
    nulls = []
    while len(nulls) < a.n_null:
        t = tuple(int(x) for x in nrng.choice(np.arange(1, q), 3, replace=False))
        if is_test and (t[1] * pow(t[0], -1, q)) % q in (omega, omega * omega % q):
            continue
        nulls.append(t)
    need = {c for g in extra_pairs + nulls for c in g} - set(data)
    for j, c in enumerate(sorted(need)):
        data[c] = char_blocks(c, q, shells, gens, n_max, a.M, a.null_seed + q, 10000 + j)
    L = max(len(x) for c in data for x in data[c][0])
    means = {c: pad(data[c][0], L).mean(0) for c in data}

    def summarise(gs):
        out = []
        for g in gs:
            idx = usable_shells(g, data, q, L)
            out.append(dict(group=list(g), usable=[int(i) for i in idx], vr=vr_on(g, means, idx)))
        vals = [o["vr"] for o in out if o["vr"] is not None]
        return dict(groups=out, mean_vr=float(np.mean(vals)) if vals else None, n_valid=len(vals))

    rep = dict(is_test=is_test, omega=omega, n_shells=len(shells),
               stored_profile_max_abs_diff=mism,
               profile_lengths=[min(len(x) for c in chars for x in data[c][0]),
                                max(len(x) for c in chars for x in data[c][0])])
    if is_test:
        rep["colour_triplets"] = summarise(groups)
        rep["conjugate_pairs"] = summarise(extra_pairs)
    else:
        rep["conjugate_pairs"] = summarise(groups)
    rep["arbitrary_triples"] = summarise(nulls)
    report[q] = rep
    def fmt(x): return "n/a" if x is None else f"{x:.2e}"
    line = f"q={q:4d} shells={len(shells):3d} profile len {rep['profile_lengths']} repro max|d|={max(mism) if mism else 'n/a'}"
    for k in ("colour_triplets", "conjugate_pairs", "arbitrary_triples"):
        if k in rep:
            us = [len(g["usable"]) for g in rep[k]["groups"]]
            line += f" | {k}: vr={fmt(rep[k]['mean_vr'])} ({rep[k]['n_valid']} groups, usable shells {min(us)}-{max(us)})"
    print(line, flush=True)
    with open(f"{a.out}.q{q}.json", "w") as f:
        json.dump({q: rep}, f, indent=1, default=lambda o: int(o) if isinstance(o, np.integer) else str(o))

with open(a.out, "w") as f:
    json.dump(report, f, indent=1, default=lambda o: int(o) if isinstance(o, np.integer) else str(o))
