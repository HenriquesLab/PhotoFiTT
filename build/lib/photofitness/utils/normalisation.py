import numpy as np
from scipy.ndimage import gaussian_filter

def normalizePercentile(x, pmin=1, pmax=99.8, axis=None, clip=False, eps=1e-20, dtype=np.float32):
    """This function is adapted from Martin Weigert"""
    """Percentile-based image normalization."""

    mi = np.percentile(x, pmin, axis=axis, keepdims=True)
    ma = np.percentile(x, pmax, axis=axis, keepdims=True)
    return normalize_mi_ma(x, mi, ma, clip=clip, eps=eps, dtype=dtype)


def normalize_mi_ma(x, mi, ma, clip=False, eps=1e-20, dtype=np.float32):  # dtype=np.float32
    """This function is adapted from Martin Weigert"""
    if dtype is not None:
        x = x.astype(dtype, copy=False)
        mi = dtype(mi) if np.isscalar(mi) else mi.astype(dtype, copy=False)
        ma = dtype(ma) if np.isscalar(ma) else ma.astype(dtype, copy=False)
        eps = dtype(eps)

    try:
        import numexpr
        x = numexpr.evaluate("(x - mi) / ( ma - mi + eps )")
    except ImportError:
        x = (x - mi) / (ma - mi + eps)

    if clip:
        x = np.clip(x, 0, 1)

    return x

def background_subtr_medFilt(stackGray):
    # Calculate the background of an image with a median filter over the z-axis.
    # The function returns the stack after subtracting the background and the background itself.
    # Real intensity values are preserved (not transformed into uint16, uint8 etc.)
    background = np.zeros_like(stackGray[0])
    # Apply median filter to data
    for r in range(stackGray.shape[1]):
        for c in range(stackGray.shape[2]):
            background[r, c] = np.median(stackGray[:, r, c])

    backRemoval = np.copy(stackGray)

    for i in range((stackGray.shape[0])):
        backRemoval[i] = stackGray[i] - background

    return backRemoval, background


def mean_match(im, mean_val=0):
    # inputI input image
    # m is the mean value of your image type (1/2, 255/2, 65535/2, ...)
    out_im = im.astype(np.float32) + (mean_val - np.mean(im.astype(np.float32)))
    return out_im


def bleach_correction(im, sigma=60, keep_mean=False):
    light_artifact = gaussian_filter(im.astype(np.float32), sigma)
    if keep_mean:
        light_artifact_correct = im.astype(np.float32) - light_artifact + np.mean(light_artifact)
    else:
        light_artifact_correct = im.astype(np.float32) - light_artifact
    return light_artifact_correct


def normalise_phc_timelapse(stack, pmin=0, pmax=100, sigma=60, keep_mean=True):
    stack = stack.astype(np.float32)
    T = stack.shape[0]
    new_im = []
    for t in range(T):
        normalised_im = normalizePercentile(stack[t], pmin=pmin, pmax=pmax)
        light_correct = bleach_correction(normalised_im, sigma=sigma, keep_mean=keep_mean)
        new_im.append(light_correct)
    return np.array(new_im)
