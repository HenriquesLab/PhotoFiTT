import numpy as np
from skimage.measure import regionprops
import scipy
def roundnessCalculator(object_matrix, projected=False):
    """
    Object matrix is binary mask with the object of interest:
    foreground = 1 and background = 0.
    This method provides the roundness as the projected roundness of the
    element with label object_lab.
    """
    # Discriminate the element of interest and get a binary image
    element = (object_matrix > 0).astype(np.uint8)
    if np.sum(element) > 0:
        props = regionprops(element)
        # Smooth the segmentation without changing its area and closing any possible hole.
        # element = cv2.dilate(element, np.ones((3,3), np.uint8))
        # element = cv2.erode(element, np.ones((3,3), np.uint8))
        if projected == True:
            projected_roundness = (props[0].perimeter ** 2) / (4 * np.pi * (np.sum(element)) )
            roundness = projected_roundness
            # roundness = np.min((projected_roundness, 1))
        else:
            M = props[0].axis_major_length
            m = props[0].axis_minor_length
            if M == 0:
                roundness = 0
            else:
                roundness = np.min((m / M, 1))
    else:
        roundness = 0
    return roundness

def smooth_labels(im_label, sigma=16, smooth_t = 0.4):
    """
    Takes each of the unique labelled objects and smooths its boundary. This function is recommended specially for
    rounded objects.
    :param im_label: mask with unique labels for each object
    :param kernel_size: sigma for the gaussian smoothing.
    :param smooth_t: threshold after smoothing. 0.4 by default.
    :return: a uniquely labeled mask in which objects have a smoother boundary.
    """
    smooth_im = np.zeros(im_label.shape, dtype=np.int16)
    labels = np.unique(im_label)
    labels = labels[labels>0]

    for l in labels:
        aux = (im_label == l).astype(np.float32)
        # b_round = gaussian(aux, sigma=kernel_size, mode='mirror', preserve_range=True)
        b_round = scipy.ndimage.gaussian_filter(aux, sigma=sigma)
        # b_round = gaussian_blur(aux, kernel_size)
        b_round = b_round > smooth_t
        indexes = np.where(b_round)
        smooth_im[indexes] = l
    return smooth_im

# @njit
# def blur(img, amt=2):
#     outimg = np.zeros((ih+amt, iw+amt), dtype=np.float32)
#     img_aux = outimg.copy()
#     img_aux[1:-1, 1:-1] = img
#     del img
#     ih, iw = img.shape
#     for i in range(amt, iw-amt):
#         for j in range(amt, ih-amt):
#             px = 0.
#             for w in range(-amt//2, amt//2):
#                 for h in range(-amt//2, amt//2):
#                     px += img_aux[i+w, j+h]
#             outimg[i, j]= px/(amt*amt)
#     return outimg

def convolution2D_numba(image, kernel):
    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros(image.shape)
    # Padd the image to deal with image borders
    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)

    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))

    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image
    # Convolve
    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
            # average the result to have it in the correct range of values
            output[row, col] /= kernel.shape[0] * kernel.shape[1]
    return output

def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

def gaussian_kernel(size, sigma=1):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

    kernel_2D *= 1.0 / kernel_2D.max()
    return kernel_2D

def gaussian_blur(image, kernel_size):
    kernel = gaussian_kernel(kernel_size, sigma=np.sqrt(kernel_size))
    return convolution2D_numba(image, kernel)

