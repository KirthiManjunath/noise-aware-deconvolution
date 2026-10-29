# 6 Experimental setup

## 6.1 Datasets

**Fluorescence Microscopy Denoising (FMD)** [Zhang et al. 2019]. Real images from commercial confocal, two-photon and wide-field microscopes. For each field of view (FOV), 50 raw frames are recorded at the same position, and their average ("avg50") is provided as a near-noise-free reference. We use three subsets, each with 20 FOVs of 512 × 512 8-bit images:

| Subset | Microscope | Sample [CHECK: against the FMD paper] | Role |
|---|---|---|---|
| WideField_BPAE_B | wide-field | BPAE cells, blue channel (nuclei) | development |
| Confocal_BPAE_B | confocal | BPAE cells, blue channel (nuclei) | test |
| TwoPhoton_MICE | two-photon | mouse brain tissue | test |

Licence: the FMD data release is CC BY-SA 4.0 (per the course sheet); the accompanying code is MIT-licensed. Source: github.com/yinhaoz/denoising-fluorescence. Downloaded on 29 Oct 2026 with `gdown`, using the Google-Drive file IDs in the authors' `download_dataset.sh`. Only the `raw/` and `gt/` folders were extracted.

**Kermany retinal OCT** [Kermany et al. 2018]. Retinal OCT B-scans labelled CNV / DME / DRUSEN / NORMAL. We drew a seeded random sample (seed 0) of 20 files from the NORMAL and DRUSEN test folders of the Kaggle mirror `paultimothymooney/kermany2018`.
- **7 of the 20 files are macOS metadata files (`._*.jpeg`, 212 bytes) packed in the archive, not images.** They are excluded, which leaves **13 B-scans** (4 DRUSEN, 9 NORMAL; e.g. 496 × 512 pixels).
- Licence: the original Mendeley release (doi:10.17632/rscbjbr9sj.3) is CC BY 4.0, but the Kaggle page lists CC BY-NC-SA 4.0. We use the images only for non-commercial academic work and cite the original. [CHECK: course team happy with this.]

## 6.2 Data partitions (fixed before any tuning)

| Partition | Images | Used for |
|---|---|---|
| Development | WideField_BPAE_B, FOVs 1–18 (FOVs 1–3 used) | NSR and RL tuning; ε, SNR threshold and bin count of the proposed method; all debugging |
| Synthetic test | Confocal_BPAE_B and TwoPhoton_MICE, FOV 19 avg50, each cut into four non-overlapping 256 × 256 quadrants (8 crops) | every number in Sections 7–9 |
| Real test | the same two FOVs: raw frame 0 versus avg50, centre 256 × 256 crop | Section 10.1 |
| OCT | 13 B-scans | Section 10.2 (qualitative) |

The test FOV is a different microscope and sample type from the development subset, so the test also measures generalization across modalities. No parameter was changed after looking at test results. The split is recorded in `configs/split.yaml`.

**Caveat on independence.** The 8 synthetic test crops come from only 2 FOVs, and quadrants of one FOV share content and imaging conditions. The 480 paired comparisons per method (8 crops × 3 PSFs × 4 noise levels × 5 seeds) are therefore not independent, and the Wilcoxon p-values in Section 7 overstate the evidence. The per-setting means and standard deviations are the primary result.

## 6.3 Pre-processing

- Images are converted to float64 (RGB averaged to gray if present).
- Each image is scaled to [0, 1] by the 0.5th and 99.5th percentiles of its **clean** reference, then clipped (`data.norm_pair`). The raw frame of the same FOV is scaled with the same two numbers, so the reference and the noisy frame stay on one intensity scale.
- After normalization, the real noise in FMD test field 19 (std of raw − avg50, centre crop) is about 0.054 (confocal) and 0.094 (two-photon). These are higher than our largest synthetic σ_n = 0.05.
- OCT B-scans are transformed to log intensity, z = log(1 + I)/log(256), and are not cropped.

## 6.4 Degradation grid

| Factor | Values |
|---|---|
| PSF | Gaussian, σ_h ∈ {1.5, 2.5, 4.0} px |
| Gaussian noise | σ_n ∈ {0.005, 0.01, 0.02, 0.05} |
| Poisson–Gaussian noise | peak photons p ∈ {30, 100, 300}, read noise σ_r = 0.01 |
| Noise seeds | 0, 1, 2, 3, 4 |
| Boundary | periodic (main), reflect (Section 9.2) |
| PSF mismatch | assumed σ_h = 2.5(1 + δ), δ ∈ {−30, …, +30} %, true 2.5 px, σ_n = 0.01 |

All parameters are in `configs/params.yaml`; the tuned values are in `configs/tuned.yaml`.

## 6.5 Metrics

| Metric | Definition | Used in |
|---|---|---|
| PSNR (dB) | 10 log₁₀(1/MSE) on outputs clipped to [0, 1] | 7, 8, 9 |
| SSIM | `skimage.metrics.structural_similarity`, data range 1 | 7, 8 |
| Log-spectral distance (dB) | RMS over ω of 10 log₁₀(\|X\|²/\|X̂\|²) | 7 |
| Edge FWHM (px) | full width at half maximum of the line-spread function (derivative of the row-averaged edge profile of a step-edge phantom, 0.2 → 0.8) | 7.3 |
| MTF50 (cycles/px) | frequency where the Fourier magnitude of the ±16 px LSF window drops to 0.5 | 7.3 |
| Overshoot (%) | peak of the edge profile above the bright level, as % of the step height (ringing) | 7.3 |
| Noise amplification (synthetic) | std in the flat half of the restored edge phantom ÷ σ_n | 7.3 |
| Noise gain (real) | std(f(raw) − f(avg50)) ÷ std(raw − avg50), with the **same** filter f applied to both (Section 10.1) | 10 |
| Chain MTF50 (real) | MTF50 of \|H\|²/(\|H\|² + λ), the transfer of blur followed by restoration | 10 |
| Runtime (ms) | wall-clock per 256 × 256 image, Colab CPU | 7 |

The MTF50 implementation was corrected on 30 Oct: the earlier version took the absolute value of the noisy derivative, which biased MTF50 low. [TBD: Section 7.3 MTF50 values come from the re-run of 03 S6 Cell C.]

**Statistics.** Results are reported as mean ± standard deviation over crops and seeds. Paired comparisons use the two-sided Wilcoxon signed-rank test on per-trial PSNR (see the caveat in 6.2).
