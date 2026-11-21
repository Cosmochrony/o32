# o32

**Limits of a Colour-Triplet Capacity Diagnostic on Heis_3(Z/qZ): Exact Unit-Scaling Invariance of the O12 Profile**

O32 — Spectral Admissibility Sub-programme.

## Status of version 2.0

Version 2.0 **replaces version 1.5 and invalidates its interpretation**. Version 1.5 presented a numerical campaign as a
test of hypothesis $[\mathrm{H\text{-}color}]$ and read it as support for an $\mathrm{SU}(3)$ colour structure. That
claim is withdrawn: the diagnostic cannot test $[\mathrm{H\text{-}color}]$, and this record now proves why.

Earlier versions remain available in the Zenodo version history for traceability.

## Abstract

The O12 three-character capacity profile $\sigma_{\mathbf c}(n)$ on $\mathrm{Heis}_3(\mathbb{Z}/q\mathbb{Z})$ is
exactly invariant under multiplication of the whole block $\mathbf c=(c_1,c_2,c_3)$ by any unit $\lambda$ of
$\mathbb{Z}/q\mathbb{Z}$. Each fingerprint vector is a single Fourier character $e_B$ with
$B=c_1b_1+c_2b_2+c_3b_3$, rank increments count distinct frequencies, and $\lambda$ permutes them.

Under the sampling law of the campaign (auxiliary characters drawn independently and uniformly from the units, rejecting blocks with $c_1+c_2+c_3=0$), the profile attached to a character
$c$ therefore has the same distribution for every $c\neq0$. The expected profiles are equal for all characters,
exactly, with no $O(q^{-1})$ term and no role for cube roots of unity. The inter-triplet variance ratio
$R_{\mathrm{var}}$, the triplet exponent $\delta_{\mathrm{tri}}$ and the covariance $C_{\mathrm{color}}$ thus have
laws that do not depend on which characters are compared: colour triplets, conjugate pairs and arbitrary triples
are indistinguishable, as null controls at $q=61$ and $q=151$ confirm. The relation
$\delta_{\mathrm{tri}}\approx3\delta_c$ is an identity of least-squares fitting.

The stored version-1.5 campaign is reproduced exactly. Its calibration mixed two averaging conventions, and its three
noise floors correspond to three conventions (zero-padded, truncated, and an unstored $M=20$ run); rebuilt on shells unaffected by rank saturation, it gives comparable ratios for all three kinds of
character sets.

## Results

- **Theorem (unit-scaling invariance).** $\sigma_{\lambda\mathbf c}(n)=\sigma_{\mathbf c}(n)$ for every
  $\lambda\in(\mathbb{Z}/q\mathbb{Z})^*$ and every shell $n$. The invariance is already stated in O12's exact rank formula; this
  record proves it from the single-frequency structure and draws its consequence for the campaign observables.
- **Corollary (character-independent law).** Under the campaign's sampling law, $\sigma$ has the same distribution
  for every first character; it replaces version 1.5's Proposition 1.
- **Corollary (non-discrimination).** No statistic of the campaign's mean profiles separates colour triplets from
  any other set of characters.
- **Proposition (slope additivity).** $\delta_{\mathrm{tri}}$ is the sum of the three fitted exponents on a common
  design, by linearity of least squares.
- **Numerics.** Exact reproduction of the stored arrays; null controls; calibration rebuilt on usable shells.

## Withdrawn from version 1.5

- The claim that the campaign tests, confirms or supports $[\mathrm{H\text{-}color}]$, and the "passes" verdict.
- Proposition 1 ($O(q^{-1})$ averaged co-admissibility) and the prediction $R_{\mathrm{var}}\propto q^{-1}$.
- The reading of the pointwise, averaged and effective equalities as levels of $[\mathrm{H\text{-}color}]$, the
  rank level, their attribution to O31 (now a withdrawal notice), and the claim that the $\mathrm{SU}(3)$
  identification is analytically established.
- The additive-structure reading of $\delta_{\mathrm{tri}}\approx3\delta_c$ and the evidential weight of the rank
  of $C_{\mathrm{color}}$.
- The colour-charge, quark, baryon, confinement and projection-tower readings, and the $\beta^*$ transfer chain.
- The noise floors $3.81$, $1.657$ and $2.04\times10^{-3}$ and the ratios $R$ derived from them.

## What survives, and with which hypotheses

- **Exact, per block, no sampling hypothesis:** invariance under multiplication of the whole block by any unit.
  The pointwise equality across a colour orbit, $\sigma_{\mathbf c}=\sigma_{\omega\mathbf c}$, is the special
  case $\lambda=\omega$; it carries no colour content.
- **In law, under the campaign sampling law and independent draws:** equal distributions, hence equal expected
  profiles, for every pair of characters; the fitted exponent has the same law for every character, so any
  common limit is not specific to colour orbits. Individual mean profiles still differ by sampling noise.
- **No discriminating power:** no statistic of these profiles can separate colour triplets from other sets of
  characters.

## Status

$[\mathrm{H\text{-}color}]$ is neither confirmed nor refuted: it is not testable with this observable. A test of a
colour orbit would need an observable that is not invariant under all units.

## Code

- **Version 2.0 (reproducible path):** `code/sigma_freq.py` and `code/v2/` (null controls, rebuild, table), with
  their JSON outputs and logs; usage and dependencies in `code/integration.md`.
- **Version 1.5 (historical):** `code/v1.5-legacy/` (campaign pipeline, `spectral_O12.py`, stored arrays,
  exact-check scripts). These reproduce an analysis whose interpretation version 2.0 invalidates; see the status
  note `code/v1.5-legacy/README.md`.

## DOI

https://doi.org/10.5281/zenodo.20145607

## Compilation

```bash
bash compile.sh
```
