# 12 Conclusion

We presented a Wiener-type deconvolution filter whose frequency-dependent regularizer is estimated from the blurred image itself. The noise power comes from the band the optics cannot pass, and the signal spectrum from a noise-corrected power-law fit. The filter costs a few FFTs and has no regularization parameter to tune.

On a controlled benchmark built from real fluorescence-microscopy images:
- it came within 0.15–0.39 dB of the oracle Wiener filter;
- it outperformed a tuned constant-NSR Wiener filter (median +0.72 dB, up to +3.5 dB), Richardson–Lucy (+2.1 dB) and unsupervised Wiener (+3.1 dB);
- it was statistically equivalent to Tikhonov regularization with GCV.

[PRELIM: On real FMD noise and on retinal OCT with an assumed PSF, it kept noise amplification between 0.6× and 1.5×, where GCV reached 4.3× and 22×.] Its practical value is therefore robustness rather than a higher PSNR.

The main limitations are a global noise model, an isotropic signal model and an assumed PSF on real data. These point to spatially adaptive and anisotropic extensions.
