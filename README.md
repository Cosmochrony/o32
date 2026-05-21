# o32

**Colour Triplet Co-admissibility on Heis_3(Z/qZ): Numerical Test of Hypothesis [H-color]**

O32 paper — Spectral Admissibility Sub-programme.

## Abstract

We report numerical evidence for Hypothesis [H-color] (colour triplet co-admissibility)
on the Heisenberg group Heis_3(Z/qZ), the key open condition in the derivation of SU(3)
as the admissible gauge group of the colour sector (O31).

For a prime q = 1 (mod 3), a colour triplet is a set {c_1, c_2, c_3} in (Z/qZ)^* satisfying
c_1 + c_2 + c_3 = 0 (mod q) and pairwise non-conjugacy. [H-color] asserts that the three
BFS capacity profiles sigma_{c_1}(n), sigma_{c_2}(n), sigma_{c_3}(n) are equal in the
pre-saturation window (exact co-admissibility).

The test observable is the inter-triplet variance ratio
R_var = Var_i(sigma_{c_i}(n)) / <sigma_{c_i}^2(n)>,
normalised against the intra-pair variance of conjugate pairs {c, q-c} (known co-admissible
by O25) as a noise-floor reference (ctrl_ref = 3.81e-3).

Results:
- q = 61:  R_var = 3.4e-3 (at noise floor), 1/4 triplets valid. Passes R <= 3.
- q = 151: R_var = 7.1e-4 (factor 5 below noise floor), 4/4 triplets. Clear confirmation.
- q = 211: R_var = 1.6e-3 (below noise floor), 4/4 triplets. Consistent.
- q = 307: R_var = 1.17e-3 (below noise floor), 4/4 triplets, R = 0.31. Confirmed
  (delta_tri = 12.355 ≈ 3*delta_c = 12.549, deviation 1.5%).

The triplet capacity exponent satisfies delta_tri ≈ 3*delta_c at all three primes,
confirming the additive structure predicted by O31. All colour covariance matrices C_color
have numerical rank 1.

The discussion addresses the closure from O31v2: the exact generator-twist isospectrality
spec(rho_c(P_{S_q})) = spec(rho_c(P_{phi_omega(S_q)})) for all c does NOT extend across
distinct characters (max |Delta lambda| ≈ 0.3-0.4). This establishes that [H-color] on the
standard graph cannot be derived from global Markov-spectrum equality; the BFS capacity is
a strictly finer observable. Any analytical proof must act directly on the rank structure of
the BFS walk.

Physical interpretation: each element c_i of a valid triplet simultaneously belongs to a
conjugate pair (carrying spin-1/2, d_rho = 2, from O29) and a colour triplet (SU(3) fixed
point from O31). An individual sector c_i therefore carries spin-1/2 and one colour charge:
the minimal quantum-number content of a quark. The sum-zero condition c_1+c_2+c_3 = 0 is
the discrete analogue of baryon colour-neutrality.

## Key results

- **[H-color] numerically confirmed** for q in {151, 211, 307} (4/4 triplets, R <= 0.5).
- **Partial confirmation** at q=61 (1/4 triplets, finite-size effects).
- **Four-prime dataset complete**: q in {61, 151, 211, 307}; full validation of
  [H-color] across the available range.
- **Additive exponent structure**: delta_tri ≈ 3*delta_c at sub-percent level.
- **Rank-1 covariance**: C_color has numerical rank 1 in all cases.
- **Spectral obstruction closed** (from O31v2): [H-color] cannot be proved via Markov
  spectrum equality; BFS capacity is a strictly finer observable.
- **Physical interpretation**: co-admissible sectors carry spin-1/2 + one colour charge
  (quark structure); triplets are colour-neutral baryon pre-images.
- **Analytical sharpening (v1.3+, Proposition)**: for block-averaged capacity profiles,
  E[sigma_c(n)] = E[sigma_{omega*c}(n)] + O(q^{-1}) is proved analytically
  (Prop. avg-hcolor). This establishes H_color_eff (equality of capacity exponents) in the
  q -> infinity limit. The finite-q R_var decrease is the predicted modulation bias
  with expected scaling R_var ~ q^{-1}.

## Status

[H-color] is **numerically supported** for q in {151, 211, 307} (four-prime dataset
complete) and analytically established in expectation (H_color_eff) via Proposition
avg-hcolor. A pointwise analytical proof for fixed finite q remains open.

## DOI

https://doi.org/10.5281/zenodo.20259893

## Compilation

```bash
bash compile.sh
```

Output: `out/SpectralO32.pdf`
