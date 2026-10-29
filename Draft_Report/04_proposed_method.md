# 4 Proposed method: spectrally adaptive Wiener filter

The Wiener filter (Section 3.3) is optimal, but it needs S_n(ω) and S_x(ω). We estimate both from the single blurred, noisy image y, with no hand-tuned regularization parameter.

## 4.1 Noise level from the noise-only band

For white noise, S_n(ω) = σ_n² at every frequency. Wherever the blur has removed the signal, the observed spectrum is noise alone. Define the noise-only band:

$$
\mathcal{B} = \{\omega : |H(\omega)|^2 < \varepsilon\}, \qquad \varepsilon = 10^{-3}.
$$

On 𝓑, E|Y(ω)|²/(MN) = |H|²S_x + σ_n² ≈ σ_n², with a relative bias of at most ε·S_x/σ_n². The estimate is the band average:

$$
\hat\sigma^2 = \frac{1}{|\mathcal{B}|}\sum_{\omega\in\mathcal{B}} \frac{|Y(\omega)|^2}{MN}.
$$

𝓑 typically holds tens of thousands of frequency bins, so the estimate has low variance. For a Gaussian PSF the band starts at |ω| = √(ln(1/ε))/(2πσ_h): 0.28, 0.17 and 0.10 cycles/pixel for σ_h = 1.5, 2.5, 4. If the PSF is so narrow that 𝓑 has fewer than 50 bins, the method falls back to the wavelet median-absolute-deviation estimator [Donoho & Johnstone 1994] (`skimage.restoration.estimate_sigma`). ε was fixed on the development set and is stored in `configs/params.yaml`.

## 4.2 Signal spectrum from a power-law fit

Natural and biological images have power spectra that fall approximately as a power of radial frequency [Field 1987; van der Schaaf & van Hateren 1996]:

$$
S_x(\omega) \approx A\,|\omega|^{-\beta}.
$$

We estimate A and β as follows.

1. Compute the per-pixel periodogram of the mean-removed image, P(ω) = |Y(ω)|²/(MN).
2. Group frequencies into 60 radial bins on |ω| ∈ (0, 0.5]. In each bin k, average to P̄_k and H̄²_k = mean |H|².
3. Keep only **reliable** bins, where the signal clearly exceeds the noise: P̄_k > 2σ̂².
4. In each kept bin, remove the noise and undo the blur: Ŝ_k = (P̄_k − σ̂²)/H̄²_k.
5. Fit log Ŝ_k = log A − β log|ω_k| by least squares, which gives (A, β).

At least 3 reliable bins are required; otherwise the method stops with an error, and this never happened on our data. Restricting the fit to reliable bins is what keeps the de-blurring step in (4) stable: bins where noise dominates, and where division by H̄² would explode, are never used.

## 4.3 The filter

$$
\lambda(\omega) = \frac{\hat\sigma^2}{A\,|\omega|^{-\beta}} = \frac{\hat\sigma^2}{A}\,|\omega|^{\beta},
\qquad
\hat X(\omega) = \frac{H^*(\omega)\,Y(\omega)}{|H(\omega)|^2 + \lambda(\omega)},
$$

with |ω| at DC replaced by the smallest non-zero frequency, so the mean brightness passes unchanged. Compared with Tikhonov–Laplacian, where λ grows as |ω|⁴ with one scale chosen by GCV:
- the exponent β is **fitted per image** (2.67 on our development image);
- the scale σ̂²/A comes from **two physical quantities**, the noise level and the signal power, rather than from a model-selection criterion.

**Algorithm 1 (spectrally adaptive Wiener).** Inputs: y (M × N), PSF h. Parameters fixed once on development data: ε = 10⁻³, SNR threshold 2, 60 bins.

1. H ← DFT of zero-padded, centred h; Y ← DFT of y.
2. σ̂² ← mean of |Y|²/(MN) over {|H|² < ε} (wavelet MAD fallback if fewer than 50 bins).
3. For each radial bin with P̄_k > 2σ̂²: Ŝ_k ← (P̄_k − σ̂²)/H̄²_k.
4. (A, β) ← least-squares fit of log Ŝ_k against log|ω_k|.
5. λ(ω) ← σ̂²|ω|^β / A.
6. Return x̂ ← IDFT{ H*Y / (|H|² + λ) }.

For real images with non-periodic borders, y is first mirror-padded by 32 pixels and the result cropped back (Section 9.2).

## 4.4 Cost

The method needs one forward and one inverse 2-D FFT of the image, plus one FFT of the padded PSF: O(MN log MN) operations. The radial binning and the fit are O(MN). The measured runtime on Colab CPU was 33 ms per 256 × 256 image, against 7 ms for constant Wiener, 49 ms for Tikhonov–GCV (61 λ evaluations), 45 ms for Richardson–Lucy and 188 ms for unsupervised Wiener (Section 7, Table 2).

## 4.5 Sanity check on development data

On a development crop (WideField_BPAE_B, field 1; σ_h = 2.5, σ_n = 0.02):
- the estimated noise level was σ̂ = 0.0200, matching the true value to four decimals;
- the fitted exponent was β = 2.67;
- the method scored 29.83 dB PSNR, against 29.61 dB for the tuned constant-NSR Wiener filter and 30.30 dB for the oracle.

*Figure 2 (`figures/fig2_lambda.png`, notebook 05 [Fig 2])* shows that the estimated λ(ω) follows the oracle NSR over the frequencies where |H|² is not negligible, at both low (0.005) and high (0.05) noise. The tuned constant NSR, by contrast, is too strong at low frequency and too weak at high frequency. [TBD: confirm this description once Fig. 2 is rendered.]
