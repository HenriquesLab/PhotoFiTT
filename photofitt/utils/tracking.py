import os
import numpy as np
import cc3d
from scipy.ndimage import gaussian_filter
import pandas as pd
from tifffile import imread

def stack_pixelwise_average(A):
    # time is in the first dimension
    A = A.astype(np.float32)
    B = np.zeros_like(A)
    B[1:-1] = 0.5 * (A[2:] + A[:-2])
    B[0] = A[0]
    B[-1] = A[-1]
    return B

def bounding_box(inst_mask, margin=5):
    BBOX = np.zeros_like(inst_mask)
    if np.sum(inst_mask) > 0:
        for t in range(inst_mask.shape[0]):
            labels = np.unique(inst_mask[t])
            if len(labels) > 1:
                for l in labels[1:]:
                    cell_r, cell_c = np.where(inst_mask[t] == l)
                    bbox_r1 = max((np.min(cell_r) - margin, 0))
                    bbox_r2 = min((np.max(cell_r) + margin, inst_mask.shape[1]))
                    bbox_c1 = max((np.min(cell_c) - margin, 0))
                    bbox_c2 = min((np.max(cell_c) + margin, inst_mask.shape[2]))
                    BBOX[t, bbox_r1:bbox_r2, bbox_c1:bbox_c2] = 1
    return BBOX

def find_concomp2d(mask, connectivity=4):
    new_mask = [cc3d.connected_components(mask[t], connectivity=connectivity) for t in range(mask.shape[0])]
    new_mask = np.array(new_mask)
    return new_mask

def remove_exisitng_labels(bin_mask, instance_mask):
    # any ce3ll (i.e. connected component) in new_mask that has some overlap with bin_mask is removed
    # return: new_mask is an image that has zero intersection with bin_mask.
    intersection = np.multiply(bin_mask, instance_mask)
    new_mask = np.zeros_like(instance_mask)
    for t in range(intersection.shape[0]):
        labels = np.unique(intersection[t])
        #  we copy and flatten because of numba
        aux = np.copy(instance_mask[t].flatten())
        for l in labels:
            indexes = np.where((aux == l))
            aux[indexes] = 0
        aux = np.reshape(aux, intersection[t].shape)
        new_mask[t] += aux
    return new_mask

def smooth_video(input_video, sigma=2):
    # Time is assumed to be in the first axis (axis=0)
    # Process (rows,time) kind of frames
    # Smooth colum-wise
    colwise = []
    video = np.copy((input_video > 0).astype(np.float32))
    for c in range(video.shape[-1]):
        colwise.append((gaussian_filter(video[..., c], sigma)))
    colwise = np.array(colwise)
    colwise = np.transpose(colwise, [1, 2, 0])
    # Smooth row-wise
    rowwise = []
    for r in range(video.shape[1]):
        rowwise.append((gaussian_filter(np.squeeze(video[:, r]), sigma)))
    rowwise = np.array(rowwise)
    rowwise = np.transpose(rowwise, [1, 0, 2])
    # Average
    video = 0.5 * (colwise + rowwise)
    return video


def fill_gaps(inst_mask, sigma=2, track_threshold=0.25):
    # create a binary mask to compute averages
    # We estimate missing data from t using t-1 and t+1.
    bin_mask = (inst_mask > 0).astype(np.uint8)

    ### Estimation 1: fill in gaps
    # Each frame t is the result of averaging t-1 and t+1. The information from frame t is not considered.
    average_mask = stack_pixelwise_average(bin_mask)
    # Threshold all those values where there has been a gap to estimate missing labels.
    # Missing label is considered when t-1 = t+1 and t may or may not have a positive pixel.
    # 0.5*(t-1 - t+1):  (1 + 0)/2 = 0.5, (1+1)/2 = 1, (0+0)/2=0
    average_mask = (average_mask >= 1).astype(np.uint8)
    # get the instances of the estimated cells
    average_mask = find_concomp2d(average_mask)
    # Remove any label that represent a cell that was already detected
    average_mask = remove_exisitng_labels(bin_mask, average_mask)
    # average_mask = np.multiply(average_mask, (1 - bin_mask))
    # Adjust label indexes to get unique numbers
    average_mask[np.where(average_mask > 0)] = average_mask[np.where(average_mask > 0)] + np.max(inst_mask)
    # Merge labels. Note that inst_mask and average_mask have zero intersection
    average_mask += inst_mask

    ### Estimation 2: smooth tracks to get long tracks
    # Now that estimations are robust, we can threshold some detections in time to still fill in gaps for the tracking
    average_mask2 = smooth_video(average_mask, sigma=sigma)
    average_mask2 = (average_mask2 >= track_threshold).astype(np.uint8)
    # get the instances of the estimated cells
    average_mask2 = find_concomp2d(average_mask2)
    # Remove any label that represent a cell that was already detected or estimated in the previous step
    # average_mask2 = remove_exisitng_labels(bin_mask, average_mask2)
    average_mask2 = remove_exisitng_labels(1 * (average_mask > 0), average_mask2)
    # # bin_mask = bounding_box(inst_mask, margin=margin)
    # We only fill in pixels that have not been segmented already.
    ## Final merge
    ## average_mask = np.multiply(average_mask2, (1-bin_mask))
    # adjust label indexes to get unique numbers
    average_mask2[np.where(average_mask2 > 0)] = average_mask2[np.where(average_mask2 > 0)] + np.max(average_mask)
    average_mask2 += average_mask
    tracks_3D = cc3d.connected_components((average_mask2 > 0).astype(np.int32), connectivity=26)
    return average_mask, tracks_3D

def count_tracked_divisions(tracks_3D, average_mask, frame_rate=4):
    # We use average_mask because it has some correction of false negatives
    length = tracks_3D.shape[0]
    counts = np.zeros((length, 2)) # for numpy: np.zeros([length, 2], dtype=np.float32)
    counts[:, 0] = frame_rate*np.arange(length)
    tracks_3D_updated = np.copy(tracks_3D)
    for t in range(length):
        # Get the tracks present in t
        tracks = np.unique(tracks_3D_updated[t])
        # tracks contains the value 0 and has all the values in inst_mask
        for cell in tracks:
            if cell > 0:
                # Check if track belongs to one or two (mitosis) cells.
                instances = np.multiply(average_mask[t], tracks_3D_updated[t] == cell)
                if len(np.unique(instances)) > 2:
                    # If track contains two cells, there's a mitosis, we count it and we do not need to count again in the future
                    counts[t, 1] += 1
                    ## update tracks to be compatible with numba. Otherwise, do:
                    # tracks_3D[tracks_3D == cell] = 0
                    aux = np.copy(tracks_3D_updated.flatten())
                    indexes = np.where((aux == cell))
                    aux[indexes] = 0
                    tracks_3D_updated = np.reshape(aux, tracks_3D_updated.shape)
    return counts

def track_video(path, track_threshold=0.25, frame_rate=4):
    inst_mask = imread(path)
    average_mask, tracks_3D = fill_gaps(inst_mask, track_threshold=track_threshold)
    counts = count_tracked_divisions(tracks_3D, average_mask, frame_rate=frame_rate)
    return counts


def tracking_metrics(path, track_info=None, column_data=[], frame_rate=4, track_threshold=0.25):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.'):
                track_info = tracking_metrics(os.path.join(path, f),track_info=track_info,
                                             column_data=column_data + [f], frame_rate=frame_rate,
                                             track_threshold=track_threshold)
            elif f.__contains__('.tif'):
                print(f)
                counts = track_video(os.path.join(path, f), track_threshold=track_threshold, frame_rate=frame_rate)
                # convert counts together with the column information into a dataframe.
                aux = pd.DataFrame(counts, columns=['frame', 'mitoses'])

                for i in range(len(column_data)):
                    aux["Subcategory-{:02d}".format(i)] = column_data[i]

                aux['video_name'] = f.split('.tif')[0]
                # Concatenate pandas data frame to the previous one
                if track_info is None:
                    track_info = aux
                else:
                    track_info = pd.concat([track_info, aux]).reset_index(drop=True)
    return track_info
