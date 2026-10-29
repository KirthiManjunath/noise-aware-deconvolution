# Forward imaging model y = h * x + n.  Owner: P1
import numpy as np
from numpy.fft import fft2, ifft2, fftfreq

def psf_size(sigma):
    return int(8 * sigma) | 1                    # odd size covering +-4 sigma

def gaussian_psf(size, sigma):
    ax = np.arange(size) - size // 2
    xx, yy = np.meshgrid(ax, ax)
    h = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return h / h.sum()                           # unit sum = brightness preserved

def airy_psf(size, radius):
    """Diffraction-limited PSF; radius = first dark ring in pixels."""
    from scipy.special import j1
    ax = np.arange(size) - size // 2
    r = np.hypot(*np.meshgrid(ax, ax)) * 3.8317 / radius
    r[r == 0] = 1e-12
    h = (2 * j1(r) / r) ** 2
    return h / h.sum()

def psf2otf(psf, shape):
    """Zero-pad the PSF to the image size and move its centre to pixel (0,0), so H has no phase ramp."""
    pad = np.zeros(shape)
    kh, kw = psf.shape
    pad[:kh, :kw] = psf
    pad = np.roll(pad, (-(kh // 2), -(kw // 2)), axis=(0, 1))
    return fft2(pad)

def blur(x, psf, boundary='periodic'):
    if boundary == 'periodic':                   # exact match to the FFT model
        return np.real(ifft2(fft2(x) * psf2otf(psf, x.shape)))
    from scipy.ndimage import convolve           # 'reflect': more realistic image borders
    return convolve(x, psf, mode='reflect')

def add_gaussian(y, sigma, rng):
    return y + sigma * rng.standard_normal(y.shape)

def add_poisson_gaussian(y, peak, read_sigma, rng):
    """peak = photon count at brightness 1.0; fewer photons = noisier."""
    return rng.poisson(np.clip(y, 0, None) * peak) / peak + read_sigma * rng.standard_normal(y.shape)

def freq_grid(shape):
    """Radial spatial frequency |w| of every FFT bin, in cycles/pixel (0 ... 0.707)."""
    wy = fftfreq(shape[0])[:, None]
    wx = fftfreq(shape[1])[None, :]
    return np.hypot(wx, wy)

def edge_phantom(n=256, low=0.2, high=0.8):
    """Vertical step edge: exact ground truth for edge width, overshoot and noise in flat areas."""
    x = np.full((n, n), low)
    x[:, n // 2:] = high
    return x
