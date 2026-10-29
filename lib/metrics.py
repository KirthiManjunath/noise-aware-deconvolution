# Evaluation metrics.  Owner: P1
import numpy as np
from numpy.fft import fft2
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

def psnr(x, xh):
    return peak_signal_noise_ratio(x, xh, data_range=1.0)

def ssim(x, xh):
    return structural_similarity(x, xh, data_range=1.0)

def lsd(x, xh):
    """Log-spectral distance in dB between true and restored spectra."""
    P = np.abs(fft2(x)) ** 2 + 1e-12
    Q = np.abs(fft2(xh)) ** 2 + 1e-12
    return np.sqrt(np.mean((10 * np.log10(P / Q)) ** 2))

def fwhm(lsf):
    """Full width at half maximum of a 1-D peak, with sub-pixel interpolation."""
    lsf = np.asarray(lsf, float); i = int(np.argmax(lsf)); half = lsf[i] / 2
    l = i
    while l > 0 and lsf[l] > half: l -= 1
    r = i
    while r < len(lsf) - 1 and lsf[r] > half: r += 1
    xl = l + (half - lsf[l]) / (lsf[l + 1] - lsf[l] + 1e-12)
    xr = r - (half - lsf[r]) / (lsf[r - 1] - lsf[r] + 1e-12)
    return xr - xl

def edge_metrics(xh, low=0.2, high=0.8, margin=40):
    """For edge_phantom outputs: edge width, MTF50, overshoot %, noise std in the flat dark half."""
    n = xh.shape[1]
    esf = xh[:, n // 2 - margin:n // 2 + margin].mean(0)    # edge spread function (row-averaged)
    lsf = np.diff(esf)                                      # signed: abs() would turn noise into a positive floor
    c = int(np.argmax(lsf))
    win = lsf[max(c - 16, 0):c + 17]                        # +-16 px around the edge
    M = np.abs(np.fft.rfft(win, 256)); M /= M[0]
    f = np.fft.rfftfreq(256)
    below = np.nonzero(M < 0.5)[0]
    return dict(
        fwhm_px=fwhm(lsf),
        mtf50=f[below[0]] if below.size else 0.5,
        overshoot_pct=100 * max(0.0, esf.max() - high) / (high - low),
        flat_std=xh[:, margin:n // 2 - margin].std(),
    )

def noise_gain(xh_noisy, xh_clean, y_noisy, y_clean):
    """Noise amplification = output noise std / input noise std. Works on real data when a clean reference exists."""
    return (xh_noisy - xh_clean).std() / (y_noisy - y_clean).std()
