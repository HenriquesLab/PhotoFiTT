import os
import cv2
import tifffile
import numpy as np

# The following lines can be used to indicate the main path and the name of the nd2 file in the terminal
# import sys
# main_path = sys.argv[0]
# folder = sys.argv[1]
# s = sys.argv[2]

# name of the input folder
main_path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Data/NikonTi/2021-12-06'
folder = "videos"
# name of the new folder which will be store in the same directory as the input folder.
new_folder = folder + "_2d_scaled"
# scaling factor
s = 10

if not os.path.exists(os.path.join(main_path, new_folder)):
    os.mkdir(os.path.join(main_path, new_folder))

for f in os.listdir(os.path.join(main_path, folder)):
    print(f)
    # Read the image
    seq = tifffile.imread(os.path.join(main_path, folder, f))
    seq = seq.astype(np.uint16)
    print(seq.shape)
    for t in range(seq.shape[0]):
        # Remove unnecessary dimensions
        im = np.squeeze(seq[t])
        # Detect if the image is a mask or the input to decide the interpolation method.
        if folder == "target":
            image_resized = cv2.resize(im, dsize=(im.shape[0] // s, im.shape[1] // s), interpolation=cv2.INTER_NEAREST)
        else:
            image_resized = cv2.resize(im, dsize=(im.shape[0] // s, im.shape[1] // s), interpolation=cv2.INTER_CUBIC)
        # Use this function only in StarDist notebooks.
        # save_tiff_imagej_compatible(os.path.join(main_path, new_folder, f.split(".tif")[0] + "_{:02d}.tif".format(t)), image_resized, "yx")

        tifffile.imsave(os.path.join(main_path, new_folder, f.split(".tif")[0] + "_{:04d}.tif".format(t)),
                        image_resized, imagej=True)

