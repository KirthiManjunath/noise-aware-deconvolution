# Noise-adaptive Wiener filter with lambda(w) = sigma_hat^2 / (A |w|^-beta).  Owner: P3
import numpy as np
from numpy.fft import fft2
from forward import psf2otf, freq_grid
from baselines import _apply

def estimate_noise_var(y, psf, eps=1e-3):
    """Where |H|^2 < eps the blurred signal is gone, so the spectrum there is pure noise."""
    H2 = np.abs(psf2otf(psf, y.shape)) ** 2
    band = H2 < eps
    if band.sum() < 50:                          # PSF too narrow: no noise-only band
        from skimage.restoration import estimate_sigma
        return float(estimate_sigma(y)) ** 2     # fall back to wavelet MAD estimate
    return float(np.mean(np.abs(fft2(y)[band]) ** 2) / y.size)

def fit_signal_psd(y, psf, sigma2, snr_min=2.0, nbins=60):
    """Fit S_x(w) = A |w|^-beta to the radially averaged, noise-corrected, de-blurred spectrum."""
    H2 = np.abs(psf2otf(psf, y.shape)) ** 2
    P = np.abs(fft2(y - y.mean())) ** 2 / y.size
    w = freq_grid(y.shape)
    edges = np.linspace(0, 0.5, nbins + 1)
    fc, Sx = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (w >= a) & (w < b) & (w > 0)
        if not m.any():
            continue
        Pm = P[m].mean()
        if Pm > snr_min * sigma2:                # keep only bins where signal clearly beats noise
            fc.append((a + b) / 2)
            Sx.append((Pm - sigma2) / H2[m].mean())
    fc, Sx = np.array(fc), np.array(Sx)
    assert len(fc) >= 3, 'too few reliable frequency bins: lower snr_min or check sigma2'
    slope, intercept = np.polyfit(np.log(fc), np.log(Sx), 1)
    return np.exp(intercept), -slope, (fc, Sx)

def adaptive_wiener(y, psf, eps=1e-3, snr_min=2.0, return_info=False):
    sigma2 = estimate_noise_var(y, psf, eps)
    A, beta, pts = fit_signal_psd(y, psf, sigma2, snr_min)
    w = freq_grid(y.shape)
    w[0, 0] = w[0, 1]                            # avoid |w| = 0 at DC
    lam = sigma2 / (A * w ** (-beta))
    xh = _apply(y, psf2otf(psf, y.shape), lam)
    info = dict(sigma2=sigma2, A=A, beta=beta, lam=lam, pts=pts)
    return (xh, info) if return_info else xh
