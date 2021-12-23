import os
import cv2
import tifffile
import numpy as np

def videos2frames(path, folder, s):
    """
    Store all the frames in a video with a certain up or downsampling.
    :param path: path with the folder containing videos and where the new images will be stored
    :param folder: name of the input folder
    :param s: scale to reduce s = 10 means reduce 10 times the original size
    :return:
    """
    new_folder = folder + "_2d"
    if not os.path.exists(os.path.join(path, new_folder)):
        os.mkdir(os.path.join(path, new_folder))
    for f in os.listdir(os.path.join(path, folder)):
        print(f)
        seq = tifffile.imread(os.path.join(path, folder, f))
        seq = seq.astype(np.uint16)
        print(seq.shape)
        for t in range(seq.shape[0]):
            im = np.squeeze(seq[t])
            if folder == "target":
                image_resized = cv2.resize(im, dsize=(im.shape[0] // s, im.shape[1] // s),
                                           interpolation=cv2.INTER_NEAREST)
            else:
                image_resized = cv2.resize(im, dsize=(im.shape[0] // s, im.shape[1] // s),
                                           interpolation=cv2.INTER_CUBIC)

            tifffile.imsave(os.path.join(path, new_folder, f.split(".tif")[0] + "_{:04d}.tif".format(t)),
                            image_resized, imagej=True)


def change_bitdepth(path, new_path):
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for f in os.listdir(path):
        print(f)
        seq = tifffile.imread(os.path.join(path, f))
        seq = seq.astype(np.uint16)
        tifffile.imsave(os.path.join(new_path, f), seq, imagej=True)

# # scaling factor
# s = 10
# path = "/content/gdrive/MyDrive/Projectos/DEEP-IMAGEJ/examples_of_models/ZeroCostDL4Mic/PHTX/nuclei_detection/test"
# folder = "input"
# videos2frames(path, folder, s)
#
# path = "/content/gdrive/MyDrive/Projectos/DEEP-IMAGEJ/examples_of_models/ZeroCostDL4Mic/PHTX/nuclei_detection/test"
# folder = "target"
# videos2frames(path, folder, s)
#
# path = "/content/gdrive/MyDrive/Projectos/DEEP-IMAGEJ/examples_of_models/ZeroCostDL4Mic/PHTX/nuclei_detection/train"
# folder = "input"
# videos2frames(path, folder, s)
#
# path = "/content/gdrive/MyDrive/Projectos/DEEP-IMAGEJ/examples_of_models/ZeroCostDL4Mic/PHTX/nuclei_detection/train"
# folder = "target"
# videos2frames(path, folder, s)
#
#
# # name of the input folder
# path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Data/NikonTi/2021-12-06'
# folder = "videos"
# # scaling factor
# s = 10
# videos2frames(path, folder, s)

### Code to convert float results from StarDist into uint16
# main_path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Analysis/StarDist/results/STARDIST-17122021'
# main_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/2021-12-06"
# for folder in os.listdir(main_path):
#     if not folder.__contains__(".DS"):
#         new_path = os.path.join(main_path, folder + "_16")
#         if not os.path.exists(new_path):
#             os.mkdir(new_path)
#         for subfolder in os.listdir(os.path.join(main_path, folder)):
#             if not subfolder.__contains__(".DS"):
#                 change_bitdepth(os.path.join(main_path, folder, subfolder), os.path.join(new_path, subfolder))

