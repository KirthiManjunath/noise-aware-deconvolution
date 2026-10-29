# 1 Introduction

Every optical imaging system blurs. In fluorescence microscopy and optical coherence tomography (OCT), a point in the sample is recorded as a spot whose shape is the system's point spread function (PSF), limited by diffraction and by the optics. The recorded image is therefore the true structure convolved with the PSF, plus detector noise: photon (Poisson) noise and read-out (Gaussian) noise in microscopy, and speckle in OCT.

Deconvolution inverts this convolution. In the frequency domain, blur multiplies each spatial frequency by the optical transfer function H(ω), which falls towards zero at high frequencies. Undoing the blur means dividing by H(ω). Where H(ω) is small, that division amplifies noise far more than it restores signal. Every practical deconvolution method is therefore a regularized inverse: it trades resolution against noise amplification through a regularization parameter λ.

How λ is chosen decides the result. Common practice is to:
- tune one constant by eye or on example images;
- pick it per image with a criterion such as generalized cross-validation (GCV) [Golub et al.];
- run an iterative method such as Richardson–Lucy and stop it early, so the iteration count acts as λ.

In each case λ is a single number applied to all frequencies. The statistically optimal (Wiener) solution instead uses a frequency-dependent λ(ω) = S_n(ω)/S_x(ω), the ratio of noise power to signal power. That requires the signal spectrum S_x, which is unknown for a real image.

The deconvolution literature for OCT [Liu et al. 2009; Woolliams et al. 2010; Schmitt 1998] and blind deconvolution [Moiseev et al. 2011] shows the gains available and also the sensitivity of these methods to noise and PSF errors.

**Contributions.**

1. A **noise-adaptive regularizer** λ(ω) = σ̂²/(A|ω|^(−β)). Here σ̂² is estimated from the band where |H(ω)|² < ε, and (A, β) from a power-law fit to the noise-corrected, de-blurred radial spectrum. No regularization parameter is tuned.
2. A **controlled benchmark** with exact ground truth, built from real fluorescence-microscopy images. It covers 3 PSF widths, 4 Gaussian noise levels and 3 Poisson–Gaussian photon levels, with 5 noise seeds each. It compares six methods, including an oracle Wiener upper bound, on fidelity (PSNR, SSIM, log-spectral distance), resolution (edge FWHM, MTF50), ringing, noise amplification and runtime.
3. An **evaluation on real noise**. The 50-frame averages of the FMD dataset serve as a clean reference, so we can measure the noise amplification of each filter on real Poisson–Gaussian noise. We also give a qualitative OCT demonstration.
4. An **ablation and robustness study**: oracle noise, oracle spectrum and constant λ variants, PSF-width mismatch of ±30 %, and boundary handling.

The rest of the report is organized as follows. Sections 2–4 give the imaging model, the regularized inverse and the proposed method. Sections 5–6 describe the baselines and the experimental setup. Sections 7–10 present the results. Section 11 discusses limitations.
