# Abstract

Deconvolution can recover resolution lost to an optical point spread function (PSF), but it amplifies noise at exactly the frequencies it tries to restore. Regularized inverse filters control this with a parameter λ that is usually hand-tuned or chosen per image by generalized cross-validation (GCV).

We propose a **spectrally adaptive Wiener filter** whose frequency-dependent regularizer λ(ω) is estimated entirely from the blurred image. The noise power comes from the frequency band where the optical transfer function is negligible, and the signal power from a power-law fit to the noise-corrected, de-blurred spectrum. The method has no tunable regularization parameter and costs a few FFTs per image.

On a controlled benchmark built from fluorescence-microscopy images (FMD dataset; 8 test crops, 3 Gaussian PSF widths, 4 noise levels, 5 noise seeds), the method:
- comes within 0.15–0.39 dB PSNR of the oracle Wiener filter, which uses the true signal spectrum;
- beats a dev-tuned constant-NSR Wiener filter by a median 0.72 dB, Richardson–Lucy by 2.10 dB and unsupervised Wiener by 3.11 dB;
- is statistically tied with Tikhonov–GCV (median difference 0.00 dB).

[PRELIM: On real FMD and OCT images with an assumed PSF, Tikhonov–GCV amplified noise by up to 4.3× (FMD) and 22× (OCT), while the proposed estimate stayed between 0.6× and 1.5×.] We report the method's limitations, including sensitivity to PSF mismatch and the assumption of stationary noise.

**Keywords:** deconvolution, Wiener filter, Tikhonov regularization, noise estimation, fluorescence microscopy, optical coherence tomography
