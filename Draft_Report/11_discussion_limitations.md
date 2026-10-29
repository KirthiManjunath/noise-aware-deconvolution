# 11 Discussion and limitations

## 11.1 What the results show

1. **Frequency-dependent regularization estimated from the data is close to optimal on matched synthetic data.** The proposed λ(ω) comes within 0.15–0.39 dB of the oracle Wiener filter without any tuning. One constant NSR, by contrast, costs up to 3.5 dB at the noise levels it was not tuned for (Table 1).
2. **On synthetic data the gain over a well-chosen Tikhonov regularizer is nil.** GCV with a Laplacian penalty, which implies the spectral model S_x ∝ |ω|⁻⁴, performs as well as our fitted |ω|^(−β) model when the noise really is white and the PSF is exact. We do not claim a PSNR improvement over Tikhonov–GCV.
3. **The advantage is robustness.** On real FMD noise and on OCT [PRELIM], GCV's choice of λ became unstable: noise gain up to 4.3× on FMD and 22× on 2 of 13 OCT scans. The proposed method's noise gain stayed within 0.6–1.5×. The proposed method ties to a physical measurement, the noise power in the band the optics cannot pass. GCV ties to a statistical criterion whose white-noise assumption real data violate.

## 11.2 Failure modes and why they occur (DSP view)

- **Ringing.** Every sharpening method overshoots by about 7–10 % at a step edge (Section 7.3). The restoration transfer function T(ω) = |H|²/(|H|² + λ) falls from ≈1 to ≈0 over a narrow band of frequencies. A sharp cut-off in frequency produces oscillations in space (the Gibbs phenomenon). A smoother roll-off would trade ringing for resolution.
- **Coloured residual noise.** Restored noise is not white: it is white noise shaped by |G(ω)|², which peaks just below the cut-off. This produces the "worm-like" texture in Fig. 9. Noise standard deviation alone understates how visible it is.
- **PSF mismatch** (Section 9.1). An assumed PSF that is too wide boosts frequencies the optics never attenuated, causing ringing halos. One that is too narrow under-corrects. [TBD: quantify from the mismatch curves.]
- **Boundaries.** Without padding, border discontinuities cost 8 dB (Section 9.2). Mirror padding removes most of this; tapering or apodization are alternatives.

## 11.3 Limitations

1. **Stationary noise model.** The method estimates one global σ̂². Poisson–Gaussian noise varies with brightness, so the filter is too strong in dark regions and too weak in bright ones. [TBD: size of the effect from Section 7.2.] A variance-stabilizing transform is not directly compatible with the linear convolution model; a spatially varying λ would be the natural extension.
2. **Isotropic power-law signal model.** Cell images contain oriented, anisotropic structure. The radial fit averages over orientation, and the ablation (Section 8) [TBD] measures how much this costs.
3. **Known, shift-invariant PSF.** All synthetic results use the true PSF. All real results assume a Gaussian whose width is swept, not measured. Resolution figures on real data are therefore relative, and recovered fine structure is not claimed to be physically real.
4. **Small, correlated test set.** The synthetic test uses 8 crops from 2 fields of view. Crops of one field are not independent, so the Wilcoxon p-values (≈10⁻⁸⁰) overstate the evidence; the per-setting means and spreads are the reliable result. The real-noise evaluation uses one raw frame of 2 fields.
5. **Reference noise.** The FMD 50-frame average still contains about 1/√50 of the single-frame noise. The real-data noise gain therefore slightly mixes in filtered reference noise; the error is about 1/50 in variance and does not affect the comparison between methods.
6. **OCT is qualitative.** Log-speckle is non-Gaussian and correlated, the PSF is assumed, and there is no reference image. Only 13 B-scans were usable after removing archive metadata files.
7. **Baseline tuning.** The constant NSR and the RL iteration count were tuned once across all noise levels. RL's best value lay on the grid edge and is being re-tuned (Section 5). Per-noise-level tuning would make the constant-NSR baseline stronger.

## 11.4 Future work

- A spatially adaptive λ from local noise estimates, for Poisson–Gaussian data.
- Anisotropic (orientation-binned) spectral fits.
- Joint estimation of the PSF width from the same spectrum, using the location of the noise floor.
- Comparison with total-variation regularization at matched noise gain.
