# 5 Baselines and implementation

All methods share one implementation of the regularized inverse (`baselines._apply`) where possible. They also share the same PSF, OTF construction and boundary handling, so differences between them come only from how they regularize.

| Method | Implementation | Regularization chosen by | Reference |
|---|---|---|---|
| Inverse filter | X̂ = H*Y/(\|H\|² + 10⁻³⁰) | none | — |
| Constant-NSR Wiener | X̂ = H*Y/(\|H\|² + NSR) | NSR tuned on development images (Section 6.2) | Wiener; Gonzalez & Woods |
| Tikhonov–GCV | Laplacian penalty, Section 3.2 | GCV per image, 61 values of λ in [10⁻⁶, 1] | Golub et al. 1979; Hansen et al. 2006 |
| Richardson–Lucy (RL) | `skimage.restoration.richardson_lucy`, input clipped to ≥ 10⁻⁶ | iteration count tuned on development images | Richardson 1972; Lucy 1974 |
| Unsupervised Wiener | `skimage.restoration.unsupervised_wiener` (Laplacian prior, Gibbs sampling of noise and prior precisions) | estimated per image by the sampler | Orieux et al. 2010 |
| Oracle Wiener | λ = σ_n²/S_x(ω), with S_x the periodogram of the true x | ground truth | upper bound only |
| **Proposed** | Algorithm 1 | estimated per image | Section 4 |

**Tuning.** Two baselines have a free parameter. The constant NSR and the RL iteration count were tuned once, on three development crops (WideField_BPAE_B, fields 1–3), averaged over every PSF width and noise level. They were then frozen in `configs/tuned.yaml` before any test image was processed.
- The constant NSR was searched over 17 log-spaced values in [10⁻⁴, 1]; the best was **0.0316**.
- The RL iteration count was searched over {5, 10, 20, 30, 50, 75, 100}; the best was **5**, the smallest value tried. Because this lies on the grid edge, the search has been extended to {1, 2, 3, 4, 5, 7, 10, 20, 30, 50}. [TBD: new rl_iter from 01 `[S3 tuning]`; update every RL number in Sections 7 and 9.]

**Why tune on all settings at once.** A single NSR or iteration count for all noise levels is how these methods are used when the noise is not known. It is also the main weakness that the adaptive methods address. A per-noise-level tuning would be a stronger (oracle-like) baseline. [CHECK: decide whether to add it as an extra row.]

**Unsupervised Wiener.** This baseline under-regularized markedly at large PSF widths. SSIM fell to 0.18 at σ_h = 4, σ_n = 0.05, and noise amplification on the edge phantom was 3.4 on average. A diagnostic cell (01, `[S3 check]`) compares the noise level estimated by its sampler with the true σ_n. [TBD: report whether the sampler underestimates σ_n (a property of the method on these images) or whether this is a wrapper issue.]

**Implementation details.**
- Images are float64 arrays in [0, 1].
- The PSF is odd-sized (8σ_h + 1) and normalized to unit sum. The OTF is computed by `psf2otf` (zero-pad and circular shift).
- Outputs are clipped to [0, 1] only for computing metrics; unclipped outputs are used for noise analysis.
- Software (Colab): Python 3, NumPy 2.1.3, SciPy 1.16.3, scikit-image 0.25.2. [TBD: Python version from `results/versions.txt`.]
- Random noise uses `numpy.random.default_rng(seed)` with seeds 0–4.
- All code is in `DSP_Deconv/lib/` (`forward.py`, `data.py`, `metrics.py`, `baselines.py`, `proposed.py`). Experiments are in notebooks 01–05.

**Code verification** (notebook 01, S2–S3):
- The inverse filter recovers a noiseless blurred image to a maximum error of 2.8 × 10⁻⁸, which checks the OTF centring.
- On a test image, every method improves on the observation.
- The oracle Wiener filter has the highest PSNR of all methods at every setting (Table 1).
