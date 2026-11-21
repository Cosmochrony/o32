# O32 code: reproducible path of version 2.0

The code of this record is split in two parts.

- **Version-2.0 reproducible path**: `sigma_freq.py` and `v2/`. These scripts produce every number of the
  O32 2.0 paper (Sections 4–5).
- **Historical version-1.5 code**: `v1.5-legacy/`. It reproduces the version-1.5 campaign, whose
  interpretation is invalidated by version 2.0. Its own `README.md` gives its status, the withdrawn verdict
  strings, its dependencies and how to run it. The version-2.0 scripts import from it only the campaign's
  sampler, BFS, generators and stored arrays, all unchanged.

Dependencies: Python ≥ 3.10, `numpy`, `matplotlib`, `joblib` (imported by the campaign module), optionally
`tqdm`; see `requirements.txt`. Matplotlib needs a writable cache: set `MPLCONFIGDIR` if the default is not
writable.

## 1. What the code computes

`sigma_freq.compute_block_capacity_freq` computes the O12 capacity profile
σ(n) = Δr_n / |S_n| by counting distinct frequencies, which is exact by Lemmas 1–2 of the paper (each
fingerprint is a single Fourier character, and the rank of a family of fingerprints is the number of distinct
frequencies it contains). Check (E1) compares it with the Gram–Schmidt profile of the campaign module.

The invariance under multiplication of the whole block by any unit (Theorem 4) and the character-independent
law under the campaign sampling law (Corollary 5) are proved in the paper; the scripts check them and their
consequences numerically, they do not establish them.

## 2. Scripts (`v2/`)

Run from `code/v2/`; `--code` defaults to the parent directory.

- `o32_null_test.py --q 61` and `o32_null_test.py --q 151 --bfs-frac 0.29 --n0 3 --n1 13`:
  - T3 (paper E1): frequency-counting σ against Gram–Schmidt σ on three random blocks (comparison over the
    common length of the two profiles);
  - T1 (paper E2): σ(λ·block) = σ(block) for thirty (block, λ) pairs with λ ≠ 1 a random unit that is not a
    cube root of unity (cube roots are excluded only to show that the invariance is not specific to them);
  - T2 (paper E3): window-averaged R_var for the four version-1.5 colour triplets against twenty arbitrary
    triples. This protocol is modelled on the campaign, not identical to it: means are zero-padded, R_var is
    averaged over the full window [n0, n1], all characters share one random stream, and the BFS runs to all
    shells.

  Outputs: `null-test-q61.log`, `null-test-q151.log`.
- `o32_rebuild.py --primes 29 61 101 151 211 307 --out rebuild.json`:
  1. reproduces each character's mean profile with the campaign's per-character streams (M = 50, seed 42,
     stream seed `42 + 997·cidx + 7c`) and compares it with the stored arrays: truncated means with
     `v1.5-legacy/results_o32.npz` (all six primes), zero-padded means with
     `v1.5-legacy/results_o32_controls.npz` (q = 29, 101);
  2. computes R_var (unbiased variance) on usable shells only: shells n ≥ 1 at which no block of any member has
     reached rank q and no member's profile has ended (so no increment is cut by saturation and no mean
     contains padding).

  One JSON file per prime is written as `<out>.q<q>.json`; the committed copies are `rebuild-q<q>.json`, and
  the console output is `rebuild.log`. Groups: the four version-1.5 colour triplets (test primes), the four
  smallest conjugate pairs, and twelve arbitrary triples with no cube-root orbit drawn with seed 20261119 + q.
  Characters already in the campaign reuse their campaign streams; only the new characters use fresh streams.
- `o32_rebuild_table.py`: turns the per-prime JSON files into the rows of the paper's rebuilt table.

## 3. Reproduction results

- Stored campaign: maximum difference 0 for every stored mean, under both conventions (truncated at all six
  primes; zero-padded for the controls q = 29, 101).
- The three version-1.5 noise floors are reproduced by the following conventions (computed with the
  version-1.5 summary logic): 3.81 × 10⁻³ = q = 29 and 101, zero-padded means; 1.657 × 10⁻³ = the same two
  primes, truncated means; 2.04 × 10⁻³ = q = 29 alone, M = 20, truncated means (not stored).
- Run times on a laptop: q ≤ 151 a few minutes; q = 211 and 307 several hours (single process).
