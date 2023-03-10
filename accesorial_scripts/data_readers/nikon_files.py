import nd2
import tifffile
import os
import numpy as np
import cv2

### Code to extract different videos from .nd2 files
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



## Clean and concatenate videos
#===========================================

last_frame = 11
s = 10
path = "/Volumes/TOSHIBA EXT/HENRIQUES-LAB/PHOTOTOXICITY/2021-12-20/CHO_DIC_damage"
if not os.path.exists(path + "_merged"):
    os.mkdir(path + "_merged")
if not os.path.exists(path + "_merged_scaled"):
    os.mkdir(path + "_merged_scaled")
files = os.listdir(path + "_001")
for f in files:
    print(f)
    if f.__contains__(".nd2"):
        video2 = nd2.ND2File(os.path.join(path + "_002", f))
        pixel_size = video2.metadata.channels[0].volume.axesCalibration[0]
        video2 = video2.to_dask()
        video2 = np.array(video2[:last_frame])
        video1 = nd2.ND2File(os.path.join(path + "_001", f))
        video1 = np.array(video1.to_dask())
        video1 = np.concatenate((video1, video2), axis=0)
        del video2
        tifffile.imsave(os.path.join(path + "_merged", f.split(".nd2")[0] + '.tif'),
                        np.expand_dims(video1, axis=[1, 2, -1]),
                        # addapt the dimensions to tifffile ordering TZCYXS
                        resolution=(1 / pixel_size, 1 / pixel_size),
                        imagej=True,
                        metadata={'spacing': 1, 'unit': 'um'})
        resized_video = []
        for t in range(len(video1)):
            frame = video1[t]
            frame = cv2.resize(frame, dsize=(frame.shape[0] // s, frame.shape[1] // s),
                                   interpolation=cv2.INTER_CUBIC)
            resized_video.append(frame)
        tifffile.imsave(os.path.join(path + "_merged_scaled", f.split(".nd2")[0] + '.tif'),
                        np.expand_dims(resized_video, axis=[1, 2, -1]),
                        # addapt the dimensions to tifffile ordering TZCYXS
                        resolution=(1 / pixel_size, 1 / pixel_size),
                        imagej=True,
                        metadata={'spacing': 1, 'unit': 'um'})