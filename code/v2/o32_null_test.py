"""O32 reconnaissance null test (read-only; imports the O32 code, writes nothing there).

T1  pointwise: sigma(lambda*block) == sigma(block) for arbitrary units lambda (not only omega).
T2  protocol:  R_var for O32 colour triplets vs. arbitrary non-orbit triples, same M, same sampling.
T3  GS check:  frequency-counting sigma == Gram-Schmidt sigma on a few blocks.
"""
import sys, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--code", required=True)
ap.add_argument("--q", type=int, default=61)
ap.add_argument("--bfs-frac", type=float, default=0.99)
ap.add_argument("--n0", type=int, default=2)
ap.add_argument("--n1", type=int, default=8)
ap.add_argument("--M", type=int, default=50)
ap.add_argument("--reps", type=int, default=20)
ap.add_argument("--seed", type=int, default=20261119)
a = ap.parse_args()
sys.path.insert(0, a.code)
import spectral_O12 as S
from sigma_freq import compute_block_capacity_freq as _freq
from o32_triplet_pipeline import primitive_cube_root, find_colour_triplets, sample_block

q = a.q
gens = S.build_generators(q)
shells = S.bfs_shells(None, None, gens, q, a.bfs_frac)
n_max = len(shells) - 1
sig = lambda b: _freq(shells, b, q, gens, n_max=n_max)[0]
rng = np.random.default_rng(a.seed)

# T3
mx = 0.0
for _ in range(3):
    b = sample_block(int(rng.integers(1, q)), q, rng)
    s1 = sig(b); s2 = S.compute_block_capacity(shells, b, q, gens, n_max=n_max)[0]
    L = min(len(s1), len(s2)); mx = max(mx, float(np.max(np.abs(s1[:L] - s2[:L]))))
print(f"q={q} shells={len(shells)}  T3 freq-vs-GS max|diff| over 3 blocks = {mx:.3e}")

# T1
omega = primitive_cube_root(q)
lams = [l for l in range(2, q) if l != omega and (omega is None or l != omega * omega % q)]
mx = 0.0
for _ in range(30):
    b = sample_block(int(rng.integers(1, q)), q, rng)
    lam = int(rng.choice(lams))
    s1, s2 = sig(b), sig((lam * b) % q)
    L = max(len(s1), len(s2))
    s1 = np.pad(s1, (0, L - len(s1))); s2 = np.pad(s2, (0, L - len(s2)))
    mx = max(mx, float(np.max(np.abs(s1 - s2))))
print(f"T1 full-block scaling by 30 random non-cube-root units: max|diff| = {mx:.3e}")

# T2
def mean_profile(c):
    st = [sig(sample_block(c, q, rng)) for _ in range(a.M)]
    L = max(len(s) for s in st)
    return np.stack([np.pad(s, (0, L - len(s))) for s in st]).mean(0)

def rvar(tri):
    s = [mean_profile(c) for c in tri]
    L = min(len(x) for x in s); stk = np.stack([x[:L] for x in s])
    vr = np.var(stk, 0) / np.mean(stk**2, 0)
    return float(np.nanmean(vr[a.n0:min(a.n1 + 1, L)]))

trip = find_colour_triplets(q, omega, 4) if omega else []
null = []
while len(null) < max(4, a.reps):
    t = tuple(int(x) for x in rng.choice(np.arange(1, q), 3, replace=False))
    if omega and (t[1] * pow(t[0], -1, q)) % q in (omega, omega * omega % q):
        continue
    null.append(t)
rt = [rvar(t) for t in trip]
rn = [rvar(t) for t in null[:a.reps]]
print(f"T2 M={a.M} window=[{a.n0},{a.n1}]")
print(f"   colour triplets {trip}: R_var = {['%.2e' % x for x in rt]}  mean {np.mean(rt) if rt else float('nan'):.2e}")
print(f"   {len(rn)} arbitrary triples: R_var mean {np.mean(rn):.2e}  median {np.median(rn):.2e}  "
      f"min {np.min(rn):.2e}  max {np.max(rn):.2e}")
