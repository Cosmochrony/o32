# O32 version-1.5 code — historical analysis, interpretation invalidated

**Status.** The files in this directory reproduce the analysis of O32 version 1.5. That version presented an
inter-triplet variance ratio, the slope relation δ_tri ≈ 3δ_c and the rank of a 3×3 covariance as a test of
hypothesis [H-color]. **O32 version 2.0 invalidates that interpretation**: the O12 capacity profile is exactly
invariant under multiplication of the whole character block by any unit of Z/qZ (Theorem 4 of O32 2.0), so
under the campaign sampling law every character has the same law of profiles and no statistic of this campaign
can separate colour triplets from other sets of characters (Corollaries 5–6).

Consequently, none of the outputs below tests, confirms or supports [H-color]. In particular the following
strings printed by these scripts are **withdrawn readings**, kept only so that historical outputs can be
reproduced byte for byte:

- `[H-color] PASSES` / `FAILS` and the criterion `R ≤ 3` (`o32_triplet_pipeline.py`);
- `[H-color]_pointwise confirmed` (`hcolor_sweep.py`) and the framing of `hcolor_exact_check.py` as a test of
  `[H-color]_pointwise`: what these scripts check is the unit-scaling invariance for λ = ω, a special case of
  Theorem 4 with no colour content;
- the “Implied beta* range” tables (`spectral_O12.py`): O6 derives only the inequality β ≤ 1/(α+½), so no
  β* chain is available;
- any attribution of a proof to O31, which is now a withdrawal notice.

Each script prints a one-line status warning on standard error when run; standard output is unchanged.

The reproducible path of version 2.0 is **not** in this directory: it is `../v2/` together with
`../sigma_freq.py` (see `../integration.md`). The version-2.0 scripts import from this directory only the
campaign's sampler (`sample_block`, `find_colour_triplets`, `find_conjugate_pairs`, per-prime tables), its BFS
and generators (`spectral_O12.build_generators`, `bfs_shells`, `compute_block_capacity`) and the stored arrays.
That code is unchanged; only its verdict strings are withdrawn.

## Files

| File | Role in version 1.5 | Runs as shipped? |
|---|---|---|
| `o32_triplet_pipeline.py` | Monte-Carlo campaign (M blocks per character, seed 42, per-character streams `seed + 997·cidx + 7c`) | yes |
| `spectral_O12.py` | O12 capacity, BFS, fitting windows, figures and tables of the O25/O32 pipelines | yes |
| `results_o32.npz` | stored campaign: means truncated to the shortest block profile, all six primes | data |
| `results_o32_controls.npz` | stored controls q = 29, 101: means zero-padded to the longest block profile | data |
| `hcolor_exact_check.py` | exact comparison of matched blocks (c1 scaled alone vs whole block scaled) | yes, via `legacy_shim.py` |
| `hcolor_sweep.py` | the same check over several primes | yes, via `legacy_shim.py` |
| `verify_uomega.py` | vector-by-vector check of the index permutation x ↦ ωx on fingerprints | yes, via `legacy_shim.py` |
| `sweep.sh` | shell loop over `hcolor_exact_check.py` | yes (set `PYTHON` to the interpreter) |
| `legacy_shim.py` | added in 2.0: supplies `bfs_shells_depth_capped` and `compute_block_capacity_freq`, which version 1.5 imported from a “unified” `spectral_O12.py` that was never shipped | — |

## Dependencies and execution

Python ≥ 3.10 with `numpy`, `matplotlib`, `joblib` and (optionally) `tqdm`; see `../requirements.txt`.
Run every script from this directory, e.g.

```
cd code/v1.5-legacy
python o32_triplet_pipeline.py --quick
python hcolor_exact_check.py --q 13 --n0 2 --n1 5 --exhaustive
python verify_uomega.py
PYTHON=python sh sweep.sh
```

`o32_triplet_pipeline.py` writes `results_o32.npz` and a `checkpoints_o32/` directory in the current
directory by default: pass `--out` and `--checkpoint-dir` to avoid overwriting the stored arrays.

## Known discrepancies of version 1.5 (documented in O32 2.0, Section 5)

- Two averaging conventions coexist in the stored arrays (truncated test means, zero-padded control means).
- The three noise floors quoted in version 1.5 (3.81, 1.657, 2.04 × 10⁻³) correspond to three conventions:
  q = 29 and 101 zero-padded; q = 29 and 101 truncated; q = 29 alone with M = 20, truncated.
- The version-1.5 parameter table gives M = 20 and the window [2, 5] at q = 29; the stored control used
  M = 50 and the window [2, 3].
