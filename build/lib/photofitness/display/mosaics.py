import os
import numpy as np
from skimage.measure import regionprops
from tifffile import imread, imsave
from photofitness.utils.morphology import roundnessCalculator

def mosaic(stack_im, path2original, min_roundness=0.5):
    """
    :param stack_im: instance mask image.
    :param path2original: path to the original image. stack_im is the instance mask of the original image.
    :param min_roundness: not used yet. It could serve to filter out unrounded objects.
    :return: mosaic image
    """
    BBOX = []
    max_cell = 0
    # Store the bounding box information for each detected cell in the image. We need to know beforehand what's the
    # maximum number of cells detected on each frame so we can calculate the optimal size of the mosaic.
    for t in range(len(stack_im)):
        labels = np.unique(stack_im[t])
        total = 0
        for l in labels:
            if l > 0:
                cell = (stack_im[t] == l).astype(np.uint8)
                if np.sum(cell) > 0:
                    if roundnessCalculator(cell, projected=False) > min_roundness:
                        props = regionprops(cell)
                        cell_info = [t] + [i for i in props[0].bbox]
                        cell_info = cell_info + [cell_info[3] - cell_info[1],
                                                 cell_info[4] - cell_info[
                                                     2]]  # [t, min row, min col, max row, max col, height, width]
                        BBOX.append(cell_info)
                        total += 1
        max_cell = np.max((max_cell, total))
    if len(BBOX) > 0:
        BBOX = np.array(BBOX)
        if len(BBOX.shape) == 1:
            BBOX = np.expand_dims(BBOX, axis=0)
        # Try to make a squared mosaic with same number of cells in rows and columns
        count_x = int(np.floor(np.sqrt(max_cell))) + 1
        count_y = int(np.ceil(max_cell / count_x))
        H = int(np.max(BBOX[:, 5])) + 3  # Add some pixels to visualise the entire cells
        W = int(np.max(BBOX[:, 6])) + 3  # Add some pixels to visualise the entire cells
        # Create the empty mosaic image
        mosaic_stack = np.zeros([stack_im.shape[0], count_y * H, count_x * W], dtype=np.uint16)
        print(mosaic_stack.shape)
        # count_x = np.floor(stack_im.shape[2] / W)
        # # count_y = np.floor(stack_im.shape[1]/H)
        stack_im = imread(path2original)
        # for each detected image, extract the original information.
        for t in range(np.max(BBOX[:, 0])):
            cells = BBOX[BBOX[:, 0] == t]
            X = 0
            Y = 0
            for c in cells:
                h = c[5]
                y = np.max((0, c[1] - int(np.floor((H - h) / 2))))
                w = c[6]
                x = np.max((0, c[2] - int(np.floor((W - w) / 2))))
                aux = stack_im[t,
                      y:np.min((stack_im.shape[1], y + H)),
                      x:np.min((stack_im.shape[2], x + W))]
                mosaic_stack[t, Y * H:Y * H + aux.shape[0], X * W:X * W + aux.shape[1]] = aux
                X += 1
                if X >= (count_x):
                    X = 0
                    Y += 1
    else:
        mosaic_stack = 0
    return mosaic_stack

def build_mosaics(path, path2original, output_path, min_roundness=0.85):
    """"""
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                build_mosaics(os.path.join(path, f), os.path.join(path2original, f),
                              os.path.join(output_path, f), min_roundness=min_roundness)
            elif f.__contains__('.tif'):
                print(f)
                im = imread(os.path.join(path, f))
                mosaic_stack = mosaic(im, os.path.join(path2original, f), min_roundness=min_roundness)
                if np.sum(mosaic_stack) > 0:
                    imsave(os.path.join(output_path, f), mosaic_stack)
