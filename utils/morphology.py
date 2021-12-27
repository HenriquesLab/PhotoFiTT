import numpy as np
from skimage.measure import regionprops

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