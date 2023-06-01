import os
import cv2
import nd2
import tifffile
import numpy as np


def videos2frames(path, folder, s=1, size=None):
    """
    Store all the frames in a video with a certain up or downsampling.
    :param path: path with the folder containing videos and where the new images will be stored
    :param folder: name of the input folder
    :param s: scale to reduce s = 10 means reduce 10 times the original size
    :param size: alternatively, one can provide the size for the X and Y dimensions. For example size = 256
    :return:
    """
    new_folder = folder + "_2d"
    if not os.path.exists(os.path.join(path, new_folder)):
        os.mkdir(os.path.join(path, new_folder))
    for f in os.listdir(os.path.join(path, folder)):
        if f.__contains__("tif"):
            print(f)
            seq = tifffile.imread(os.path.join(path, folder, f))
            seq = seq.astype(np.uint16)
            print(seq.shape)
            if len(seq.shape)==3: # time series + T is the first dimension in tiff
                for t in range(seq.shape[0]):
                    im = np.squeeze(seq[t])
                    if size is not None:
                        new_size = (size, size)
                    else:
                        new_size = (im.shape[0] // s, im.shape[1] // s)
                    if folder.__contains__("target") or folder.__contains__("mask"):
                        image_resized = cv2.resize(im, dsize=new_size,
                                                   interpolation=cv2.INTER_NEAREST)
                    else:
                        image_resized = cv2.resize(im, dsize=new_size,
                                                   interpolation=cv2.INTER_CUBIC)

                    tifffile.imsave(os.path.join(path, new_folder, f.split(".tif")[0] + "_{:04d}.tif".format(t)),
                                    image_resized, imagej=True)
            else:
                seq = np.squeeze(seq)
                if size is not None:
                    new_size = (size, size)
                else:
                    new_size = (seq.shape[0] // s, seq.shape[1] // s)
                if folder.__contains__("target") or folder.__contains__("mask"):
                    image_resized = cv2.resize(seq, dsize=new_size,
                                               interpolation=cv2.INTER_NEAREST)
                else:
                    image_resized = cv2.resize(seq, dsize=new_size,
                                               interpolation=cv2.INTER_CUBIC)

                tifffile.imsave(os.path.join(path, new_folder, f), image_resized, imagej=True)

def change_bitdepth(path, new_path):
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for f in os.listdir(path):
        print(f)
        seq = tifffile.imread(os.path.join(path, f))
        seq = seq.astype(np.uint16)
        tifffile.imsave(os.path.join(new_path, f), seq, imagej=True)


def nikon2tiff(path, output_path, s):
    folders = os.listdir(path)
    folders.sort
    print(folders)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for f in folders:
        if f[0] != '.':
            if not f.__contains__('.nd2'):
                nikon2tiff(os.path.join(path, f), os.path.join(output_path, f), s)
            else:
                print(f)
                video = nd2.ND2File(os.path.join(path, f))
                pixel_size = video.metadata.channels[0].volume.axesCalibration[0]
                video = video.to_dask()
                resized_video = []
                for t in range(len(video)):
                    frame = np.array(video[t])
                    if s != 1:
                        frame = cv2.resize(frame, dsize=(int(frame.shape[0] // s), int(frame.shape[1] // s)),
                                           interpolation=cv2.INTER_CUBIC)
                    resized_video.append(frame)
                resized_video = np.array(resized_video)
                tifffile.imsave(os.path.join(output_path, f.split(".nd2")[0] + '.tif'),
                                np.expand_dims(resized_video, axis=[1, 2, -1]),
                                # addapt the dimensions to tifffile ordering TZCYXS
                                resolution=(1 / (s*pixel_size), 1 / (s*pixel_size)),
                                imagej=True,
                                metadata={'spacing': 1, 'unit': 'um'})

def resize_files_in_folder(path, output_path, s, pixel_size):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    files = os.listdir(path)
    for f in files:
        print(f)
        if f.__contains__(".tif"):
            video1 = tifffile.imread(os.path.join(path, f))
            resized_video = []
            for t in range(len(video1)):
                frame = video1[t]
                frame = cv2.resize(frame, dsize=(int(frame.shape[0] // s), int(frame.shape[1] // s)),
                                   interpolation=cv2.INTER_CUBIC)
                resized_video.append(frame)
            tifffile.imsave(os.path.join(output_path, f),
                            np.expand_dims(resized_video, axis=[1, 2, -1]),
                            # addapt the dimensions to tifffile ordering TZCYXS
                            resolution=(1 / (s*pixel_size), 1 / (s*pixel_size)),
                            imagej=True,
                            metadata={'spacing': 1, 'unit': 'um'})