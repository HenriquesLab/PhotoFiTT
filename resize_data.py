## TRAINING DATA RESAMPLING
#===========================================
# from utils.data import videos2frames
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
## FULL DATA RESAMPLING
#===========================================
# from utils.data import videos2frames
# # name of the input folder
# path = '/Volumes/OCB-All/Projects/OCB004_Phototoxicity/Data/NikonTi/2021-12-06'
# folder = "videos"
# # scaling factor
# s = 10
# videos2frames(path, folder, s)


## READ NIKON FIELS, RESIZE AND SAVE
#===========================================

# # The following lines can be used to indicate the main path and the name of the nd2 file in the terminal
# import sys
# path = sys.argv[1]
# output_path = sys.argv[2]
# s = float(sys.argv[3])
#
# # path = "/Volumes/TOSHIBA EXT/HENRIQUES-LAB/PHOTOTOXICITY/2021-12-20/CHO_DIC_fast-acq_"
# # output_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/2021-12-20/scaled_x8/CHO_DIC_fast-acq_"
# # s = 8
# from utils.data import nikon2tiff
# nikon2tiff(path, output_path, s)

## NORMAL SCRIPT TO RESIZE STACKS STORE AS TIFF FILES
#===========================================
from utils.data import resize_files_in_folder
import sys
path = sys.argv[1]
output_path = sys.argv[2]
s = float(sys.argv[3])
# path = "/Volumes/TOSHIBA EXT/HENRIQUES-LAB/PHOTOTOXICITY/2021-12-20/CHO_DIC_damage_merged"
# output_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/2021-12-20/scaled_x8/CHO_DIC_damage_merged"
pixel_size = 0.1083333
resize_files_in_folder(path, output_path, s, pixel_size)

### Convert STARDIST float results to uint16
#===========================================
# from utils.data import change_bitdepth
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

