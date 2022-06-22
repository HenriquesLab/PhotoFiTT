import slideio
import tifffile
import os
import numpy as np
import cv2
import czifile as zis

### Code to extract different videos from .nd2 files
# Information about the directory and the pixel_size (height)
main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb/additional_files_originals/2022-06-09"
# main_path = '/Volumes/OCB-Data 1/Phototoxicity/ITQB/20220609/2022-06-09'
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