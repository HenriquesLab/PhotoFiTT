# Requires numpy, dask, nd2, tifffile
import nd2
import tifffile
import numpy as np
import os

# The following lines can be used to indicate the main path and the name of the nd2 file in the terminal
# import sys
# main_path = sys.argv[0]
# file_name = sys.argv[1]
# pixel_size = sys.argv[2]

# Information about the directory and the pixel_size (height)
main_path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Data/NikonTi/2021-12-06'
file_name = 'CHO_20h_DIC.nd2'
pixel_size = 0.1083

# Read the file
f = nd2.ND2File(os.path.join(main_path, file_name))
print("{} file loaded in python".format(file_name))
# f has shape (frames, position, height, width)
D = f.to_dask()
D = D.transpose([1, 0, 2, 3])

# Extract each of the videos and store them independently
for fov in range(len(D)):
    video = np.array(D[fov])
    print("Series {} loaded as numpy array".format(fov))
    tifffile.imsave(os.path.join(main_path, '{:02d}.tif'.format(fov)),
                    np.expand_dims(video, axis=[1, 2, -1]), # addapt the dimensions to tifffile ordering TZCYXS
                    resolution=(1 / pixel_size, 1 / pixel_size),
                    imagej=True,
                    metadata={'spacing': 1, 'unit': 'um'})
    del video
    print("Series {} stored as a tiff file in the server".format(fov))