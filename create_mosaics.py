from utils.display import build_mosaics
import os

import sys
# path = sys.argv[1]
# path2original = sys.argv[2]
# output_path = sys.argv[3]

path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_2/masks/scaled_1.5709_results/stardist_prob03/"
path2original = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_2/inputs/scaled_1.5709_results/2022-07-20"
output_path = "/Users/esti/Documents/PROYECTOS/PHX/mitosis_mediated_data_itqb_2/results/scaled_1.5709_results"

roundness = [0.0, 0.5, 0.85, 0.9, 0.95, 0.97]

for r in roundness:
    output_path_folder = os.path.join(output_path, "mosaics_roundness_{}".format(r))
    build_mosaics(path, path2original, output_path_folder, min_roundness=r)
