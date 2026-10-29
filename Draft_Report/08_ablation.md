# 8 Ablation

The proposed λ(ω) has two estimated ingredients: the noise level σ̂² (Section 4.1) and the signal-spectrum model A|ω|^(−β) (Section 4.2). To see which one limits performance, we replace each with its true value, one at a time. To check whether the frequency shaping matters at all, we also collapse λ(ω) to a single constant.

| Variant | Noise level | Signal spectrum | λ |
|---|---|---|---|
| **Full** (proposed) | σ̂² from the noise band | power-law fit | σ̂²/(A\|ω\|^(−β)) |
| Oracle σ | true σ_n² | power-law fit (refitted with σ_n²) | σ_n²/(A\|ω\|^(−β)) |
| Oracle S_x | σ̂² | true periodogram of x | σ̂²/S_x(ω) |
| Constant λ | σ̂² | power-law fit | geometric mean of the full λ(ω), one value for all ω |

All variants run on the same 480 degraded test images as Section 7, using the same seeds. The "full" variant must therefore reproduce the proposed method's numbers exactly; notebook 02 `[Ablation Cell C]` checks this.

**Table 8 — PSNR change relative to the full method (dB), mean ± std** (`results/tables/table8_ablation.csv`, `figures/fig7_ablation.png`):

| σ_h | Oracle σ | Oracle S_x | Constant λ |
|---|---|---|---|
| 1.5 | [TBD] | [TBD] | [TBD] |
| 2.5 | [TBD] | [TBD] | [TBD] |
| 4.0 | [TBD] | [TBD] | [TBD] |

**How to read it.** A positive value means the true quantity does better, so that estimate is the bottleneck. A negative constant-λ value means the frequency shaping is worth that many dB.

**Expected outcome**, stated before the run so the result can confirm or refute it:
- **Oracle σ ≈ 0 dB.** The noise estimate was exact to four decimals on development data (σ̂ = 0.0200 for σ_n = 0.02). Table 9 (`table9_estimator_accuracy.csv`) reports σ̂/σ_n over all settings.
- **Oracle S_x ≈ +0.15 to +0.39 dB**, close to the whole proposed-to-oracle gap in Table 1. That would locate the remaining gap in the isotropic power-law model, which cannot represent the anisotropic, oriented structure of real cell images.
- **Constant λ < 0.** If the shaping matters, collapsing λ(ω) should cost about as much as the gap between the proposed method and the constant-NSR Wiener filter.

[TBD: replace this paragraph with the measured outcome, 3–4 sentences, including any surprise.]

**Estimator accuracy** [TBD from Table 9]:
- the mean and spread of σ̂/σ_n for each PSF and noise level;
- the range of fitted β.

Expected: σ̂/σ_n ≈ 1 when the noise-only band is large (σ_h ≥ 2.5). There may be a slight over-estimate at σ_h = 1.5, σ_n = 0.005, where the band starts at 0.28 cycles/px and residual signal can leak in.
