# 10 Real biomedical images

Real images have neither a ground truth nor a known PSF, so this section answers narrower questions than Sections 7–9:
- How much does each method amplify **real** detector noise?
- How much resolution does it deliver for an assumed PSF?
- Does its behaviour on real data match the synthetic results?

Every result here assumes a Gaussian PSF. Structures that appear after deconvolution are not claimed to be physically real.

## 10.1 Fluorescence microscopy (FMD), noise on real data

**Protocol.** For each test FOV (Confocal_BPAE_B and TwoPhoton_MICE, FOV 19), we take one raw frame and the 50-frame average of the same field, centre 256 × 256 crop. The average has 1/√50 ≈ 14 % of the raw noise, so raw − avg50 is almost pure real noise.

For each method we:
1. **design the filter once, on the raw frame**, exactly as it would be used: σ̂, A and β for the proposed method; λ from GCV for Tikhonov; the tuned NSR for the constant Wiener filter;
2. apply that **same** filter to both the raw frame and the average.

The difference of the two outputs is the filtered noise, so:

$$
g_n = \frac{\operatorname{std}\big(f(\text{raw}) - f(\text{avg50})\big)}{\operatorname{std}(\text{raw} - \text{avg50})}.
$$

Designing the filter separately on each image would be wrong for the adaptive methods. On the nearly clean average, GCV chooses a far smaller λ, so the two outputs would come from different filters and their difference would not be noise. Resolution is summarized by the chain MTF50 of |H|²/(|H|² + λ) (Section 3.4). Images are mirror-padded by 32 px. The PSF width is unknown, so we sweep σ_h ∈ {1.0, 1.5, 2.0} px.

**Table 6 — noise gain g_n on real FMD noise** [PRELIM: laptop run on the Drive snapshot; replace with `results/real_fmd.csv` from Colab notebook 04]:

| FOV | Assumed σ_h | Const. Wiener | Tikhonov–GCV | RL | **Proposed** |
|---|---|---|---|---|---|
| Confocal | 1.0 | 1.51 | 0.73 | 0.82 | **0.68** |
| Confocal | 1.5 | 1.13 | 1.24 | 0.67 | **0.94** |
| Confocal | 2.0 | 0.96 | **4.29** | 0.59 | **1.47** |
| Two-photon | 1.0 | 1.56 | 0.58 | 0.71 | **0.60** |
| Two-photon | 1.5 | 1.12 | 0.87 | 0.55 | **0.76** |
| Two-photon | 2.0 | 0.90 | 1.70 | 0.47 | **1.11** |

**Chain MTF50 (cycles/px)** [PRELIM]: the blur alone gives 0.188 / 0.128 / 0.098 for σ_h = 1.0 / 1.5 / 2.0.

| FOV | Assumed σ_h | Const. Wiener | Tikhonov–GCV | Proposed |
|---|---|---|---|---|
| Confocal | 1.0 | 0.298 | 0.218 | 0.208 |
| Confocal | 1.5 | 0.198 | 0.208 | 0.188 |
| Confocal | 2.0 | 0.152 | 0.212 | 0.173 |
| Two-photon | 1.0 | 0.298 | 0.198 | 0.202 |
| Two-photon | 1.5 | 0.198 | 0.188 | 0.178 |
| Two-photon | 2.0 | 0.152 | 0.182 | 0.162 |

**Findings** [PRELIM, to be confirmed with Colab numbers]:

1. **Tikhonov–GCV is unstable on real data.** As the assumed PSF widens, GCV picks ever smaller λ. At σ_h = 2.0 it reaches the highest resolution (0.21 cycles/px) but amplifies real noise **4.3×** (confocal). On synthetic data, with white noise and a matched PSF, it was equal to the proposed method. A plausible cause: GCV assumes white noise, while real FMD noise is signal-dependent (Poisson–Gaussian) and may be spatially correlated. [CHECK: whether FMD raw noise has measurable spatial correlation.]
2. **The proposed method stays moderate.** Its noise gain is between 0.60 and 1.47 everywhere, at a resolution close to Tikhonov's for σ_h ≤ 1.5. Its σ̂² comes from a physical noise measurement, which is not fooled in the same way.
3. **The constant Wiener filter does not adapt to the PSF.** At σ_h = 1 its fixed NSR gives the highest MTF50 (0.30) with gain 1.5–1.6. At σ_h = 2 it gives the lowest MTF50 (0.15).
4. **RL** (5 iterations) has a noise gain below 1, meaning it smooths, consistent with its minimal sharpening in Section 7.3.

*Figure 8 (`figures/real_fmd_tradeoff.png`, notebook 04):* noise gain (log scale) against chain MTF50. Each method is one point per assumed PSF; "observed" (no restoration) sits at gain 1.

*Figure 9 (`figures/real_fmd_panels.png`):* raw frame, average and the restorations at σ_h = 1.5, with a 64 × 64 zoom on a background region near a nucleus. The zoom shows the visible form of noise gain: every linear method turns white pixel noise into a correlated, "worm-like" texture whose grain size follows the filter's pass-band. RL leaves the smoothest background.

## 10.2 Retinal OCT (qualitative)

**Protocol.** Speckle is multiplicative, so the restoration works on log intensity. OCT lateral resolution is limited by the beam waist and axial resolution by the source bandwidth. We model only the lateral blur, a 1-D Gaussian with an assumed σ = 2 px along x, and apply the same design-once filters.

Noise is measured in a background band: the darkest 24-row strip in the top 40 % of each B-scan, which is vitreous above the retina. The metric is the ratio of its standard deviation after and before restoration.

**Table 7 — background noise ratio over 13 B-scans** [PRELIM]:

| Method | Mean | Range | Notes |
|---|---|---|---|
| Constant Wiener | 1.45 | 1.29–1.54 | consistent mild amplification |
| Tikhonov–GCV | 3.90 | 0.58–22.0 | **two scans at 16.8× and 22.0×** (both NORMAL) |
| **Proposed** | **1.02** | **0.65–1.25** | no failures |

The proposed method never fails on these 13 scans, while GCV fails badly on 2 of them. This repeats the FMD pattern. In the panel (`figures/real_oct_panels.png`), the retinal layers and the drusen elevations sharpen laterally under all three methods.

These OCT results are **qualitative**:
- there is no ground truth;
- the PSF is assumed;
- log-speckle violates the Gaussian white-noise assumption, since it is heavy-tailed and spatially correlated over the speckle size;
- the vitreous "background" is itself speckle, not detector noise.

The two GCV failures are NORMAL-395557-1 and NORMAL-438684-3 [PRELIM]. On both, GCV chose a λ small enough to push the lateral MTF50 to 0.34–0.35 cycles/px, against about 0.18 for the proposed method. [TBD: look at the two scans and add one sentence on what they share, e.g. little retinal signal or strong vertical striping.]
