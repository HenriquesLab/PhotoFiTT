import slideio
import tifffile
import os
import numpy as np
import cv2

### Code to extract different videos from .nd2 files
# Information about the directory and the pixel_size (height)
main_path = '/Volumes/OCB-Data 1/Phototoxicity/ITQB/20220609/2022-06-09'
output_path = '/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb/2022-06-09'
if not os.path.exists(output_path):
    os.mkdir(output_path)
file_name = 'CHO_20x_live-02.czi'
pixel_size = 0.5500 # x20 objective
time_interval = 240 # seconds (4 mins)
# Get CZI object to recover the number of scenes of this file
f = zis.CziFile(os.path.join(main_path, file_name))
# axes will give a string
czi_dimstring = f.axes
scenes = f.shape[czi_dimstring.index('S')]
slide = slideio.open_slide(os.path.join(main_path, file_name),"CZI")
print("{} file loaded in python".format(file_name))

# Extract each of the videos and store them independently
for s in range(scenes):
    # read out a single scene
    scene = slide.get_scene(s)
    video = scene.read_block(frames=(0, scene.num_t_frames)) 
    print("Series {} loaded as numpy array".format(s))
    tifffile.imsave(os.path.join(output_path, '{:02d}.tif'.format(s)),
                    np.expand_dims(video, axis=[1, 2, -1]), # addapt the dimensions to tifffile ordering TZCYXS
                    resolution=(1 / pixel_size, 1 / pixel_size),
                    imagej=True,
                    metadata={'spacing': 1, 'unit': 'um'})
    del video
    print("Series {} stored as a tiff file".format(s))



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