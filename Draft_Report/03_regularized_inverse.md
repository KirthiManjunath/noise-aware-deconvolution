# 3 Regularized inverse: derivation

## 3.1 The inverse filter and its noise gain

Dividing the observation by the transfer function gives the inverse filter:

$$
\hat X_{\text{inv}}(\omega) = \frac{Y(\omega)}{H(\omega)} = X(\omega) + \frac{N(\omega)}{H(\omega)}.
$$

The first term is perfect recovery. The second is the noise divided by H. For white noise of variance σ_n², the variance of the restoration error is, by Parseval:

$$
\mathbb{E}\,\|\hat x_{\text{inv}} - x\|^2 / (MN) = \sigma_n^2 \cdot \frac{1}{MN}\sum_\omega \frac{1}{|H(\omega)|^2}.
$$

For a Gaussian PSF, |H|⁻² grows like exp(4π²σ_h²|ω|²). At σ_h = 1.5 and |ω| = 0.7 this factor is about 10¹⁹. That is why the inverse filter is unusable.

Our implementation confirms it (notebook 01, S2). On a noiseless blurred image (σ_h = 1.5) the inverse filter recovers x to a maximum error of 2.8 × 10⁻⁸, which verifies the OTF construction. Adding noise of only σ_n = 0.001 raises the maximum error to 1.4 × 10⁵. On the full benchmark the inverse filter scores 3.4 dB PSNR (Section 7).

## 3.2 Tikhonov regularization

Tikhonov regularization chooses the image that fits the data while staying smooth:

$$
\hat x = \arg\min_x \;\|y - h*x\|^2 + \lambda\,\|\ell * x\|^2,
$$

where ℓ is the discrete Laplacian [[0, −1, 0], [−1, 4, −1], [0, −1, 0]]. Both terms are diagonal in the Fourier domain, so the minimizer is found frequency by frequency. Setting the derivative with respect to X(ω)* to zero gives:

$$
\hat X(\omega) = \frac{H^*(\omega)\,Y(\omega)}{|H(\omega)|^2 + \lambda\,|L(\omega)|^2}.
$$

The scalar λ is chosen by **generalized cross-validation** [Golub, Heath & Wahba 1979]. Writing the filter gain as φ(ω) = |H|²/(|H|² + λ|L|²), the GCV score is:

$$
\mathrm{GCV}(\lambda) = \frac{\sum_\omega |1-\varphi(\omega)|^2\,|Y(\omega)|^2}{\big(\sum_\omega (1-\varphi(\omega))\big)^2},
$$

the residual energy divided by the squared effective number of degrees of freedom left in the residual. We minimize it over 61 log-spaced values λ ∈ [10⁻⁶, 1]. GCV needs no knowledge of x or σ_n.

## 3.3 The Wiener filter as the optimal frequency-dependent λ

Suppose x and n are uncorrelated, zero-mean, wide-sense-stationary random fields with power spectra S_x(ω) and S_n(ω). We look for a linear filter G(ω), so that X̂ = G·Y, that minimizes the mean squared error E|X − GY|² at every ω. Expanding with Y = HX + N:

$$
\mathbb{E}|X - GY|^2 = |1 - GH|^2 S_x + |G|^2 S_n.
$$

Differentiating with respect to G* and setting the result to zero gives the Wiener filter:

$$
G_W(\omega) = \frac{H^*(\omega)\,S_x(\omega)}{|H(\omega)|^2 S_x(\omega) + S_n(\omega)} = \frac{H^*(\omega)}{|H(\omega)|^2 + \lambda(\omega)}, \qquad \lambda(\omega) = \frac{S_n(\omega)}{S_x(\omega)}.
$$

This is the regularized inverse from the project brief, X̂ = H*Y/(|H|² + λ(ω)). It identifies λ(ω) as the **noise-to-signal ratio (NSR)** at each frequency. The three practical choices differ only in how they set λ:

| Method | λ(ω) | Needs |
|---|---|---|
| Inverse | 0 (here 10⁻³⁰, a division guard) | nothing; unusable with noise |
| Constant-NSR Wiener | one constant, tuned on development images | a tuning set |
| Tikhonov–GCV | λ_GCV · \|L(ω)\|², which grows as \|ω\|⁴ | nothing (λ from y) |
| Oracle Wiener | σ_n² / S_x(ω) from the true x | ground truth; upper bound only |
| **Proposed** | σ̂² / (A\|ω\|^(−β)), which grows as \|ω\|^β | nothing (σ̂, A, β from y) |

Tikhonov with a Laplacian is itself a Wiener filter with the implicit signal model S_x ∝ |ω|⁻⁴, since |L(ω)|² ≈ (2π|ω|)⁴ at low frequency. Its single λ sets the ratio of noise to that fixed spectral shape. The proposed method estimates both the noise level and the spectral exponent β from the data.

## 3.4 Noise gain and resolution of a linear restoration

For any linear filter G, white input noise of variance σ_n² leaves with variance σ_n² · mean_ω |G(ω)|². The **noise gain** is therefore:

$$
g_n = \sqrt{\tfrac{1}{MN}\textstyle\sum_\omega |G(\omega)|^2}.
$$

The **resolution delivered** is set by the transfer function of the whole chain, blur followed by restoration:

$$
T(\omega) = G(\omega)H(\omega) = \frac{|H(\omega)|^2}{|H(\omega)|^2 + \lambda(\omega)} \in [0, 1].
$$

We summarize it by its MTF50, the radial frequency where T first drops below 0.5. Every regularized inverse is a point on a trade-off: smaller λ raises the MTF50 but also raises g_n. Section 10 measures both on real images.
