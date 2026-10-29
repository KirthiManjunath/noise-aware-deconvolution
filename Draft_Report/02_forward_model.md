# 2 Forward imaging model

## 2.1 Continuous-to-discrete model

We model a grayscale image as a 2-D discrete signal on an M × N pixel grid, with intensities normalized to [0, 1] (Section 6.3). The observed image y is the unknown object x convolved with the PSF h, plus additive noise n:

$$
y[m,n] \;=\; (h * x)[m,n] + n[m,n] \;=\; \sum_{k,l} h[k,l]\,x[m-k,\,n-l] + n[m,n].
$$

| Symbol | Meaning | Units / convention |
|---|---|---|
| x[m, n] | true object intensity | normalized, 0–1 |
| h[k, l] | point spread function, odd size K × K, centred, Σh = 1 | dimensionless; Σh = 1 preserves mean brightness |
| n[m, n] | noise | same units as x |
| y[m, n] | recorded image | same units as x |
| m, n | pixel indices | samples |
| ω = (ω_x, ω_y) | spatial frequency | cycles/pixel, each component in [−0.5, 0.5) |
| \|ω\| | radial frequency | cycles/pixel, 0 … 0.707 |

Convolution in the experiments is **circular** (periodic boundaries) unless stated otherwise. That makes the discrete Fourier transform (DFT) diagonalize the blur exactly:

$$
Y(\omega) = H(\omega)\,X(\omega) + N(\omega),
$$

where capitals denote 2-D DFTs over the M × N grid. H(ω) is the optical transfer function (OTF), and |H(ω)| is the modulation transfer function (MTF). To compute H without a phase ramp, the K × K PSF is zero-padded to M × N and circularly shifted so that its centre sits at pixel (0, 0) (`psf2otf` in `lib/forward.py`). Section 9.2 studies the more realistic mirror ("reflect") boundary.

## 2.2 PSF models

**Gaussian PSF.** This is the main model throughout:

$$
h[k,l] \propto \exp\!\left(-\frac{k^2 + l^2}{2\sigma_h^2}\right), \qquad |k|,|l| \le 4\sigma_h,
$$

truncated to a square of side 8σ_h + 1 (rounded to odd) and normalized to unit sum. We use σ_h ∈ {1.5, 2.5, 4.0} pixels. A Gaussian has a Gaussian transfer function:

$$
|H(\omega)| = \exp\!\left(-2\pi^2\sigma_h^2|\omega|^2\right),
$$

so the MTF of the blur alone falls to 0.5 at |ω| = √(ln 2 / 2π²)/σ_h ≈ 0.187/σ_h cycles/pixel: 0.125, 0.075 and 0.047 for our three widths. At |ω| = 0.5 the transfer is about 1.5 × 10⁻⁵ for σ_h = 1.5 and about 10⁻³⁴ for σ_h = 4. Those frequencies are effectively lost and can only be recovered by amplifying noise (Fig. 1, right panel).

The width relates to the more familiar full width at half maximum by FWHM = 2√(2 ln 2) σ_h ≈ 2.355 σ_h, giving 3.5, 5.9 and 9.4 pixels.

**Airy PSF.** A diffraction-limited PSF, (2J₁(r)/r)², is implemented (`airy_psf`) for completeness. [TBD: either report one Airy experiment or delete this paragraph.]

## 2.3 Noise models

1. **Additive white Gaussian noise**, n ~ 𝒩(0, σ_n²) independently per pixel, with σ_n ∈ {0.005, 0.01, 0.02, 0.05}. Its power spectrum is flat. With the unnormalized DFT, E|N(ω)|² = MN σ_n² at every ω. We therefore write all power spectra per pixel, S(ω) = E|·(ω)|²/(MN), so the noise power spectral density is simply S_n(ω) = σ_n².

2. **Poisson–Gaussian noise**, the standard model for fluorescence detectors and the noise in the FMD dataset [Zhang et al. 2019]:

$$
y = \frac{1}{p}\,\mathrm{Poisson}\big(p\,(h*x)\big) + n_r, \qquad n_r \sim \mathcal{N}(0, \sigma_r^2),
$$

where p is the photon count at intensity 1.0 (p ∈ {30, 100, 300}; larger p means less noise) and σ_r = 0.01 is the read-noise level. The noise variance depends on the signal, Var = (h*x)/p + σ_r². The linear methods in this report treat it through its spatial average, σ_eff² = mean(h*x)/p + σ_r².

3. **Speckle (OCT)** is multiplicative, y = x·s. Taking the logarithm turns it into an additive term, log y = log x + log s, so the OCT experiments (Section 10.2) operate on log intensity. Log-speckle is neither Gaussian nor white in general. This is a limitation of the OCT demonstration (Section 11).

## 2.4 Assumptions

- **Shift-invariant blur.** One PSF applies to the whole field of view. Real objectives vary across the field and with depth.
- **Known PSF.** In the synthetic experiments the true PSF is used for deconvolution, except in the mismatch study (Section 9.1). On real images it is **assumed** to be Gaussian, with σ_h swept over {1, 1.5, 2} px (Section 10).
- **Noise independent of the object** (Gaussian case) or **Poisson–Gaussian with known structure but unknown level** (microscopy case). None of the methods is given the noise level, except the oracle.
- **2-D processing.** Each image is processed independently. There is no 3-D (z-stack) deconvolution.

*Figure 1 (`figures/fig1_forward_model.png`, notebook 05 [Fig 1]):* clean development crop, Gaussian PSF (σ_h = 2.5 px), blurred and noisy observation (σ_n = 0.02), and |H| along one frequency axis for the three PSF widths. A dotted line marks |H| = √ε, the start of the noise-only band used in Section 4.
