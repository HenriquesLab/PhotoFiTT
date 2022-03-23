import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import cv2
from tifffile import imread, imsave
from utils.morphology import smooth_labels

files = {"2021-12-06": {
                        "11": 5,
                        "14": 6,
                        "12": 3,
                        "15": 4
                                },
        "2021-11-23": {
                        "07": 6,
                        "14": 14,
                        "16": 15,
                        "17": 3
                                }
        }

s = 8
main_path = "/Users/esti/Documents/PHX/ground_truth/masks"
output_path = "/Users/esti/Documents/PHX/ground_truth/upsampled_masks"
if not os.path.exists(output_path):
    os.mkdir(output_path)

for f in files.keys():
    folder_name = f
    for v in files[f]:
        print(files[f][v])
        video_mask = imread(os.path.join(main_path, f, v+'.tif'))
        for i in range(files[f][v]-1, files[f][v]+1):
            frame = video_mask[i]
            frame = cv2.resize(frame, dsize=(int(frame.shape[0] * s), int(frame.shape[1] * s)),
                               interpolation=cv2.INTER_NEAREST)
            frame = smooth_labels(frame)
            imsave(os.path.join(output_path, f + "_" + v + "_{:03d}.tif".format(i+1)),
                            frame, imagej=True)





