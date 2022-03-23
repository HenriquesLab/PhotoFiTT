from utils.display import build_mosaics
import os

import sys
path = sys.argv[1]
path2original = sys.argv[2]
output_path = sys.argv[3]
roundness = [0.0, 0.5, 0.85, 0.9, 0.95, 0.97]

for r in roundness:
    output_path_folder = os.path.join(output_path, "mosaics_roundness_{}".format(r))
    build_mosaics(path, path2original, output_path_folder, min_roundness=r)
