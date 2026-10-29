# 7 Results on the controlled benchmark

> Numbers for `wiener_const` and `rl` will change after RL re-tuning (README step 2). Numbers for all other methods come from `results/synthetic_gauss_test.csv` (Colab run, 30 Oct) and will not change.

## 7.1 Gaussian noise: fidelity

**Table 1 — PSNR (dB), mean ± std over 8 test crops × 5 seeds** (`results/tables/table1_gauss_psnr.csv`). The inverse filter scored 3.37 dB everywhere and is omitted.

| σ_h | σ_n | Const. Wiener | Tikhonov–GCV | RL | Unsup. Wiener | **Proposed** | Oracle Wiener |
|---|---|---|---|---|---|---|---|
| 1.5 | 0.005 | 33.75 ± 1.69 | 34.53 ± 1.51 | 31.73 ± 1.51 | 33.91 ± 1.32 | **34.47 ± 1.53** | 34.79 ± 1.54 |
| 1.5 | 0.01 | 33.05 ± 1.46 | 33.51 ± 1.52 | 31.63 ± 1.47 | 32.62 ± 1.22 | **33.44 ± 1.55** | 33.79 ± 1.55 |
| 1.5 | 0.02 | 31.30 ± 1.06 | 32.32 ± 1.49 | 31.27 ± 1.35 | 31.04 ± 1.06 | **32.26 ± 1.54** | 32.63 ± 1.54 |
| 1.5 | 0.05 | 26.77 ± 0.48 | 30.43 ± 1.50 | 29.44 ± 0.87 | 28.43 ± 0.80 | **30.41 ± 1.51** | 30.80 ± 1.51 |
| 2.5 | 0.005 | 30.52 ± 1.98 | 31.85 ± 1.69 | 28.63 ± 1.69 | 29.28 ± 0.95 | **31.82 ± 1.72** | 32.04 ± 1.72 |
| 2.5 | 0.01 | 30.38 ± 1.91 | 31.08 ± 1.70 | 28.61 ± 1.68 | 28.13 ± 0.85 | **31.06 ± 1.71** | 31.30 ± 1.71 |
| 2.5 | 0.02 | 29.92 ± 1.73 | 30.18 ± 1.71 | 28.52 ± 1.64 | 26.72 ± 0.69 | **30.18 ± 1.72** | 30.44 ± 1.71 |
| 2.5 | 0.05 | 28.02 ± 1.19 | 28.79 ± 1.71 | 27.83 ± 1.35 | 24.53 ± 0.54 | **28.83 ± 1.71** | 29.11 ± 1.70 |
| 4.0 | 0.005 | 27.89 ± 2.09 | 29.33 ± 1.89 | 26.36 ± 1.81 | 24.33 ± 0.62 | **29.34 ± 1.90** | 29.49 ± 1.89 |
| 4.0 | 0.01 | 27.86 ± 2.07 | 28.77 ± 1.88 | 26.35 ± 1.81 | 23.30 ± 0.51 | **28.78 ± 1.89** | 28.95 ± 1.89 |
| 4.0 | 0.02 | 27.74 ± 2.01 | 28.17 ± 1.87 | 26.32 ± 1.79 | 22.22 ± 0.43 | **28.19 ± 1.88** | 28.36 ± 1.88 |
| 4.0 | 0.05 | 27.13 ± 1.75 | 27.29 ± 1.83 | 25.97 ± 1.60 | 20.52 ± 0.36 | **27.31 ± 1.86** | 27.50 ± 1.86 |

The standard deviations (about 1.5–2 dB) mostly reflect differences between the 8 crops, not between methods. All methods move together from crop to crop, so the paired differences below are far more precise than the table's spread suggests.

**Main findings.**

1. **The proposed method is close to the oracle.** Its mean gap to the oracle Wiener filter is only 0.15–0.19 dB at σ_h = 4, 0.23–0.28 dB at σ_h = 2.5 and 0.32–0.39 dB at σ_h = 1.5. That is achieved with no knowledge of x or σ_n.
2. **It clearly beats the constant-NSR Wiener filter.** The median paired gain is +0.72 dB overall (Wilcoxon p = 2.3 × 10⁻⁸⁰). The largest gain is +3.54 dB at σ_h = 1.5, σ_n = 0.05, the setting furthest from what one constant NSR can serve. One tuned constant cannot be right for every noise level and PSF width; the adaptive λ(ω) is.
3. **It beats both iterative and Bayesian baselines.**
   - Against RL (5 iterations): median +2.10 dB, p = 8.6 × 10⁻⁸⁰.
   - Against unsupervised Wiener: median +3.11 dB, p = 2.3 × 10⁻⁸⁰.
   - Unsupervised Wiener degrades fastest as the PSF widens (Section 5).
4. **It ties Tikhonov–GCV.**
   - The median paired difference is 0.00 dB (p = 0.047), and the proposed method wins 54 % of the 480 paired trials.
   - Per setting, the median difference ranges from −0.06 dB (σ_h = 1.5) to +0.04 dB (σ_h = 2.5, σ_n = 0.05). The proposed method is slightly behind for narrow PSFs and slightly ahead for wide ones.
   - Given the dependence between crops (Section 6.2), we regard the two as **equivalent in PSNR on synthetic data**.
   - The difference between them shows on real images (Section 10).

**SSIM** [TBD: Table 1b from `table1b_gauss_ssim.csv`] mostly follows PSNR. Two exceptions:
- RL and the constant Wiener filter have the highest SSIM at low noise and wide PSFs (e.g. 0.844 and 0.857 against 0.795 for the proposed method at σ_h = 4, σ_n = 0.005). Both smooth more, and SSIM rewards smooth, artefact-free structure.
- Unsupervised Wiener's SSIM collapses (0.18–0.30 at σ_h = 4), consistent with its noise amplification.

*Figure 3 (`fig3_psnr_vs_noise.png`):* PSNR against σ_n for each PSF width, mean ± std.

## 7.2 Poisson–Gaussian noise

[TBD: run 03 `[S6 Cell B2]`, then write 3–4 sentences from `table3_pg_psnr.csv`, `fig3b_psnr_poisson.png` and the `poisson_gaussian` rows of `wilcoxon.csv`.] The main question: does a method that assumes white, signal-independent noise keep its advantage when the noise variance follows the signal? Expectation, to be confirmed or refuted: the global σ̂² estimates the **average** noise variance, so the filter is mis-tuned in very bright and very dark regions. The gap to the oracle may grow at low photon counts (p = 30).

## 7.3 Resolution, ringing and noise amplification (edge phantom)

A vertical step (0.2 → 0.8) blurred with σ_h = 2.5 px has a theoretical edge width (FWHM of the line-spread function) of 2.355 × 2.5 = 5.9 px. Restoration should narrow it without adding overshoot or noise.

**Table 4 — edge metrics, mean over 5 seeds** (`edge_test.csv`; MTF50 omitted pending the re-run with the corrected metric):

| Method | FWHM at σ_n = 0.005 → 0.05 (px) | Overshoot, mean (%) | Noise amplification at σ_n = 0.005 → 0.05 |
|---|---|---|---|
| Constant Wiener | 4.82 → 4.79 | 1.3 | 0.62 → 0.62 |
| Tikhonov–GCV | 3.92 → 6.01 | 7.6 | 1.73 → 0.30 |
| RL (5 iter.) | 5.69 → 5.71 | 7.5 | 3.12 → 0.42 |
| Unsup. Wiener | 3.32 → 4.04 | 8.1 | 6.12 → 1.35 |
| **Proposed** | **3.95 → 5.98** | **7.4** | **1.68 → 0.30** |
| Oracle Wiener | 2.85 → 3.59 | 9.4 | 1.33 → 0.16 |

The adaptive methods behave as the theory predicts: they **trade resolution for noise according to the noise level**.
- At low noise the proposed method narrows the edge from 5.9 to 3.95 px and lets noise through (gain 1.68).
- At high noise it barely sharpens (5.98 px) but suppresses noise to 0.30 of its input.

The constant-NSR filter applies the same compromise everywhere: an edge width of 4.8 px and noise gain 0.62 at every noise level, with little overshoot (1.3 %). It is too cautious at low noise and too aggressive at high noise, which matches its PSNR deficit in Table 1.

RL at 5 iterations hardly sharpens at all (5.7 px). That shows the dev-tuned iteration count is close to "no deconvolution" and motivates the re-tuning. Every sharpening method rings at about 7–10 % overshoot; this is the price of the abrupt gain roll-off in G(ω) (Section 11).

[TBD: corrected MTF50 column from the re-run; Figure 4 `fig4_edge_profiles.png`.]

## 7.4 Cost

Mean runtime per 256 × 256 image on Colab CPU:

| Method | Runtime (ms) |
|---|---|
| Constant Wiener | 7 |
| Oracle Wiener | 10 |
| **Proposed** | **33** |
| RL | 45 |
| Tikhonov–GCV | 49 |
| Unsupervised Wiener | 188 |

The proposed method costs about 4.5× a fixed Wiener filter (the extra FFT plus binning) and is faster than GCV's 61-point search.
