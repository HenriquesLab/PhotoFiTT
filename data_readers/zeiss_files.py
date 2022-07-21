import slideio
import tifffile
import os
import numpy as np
import cv2
import czifile as zis

### Code to extract different videos from .czi files
# Information about the directory and the pixel_size (height)
# main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb/additional_files_originals/2022-06-09"
main_path = "/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Data/ZeissWF-ITQB/20220720/Individual"
# main_path = '/Volumes/OCB-Data 1/Phototoxicity/ITQB/20220609/2022-06-09'
output_path = '/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_2/2022-07-20'
if not os.path.exists(output_path):
    os.mkdir(output_path)

pixel_size = 0.5500 # x20 objective
time_interval = 240 # seconds (4 mins)
scale = 1.5709

##### THIS CODE WILL EXTRACT DIFFERENT STACKS CONTAINED IN A SINGLE .CZI FILE
#----------------------------------------------------------------------------
# Get CZI object to recover the number of scenes of this file
file_name = 'CHO_20x_live-02.czi'
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

# THIS FILE WILL CONVERT EACH CZI FILE INTO A DOWN/UP-SAMPLED TIFF FILE
#----------------------------------------------------------------------
files = os.listdir(main_path)
# Get CZI object to recover the number of scenes of this file
for file_name in files:
    if file_name.__contains__(".czi"):
        f = zis.CziFile(os.path.join(main_path, file_name))
        video = f.asarray()
        video = video.squeeze()
        print("{} file loaded in python".format(file_name))
        resized_video = []
        for t in range(len(video)):
            frame = video[t]
            frame = cv2.resize(frame, dsize=(int(frame.shape[0] // scale), int(frame.shape[1] // scale)),
                               interpolation=cv2.INTER_CUBIC)
            resized_video.append(frame)
        tifffile.imsave(os.path.join(output_path, '{}.tif'.format(file_name.split(".czi")[0])),
                        np.expand_dims(resized_video, axis=[1, 2, -1]), # addapt the dimensions to tifffile ordering TZCYXS
                        resolution=(1 / (pixel_size*scale), 1 / (pixel_size*scale)),
                        imagej=True,
                        metadata={'spacing': 1, 'unit': 'um'})
        del video