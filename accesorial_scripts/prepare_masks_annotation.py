import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import cv2
from tifffile import imread, imsave
from utils.morphology import smooth_labels
import numpy as np

# files = {"2021-12-06": {
#                         "11": 5,
#                         "14": 6,
#                         "12": 3,
#                         "15": 4
#                                 },
# files = {       "2021-11-23": {
#                         "07": 6,
#                         "14": 14,
#                         "16": 15,
#                         "17": 3
#                                 }
#         }
# files = {       "2022-01-26": {
#                         "11": 14,
#                         "11": 32,
#                         "12": 12,
#                         "12": 20,
#                         "13": 6,
#                         "13": 27
#                                 }
#         }
# files = {       "2022-02-02": {
#                         "15_W5": 10,
#                         "15_W5": 23,
#                                 }
#         }
# files = {       "2022-04-20": {
#                         "13_W3": 10,
#                         "13_W3": 16,
#                         "18_UV2-3": 20,
#                         "18_UV2-3": 10,
#                         "20_UV2-5": 12,
#                         "20_UV2-5": 25
#                                 }
#         }
# files = {       "2022-04-21": {
#                         "17_UV2-2": 6,
#                         "17_UV2-2": 16,
#                         "17_UV2-2": 25,
#                         "19_UV2-4": 30,
#                         "19_UV2-4": 4,
#                         "19_UV2-4": 15
#         }}
# s = 8
# size=7885
# main_path = "/Users/esti/Documents/PHX/ground_truth/masks/2do"
# output_path = "/Users/esti/Documents/PHX/ground_truth/upsampled_masks"
# if not os.path.exists(output_path):
#     os.mkdir(output_path)
#
# for f in files.keys():
#     folder_name = f
#     for v in files[f]:
#         print(files[f][v])
#         video_mask = imread(os.path.join(main_path, f, v+'.tif'))
#         for i in range(files[f][v]-1, files[f][v]+1):
#             frame = video_mask[i]
#             frame = cv2.resize(frame, dsize=(size, size),
#                                interpolation=cv2.INTER_NEAREST)
#             frame = smooth_labels(frame)
#             imsave(os.path.join(output_path, f + "_" + v + "_{:03d}.tif".format(i+1)),
#                             frame, imagej=True)

main_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis-mediated-data-itqb"
folder_name = "2022-06-09"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/ground_truth_to_correct/Brightfield"
if not os.path.exists(output_path):
    os.mkdir(output_path)
if not os.path.exists(os.path.join(output_path, "input")):
    os.mkdir(os.path.join(output_path, "input"))
if not os.path.exists(os.path.join(output_path, "masks2clean")):
    os.mkdir(os.path.join(output_path, "masks2clean"))
files = os.listdir(os.path.join(main_path, folder_name, "raw"))
masks_path = os.path.join(main_path, folder_name, "masks", "scaled_x8_results")

for f in files:
    if f.__contains__(".tif"):
        file_name = f.split(".tif")[0]
        print(f)
        video = imread(os.path.join(main_path, folder_name, "raw", f))
        video_mask = imread(os.path.join(masks_path, f))
        t = np.random.randint(0, len(video))
        frame = video[t]
        size = frame.shape[1]
        imsave(os.path.join(output_path, "input", folder_name + "_" + file_name + "_{:03d}.tif".format(t + 1)),
               frame, imagej=True)
        frame = video_mask[t]
        frame = cv2.resize(frame, dsize=(size, size),
                           interpolation=cv2.INTER_NEAREST)
        frame = smooth_labels(frame)
        imsave(os.path.join(output_path, "masks2clean", folder_name + "_" + file_name + "_{:03d}.tif".format(t + 1)),
                        frame, imagej=True)





