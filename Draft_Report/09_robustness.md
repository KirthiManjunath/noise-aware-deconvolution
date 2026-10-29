# 9 Robustness

## 9.1 PSF mismatch

In practice the PSF is measured or modelled, never known exactly. We blurred the 8 test crops with σ_h = 2.5 px (σ_n = 0.01, seeds 0–2). We then deconvolved them assuming σ_h = 2.5(1 + δ) for δ ∈ {−30, −20, −10, 0, +10, +20, +30} %.

[TBD: Figure 5 left panel + Table 5 from `psf_mismatch.csv` (03 `[S7 Cell A]`, re-run on all 8 crops). A preliminary single-crop run gave curves that peak at δ = 0 for every method. Report:
- the PSNR loss at ±10 % and ±30 % for each method;
- whether the proposed method degrades faster or slower than Tikhonov–GCV.]

**Mechanism** (for the discussion of the measured curves):
- **Assumed PSF too narrow (δ < 0):** the filter under-corrects. The output stays blurred but is free of artefacts, so the loss is gradual.
- **Assumed PSF too wide (δ > 0):** the filter boosts frequencies the true OTF never attenuated, which produces ringing halos around edges. The loss is usually steeper.

The proposed method has an additional sensitivity. Its noise-only band is defined by the **assumed** |H|². If the PSF is assumed too wide, the band starts too low and includes residual signal, so σ̂² is over-estimated and the filter becomes more conservative. That partly offsets the ringing. If the PSF is assumed too narrow, the band shrinks; it still contains only noise, so σ̂² stays unbiased.

## 9.2 Boundary conditions

FFT-based deconvolution assumes the image is periodic. A real image is not: its left and right edges do not match. The discontinuity has energy at every frequency, which the inverse filter amplifies into bands of ringing along the borders.

We blurred the test crops with mirror ("reflect") boundaries, the realistic case, and deconvolved them with and without 32-pixel mirror padding. On the first test crop (σ_h = 2.5, σ_n = 0.01), padding raised the proposed method's PSNR from **27.19 dB to 35.28 dB**, a gain of 8.1 dB. The error map without padding (`figures/boundary_error_map.png`, Figure 5) concentrates almost entirely in bands about 10–20 px wide along the four borders. [CHECK: band width against the figure.]

[TBD: Table 5b from `boundary.csv`, all 8 crops × 3 linear methods.] This effect is larger than any difference between methods in Table 1. **Every real-image result in Section 10 therefore uses mirror padding**, and a deconvolution method compared without matched boundary handling is not a fair comparison.
